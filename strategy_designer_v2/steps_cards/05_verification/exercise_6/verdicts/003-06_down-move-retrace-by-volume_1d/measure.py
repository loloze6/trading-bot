import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    thin_vals, heavy_vals = [], []
    pooled = []  # (abs_drop, share, group)

    for coin, windows in bars.items():
        for w, df in windows.items():
            if df is None or len(df) < 2:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            prev_close = close.shift(1)
            next_close = close.shift(-1)
            drop = close / prev_close - 1.0          # the bar's own one-bar move, inside the window
            nxt = next_close / close - 1.0           # next-bar return, inside the window
            regime = d["regime"].astype(str)
            for i in range(len(d)):
                dr, nr, rg = drop.iloc[i], nxt.iloc[i], regime.iloc[i]
                if not np.isfinite(dr) or not np.isfinite(nr) or dr >= 0:
                    continue
                if rg == "mean_reversion":
                    grp = "thin"
                elif rg == "trending":
                    grp = "heavy"
                else:
                    continue
                share = nr / abs(dr)
                if not np.isfinite(share):
                    continue
                pooled.append((abs(dr), share, grp))
                (thin_vals if grp == "thin" else heavy_vals).append(share)

    n_thin, n_heavy = len(thin_vals), len(heavy_vals)
    thin = np.array(thin_vals, dtype=float)
    heavy = np.array(heavy_vals, dtype=float)

    diff, t = None, None
    thin_mean = float(thin.mean()) if n_thin else None
    heavy_mean = float(heavy.mean()) if n_heavy else None
    if n_thin >= 2 and n_heavy >= 2:
        diff = float(thin.mean() - heavy.mean())
        tt = stats.ttest_ind(thin, heavy, equal_var=False)
        t = float(tt.statistic) if np.isfinite(tt.statistic) else None

    # Supporting check: thin-minus-heavy within terciles of drop size (pooled)
    sup_value, sup_passed = None, None
    if pooled and diff is not None and diff != 0:
        arr = pd.DataFrame(pooled, columns=["absdrop", "share", "grp"])
        try:
            arr["terc"] = pd.qcut(arr["absdrop"].rank(method="first"), 3, labels=False)
            same = 0
            valid = 0
            for k in range(3):
                sub = arr[arr["terc"] == k]
                a = sub.loc[sub["grp"] == "thin", "share"]
                b = sub.loc[sub["grp"] == "heavy", "share"]
                if len(a) == 0 or len(b) == 0:
                    continue
                valid += 1
                dk = a.mean() - b.mean()
                if np.sign(dk) == np.sign(diff):
                    same += 1
            sup_value = float(same)
            sup_passed = bool(same >= 2)
        except Exception:
            sup_value, sup_passed = None, None

    if n_thin < 20 or n_heavy < 20:
        status = "inconclusive"
        decided = "Fewer than 20 thin or 20 heavy down bars in total, so the test is inconclusive."
    elif diff is None or t is None:
        status = "inconclusive"
        decided = "The difference or its Welch t could not be computed, so the test is inconclusive."
    elif diff > 0 and t >= 2 and thin_mean > 0:
        status = "confirmed"
        decided = "The thin-minus-heavy difference is above 0 with Welch t >= 2 and the thin group's mean give-back share is above 0."
    elif diff == 0 or (diff < 0 and t <= -1):
        status = "rejected"
        decided = "The difference is at or below 0 with the heavy group's give-back at or above the thin group's at t <= -1 (or exactly 0)."
    elif diff > 0 and t < 2:
        status = "inconclusive"
        decided = "A positive difference with Welch t below 2."
    elif diff < 0 and t > -1:
        status = "inconclusive"
        decided = "A negative difference with Welch t above -1."
    else:
        status = "inconclusive"
        decided = "Positive difference with t >= 2 but the thin group's mean give-back share is not above 0, so no confirm or reject rule is met."

    return {
        "status": status,
        "main_measure": {
            "name": "thin minus heavy mean next-bar give-back share (next return / |drop|)",
            "value": diff,
            "statistic": {"name": "Welch t", "value": t} if t is not None else None,
            "threshold": "difference > 0 with Welch t >= 2 and thin mean > 0 confirms; difference <= 0 with t <= -1 rejects",
        },
        "supporting_check": {
            "name": "drop-size terciles (of 3) where thin-minus-heavy has the overall sign; pass if >= 2",
            "value": sup_value,
            "passed": sup_passed,
        },
        "counts": {"thin down bars": int(n_thin), "heavy down bars": int(n_heavy)},
        "decided_by": decided,
        "reading": (
            "Thin/heavy down bars are taken from the strategy's regime label (mean_reversion = thin, trending = heavy) on bars whose close-to-close move inside the window is negative, "
            "terciles are of |drop| pooled over both groups with signs compared to the overall difference, and the overlapping reject/inconclusive rules are reconciled by rejecting a negative "
            "difference only when t <= -1 (a zero difference rejects), with a positive t >= 2 difference but non-positive thin mean left inconclusive."
        ),
    }
