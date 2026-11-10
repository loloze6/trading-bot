import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    in_rets = []
    all_rets = []
    n_stretches = 0

    for coin in sorted(bars.keys()):
        for window in sorted(bars[coin].keys()):
            df = bars[coin][window].reset_index(drop=True)
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            # next-bar return inside this window only
            nxt = close.shift(-1) / close - 1.0
            # non-overlapping grid for h=1: every bar from position 0
            valid_all = nxt.notna()
            all_rets.extend(nxt[valid_all].tolist())
            in_mask = valid_all & fc.notna() & (fc > 0)
            in_rets.extend(nxt[in_mask].tolist())

            # distinct stretches: runs of consecutive forecast > 0 bars inside the window
            pos = (fc > 0) & fc.notna()
            starts = pos & ~pos.shift(1, fill_value=False)
            n_stretches += int(starts.sum())

    in_arr = np.asarray(in_rets, dtype=float)
    all_arr = np.asarray(all_rets, dtype=float)
    n_in = int(in_arr.size)
    n_all = int(all_arr.size)

    mean_in = float(np.mean(in_arr)) if n_in > 0 else None
    mean_all = float(np.mean(all_arr)) if n_all > 0 else None
    diff = (mean_in - mean_all) if (mean_in is not None and mean_all is not None) else None

    t_val = None
    if n_in >= 2 and n_all >= 2:
        t_res = stats.ttest_ind(in_arr, all_arr, equal_var=False)
        t_val = float(t_res.statistic)
        if not np.isfinite(t_val):
            t_val = None

    up_in = float(np.mean(in_arr > 0)) if n_in > 0 else None
    up_all = float(np.mean(all_arr > 0)) if n_all > 0 else None
    up_diff = (up_in - up_all) if (up_in is not None and up_all is not None) else None
    sup_passed = (bool(up_in > up_all) if up_diff is not None else None)

    if n_in < 100 or n_stretches < 3:
        status = "inconclusive"
        decided_by = (f"Inconclusive: fewer than 100 in-stretch bars ({n_in}) or fewer than 3 distinct "
                      f"up-cross stretches ({n_stretches}) across the windows.")
    elif diff is None or t_val is None:
        status = "inconclusive"
        decided_by = "Inconclusive: the mean difference or its t-statistic could not be computed."
    elif t_val <= -2.0:
        status = "rejected"
        decided_by = (f"Rejected: t-statistic {t_val:.3f} is -2.0 or lower, so moves reverse after up-crosses.")
    elif diff <= 0:
        status = "rejected"
        decided_by = (f"Rejected: the in-stretch mean daily return is at or below the all-bar mean "
                      f"(difference {diff:.6f}), so there is no persistence.")
    elif t_val >= 2.0 and sup_passed:
        status = "confirmed"
        decided_by = (f"Confirmed: the in-stretch mean exceeds the all-bar mean with t {t_val:.3f} >= 2.0 "
                      f"and the in-stretch up-day share exceeds the all-bar share.")
    elif t_val >= 2.0:
        status = "inconclusive"
        decided_by = (f"Inconclusive: t {t_val:.3f} >= 2.0 but the in-stretch up-day share does not exceed "
                      f"the all-bar share, so the confirm rule is not fully met and no reject rule applies.")
    else:
        status = "inconclusive"
        decided_by = (f"Inconclusive: the in-stretch mean exceeds the all-bar mean but t {t_val:.3f} lies "
                      f"between -2.0 and 2.0.")

    return {
        "status": status,
        "main_measure": {
            "name": "in-stretch minus all-bar mean next-bar return (before costs)",
            "value": None if diff is None else float(diff),
            "statistic": None if t_val is None else {"name": "Welch t (in-stretch vs all bars)", "value": t_val},
            "threshold": "confirm if difference > 0 with one-sided t >= 2.0; reject if difference <= 0 or t <= -2.0",
        },
        "supporting_check": {
            "name": "in-stretch up-day share minus all-bar up-day share",
            "value": None if up_diff is None else float(up_diff),
            "passed": sup_passed,
        },
        "counts": {
            "in-stretch bars": n_in,
            "all bars": n_all,
            "distinct up-cross stretches": int(n_stretches),
            "in-stretch mean": mean_in,
            "all-bar mean": mean_all,
            "in-stretch up-day share": up_in,
            "all-bar up-day share": up_all,
        },
        "decided_by": decided_by,
        "reading": ("In-stretch means forecast > 0. With a 1-bar horizon, every bar with a next close in its window is a "
                    "non-overlapping return, pooled over all coins and windows. The t is Welch's on in-stretch versus "
                    "all-bar returns. Distinct up-cross stretches are runs of consecutive forecast > 0 bars inside each "
                    "window, including a run that starts at a window's first row. Any non-positive mean difference "
                    "rejects, as the reject rule states, so 'between -2.0 and 2.0' is inconclusive only when the "
                    "difference is positive.")
    }
