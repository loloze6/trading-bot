import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.wkend.last_history_value"
    H = 2
    MIN_CASES = 300

    active_total = 0
    active_agree = 0
    cases = []  # (forecast, r2, weekend_sign, coin)
    m2_by_coin = {}

    for coin, wins in bars.items():
        # Holding the coin: mean non-overlapping 2-bar return, pooled over all windows of the coin
        grid_rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).to_numpy()
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                r = c[idx + H] / c[idx] - 1.0
                grid_rets.extend([x for x in r if np.isfinite(x)])
        m2_by_coin[coin] = float(np.mean(grid_rets)) if len(grid_rets) else np.nan

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            is_sunday = (ts.dt.dayofweek == 6).to_numpy()
            close = df["close"].astype(float).to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy()
            else:
                raw = np.full(len(df), np.nan)
            # weekend move from prices inside the window, as fallback where the raw value is missing
            prev = np.concatenate([[np.nan], close[:-1]])
            r1 = close / prev - 1.0
            move = np.where(np.isfinite(raw), raw, r1)

            n = len(df)
            for t in range(n):
                f = fc[t]
                if not np.isfinite(f) or f == 0:
                    continue
                active_total += 1
                s = np.sign(move[t]) if np.isfinite(move[t]) else 0.0
                if is_sunday[t] and s != 0 and np.sign(f) == -s:
                    active_agree += 1
                if is_sunday[t] and t + H < n and np.isfinite(move[t]) and move[t] != 0:
                    r2 = close[t + H] / close[t] - 1.0
                    if np.isfinite(r2):
                        cases.append((float(f), float(r2), float(np.sign(move[t])), coin))

    main_name = "pooled mean of (forecast/10) x (r2 - m2) on Sunday-close active bars"
    threshold = "confirm: mean > 0 with t >= 2.0 and supporting check > 0; reject: mean < 0 with t <= -2.0; at least 300 Sunday cases"
    supp_name = "mean of -sign(weekend move) x (r2 - m2), top half of |forecast| minus bottom half"

    if active_total == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": supp_name, "value": None, "passed": None},
            "counts": {"Sunday cases": 0},
            "decided_by": "No bar has a non-zero forecast, so fewer than the 300 Sunday cases the plan needs.",
            "reading": "Situation = bar starting on Sunday (UTC) with forecast sign opposite to the sign of the raw vol-scaled Sunday return.",
        }

    agreement = active_agree / active_total
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"Sunday cases": len(cases)},
            "decided_by": "Fewer than 90% of active bars are Sunday-close bars with a forecast opposite to the weekend move, as the plan's Fidelity requires.",
            "reading": "Situation = bar starting on Sunday (UTC); expected side = minus the sign of the raw vol-scaled Sunday return (price return where the raw value is missing).",
        }

    f = np.array([c[0] for c in cases])
    r2 = np.array([c[1] for c in cases])
    sgn = np.array([c[2] for c in cases])
    m2 = np.array([m2_by_coin[c[3]] for c in cases]) if cases else np.array([])
    ok = np.isfinite(m2)
    f, r2, sgn, m2 = f[ok], r2[ok], sgn[ok], m2[ok]
    n = len(f)
    excess = r2 - m2
    vals = (f / 10.0) * excess

    mean = float(np.mean(vals)) if n else None
    if n >= 2 and np.std(vals, ddof=1) > 0:
        tstat = float(mean / (np.std(vals, ddof=1) / np.sqrt(n)))
    else:
        tstat = None

    supp_val = None
    supp_pass = None
    n_hi = n_lo = 0
    if n >= 2:
        a = np.abs(f)
        med = np.median(a)
        hi = a > med
        lo = ~hi
        n_hi, n_lo = int(hi.sum()), int(lo.sum())
        rev = -sgn * excess
        if n_hi > 0 and n_lo > 0:
            supp_val = float(np.mean(rev[hi]) - np.mean(rev[lo]))
            supp_pass = bool(supp_val > 0)

    counts = {"Sunday cases": int(n), "larger |forecast| half": n_hi, "smaller |forecast| half": n_lo}
    reading = ("Cases are bars starting on Sunday (UTC) with non-zero forecast and close[t+2] in the same window; "
               "m2 is each coin's mean 2-bar return on the grid 0,2,4,... of every window pooled over windows; "
               "the median split puts |forecast| above the median in the larger half and the rest in the smaller half; "
               "weekend move sign is the sign of the raw component value.")

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} Sunday cases, below the plan's minimum of 300."
    elif tstat is None:
        status = "inconclusive"
        decided = "The t of the mean cannot be computed (zero dispersion), so it meets neither the confirm nor the reject rule."
    elif mean > 0 and tstat >= 2.0 and supp_pass:
        status = "confirmed"
        decided = "The mean is above 0 with t >= 2.0 and the supporting check is above 0."
    elif mean < 0 and tstat <= -2.0:
        status = "rejected"
        decided = "The mean is below 0 with t <= -2.0."
    elif tstat >= 2.0:
        status = "inconclusive"
        decided = "t >= 2.0 but the supporting check is at or below 0 (or not computable), which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2.0 and 2.0, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": {"name": "ordinary t of the mean", "value": tstat} if tstat is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {"name": supp_name, "value": supp_val, "passed": supp_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
