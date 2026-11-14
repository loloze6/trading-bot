import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    POS = "postRebalance_current_allocation"
    act_pos, act_exc, act_ret = [], [], []
    for coin in sorted(bars.keys()):
        for window in sorted(bars[coin].keys()):
            df = bars[coin][window].reset_index(drop=True)
            if df is None or len(df) < 2:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").astype(float)
            ret = close.shift(-1) / close - 1.0  # next-bar return, inside the window only
            valid_ret = ret.dropna()
            if len(valid_ret) == 0:
                continue
            bench = float(valid_ret.mean())  # coin's mean daily return over all bars of this window
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            pos = pd.to_numeric(df[POS], errors="coerce")
            mask = (fc > 0) & ret.notna() & pos.notna()
            act_pos.extend(pos[mask].astype(float).tolist())
            act_ret.extend(ret[mask].astype(float).tolist())
            act_exc.extend((ret[mask] - bench).astype(float).tolist())

    p = np.asarray(act_pos, dtype=float)
    r = np.asarray(act_ret, dtype=float)
    x = np.asarray(act_exc, dtype=float)
    n_active = int(len(p))

    # main measure: position-weighted mean next-bar excess return
    wmean = None
    t_main = None
    sw = float(np.sum(p)) if n_active else 0.0
    if n_active >= 2 and sw != 0:
        wmean = float(np.sum(p * x) / sw)
        g = p * x
        sd = float(np.std(g, ddof=1))
        if sd > 0:
            t_main = float(np.mean(g) / (sd / np.sqrt(len(g))))
        else:
            t_main = float("inf") if np.mean(g) > 0 else (float("-inf") if np.mean(g) < 0 else 0.0)

    # supporting check: top third minus bottom third of positions, next-bar return
    diff = None
    t_sup = None
    k = n_active // 3
    if k >= 2:
        order = np.argsort(p, kind="mergesort")
        bottom = r[order[:k]]
        top = r[order[-k:]]
        diff = float(np.mean(top) - np.mean(bottom))
        tt = stats.ttest_ind(top, bottom, equal_var=False)
        t_sup = float(tt.statistic) if np.isfinite(tt.statistic) else None

    sup_passed = None if diff is None else bool(diff > 0)

    # decision
    if n_active < 60:
        status = "inconclusive"
        decided_by = f"Fewer than 60 active bars in total ({n_active}), so the test is inconclusive."
    elif wmean is None:
        status = "inconclusive"
        decided_by = "The position-weighted mean could not be computed (zero total position on active bars), so the test is inconclusive."
    elif wmean <= 0:
        status = "rejected"
        decided_by = "The position-weighted mean next-bar excess return is <= 0."
    elif diff is not None and t_sup is not None and diff < 0 and t_sup <= -2:
        status = "rejected"
        decided_by = "The top third of positions has a lower next-bar return than the bottom third with Welch t <= -2."
    elif t_main is not None and t_main >= 2 and diff is not None and diff > 0:
        status = "confirmed"
        decided_by = "Pooled over the windows, the position-weighted mean next-bar excess return is above 0 with t >= 2 and the top-minus-bottom-third difference is also positive."
    elif t_main is None or t_main < 2:
        status = "inconclusive"
        decided_by = "The excess return is positive but its t is below 2."
    else:
        status = "inconclusive"
        decided_by = "The main measure is positive with t >= 2 but the supporting check does not have the same sign (or could not be computed)."

    return {
        "status": status,
        "main_measure": {
            "name": "position-weighted mean next-bar excess return on active bars",
            "value": wmean,
            "statistic": None if t_main is None else {"name": "t of the mean of position x excess return", "value": t_main},
            "threshold": "above 0 with t >= 2 to confirm; <= 0 rejects",
        },
        "supporting_check": {
            "name": "next-bar return, top third minus bottom third of positions (Welch t %s)" % (
                "n/a" if t_sup is None else f"{t_sup:.3f}"),
            "value": diff,
            "passed": sup_passed,
        },
        "counts": {"active bars": n_active, "bars per third": int(k)},
        "decided_by": decided_by,
        "reading": ("Active bars are rows with forecast > 0 and a next close in the same window, the weight is "
                    "postRebalance_current_allocation, excess is the next-bar return minus the mean next-bar return of all "
                    "bars of that same window, the weighted mean is sum(pos*excess)/sum(pos) with its t taken as the ordinary "
                    "t of the per-bar pos*excess values, and the thirds are the floor(n/3) lowest and highest positions "
                    "compared by Welch t (top minus bottom)."),
    }
