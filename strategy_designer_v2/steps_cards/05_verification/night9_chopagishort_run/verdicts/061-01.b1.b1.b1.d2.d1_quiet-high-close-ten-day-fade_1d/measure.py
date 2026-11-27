import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    BAND = 2.0
    LOC_COL = "debug_info.components.high_close.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float)
            high = d["high"].astype(float)
            low = d["low"].astype(float)
            rng = (high - low)
            loc_px = ((close - low) / rng.replace(0, np.nan))
            if LOC_COL in d.columns:
                loc = pd.to_numeric(d[LOC_COL], errors="coerce").fillna(loc_px)
            else:
                loc = loc_px
            r = close.pct_change()
            vol = r.rolling(20, min_periods=20).std(ddof=1)
            gain = r / vol.replace(0, np.nan)
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series([""] * len(d))
            profile_ok = regime.str.lower() != "chop"
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            active = f != 0
            for i in np.where(active.values)[0]:
                g = gain.iloc[i]
                lc = loc.iloc[i]
                if pd.isna(g) or pd.isna(lc):
                    continue  # missing value: left out of this measure
                n_active += 1
                sit = (lc >= 0.75 - 1e-9) and (r.iloc[i] > 0) and (g <= 1.0 + 0.1) and bool(profile_ok.iloc[i])
                if sit and f.iloc[i] < 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean short-side unusual 10-bar move per case (return minus normal drift, sign flipped)"
    threshold = "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2"
    reading = ("Situation recomputed from prices (close location, 1-bar return over 20-bar std of daily returns, "
               "10% tolerance on the upper gain bound) with the profile taken as regime not 'chop'; a bet is a rise of "
               "|forecast| on the short side of at least 2 points from its lowest level since the last bet, the first bet "
               "of each 10-bar grid cell is the case; the split puts cases with |forecast| >= median in the larger half "
               "and < median in the smaller; same-day cases pooled by summing deviations per day.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are short bars of the plan's situation (close location >= 0.75, "
                           "up day of at most one 20-day std, choppy-agitated profile)."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = []  # (day, unusual_short, absforecast)
    for coin, wins in bars.items():
        # normal drift: mean of non-overlapping 10-bar returns over all windows
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                if c[p] > 0 and np.isfinite(c[p]) and np.isfinite(c[p + H]):
                    rets.append(c[p + H] / c[p] - 1.0)
        if len(rets) == 0:
            continue
        drift = float(np.mean(rets))
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            c = d["close"].astype(float).values
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            side = 0
            ref = 0.0
            taken_cells = set()
            for i in range(len(d)):
                fi = f[i]
                s = int(np.sign(fi))
                if s != side:
                    side = s
                    ref = 0.0
                if s >= 0:
                    continue
                m = -fi
                if m - ref >= BAND - 1e-12:
                    ref = m
                    cell = i // H
                    if cell in taken_cells:
                        continue
                    taken_cells.add(cell)
                    if i + H < len(c) and c[i] > 0 and np.isfinite(c[i + H]):
                        ret = c[i + H] / c[i] - 1.0
                        cases.append((ts.iloc[i].date().isoformat(), -(ret - drift), abs(fi)))
                else:
                    ref = min(ref, m)

    n = len(cases)
    days = sorted(set(x[0] for x in cases))
    n_days = len(days)
    counts = {"cases": int(n), "distinct days": int(n_days)}

    mean = None
    t = None
    if n > 0:
        vals = np.array([x[1] for x in cases], dtype=float)
        mean = float(vals.mean())
        dev = pd.Series(vals - mean).groupby([x[0] for x in cases]).sum()
        se = np.sqrt(float((dev.values ** 2).sum())) / n
        t = float(mean / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n > 0:
        a = np.array([x[2] for x in cases], dtype=float)
        vals = np.array([x[1] for x in cases], dtype=float)
        med = float(np.median(a))
        big = vals[a >= med]
        small = vals[a < med]
        if len(big) > 0 and len(small) > 0:
            sup_val = float(big.mean() - small.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    main = {"name": main_name, "value": mean,
            "statistic": ({"name": "t of the mean, same-day cases pooled", "value": t} if t is not None else None),
            "threshold": threshold}
    support = {"name": "larger-|forecast| half minus smaller half, mean short-side unusual move",
               "value": sup_val, "passed": sup_pass}

    if n < 30 or n_days < 30:
        status = "not observable"
        decided = f"Minimum counts not reached: {n} cases on {n_days} distinct days (plan needs 30 of each)."
    elif t is not None and mean > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean short-side unusual move above 0 with t >= 2 and the supporting check passes."
    elif t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = "Mean short-side unusual move below 0 with t <= -2."
    elif t is not None and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check failed, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2 (or undefined), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
