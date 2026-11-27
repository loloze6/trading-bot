import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    BAND = 2.0
    LOC_COL = "debug_info.components.low_close.last_history_value"
    EPS = 1e-9

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            hi = df["high"].astype(float).values
            lo = df["low"].astype(float).values
            cl = df["close"].astype(float).values
            rng = hi - lo
            with np.errstate(divide="ignore", invalid="ignore"):
                loc_px = np.where(rng > 0, (hi - cl) / rng, np.nan)
            if LOC_COL in df.columns:
                rec = pd.to_numeric(df[LOC_COL], errors="coerce").values
                loc = np.where(np.isfinite(rec), rec, loc_px)
            else:
                loc = loc_px
            reg = df["regime"].astype(str).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            active = fc != 0
            agitated = reg != "chop"
            situ = np.isfinite(loc) & (loc >= 0.75 - EPS) & agitated
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on short side": n_agree},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are agitated bars (not vetoed to chop) "
                           "with (high-close)/(high-low) >= 0.75 and a short forecast, as the Fidelity's situation requires."),
            "reading": ("Agitation is read from the regime column not being the veto's 'chop' (the 365-bar volatility "
                        "percentile cannot be rebuilt inside ~120-bar windows); the close location is the recorded raw "
                        "value where present, else recomputed from the prices."),
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, day, unusual, absf)
    for coin in sorted(bars):
        # normal drift: mean non-overlapping 7-bar return over all windows
        drift_rets = []
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            cl = df["close"].astype(float).values
            for p in range(0, len(cl) - H, H):
                if cl[p] > 0 and np.isfinite(cl[p]) and np.isfinite(cl[p + H]):
                    drift_rets.append(cl[p + H] / cl[p] - 1.0)
        if len(drift_rets) == 0:
            continue
        drift = float(np.mean(drift_rets))

        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            cl = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            # short bets: rise of the short forecast's size of >= BAND above its lowest since last bet
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            for i in range(n):
                if fc[i] < 0:
                    m = -fc[i]
                    if m - ref >= BAND - EPS:
                        bet[i] = True
                        ref = m
                    else:
                        ref = min(ref, m)
                else:
                    ref = 0.0
            # once per grid cell
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                if not (np.isfinite(cl[t]) and np.isfinite(cl[t + H]) and cl[t] > 0):
                    continue
                ret = cl[t + H] / cl[t] - 1.0
                unusual = -(ret - drift)
                day = ts.iloc[t].strftime("%Y-%m-%d")
                cases.append((coin, day, float(unusual), float(abs(fc[t])), ts.iloc[t].value))

    n_cases = len(cases)
    days = sorted(set(c[1] for c in cases))
    n_days = len(days)

    mean = float(np.mean([c[2] for c in cases])) if n_cases else None
    tval = None
    if n_cases >= 2 and n_days >= 2:
        x = np.array([c[2] for c in cases])
        dev = pd.Series(x - mean).groupby([c[1] for c in cases]).sum().values
        G = len(dev)
        var = (G / (G - 1)) * np.sum(dev ** 2) / (n_cases ** 2)
        se = np.sqrt(var)
        if se > 0:
            tval = float(mean / se)

    # supporting check: larger-|forecast| half vs smaller half
    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        order = sorted(cases, key=lambda c: (-c[3], c[4], c[0]))
        k = n_cases // 2
        big = [c[2] for c in order[:k]]
        small = [c[2] for c in order[n_cases - k:]]
        sup_val = float(np.mean(big) - np.mean(small))
        sup_pass = bool(sup_val > 0)

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, fewer than the plan's minimum of 30."
    elif mean is not None and tval is not None and mean > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean unusual move is positive with t >= 2 and the larger-|forecast| half beats the smaller half."
    elif mean is not None and tval is not None and mean < 0 and tval <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2."
    else:
        status = "inconclusive"
        if tval is not None and mean is not None and mean > 0 and tval >= 2:
            decided = "A confirming t >= 2 but the supporting check failed."
        else:
            decided = "The t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": passed},
        "main_measure": {
            "name": "mean unusual 7-bar move in the short direction (return minus coin drift)",
            "value": mean,
            "statistic": None if tval is None else {"name": "t of the mean, cases of one day summed", "value": tval},
            "threshold": "confirm: mean > 0 with t >= 2 (and supporting check); reject: mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "mean unusual move, larger-|forecast| half minus smaller half",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"cases": n_cases, "distinct case days": n_days},
        "decided_by": decided,
        "reading": ("Agitation for the situation check is the regime not being the veto's 'chop'; a case is the first short "
                    "bet in each 7-bar grid cell (cases whose 7-bar return leaves the window are dropped); the halves are "
                    "the n//2 cases with the largest and the n//2 with the smallest |forecast| (middle case dropped if n is "
                    "odd); the t uses a day-clustered standard error; fewer than 30 case days is reported as 'not observable' "
                    "per the workflow's minimum-count rule."),
    }
