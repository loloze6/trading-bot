import numpy as np
import pandas as pd


def measure(bars):
    H = 18
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.nr_breakout.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            high = pd.to_numeric(df["high"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            prior_high = high.shift(1).rolling(12, min_periods=12).max()
            price_sit = (close > prior_high)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                sit = pd.Series(np.where(raw.notna(), raw > 0, price_sit), index=df.index).astype(bool)
            else:
                sit = price_sit.fillna(False).astype(bool)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & sit & (fc > 0)).sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = bool(agreement >= 0.9)
    else:
        agreement = None
        passed = None

    main_name = "mean excess 18-bar return of bets (return minus coin's normal 18-bar drift), before costs"
    main_thr = "confirm: mean > 0 with t >= 2 and supporting check passing; reject: mean < 0 with t <= -2; at least 30 independent cases"
    sup_name = "mean excess return of cases above the median signal forecast minus those at or below it"

    if passed is False:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"independent cases": None},
            "decided_by": "Fewer than 90% of bars with a non-zero forecast are long bars where the close sits above the prior 12-bar high, as the Fidelity's situation and side require.",
            "reading": "The situation is read as a raw component value above zero (recomputed from prices as close above the prior 12-bar highest high where the raw value is missing), on the long side.",
        }

    # ---------- 2. criterion ----------
    excess = []
    sig_fc = []
    for coin, wins in bars.items():
        # coin's normal 18-bar drift: non-overlapping grid of all its windows
        drift_rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for p in range(0, len(c) - H, H):
                a, b = c[p], c[p + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    drift_rets.append(b / a - 1.0)
        if len(drift_rets) == 0:
            continue
        drift = float(np.mean(drift_rets))

        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            n = len(f)
            low = 0.0
            seen_cells = set()
            for t in range(n):
                ft = f[t]
                if ft <= 0:
                    low = 0.0
                    continue
                low = min(low, ft)
                if ft - low >= BAND:
                    low = ft  # bet made: reference resets to this level
                    cell = t // H
                    if cell in seen_cells:
                        continue
                    seen_cells.add(cell)
                    if t + H < n and np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0:
                        r = c[t + H] / c[t] - 1.0
                        excess.append(r - drift)
                        sig_fc.append(ft)

    excess = np.asarray(excess, dtype=float)
    sig_fc = np.asarray(sig_fc, dtype=float)
    n_cases = int(len(excess))

    mean_ex = float(np.mean(excess)) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = float(np.std(excess, ddof=1))
        if sd > 0:
            t_stat = float(mean_ex / (sd / np.sqrt(n_cases)))

    sup_val = None
    sup_pass = None
    n_upper = n_lower = 0
    if n_cases > 0:
        med = float(np.median(sig_fc))
        up = excess[sig_fc > med]
        lo = excess[sig_fc <= med]
        n_upper, n_lower = int(len(up)), int(len(lo))
        if n_upper > 0 and n_lower > 0:
            sup_val = float(np.mean(up) - np.mean(lo))
            sup_pass = bool(sup_val > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} independent cases across all coins and windows, below the plan's minimum of 30."
    elif t_stat is not None and mean_ex > 0 and t_stat >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The mean excess return is positive with t >= 2 and the upper-minus-lower half difference is above 0."
    elif t_stat is not None and mean_ex < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean excess return is negative with t <= -2."
    elif t_stat is not None and t_stat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check (upper half minus lower half > 0) fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t of the mean excess return lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement),
                            "passed": passed},
        "main_measure": {"name": main_name,
                         "value": mean_ex,
                         "statistic": None if t_stat is None else {"name": "t of the mean", "value": t_stat},
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": {"independent cases": n_cases,
                   "upper half cases": n_upper,
                   "lower half cases": n_lower},
        "decided_by": decided,
        "reading": "A case is the first long bet (forecast rise of at least 2 points from its lowest positive level since the last bet, from 0 after flat) in each 18-bar grid cell counted from each window's first row, with its 18-bar return needing to end inside the window; the median split puts cases with forecast strictly above the median in the upper half and those at or below it in the lower half.",
    }
