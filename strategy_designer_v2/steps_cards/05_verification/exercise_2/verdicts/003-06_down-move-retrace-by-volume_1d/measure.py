import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    rows = []
    for coin, windows in bars.items():
        for win, df in windows.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            drop = close / close.shift(1) - 1.0          # this bar's one-bar move, inside the window
            nxt = close.shift(-1) / close - 1.0          # next-bar return, inside the window
            reg = d["regime"].astype(str)
            for i in range(len(d)):
                r = reg.iloc[i]
                if r not in ("mean_reversion", "trending"):
                    continue
                dr, nr = drop.iloc[i], nxt.iloc[i]
                if pd.isna(dr) or pd.isna(nr) or not (dr < 0):
                    continue
                rows.append({
                    "group": "thin" if r == "mean_reversion" else "heavy",
                    "absdrop": abs(dr),
                    "share": nr / abs(dr),
                })

    data = pd.DataFrame(rows, columns=["group", "absdrop", "share"])
    thin = data.loc[data["group"] == "thin", "share"].to_numpy(dtype=float)
    heavy = data.loc[data["group"] == "heavy", "share"].to_numpy(dtype=float)
    n_thin, n_heavy = len(thin), len(heavy)
    cases = int(n_thin + n_heavy)

    reading = ("Thin and heavy down bars are taken from the strategy's regime label (mean_reversion = thin, "
               "trending = heavy) on bars whose own close-to-close move inside the window is negative and whose "
               "next close is in the same window; terciles are cut on |drop| pooled across both groups; "
               "since the reject and inconclusive rules overlap, a negative difference with t above -1 is "
               "inconclusive and the reject rule needs t of -1 or lower (or a difference of exactly 0); a positive "
               "difference with t >= 2 but a thin mean <= 0 is inconclusive; the supporting check is reported "
               "but does not change the status, as the plan's rules do not use it.")

    thr = "thin-minus-heavy > 0 with Welch t >= 2 and thin mean > 0 (reject: <= 0 with t <= -1)"
    name = "mean next-bar give-back share (next return / |drop|), thin minus heavy down bars"

    diff = None
    t = None
    thin_mean = float(np.mean(thin)) if n_thin > 0 else None
    if n_thin >= 2 and n_heavy >= 2:
        diff = float(np.mean(thin) - np.mean(heavy))
        tt = stats.ttest_ind(thin, heavy, equal_var=False)
        t = float(tt.statistic) if np.isfinite(tt.statistic) else None
    elif n_thin >= 1 and n_heavy >= 1:
        diff = float(np.mean(thin) - np.mean(heavy))

    # supporting check: terciles of drop size pooled across groups
    sup_val = None
    sup_pass = None
    if len(data) >= 3 and diff is not None and diff != 0:
        try:
            terc = pd.qcut(data["absdrop"].rank(method="first"), 3, labels=False)
            same = 0
            for k in range(3):
                sub = data[terc == k]
                a = sub.loc[sub["group"] == "thin", "share"]
                b = sub.loc[sub["group"] == "heavy", "share"]
                if len(a) == 0 or len(b) == 0:
                    continue
                dk = a.mean() - b.mean()
                if np.sign(dk) == np.sign(diff) and dk != 0:
                    same += 1
            sup_val = int(same)
            sup_pass = bool(same >= 2)
        except Exception:
            sup_val, sup_pass = None, None

    supporting = {"name": "same-sign thin-minus-heavy difference in terciles of drop size (of 3, need >= 2)",
                  "value": sup_val, "passed": sup_pass}

    if n_thin < 20 or n_heavy < 20 or diff is None:
        status = "inconclusive"
        decided = (f"Inconclusive: fewer than 20 thin ({n_thin}) or 20 heavy ({n_heavy}) down bars in total.")
    elif t is None:
        status = "inconclusive"
        decided = "Inconclusive: the Welch t-statistic could not be computed."
    elif diff > 0 and t >= 2 and thin_mean is not None and thin_mean > 0:
        status = "confirmed"
        decided = "Confirmed: the thin-minus-heavy difference is above 0 with Welch t >= 2 and the thin mean give-back share is above 0."
    elif diff > 0:
        status = "inconclusive"
        if t < 2:
            decided = "Inconclusive: a positive difference with a t-statistic below 2."
        else:
            decided = "Inconclusive: a positive difference with t >= 2 but the thin group's mean give-back share is not above 0."
    elif diff < 0 and t > -1:
        status = "inconclusive"
        decided = "Inconclusive: a negative difference with a t-statistic above -1."
    else:
        status = "rejected"
        decided = "Rejected: the difference is at or below 0, with the heavy group's give-back share at or above the thin group's and t of -1 or lower."

    return {
        "status": status,
        "main_measure": {"name": name, "value": diff, "threshold": thr},
        "supporting_check": supporting,
        "cases": cases,
        "decided_by": decided,
        "reading": reading,
    }
