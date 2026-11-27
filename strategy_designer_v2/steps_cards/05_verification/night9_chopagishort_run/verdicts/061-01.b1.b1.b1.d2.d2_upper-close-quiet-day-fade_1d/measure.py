import numpy as np
import pandas as pd


def _to_dt(s):
    if np.issubdtype(s.dtype, np.number):
        mx = float(np.nanmax(s.values)) if len(s) else 0.0
        unit = "ms" if mx > 1e11 else "s"
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    H = 10
    BAND = 2.0
    CP = "debug_info.components.close_pos.last_history_value"

    n_active = 0
    n_agree = 0
    cases = []  # dicts: coin, day, unusual, absf

    for coin, wins in bars.items():
        prepared = {}
        grid_rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            prepared[w] = df
            c = df["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                if c[i] > 0 and np.isfinite(c[i]) and np.isfinite(c[i + H]):
                    grid_rets.append(c[i + H] / c[i] - 1.0)
        drift = float(np.mean(grid_rets)) if grid_rets else np.nan

        for w, df in prepared.items():
            o_close = df["close"].astype(float)
            high = df["high"].astype(float)
            low = df["low"].astype(float)
            fc = df["forecast"].astype(float).fillna(0.0).values
            rng = (high - low).replace(0, np.nan)
            loc = (o_close - low) / rng
            if CP in df.columns:
                cp = df[CP].astype(float)
                loc_rec = (cp + 1.0) / 2.0
                loc = loc_rec.where(cp.notna(), loc)
            r = o_close.pct_change()
            vol = r.rolling(20, min_periods=20).std(ddof=1)
            vsr = (r / vol.replace(0, np.nan)).values
            locv = loc.values

            # situation check
            for i in range(len(df)):
                if fc[i] != 0:
                    if not (np.isfinite(locv[i]) and np.isfinite(vsr[i])):
                        continue
                    n_active += 1
                    sit = (locv[i] >= 0.5 - 1e-12) and (vsr[i] > 0) and (vsr[i] <= 1.0 + 1e-9)
                    if sit and fc[i] < 0:
                        n_agree += 1

            # bets on the short side
            s = np.where(fc < 0, -fc, 0.0)
            m = 0.0
            bet = np.zeros(len(df), dtype=bool)
            for i in range(len(df)):
                if s[i] <= 0:
                    m = 0.0
                    continue
                if s[i] - m >= BAND - 1e-12:
                    bet[i] = True
                    m = s[i]
                else:
                    m = min(m, s[i])

            ts = _to_dt(df["timestamp"])
            c = o_close.values
            seen_cells = set()
            for i in np.where(bet)[0]:
                cell = i // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if i + H >= len(df) or not np.isfinite(drift):
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                ret = c[i + H] / c[i] - 1.0
                cases.append({
                    "day": str(ts.iloc[i].date()),
                    "unusual": -(ret - drift),
                    "absf": abs(fc[i]),
                })

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    sit = {"agreement": float(agreement), "passed": bool(passed)}
    reading = ("Situation = close location >= 0.5 of the day's range and 0 < day return / 20-day std (ddof 1, current day included) <= 1, short side, profile not re-checked, bars without 20 returns left out; "
               "a case is the first short-side bet (rise of -forecast >= 2 from its low since the last bet) in each 10-bar grid cell of a window; "
               "the day-clustered t uses sqrt(G/(G-1) * sum of squared per-day deviation sums)/n; "
               "the larger half is |forecast| above the median, the smaller at or below it; "
               "the plan's 'fewer than 30 cases or days' is treated as the minimum counts (not observable).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": sit,
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": f"only {agreement:.1%} of active bars are upper-close small-gain days on the short side (below 90%).",
            "reading": reading,
        }

    n = len(cases)
    days = sorted(set(cs["day"] for cs in cases))
    G = len(days)
    counts = {"cases": int(n), "distinct days": int(G)}
    x = np.array([cs["unusual"] for cs in cases], dtype=float)
    mean = float(np.mean(x)) if n else None
    tval = None
    if n >= 2 and G >= 2:
        dev = pd.Series(x - mean).groupby([cs["day"] for cs in cases]).sum().values
        se = np.sqrt(G / (G - 1.0) * np.sum(dev ** 2)) / n
        tval = float(mean / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n >= 2:
        a = np.array([cs["absf"] for cs in cases], dtype=float)
        med = np.median(a)
        big = x[a > med]
        small = x[a <= med]
        if len(big) > 0 and len(small) > 0:
            sup_val = float(big.mean() - small.mean())
            sup_pass = bool(sup_val > 0)

    main = {
        "name": "mean unusual 10-bar move of short cases",
        "value": mean,
        "statistic": {"name": "day-clustered t", "value": tval} if tval is not None else None,
        "threshold": "confirm: mean > 0 with t >= 2 and supporting check passing; reject: mean < 0 with t <= -2",
    }
    supp = {"name": "mean unusual move, larger |forecast| half minus smaller half",
            "value": sup_val, "passed": sup_pass}

    if n < 30 or G < 30:
        status = "not observable"
        decided = f"minimum counts not reached: {n} cases (need 30) on {G} distinct days (need 30)."
    elif tval is None:
        status = "inconclusive"
        decided = "the t could not be computed, so neither rule is met."
    elif mean > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "mean unusual move positive with t >= 2 and the larger half beats the smaller half."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the supporting check fails, which the plan calls inconclusive."
    elif mean < 0 and tval <= -2:
        status = "rejected"
        decided = "mean unusual move negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
