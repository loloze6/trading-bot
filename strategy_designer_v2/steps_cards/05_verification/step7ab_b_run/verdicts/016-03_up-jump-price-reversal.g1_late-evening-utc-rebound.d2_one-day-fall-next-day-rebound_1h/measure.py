import numpy as np
import pandas as pd


def measure(bars):
    H = 24
    RAW = "debug_info.components.fall24.last_history_value"

    # ---------- 1. Situation check: a 24-hour fall (raw 24-bar return < 0), expected side long ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            recomputed = close / close.shift(H) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & (raw < 0) & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "t of mean of (forecast/10) x (24-bar forward return minus coin's normal 24-bar drift), grid cases with forecast > 0"
    main_threshold = "confirm if t >= 2 (with upper-minus-lower half difference > 0); reject if t <= -2; else inconclusive"
    sup_name = "mean excess 24-bar forward return, upper half minus lower half at median forecast"
    reading = ("Cases are bars at positions 0, 24, 48, ... of each window with forecast > 0 and a forward return inside "
               "the window; the coin's normal drift is the mean 24-bar return over all grid bars of all its windows; "
               "the upper half is forecast > median and the lower half forecast <= median; the plan's 200-case minimum, "
               "when not reached, gives 'not observable' as the workflow requires.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "grid cases with forecast > 0": None},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are bars after a 24-hour fall with a "
                           "long (positive) forecast, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    case_fc = []
    case_ret = []
    case_coin = []
    drift = {}
    for coin, wins in bars.items():
        all_rets = []
        coin_fc, coin_ret = [], []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for i in range(0, n, H):
                j = i + H
                if j >= n:
                    break
                c0, c1 = close[i], close[j]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    coin_fc.append(fc[i])
                    coin_ret.append(r)
        drift[coin] = float(np.mean(all_rets)) if all_rets else np.nan
        case_fc.extend(coin_fc)
        case_ret.extend(coin_ret)
        case_coin.extend([coin] * len(coin_fc))

    fcs = np.array(case_fc, dtype=float)
    rets = np.array(case_ret, dtype=float)
    dr = np.array([drift[c] for c in case_coin], dtype=float)
    excess = rets - dr
    ok = np.isfinite(excess) & np.isfinite(fcs)
    fcs, excess = fcs[ok], excess[ok]
    n_cases = int(len(fcs))
    counts = {"grid cases with forecast > 0": n_cases}

    vals = (fcs / 10.0) * excess
    mean_val = float(np.mean(vals)) if n_cases > 0 else None
    t = None
    if n_cases > 1:
        sd = float(np.std(vals, ddof=1))
        if sd > 0:
            t = float(mean_val / (sd / np.sqrt(n_cases)))

    diff = None
    n_up = n_lo = 0
    if n_cases > 0:
        med = float(np.median(fcs))
        up = fcs > med
        lo = ~up
        n_up, n_lo = int(up.sum()), int(lo.sum())
        if n_up > 0 and n_lo > 0:
            diff = float(np.mean(excess[up]) - np.mean(excess[lo]))
    counts["upper half cases"] = n_up
    counts["lower half cases"] = n_lo
    sup_passed = None if diff is None else bool(diff > 0)

    main = {"name": main_name, "value": mean_val,
            "statistic": None if t is None else {"name": "ordinary t of the mean", "value": t},
            "threshold": main_threshold}
    sup = {"name": sup_name, "value": diff, "passed": sup_passed}

    if n_cases < 200:
        status = "not observable"
        decided = f"Only {n_cases} grid cases with forecast > 0, below the plan's minimum of 200."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the main measure could not be computed (zero dispersion), so neither confirm nor reject rule is met."
    elif t >= 2 and sup_passed:
        status = "confirmed"
        decided = "The main measure's t is 2 or more and the upper-half minus lower-half difference is positive."
    elif t <= -2:
        status = "rejected"
        decided = "The main measure's t is -2 or less."
    elif t >= 2:
        status = "inconclusive"
        decided = "The main measure's t is 2 or more but the upper-half minus lower-half difference is 0 or below."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
