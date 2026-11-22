import numpy as np
import pandas as pd


def measure(bars):
    H = 78
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.capitulation_panic.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            active = f.notna() & (f != 0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # situation: graded prior-fall x panic reading is positive, which happens
            # only when both the 540-bar prior return and the stretch return are negative
            situ = raw.notna() & (raw > 0)
            ok = active & situ & (f > 0)  # expected side: long (a rise)
            n_active += int(active.sum())
            n_agree += int(ok.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean unusual 78-bar move per long case (return minus coin's normal 78-bar drift)"
    main_thr = "confirm: mean > 0 with t >= 2 over >= 30 cases and weighted check > 0; reject: mean < 0 with t <= -2 over >= 30 cases"
    reading = ("The situation is read as bars where the component's raw value is positive (prior 540-bar return and "
               "stretch return both negative), the side long; a case is the first bet (forecast rise of >= 2 points "
               "from its lowest positive level since the last bet, reset to 0 when flat) in each 78-bar grid cell "
               "counted from each window's first row, the normal drift is the mean of the coin's non-overlapping "
               "78-bar returns over all its windows, and cases whose 78-bar return leaves the window are dropped.")

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": {"name": "forecast-weighted mean unusual move > 0", "value": None, "passed": None},
            "counts": {"cases": 0},
            "decided_by": "The strategy took no position, so no case exists; the minimum of 30 cases is not reached.",
            "reading": reading,
        }

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the prior-fall "
                           "times panic reading is positive, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    unusual = []
    weights = []
    for coin, wins in bars.items():
        # normal drift: mean 78-bar return on non-overlapping grid over all windows
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for i in range(0, len(c) - H, H):
                a, b = c[i], c[i + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    grid_rets.append(b / a - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            n = len(f)
            base = 0.0
            bets = []
            for t in range(n):
                ft = f[t]
                if ft <= 0:
                    base = 0.0
                    continue
                if ft - base >= BAND:
                    bets.append(t)
                    base = ft
                else:
                    base = min(base, ft)
            seen_cells = set()
            for t in bets:
                cell = t // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if t + H >= n:
                    continue
                a, b = c[t], c[t + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0):
                    continue
                unusual.append((b / a - 1.0) - drift)
                weights.append(f[t])

    u = np.asarray(unusual, dtype=float)
    wts = np.asarray(weights, dtype=float)
    n_cases = int(len(u))

    mean_u = float(np.mean(u)) if n_cases > 0 else None
    t_stat = None
    if n_cases >= 2:
        sd = float(np.std(u, ddof=1))
        if sd > 0:
            t_stat = float(mean_u / (sd / np.sqrt(n_cases)))
    wmean = float(np.sum(u * wts) / np.sum(wts)) if n_cases > 0 and np.sum(wts) > 0 else None
    sup_passed = None if wmean is None else bool(wmean > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 30 cases."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move cannot be computed (zero spread), so it meets neither rule."
    elif mean_u > 0 and t_stat >= 2 and sup_passed:
        status = "confirmed"
        decided = "Mean unusual move positive with t >= 2 over at least 30 cases, and the forecast-weighted mean is above 0."
    elif mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "Mean unusual move negative with t <= -2 over at least 30 cases."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the forecast-weighted mean unusual move is not above 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_stat is None else {"name": "ordinary t of the mean", "value": t_stat},
            "threshold": main_thr,
        },
        "supporting_check": {"name": "forecast-weighted mean unusual move > 0", "value": wmean, "passed": sup_passed},
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
