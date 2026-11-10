import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    POS = "postRebalance_current_allocation"
    MIN_ACTIVE = 60

    act_ret, act_exc, act_pos = [], [], []
    n_windows = 0

    for coin, wins in bars.items():
        for wname, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            # next-bar return inside this window only (horizon 1: every bar, no overlap)
            nxt = close.shift(-1) / close - 1.0
            # coin's mean daily return over all bars of the same window
            all_valid = nxt.dropna()
            if len(all_valid) == 0:
                continue
            n_windows += 1
            mean_all = float(all_valid.mean())
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            pos = pd.to_numeric(d[POS], errors="coerce")
            mask = (fc > 0) & nxt.notna() & pos.notna()
            for i in np.where(mask.values)[0]:
                r = float(nxt.iloc[i])
                act_ret.append(r)
                act_exc.append(r - mean_all)
                act_pos.append(float(pos.iloc[i]))

    act_ret = np.array(act_ret, dtype=float)
    act_exc = np.array(act_exc, dtype=float)
    act_pos = np.array(act_pos, dtype=float)
    n_active = int(len(act_ret))

    # main measure: position-weighted mean next-bar excess return
    main_val, main_t = None, None
    wsum = float(act_pos.sum()) if n_active else 0.0
    if n_active > 0 and wsum > 0:
        main_val = float(np.sum(act_exc * act_pos) / wsum)
        if n_active >= 2:
            z = act_exc * act_pos / (wsum / n_active)  # its mean equals the weighted mean
            sd = float(np.std(z, ddof=1))
            if sd > 0:
                main_t = float(np.mean(z) / (sd / np.sqrt(n_active)))
            else:
                main_t = float(np.inf) if np.mean(z) > 0 else (float(-np.inf) if np.mean(z) < 0 else 0.0)

    # supporting check: top third of positions minus bottom third, next-bar return, Welch t
    k = n_active // 3
    sup_diff, sup_t = None, None
    if k >= 1:
        order = np.argsort(act_pos, kind="mergesort")
        bottom = act_ret[order[:k]]
        top = act_ret[order[-k:]]
        sup_diff = float(np.mean(top) - np.mean(bottom))
        if k >= 2:
            tt = stats.ttest_ind(top, bottom, equal_var=False)
            sup_t = float(tt.statistic) if np.isfinite(tt.statistic) else None
    sup_passed = None if sup_diff is None else bool(sup_diff > 0)

    # decision
    if n_active < MIN_ACTIVE:
        status = "inconclusive"
        decided = f"Only {n_active} active bars (< {MIN_ACTIVE} needed in total), so the test is inconclusive."
    elif main_val is None:
        status = "inconclusive"
        decided = "The position-weighted mean could not be computed (no positive position weight), so the test is inconclusive."
    elif main_val <= 0:
        status = "rejected"
        decided = "Reject: the position-weighted mean next-bar excess return is <= 0."
    elif sup_diff is not None and sup_diff < 0 and sup_t is not None and sup_t <= -2:
        status = "rejected"
        decided = "Reject: the top third of positions has a lower next-bar return than the bottom third with Welch t <= -2."
    elif main_t is not None and main_t >= 2 and sup_passed:
        status = "confirmed"
        decided = "Confirm: pooled over the windows the position-weighted mean next-bar excess return is above 0 with t >= 2 and the top-minus-bottom-third check has the same (positive) sign."
    elif main_t is None or main_t < 2:
        status = "inconclusive"
        decided = "Inconclusive: the excess return is positive but its t is below 2."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the main measure is positive but the supporting check does not have the same sign."

    return {
        "status": status,
        "main_measure": {
            "name": "position-weighted mean next-bar excess return on active bars",
            "value": main_val,
            "statistic": None if main_t is None else {"name": "t of the weighted mean", "value": main_t},
            "threshold": "above 0 with t >= 2 to confirm; <= 0 rejects",
        },
        "supporting_check": {
            "name": "next-bar return, top third minus bottom third of positions",
            "value": sup_diff,
            "passed": sup_passed,
        },
        "counts": {"active bars": n_active, "windows": n_windows},
        "decided_by": decided,
        "reading": (
            "Active bars are forecast > 0 with a next close in the same window, weighted by postRebalance_current_allocation; "
            "excess return is the next-bar return minus that window's mean next-bar return over all its bars; the t of the weighted mean "
            "is the ordinary t of the values position x excess / mean position (whose mean equals the weighted mean); thirds are the "
            "floor(n/3) smallest and largest positions pooled over all windows, compared by Welch t (top minus bottom); the 60-bar minimum is checked before the reject rules."
        ),
    }
