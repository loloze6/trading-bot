import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    thin_vals, heavy_vals, thin_drop, heavy_drop = [], [], [], []

    for coin, windows in bars.items():
        for w, df in windows.items():
            if df is None or len(df) < 3:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            move = close / close.shift(1) - 1.0          # this bar's one-day move, inside the window
            nxt = close.shift(-1) / close - 1.0          # next-bar return, inside the window
            regime = d["regime"].astype(str)
            for i in range(len(d)):
                m, r, reg = move.iloc[i], nxt.iloc[i], regime.iloc[i]
                if not np.isfinite(m) or not np.isfinite(r) or m >= 0:
                    continue
                share = r / abs(m)
                if reg == "mean_reversion":
                    thin_vals.append(share)
                    thin_drop.append(abs(m))
                elif reg == "trending":
                    heavy_vals.append(share)
                    heavy_drop.append(abs(m))

    thin = np.array(thin_vals, dtype=float)
    heavy = np.array(heavy_vals, dtype=float)
    n_thin, n_heavy = int(len(thin)), int(len(heavy))

    thin_mean = float(np.mean(thin)) if n_thin else None
    heavy_mean = float(np.mean(heavy)) if n_heavy else None
    diff = (thin_mean - heavy_mean) if (thin_mean is not None and heavy_mean is not None) else None

    t_stat = None
    if n_thin >= 2 and n_heavy >= 2:
        t = stats.ttest_ind(thin, heavy, equal_var=False).statistic
        t_stat = float(t) if np.isfinite(t) else None

    # Supporting check: drop-size terciles pooled across both groups
    sup_value, sup_passed = None, None
    if n_thin + n_heavy >= 3 and diff is not None:
        sizes = np.concatenate([np.array(thin_drop), np.array(heavy_drop)])
        vals = np.concatenate([thin, heavy])
        grp = np.array(["thin"] * n_thin + ["heavy"] * n_heavy)
        try:
            terc = pd.qcut(pd.Series(sizes).rank(method="first"), 3, labels=False).to_numpy()
            sign_overall = np.sign(diff)
            same = 0
            for k in range(3):
                mask = terc == k
                tv = vals[mask & (grp == "thin")]
                hv = vals[mask & (grp == "heavy")]
                if len(tv) and len(hv):
                    dk = float(np.mean(tv) - np.mean(hv))
                    if sign_overall != 0 and np.sign(dk) == sign_overall:
                        same += 1
            sup_value = int(same)
            sup_passed = bool(same >= 2)
        except Exception:
            sup_value, sup_passed = None, None

    if n_thin < 20 or n_heavy < 20 or diff is None or t_stat is None:
        status = "inconclusive"
        decided = "Inconclusive: fewer than 20 thin or 20 heavy down bars in total (or the statistic cannot be computed)."
    elif diff > 0 and t_stat >= 2 and thin_mean > 0:
        status = "confirmed"
        decided = "Confirm: thin-minus-heavy difference above 0 with Welch t >= 2 and the thin group's mean give-back share above 0."
    elif diff == 0 or (diff < 0 and t_stat <= -1):
        status = "rejected"
        decided = "Reject: the difference is at or below 0 with the heavy group's give-back at or above the thin group's at t <= -1."
    elif diff > 0 and t_stat >= 2:
        status = "inconclusive"
        decided = "Inconclusive: positive difference with t >= 2 but the thin group's mean give-back share is not above 0, so neither confirm nor reject is met."
    elif diff > 0:
        status = "inconclusive"
        decided = "Inconclusive: a positive difference with Welch t below 2."
    else:
        status = "inconclusive"
        decided = "Inconclusive: a negative difference with Welch t above -1."

    return {
        "status": status,
        "main_measure": {
            "name": "thin-minus-heavy mean next-bar give-back share (next return / |drop|)",
            "value": diff,
            "statistic": {"name": "Welch t", "value": t_stat} if t_stat is not None else None,
            "threshold": "difference > 0 with Welch t >= 2 and thin mean > 0 to confirm; difference <= 0 with t <= -1 to reject",
        },
        "supporting_check": {
            "name": "terciles of drop size where thin-minus-heavy has the overall sign (need >= 2 of 3)",
            "value": sup_value,
            "passed": sup_passed,
        },
        "counts": {"thin down bars": n_thin, "heavy down bars": n_heavy},
        "decided_by": decided,
        "reading": "Thin and heavy down bars are taken from the strategy's own regime label (mean_reversion = thin, trending = heavy) on bars whose in-window close-to-close move is negative, the window's first row (no prior close) and last row (no next close) are dropped, terciles are equal-count cuts of |drop| pooled over both groups, and the reject rule's 'at or below 0' is read together with the inconclusive rule so a negative difference needs t <= -1 (an exactly zero difference rejects)."
    }
