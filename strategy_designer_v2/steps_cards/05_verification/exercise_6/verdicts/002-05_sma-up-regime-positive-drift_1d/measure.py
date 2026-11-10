import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    in_rets = []
    all_rets = []
    n_stretches = 0

    for coin, windows in bars.items():
        for w, df in windows.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            # next-bar return inside the window only
            ret = close.shift(-1) / close - 1.0

            # distinct up-cross stretches: maximal runs of consecutive bars with forecast > 0 in this window
            pos = (fc > 0).fillna(False).to_numpy()
            if len(pos) > 0:
                starts = pos & ~np.concatenate([[False], pos[:-1]])
                n_stretches += int(starts.sum())

            # horizon 1 bar: non-overlapping grid is every bar (positions 0, 1, 2, ...)
            valid_all = ret.notna() & fc.notna()
            all_rets.append(ret[valid_all].to_numpy())
            valid_in = valid_all & (fc > 0)
            in_rets.append(ret[valid_in].to_numpy())

    in_r = np.concatenate(in_rets) if in_rets else np.array([])
    all_r = np.concatenate(all_rets) if all_rets else np.array([])
    n_in = int(len(in_r))
    n_all = int(len(all_r))

    mean_in = float(np.mean(in_r)) if n_in > 0 else None
    mean_all = float(np.mean(all_r)) if n_all > 0 else None
    diff = (mean_in - mean_all) if (mean_in is not None and mean_all is not None) else None

    t_val = None
    if n_in >= 2 and n_all >= 2:
        t, _ = stats.ttest_ind(in_r, all_r, equal_var=False)
        if np.isfinite(t):
            t_val = float(t)

    up_in = float(np.mean(in_r > 0)) if n_in > 0 else None
    up_all = float(np.mean(all_r > 0)) if n_all > 0 else None
    up_diff = (up_in - up_all) if (up_in is not None and up_all is not None) else None
    sup_passed = (bool(up_diff > 0) if up_diff is not None else None)

    if n_in < 100 or n_stretches < 3 or diff is None or t_val is None:
        status = "inconclusive"
        decided_by = ("Inconclusive: fewer than 100 in-stretch bars or fewer than 3 distinct up-cross stretches "
                      "across the windows (or the t-statistic could not be computed).")
    elif diff <= 0:
        status = "rejected"
        if t_val <= -2.0:
            decided_by = ("Reject: the in-stretch mean daily return is below the all-bar mean with a t-statistic "
                          "of -2.0 or lower, so moves reverse after up-crosses.")
        else:
            decided_by = ("Reject: the in-stretch mean daily return is at or below the all-bar mean, "
                          "so there is no persistence.")
    elif t_val >= 2.0 and sup_passed:
        status = "confirmed"
        decided_by = ("Confirm: the in-stretch mean daily return exceeds the all-bar mean with a one-sided "
                      "t-statistic of at least 2.0, and the in-stretch up-day share exceeds the all-bar share.")
    elif t_val >= 2.0:
        status = "inconclusive"
        decided_by = ("Inconclusive: the t-statistic is at least 2.0 but the in-stretch up-day share does not "
                      "exceed the all-bar share, so the confirm rule is not fully met.")
    else:
        status = "inconclusive"
        decided_by = ("Inconclusive: the in-stretch mean exceeds the all-bar mean but the t-statistic lies "
                      "between -2.0 and 2.0.")

    return {
        "status": status,
        "main_measure": {
            "name": "in-stretch minus all-bar mean next-bar return (before costs)",
            "value": float(diff) if diff is not None else None,
            "statistic": ({"name": "Welch t (in-stretch minus all bars)", "value": t_val}
                          if t_val is not None else None),
            "threshold": ("confirm if the difference is > 0 with t >= 2.0; reject if the difference is <= 0 "
                          "(or t <= -2.0); otherwise inconclusive"),
        },
        "supporting_check": {
            "name": "in-stretch up-day share minus all-bar up-day share",
            "value": float(up_diff) if up_diff is not None else None,
            "passed": sup_passed,
        },
        "counts": {
            "in-stretch bars": n_in,
            "distinct up-cross stretches": int(n_stretches),
            "all bars": n_all,
        },
        "decided_by": decided_by,
        "reading": ("In-stretch means forecast > 0. With a 1-bar horizon every bar is on the non-overlapping grid. "
                    "The 'all bars' group includes the in-stretch bars, and the two groups are compared with "
                    "Welch t. A distinct up-cross stretch is a maximal run of consecutive forecast > 0 bars "
                    "within one window, including a run already under way at the window's start. An up day is a "
                    "next-bar return > 0. A difference at or below 0 rejects even when t lies between -2 and 2, "
                    "because the plan's reject rule says so explicitly."),
    }
