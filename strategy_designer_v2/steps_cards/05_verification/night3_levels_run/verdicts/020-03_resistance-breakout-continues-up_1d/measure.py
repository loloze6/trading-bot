import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.res_break.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0)
            # Situation: a close through a held swing-high level, i.e. a positive raw value; side: long.
            situ = raw.notna() & (raw > 0) & (f > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean excess 5-bar return over cases (case return minus coin's normal 5-bar drift)"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 cases; reject: mean < 0 with t <= -2 over >= 30 cases"
    reading = ("A case is the first bet bar (long forecast rise of at least 2 points from its lowest level "
               "since the last bet, from 0 after a flat) in each 5-bar grid cell counted from each window's "
               "first row, dropped if its 5-bar return leaves the window; the median split puts raw values "
               "strictly above the median in the top half and the rest in the bottom half.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": None, "active bars": n_active},
            "decided_by": ("Fewer than 90 % of the active bars (forecast not zero) are long bars on which the "
                           "component's raw value shows a close crossing above a held swing-high level"
                           if n_active > 0 else
                           "The record has no active bars, so the forecast never acts on the plan's situation"),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    excess = []
    raws = []
    for coin, wins in bars.items():
        # normal 5-bar drift: mean of non-overlapping 5-bar returns over all the coin's windows
        drift_rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    drift_rets.append(c[i + H] / c[i] - 1.0)
        if len(drift_rets) == 0:
            continue
        drift = float(np.mean(drift_rets))

        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            if RAW in df.columns:
                rv = pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
            else:
                rv = np.full(len(df), np.nan)
            n = len(df)
            # bet detection on the long side
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            for i in range(n):
                fi = f[i]
                if fi <= 0:
                    ref = 0.0
                    continue
                if fi - ref >= BAND:
                    bet[i] = True
                    ref = fi
                else:
                    ref = min(ref, fi)
            # one case per 5-bar grid cell
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H])) or c[t] == 0:
                    continue
                excess.append(c[t + H] / c[t] - 1.0 - drift)
                raws.append(rv[t])

    excess = np.asarray(excess, dtype=float)
    raws = np.asarray(raws, dtype=float)
    n_cases = int(len(excess))

    mean_ex = float(np.mean(excess)) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = float(np.std(excess, ddof=1))
        if sd > 0:
            t_stat = float(mean_ex / (sd / np.sqrt(n_cases)))

    # supporting check
    sup_val = None
    sup_pass = None
    n_top = n_bot = 0
    ok = np.isfinite(raws)
    if ok.sum() > 0:
        r = raws[ok]
        e = excess[ok]
        med = float(np.median(r))
        top = e[r > med]
        bot = e[r <= med]
        n_top, n_bot = int(len(top)), int(len(bot))
        if n_top > 0 and n_bot > 0:
            sup_val = float(np.mean(top) - np.mean(bot))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Fewer than 30 cases in total ({n_cases}), the plan's minimum count, so the data cannot show the idea."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean excess return could not be computed (zero dispersion), so neither confirm nor reject is met."
    elif mean_ex > 0 and t_stat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean excess 5-bar return positive with t >= 2 over at least 30 cases, and the top-minus-bottom raw-value difference is above 0."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the top-minus-bottom difference of mean excess return is not above 0."
    elif mean_ex < 0 and t_stat <= -2:
        status = "rejected"
        decided = "Mean excess 5-bar return negative with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "t strictly between -2 and 2 (with at least 30 cases)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": ({"name": "ordinary t of the mean", "value": t_stat} if t_stat is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess return, top half minus bottom half of raw value (N x margin)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"cases": n_cases, "top half cases": n_top, "bottom half cases": n_bot, "active bars": n_active},
        "decided_by": decided,
        "reading": reading,
    }
