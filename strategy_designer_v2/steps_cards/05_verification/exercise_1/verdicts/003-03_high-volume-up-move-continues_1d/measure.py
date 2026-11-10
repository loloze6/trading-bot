import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    POS = "postRebalance_current_allocation"
    rows = []  # (position, next_ret, excess)
    for coin, wins in bars.items():
        for wname, df in wins.items():
            if df is None or len(df) < 2:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0  # next-bar return, inside this window only
            win_mean = nxt.dropna().mean()  # coin's mean daily return over all bars of this window
            if not np.isfinite(win_mean):
                continue
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            pos = pd.to_numeric(d[POS], errors="coerce")
            mask = (fc > 0) & nxt.notna() & pos.notna()
            for i in np.where(mask.values)[0]:
                r = float(nxt.iloc[i])
                rows.append((float(pos.iloc[i]), r, r - float(win_mean)))

    n = len(rows)
    main_name = "position-weighted mean next-bar excess return on active bars"
    main_thr = "above 0 with t >= 2 to confirm; <= 0 rejects"
    sup_name = "next-bar return, top third minus bottom third of positions"

    main_val, main_t = None, None
    sup_val, sup_t, sup_pass = None, None, None

    if n > 0:
        arr = np.array(rows, dtype=float)
        w, ret, ex = arr[:, 0], arr[:, 1], arr[:, 2]
        mw = w.mean()
        if mw != 0 and np.isfinite(mw):
            x = w * ex / mw  # mean of x equals the position-weighted mean
            main_val = float(x.mean())
            if n > 1 and x.std(ddof=1) > 0:
                main_t = float(x.mean() / (x.std(ddof=1) / np.sqrt(n)))
        k = n // 3
        if k >= 2:
            order = np.argsort(w, kind="mergesort")
            bot, top = ret[order[:k]], ret[order[-k:]]
            sup_val = float(top.mean() - bot.mean())
            tt = stats.ttest_ind(top, bot, equal_var=False)
            sup_t = float(tt.statistic) if np.isfinite(tt.statistic) else None
            sup_pass = bool(sup_val > 0)

    if n < 60:
        status = "inconclusive"
        decided = f"Only {n} active bars, fewer than the 60 required, so the test is inconclusive."
    elif main_val is None:
        status = "inconclusive"
        decided = "The position-weighted mean could not be computed (positions sum to zero), so the test is inconclusive."
    elif main_val <= 0:
        status = "rejected"
        decided = "The position-weighted mean next-bar excess return is <= 0, which rejects."
    elif sup_val is not None and sup_val < 0 and sup_t is not None and sup_t <= -2:
        status = "rejected"
        decided = "The top third of positions has a lower next-bar return than the bottom third with t <= -2, which rejects."
    elif main_t is not None and main_t >= 2 and sup_val is not None and sup_val > 0:
        status = "confirmed"
        decided = "Pooled over the windows, the excess return is above 0 with t >= 2 and the supporting check has the same sign, which confirms."
    elif main_t is None or main_t < 2:
        status = "inconclusive"
        decided = "The excess return is positive but with t < 2, which is inconclusive."
    else:
        status = "inconclusive"
        decided = "The main measure is positive but the supporting check has the opposite sign (or could not be computed), which is inconclusive."

    return {
        "status": status,
        "main_measure": {"name": main_name, "value": main_val, "threshold": main_thr,
                         "t_stat": main_t},
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass,
                             "t_stat": sup_t},
        "cases": int(n),
        "decided_by": decided,
        "reading": ("Active bars are forecast > 0 rows with a next close in the same window. "
                    "Each bar's excess return is its next-bar return minus the mean next-bar return "
                    "over all bars of its own window. The weighted mean is weighted by "
                    "postRebalance_current_allocation, with t taken from the per-bar values "
                    "position*excess/mean(position). Thirds are the n//3 lowest and highest positions "
                    "among pooled active bars, ranked by stable sort and compared with Welch's t-test."),
    }
