import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    rows = []
    for coin, wins in bars.items():
        for wname, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            if "regime" not in d.columns or "close" not in d.columns:
                continue
            close = pd.to_numeric(d["close"], errors="coerce")
            drop = close / close.shift(1) - 1.0          # the bar's one-day move, inside this window only
            nxt = close.shift(-1) / close - 1.0          # next-bar return, inside this window only
            reg = d["regime"].astype(str)
            for i in range(len(d)):
                r = reg.iloc[i]
                if r not in ("trending", "mean_reversion"):
                    continue
                dr, nr = drop.iloc[i], nxt.iloc[i]
                if not (np.isfinite(dr) and np.isfinite(nr)) or dr >= 0:
                    continue
                rows.append({
                    "group": "heavy" if r == "trending" else "thin",
                    "absdrop": abs(dr),
                    "share": nr / abs(dr),
                })
    data = pd.DataFrame(rows, columns=["group", "absdrop", "share"])
    thin = data.loc[data["group"] == "thin", "share"].to_numpy(dtype=float)
    heavy = data.loc[data["group"] == "heavy", "share"].to_numpy(dtype=float)
    n_thin, n_heavy = int(len(thin)), int(len(heavy))

    diff, t = None, None
    thin_mean = float(np.mean(thin)) if n_thin > 0 else None
    heavy_mean = float(np.mean(heavy)) if n_heavy > 0 else None
    if n_thin >= 2 and n_heavy >= 2:
        diff = thin_mean - heavy_mean
        tt = stats.ttest_ind(thin, heavy, equal_var=False).statistic
        t = float(tt) if np.isfinite(tt) else None

    # supporting check: terciles of drop size pooled across groups
    sup_val, sup_pass, n_same = None, None, 0
    if len(data) >= 3 and diff is not None and diff != 0:
        ranks = data["absdrop"].rank(method="first")
        data["terc"] = pd.qcut(ranks, 3, labels=False)
        sgn = np.sign(diff)
        for k in range(3):
            sub = data[data["terc"] == k]
            a = sub.loc[sub["group"] == "thin", "share"]
            b = sub.loc[sub["group"] == "heavy", "share"]
            if len(a) > 0 and len(b) > 0 and np.sign(a.mean() - b.mean()) == sgn:
                n_same += 1
        sup_val = n_same
        sup_pass = bool(n_same >= 2)

    if n_thin < 20 or n_heavy < 20 or diff is None or t is None:
        status = "inconclusive"
        decided = "Fewer than 20 thin or 20 heavy down bars (or no usable t-statistic), so the test is inconclusive."
    elif diff > 0 and t >= 2 and thin_mean > 0:
        status = "confirmed"
        decided = "Thin-minus-heavy difference is above 0 with Welch t >= 2 and the thin group's mean give-back share is above 0."
    elif diff <= 0 and t <= -1:
        status = "rejected"
        decided = "The difference is at or below 0 and the heavy group's give-back share is at or above the thin group's with t <= -1."
    elif diff == 0:
        status = "rejected"
        decided = "The difference is exactly 0, which the reject rule covers."
    else:
        status = "inconclusive"
        decided = ("A positive difference with t below 2 (or thin mean not above 0), or a negative difference "
                   "with t above -1, so the test is inconclusive.")

    return {
        "status": status,
        "main_measure": {
            "name": "thin minus heavy mean next-bar give-back share of drop",
            "value": None if diff is None else float(diff),
            "statistic": None if t is None else {"name": "Welch t", "value": float(t)},
            "threshold": "difference > 0 with Welch t >= 2 and thin mean share > 0 to confirm; difference <= 0 with t <= -1 to reject",
        },
        "supporting_check": {
            "name": "terciles of drop size with same-sign thin-minus-heavy difference (of 3)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {
            "thin down bars": n_thin,
            "heavy down bars": n_heavy,
            "thin mean give-back share": thin_mean,
            "heavy mean give-back share": heavy_mean,
        },
        "decided_by": decided,
        "reading": ("Thin/heavy down bars are taken from the strategy's regime label (mean_reversion = thin, trending = heavy) "
                    "with the drop computed as close[t]/close[t-1]-1 < 0 inside each window (a window's first row has no drop "
                    "and is left out); because the reject and inconclusive rules overlap for negative differences, a negative "
                    "difference rejects only when Welch t <= -1 (or the difference is exactly 0), and the supporting check counts "
                    "terciles (equal-count by pooled |drop|) whose difference has the main difference's sign and is reported "
                    "without changing the verdict."),
    }
