import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    thin_vals, heavy_vals = [], []
    thin_drops, heavy_drops = [], []

    for coin, windows in bars.items():
        for w, df in windows.items():
            if df is None or len(df) < 2:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            drop = close / close.shift(1) - 1.0          # the bar's own one-day move, inside the window
            nxt = close.shift(-1) / close - 1.0          # next-bar return, inside the window
            regime = d["regime"].astype(str)
            for i in range(len(d)):
                dr, nr, rg = drop.iloc[i], nxt.iloc[i], regime.iloc[i]
                if pd.isna(dr) or pd.isna(nr) or not (dr < 0):
                    continue
                share = nr / abs(dr)
                if not np.isfinite(share):
                    continue
                if rg == "mean_reversion":
                    thin_vals.append(share)
                    thin_drops.append(abs(dr))
                elif rg == "trending":
                    heavy_vals.append(share)
                    heavy_drops.append(abs(dr))

    thin = np.array(thin_vals, dtype=float)
    heavy = np.array(heavy_vals, dtype=float)
    n_thin, n_heavy = int(len(thin)), int(len(heavy))

    def fnum(x):
        return None if x is None or not np.isfinite(x) else float(x)

    thin_mean = thin.mean() if n_thin > 0 else np.nan
    heavy_mean = heavy.mean() if n_heavy > 0 else np.nan
    diff = thin_mean - heavy_mean if (n_thin > 0 and n_heavy > 0) else np.nan
    t = np.nan
    if n_thin >= 2 and n_heavy >= 2:
        t = stats.ttest_ind(thin, heavy, equal_var=False).statistic

    # Supporting check: thin-minus-heavy within terciles of |drop| (pooled)
    supp_value, supp_passed = None, None
    all_drops = np.array(thin_drops + heavy_drops, dtype=float)
    if len(all_drops) >= 3 and np.isfinite(diff) and diff != 0:
        q1, q2 = np.quantile(all_drops, [1 / 3, 2 / 3])
        td, hd = np.array(thin_drops), np.array(heavy_drops)

        def terc(x):
            return np.where(x <= q1, 0, np.where(x <= q2, 1, 2))

        tt, ht = terc(td), terc(hd)
        same = 0
        for k in range(3):
            a, b = thin[tt == k], heavy[ht == k]
            if len(a) > 0 and len(b) > 0:
                dk = a.mean() - b.mean()
                if np.sign(dk) == np.sign(diff):
                    same += 1
        supp_value = float(same)
        supp_passed = bool(same >= 2)

    if n_thin < 20 or n_heavy < 20:
        status = "inconclusive"
        decided = "Fewer than 20 thin or 20 heavy down bars in total, so the test is inconclusive."
    elif not np.isfinite(diff) or not np.isfinite(t):
        status = "inconclusive"
        decided = "The difference or its Welch t could not be computed, so the test is inconclusive."
    elif diff > 0 and t >= 2 and thin_mean > 0:
        status = "confirmed"
        decided = "The thin-minus-heavy difference is above 0 with Welch t of 2 or more and the thin group's mean give-back share is above 0."
    elif diff <= 0 and t <= -1:
        status = "rejected"
        decided = "The heavy group's give-back share is at or above the thin group's with a Welch t of -1 or lower."
    elif diff > 0:
        status = "inconclusive"
        decided = "A positive difference without meeting t of 2 or more with a positive thin mean, so the test is inconclusive."
    else:
        status = "inconclusive"
        decided = "A non-positive difference with t above -1, so the test is inconclusive."

    return {
        "status": status,
        "main_measure": {
            "name": "thin-minus-heavy mean next-bar give-back share of the drop",
            "value": fnum(diff),
            "statistic": {"name": "Welch t", "value": fnum(t)} if np.isfinite(t) else None,
            "threshold": "difference above 0 with Welch t >= 2 and thin mean share above 0 to confirm; difference at or below 0 with t <= -1 to reject",
        },
        "supporting_check": {
            "name": "terciles of drop size where thin-minus-heavy has the main difference's sign (need >= 2 of 3)",
            "value": supp_value,
            "passed": supp_passed,
        },
        "counts": {
            "thin down bars": n_thin,
            "heavy down bars": n_heavy,
        },
        "decided_by": decided,
        "reading": "Thin and heavy down bars are taken from the strategy's own regime label (mean_reversion = thin, trending = heavy) on bars whose in-window close-to-close move is negative (first row of each window dropped as it has no prior close), and since the plan's reject and inconclusive rules overlap for a negative difference, reject is applied only when the difference is at or below 0 with Welch t of -1 or lower, with a positive difference that fails the confirm rule treated as inconclusive.",
    }
