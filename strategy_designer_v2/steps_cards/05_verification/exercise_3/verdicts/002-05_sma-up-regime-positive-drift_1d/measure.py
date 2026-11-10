import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    in_rets = []
    all_rets = []
    n_stretches = 0

    for coin in bars:
        for window in bars[coin]:
            df = bars[coin][window]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            # next-bar return inside this window only (h = 1, so every bar is on the non-overlapping grid)
            ret = close.shift(-1) / close - 1.0

            # all bars: need the return only
            r_all = ret.dropna()
            all_rets.append(r_all.values)

            # in-stretch bars: forecast > 0 and a valid return
            mask_in = (fc > 0) & ret.notna() & fc.notna()
            in_rets.append(ret[mask_in].values)

            # distinct stretches: contiguous runs of forecast > 0 within the window
            pos = (fc > 0).fillna(False).astype(bool).values
            if len(pos) > 0:
                starts = pos & ~np.concatenate([[False], pos[:-1]])
                n_stretches += int(starts.sum())

    in_r = np.concatenate(in_rets) if in_rets else np.array([])
    all_r = np.concatenate(all_rets) if all_rets else np.array([])
    n_in = int(len(in_r))
    n_all = int(len(all_r))

    mean_in = float(np.mean(in_r)) if n_in > 0 else None
    mean_all = float(np.mean(all_r)) if n_all > 0 else None
    diff = (mean_in - mean_all) if (mean_in is not None and mean_all is not None) else None

    t_val = None
    if n_in >= 2 and n_all >= 2:
        t_res = stats.ttest_ind(in_r, all_r, equal_var=False)
        t_val = float(t_res.statistic) if np.isfinite(t_res.statistic) else None

    up_in = float(np.mean(in_r > 0)) if n_in > 0 else None
    up_all = float(np.mean(all_r > 0)) if n_all > 0 else None
    up_diff = (up_in - up_all) if (up_in is not None and up_all is not None) else None
    sup_passed = (bool(up_in > up_all)) if up_diff is not None else None

    counts = {
        "in-stretch bars": n_in,
        "distinct up-cross stretches": int(n_stretches),
        "all bars": n_all,
    }

    if n_in < 100 or n_stretches < 3:
        status = "inconclusive"
        decided_by = ("Inconclusive: fewer than 100 in-stretch bars or fewer than 3 distinct "
                      "up-cross stretches across the windows.")
    elif diff is None or t_val is None:
        status = "inconclusive"
        decided_by = "Inconclusive: the t-statistic on the difference could not be computed."
    elif diff <= 0:
        status = "rejected"
        if t_val <= -2.0:
            decided_by = ("Reject: the in-stretch mean daily return is below the all-bar mean with a "
                          "t-statistic of -2.0 or lower, so moves reverse after up-crosses.")
        else:
            decided_by = ("Reject: the in-stretch mean daily return is at or below the all-bar mean, "
                          "so there is no persistence.")
    elif t_val >= 2.0 and sup_passed:
        status = "confirmed"
        decided_by = ("Confirm: the in-stretch mean daily return exceeds the all-bar mean with a "
                      "one-sided t-statistic of at least 2.0, and the in-stretch up-day share exceeds "
                      "the all-bar share.")
    elif t_val >= 2.0:
        status = "inconclusive"
        decided_by = ("Inconclusive: the t-statistic reaches 2.0, but the in-stretch up-day share does "
                      "not exceed the all-bar share, so the confirm rule is not fully met and no reject "
                      "rule applies.")
    else:
        status = "inconclusive"
        decided_by = ("Inconclusive: the in-stretch mean exceeds the all-bar mean, but the t-statistic "
                      "lies between -2.0 and 2.0.")

    return {
        "status": status,
        "main_measure": {
            "name": "in-stretch minus all-bar mean next-bar return (before costs)",
            "value": diff,
            "statistic": ({"name": "Welch t (in-stretch minus all bars)", "value": t_val}
                          if t_val is not None else None),
            "threshold": ("confirm if difference > 0 with t >= 2.0; reject if difference <= 0 or "
                          "t <= -2.0; inconclusive if t is between -2.0 and 2.0"),
        },
        "supporting_check": {
            "name": "in-stretch up-day share minus all-bar up-day share",
            "value": up_diff,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("In-stretch bars are the bars with forecast > 0. Distinct up-cross stretches are "
                    "contiguous runs of forecast > 0 within each window, counting a run that is already "
                    "on at a window's first row. Every bar's next-bar return is used, since h = 1 makes "
                    "every bar non-overlapping. The test is Welch's t of in-stretch returns against "
                    "all-bar returns. An up day is a next-bar return > 0."),
    }
