import json
import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    BAND = 2.0
    PIERCE_PERIOD = 30
    TREND_PERIOD = 60
    TREND_VETO = 10.0
    MIN_CASES = 20
    MIN_DAYS = 15

    def _parse(x):
        if isinstance(x, dict):
            return x
        if isinstance(x, str):
            try:
                v = json.loads(x)
                return v if isinstance(v, dict) else None
            except Exception:
                return None
        return None

    def get_comp(df, cid, field):
        col = "debug_info.components.%s.%s" % (cid, field)
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce").reset_index(drop=True)
        if "debug_info.components" in df.columns:
            out = []
            for x in df["debug_info.components"].tolist():
                d = _parse(x)
                v = np.nan
                if d is not None:
                    c = d.get(cid)
                    if isinstance(c, dict) and field in c:
                        try:
                            v = float(c[field])
                        except Exception:
                            v = np.nan
                out.append(v)
            return pd.Series(out, dtype=float)
        return pd.Series([np.nan] * len(df), dtype=float)

    # ---------- pass 1: situation check, drift, cases ----------
    n_active = 0
    n_agree = 0
    cases = []  # (coin, day, ret, absfc)
    drift = {}

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        grid_rets = []
        coin_cases = []
        for w in sorted(wins.keys(), key=lambda s: (len(str(s)), str(s))):
            df = wins[w].reset_index(drop=True)
            if len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce")
            low = pd.to_numeric(df["low"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)

            # pierce: recorded raw value, else recomputed from prices
            rec = get_comp(df, "pierce", "last_history_value")
            prior_low = low.shift(1).rolling(PIERCE_PERIOD, min_periods=PIERCE_PERIOD).min()
            recomputed = pd.Series(np.where(
                prior_low.notna() & (low < prior_low) & (close >= prior_low),
                (prior_low - low) / prior_low * 100.0,
                np.where(prior_low.notna(), 0.0, np.nan)), dtype=float)
            pierce_val = rec.where(rec.notna(), recomputed)
            pierce_ok = (pierce_val > 0).fillna(False)

            # rising profile: 60-bar price evolution > 10, else detector's decision
            evo = (close / close.shift(TREND_PERIOD) - 1.0) * 100.0
            rising = pd.Series(np.where(evo.notna(), evo > TREND_VETO,
                                        regime == "mean_reversion"), dtype=bool)

            active = fc != 0
            situ = pierce_ok & rising & (fc < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

            # non-overlapping grid returns for drift
            for p in range(0, n - H, H):
                c0, c1 = close.iloc[p], close.iloc[p + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                    grid_rets.append(c1 / c0 - 1.0)

            # bets on the short side
            ref = 0.0
            prev_side = 0
            bet_bars = []
            for i in range(n):
                f = fc.iloc[i]
                side = int(np.sign(f))
                if side == 0:
                    ref = 0.0
                    prev_side = 0
                    continue
                if side != prev_side:
                    ref = 0.0
                m = abs(f)
                if m - ref >= BAND:
                    if side < 0:
                        bet_bars.append(i)
                    ref = m
                else:
                    ref = min(ref, m)
                prev_side = side

            seen_cells = set()
            for i in bet_bars:
                cell = i // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if i + H >= n:
                    continue
                c0, c1 = close.iloc[i], close.iloc[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1) and c0 > 0):
                    continue
                coin_cases.append((coin, ts.iloc[i].strftime("%Y-%m-%d"),
                                   c1 / c0 - 1.0, abs(float(fc.iloc[i]))))
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan
        cases.extend(coin_cases)

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean signed (short) unusual 10-bar move vs coin's normal drift"
    thr = "confirm: mean > 0 with t >= 2 and depth slope > 0; reject: mean < 0 with t <= -2"
    reading_base = ("Rising profile recomputed as 60-bar close change > 10% inside the window (regime column used where "
                    "60 prior bars are missing), pierce from the recorded raw value else from prices; a case is the first "
                    "short-side bet (forecast rise of >= 2 points) in each 10-bar grid cell with a full 10-bar return in its "
                    "window, day-clustered t uses summed deviations per UTC day with a G/(G-1) correction.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are short bars on a reclaimed pierce of the "
                           "30-day low in a rising market, as the Fidelity requires."),
            "reading": reading_base,
        }

    # ---------- main measure ----------
    vals, days, absf = [], [], []
    for coin, day, r, a in cases:
        d = drift.get(coin, np.nan)
        if not np.isfinite(d):
            continue
        vals.append(-(r - d))
        days.append(day)
        absf.append(a)
    vals = np.array(vals, dtype=float)
    absf = np.array(absf, dtype=float)
    n_cases = int(len(vals))
    n_days = int(len(set(days)))
    counts = {"cases": n_cases, "distinct days": n_days}

    mean = float(np.mean(vals)) if n_cases > 0 else None
    t = None
    if n_cases > 1 and n_days > 1:
        dev = pd.Series(vals - mean).groupby(pd.Series(days)).sum().values
        G = len(dev)
        var = (G / (G - 1.0)) * np.sum(dev ** 2) / (n_cases ** 2)
        se = float(np.sqrt(var))
        t = float(mean / se) if se > 0 else None

    slope = None
    if n_cases > 1 and np.var(absf) > 0:
        slope = float(np.polyfit(absf, vals, 1)[0])
    slope_pass = None if slope is None else bool(slope > 0)

    main = {"name": main_name, "value": mean,
            "statistic": None if t is None else {"name": "t of the mean, same-day cases as one", "value": t},
            "threshold": thr}
    supp = {"name": "slope of signed unusual move on |forecast|", "value": slope, "passed": slope_pass}

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = "Minimum not reached: fewer than 20 cases or cases on fewer than 15 distinct days (%d cases, %d days)." % (n_cases, n_days)
    elif mean is None or t is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed, so neither the confirm nor the reject rule is met."
    elif mean > 0 and t >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "Confirm: the mean signed unusual move is above 0 with t >= 2 and the depth slope is above 0."
        else:
            status = "inconclusive"
            decided = "Inconclusive: a confirming mean whose depth slope is not above 0."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "Reject: the mean signed unusual move is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
