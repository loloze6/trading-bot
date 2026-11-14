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
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            # next-bar return inside this window only
            r = close.shift(-1) / close - 1.0

            valid_all = r.notna() & np.isfinite(r)
            all_rets.append(r[valid_all].to_numpy())

            in_mask = valid_all & fc.notna() & (fc > 0)
            in_rets.append(r[in_mask].to_numpy())

            # distinct in-stretch runs (consecutive bars with forecast > 0) inside this window
            pos = (fc > 0).fillna(False).astype(int).to_numpy()
            if len(pos) > 0:
                starts = np.sum((pos[1:] == 1) & (pos[:-1] == 0)) + (1 if pos[0] == 1 else 0)
                n_stretches += int(starts)

    in_r = np.concatenate(in_rets) if in_rets else np.array([])
    all_r = np.concatenate(all_rets) if all_rets else np.array([])
    n_in = int(len(in_r))
    n_all = int(len(all_r))

    mean_in = float(np.mean(in_r)) if n_in > 0 else None
    mean_all = float(np.mean(all_r)) if n_all > 0 else None
    diff = (mean_in - mean_all) if (mean_in is not None and mean_all is not None) else None

    t_stat = None
    if n_in >= 2 and n_all >= 2:
        t, _ = stats.ttest_ind(in_r, all_r, equal_var=False)
        if np.isfinite(t):
            t_stat = float(t)

    up_in = float(np.mean(in_r > 0)) if n_in > 0 else None
    up_all = float(np.mean(all_r > 0)) if n_all > 0 else None
    sup_passed = (up_in > up_all) if (up_in is not None and up_all is not None) else None
    sup_value = (up_in - up_all) if sup_passed is not None else None

    if n_in < 100 or n_stretches < 3 or diff is None or t_stat is None:
        status = "inconclusive"
        decided_by = (f"Inconclusive rule: {n_in} in-stretch bars (need >= 100) and "
                      f"{n_stretches} distinct up-cross stretches (need >= 3), or the measure could not be computed.")
    elif diff <= 0 or t_stat <= -2.0:
        status = "rejected"
        decided_by = ("Reject rule: the in-stretch mean daily return is at or below the all-bar mean"
                      + (" with t <= -2.0 (moves reverse)." if t_stat <= -2.0 else "."))
    elif t_stat >= 2.0 and sup_passed:
        status = "confirmed"
        decided_by = ("Confirm rule: the in-stretch mean exceeds the all-bar mean with one-sided t >= 2.0 "
                      "and the in-stretch up-day share exceeds the all-bar share.")
    else:
        status = "inconclusive"
        if t_stat < 2.0:
            decided_by = "Inconclusive rule: the t-statistic lies between -2.0 and 2.0."
        else:
            decided_by = ("Neither confirm nor reject is met: t >= 2.0 but the in-stretch up-day share "
                          "does not exceed the all-bar share, so the result is inconclusive.")

    return {
        "status": status,
        "main_measure": {
            "name": "in-stretch minus all-bar mean next-bar return (before costs)",
            "value": diff,
            "threshold": "above 0 with one-sided t-statistic >= 2.0 confirms; at or below 0 or t <= -2.0 rejects",
        },
        "supporting_check": {
            "name": "in-stretch up-day share minus all-bar up-day share",
            "value": sup_value,
            "passed": sup_passed,
        },
        "cases": n_in,
        "decided_by": decided_by,
        "reading": ("In-stretch bars are rows with forecast > 0 and next-bar returns are taken inside each window. "
                    "The t-statistic on the difference is a Welch two-sample t-test of in-stretch returns against all-bar returns, "
                    "and an up day is a next-bar return > 0. "
                    f"Distinct up-cross stretches are runs of consecutive forecast > 0 bars inside each window ({n_stretches} found). "
                    f"t = {t_stat}, mean_in = {mean_in}, mean_all = {mean_all}, n_all = {n_all}."),
    }
