import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    rows = []
    for coin, windows in bars.items():
        for wname, df in windows.items():
            if df is None or len(df) < 3:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            drop = close / close.shift(1) - 1.0          # the bar's own one-day move, inside the window
            nxt = close.shift(-1) / close - 1.0          # next-bar return, inside the window
            regime = d["regime"].astype(str)
            for i in range(len(d)):
                dr, nr, rg = drop.iloc[i], nxt.iloc[i], regime.iloc[i]
                if pd.isna(dr) or pd.isna(nr) or not (dr < 0):
                    continue
                if rg == "mean_reversion":
                    grp = "thin"
                elif rg == "trending":
                    grp = "heavy"
                else:
                    continue
                rows.append({"grp": grp, "absdrop": abs(dr), "share": nr / abs(dr)})

    data = pd.DataFrame(rows, columns=["grp", "absdrop", "share"])
    thin = data.loc[data["grp"] == "thin", "share"].to_numpy(dtype=float)
    heavy = data.loc[data["grp"] == "heavy", "share"].to_numpy(dtype=float)
    n_thin, n_heavy = len(thin), len(heavy)
    cases = int(n_thin + n_heavy)

    diff = None
    t = None
    if n_thin >= 2 and n_heavy >= 2:
        diff = float(np.mean(thin) - np.mean(heavy))
        tt = stats.ttest_ind(thin, heavy, equal_var=False)
        t = float(tt.statistic) if np.isfinite(tt.statistic) else None
    elif n_thin >= 1 and n_heavy >= 1:
        diff = float(np.mean(thin) - np.mean(heavy))

    # Supporting check: terciles of drop size pooled across groups
    supp_value = None
    supp_passed = None
    if diff is not None and len(data) >= 3 and diff != 0:
        try:
            data = data.copy()
            data["terc"] = pd.qcut(data["absdrop"].rank(method="first"), 3, labels=False)
            same = 0
            for k in range(3):
                sub = data[data["terc"] == k]
                a = sub.loc[sub["grp"] == "thin", "share"]
                b = sub.loc[sub["grp"] == "heavy", "share"]
                if len(a) > 0 and len(b) > 0:
                    dk = a.mean() - b.mean()
                    if np.sign(dk) == np.sign(diff) and dk != 0:
                        same += 1
            supp_value = int(same)
            supp_passed = bool(same >= 2)
        except Exception:
            supp_value, supp_passed = None, None

    thin_mean = float(np.mean(thin)) if n_thin > 0 else None

    if n_thin < 20 or n_heavy < 20 or diff is None or t is None:
        status = "inconclusive"
        decided = f"Fewer than 20 thin ({n_thin}) or 20 heavy ({n_heavy}) down bars, or the t-statistic cannot be computed, so the test is inconclusive."
    elif diff > 0 and t >= 2 and thin_mean is not None and thin_mean > 0:
        status = "confirmed"
        decided = "The thin-minus-heavy difference is above 0 with a Welch t of 2 or more and the thin group's mean give-back share is above 0."
    elif diff == 0 or (diff < 0 and t <= -1):
        status = "rejected"
        decided = "The difference is at or below 0 with the heavy group's give-back share at or above the thin group's at a t-statistic of -1 or lower."
    elif diff > 0 and t < 2:
        status = "inconclusive"
        decided = "A positive difference with a Welch t below 2 is inconclusive."
    elif diff < 0 and t > -1:
        status = "inconclusive"
        decided = "A negative difference with a Welch t above -1 is inconclusive."
    else:
        status = "inconclusive"
        decided = "The difference is positive with t of 2 or more but the thin group's mean give-back share is not above 0, so no confirm or reject rule is met."

    return {
        "status": status,
        "main_measure": {
            "name": "thin-minus-heavy mean next-bar give-back share (next return / |drop|)",
            "value": diff,
            "threshold": "above 0 with Welch t >= 2 (and thin mean > 0) to confirm; at or below 0 with t <= -1 to reject",
        },
        "supporting_check": {
            "name": "terciles of drop size with the same sign of thin-minus-heavy difference (need >= 2 of 3)",
            "value": supp_value,
            "passed": supp_passed,
        },
        "cases": cases,
        "decided_by": decided,
        "reading": (
            "Thin and heavy down bars are taken from the strategy's regime label (mean_reversion = thin, trending = heavy) "
            "on bars whose close-to-close move within the window is negative, so the first bar of each window is left out; "
            "the reject rule's 'at or below 0' is read together with the inconclusive rule, so a negative difference rejects "
            "only with t <= -1 while a zero difference rejects; 'same sign' in terciles means the same sign as the pooled difference, "
            "and a tercile missing either group does not count."
        ),
    }
