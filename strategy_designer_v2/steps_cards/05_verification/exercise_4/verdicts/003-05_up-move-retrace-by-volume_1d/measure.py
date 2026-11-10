import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    thin_shares, heavy_shares = [], []
    sup = {"thin": {"strat": 0.0, "hold": 0.0, "n": 0},
           "heavy": {"strat": 0.0, "hold": 0.0, "n": 0}}

    for coin, windows in bars.items():
        for w, df in windows.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            move = close / close.shift(1) - 1.0          # the sharp move's own one-bar return, inside the window
            nxt = close.shift(-1) / close - 1.0           # next bar's close-to-close return, inside the window
            alloc = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce")
            regime = df["regime"].astype(str)

            for i in range(len(df)):
                r = regime.iloc[i]
                if r == "mean_reversion":
                    grp = "thin"
                elif r == "trending":
                    grp = "heavy"
                else:
                    continue
                m, n = move.iloc[i], nxt.iloc[i]
                if pd.notna(m) and pd.notna(n) and m != 0:
                    share = n / m
                    if grp == "thin":
                        thin_shares.append(share)
                    else:
                        heavy_shares.append(share)
                a = alloc.iloc[i]
                if pd.notna(a) and pd.notna(n):
                    sup[grp]["strat"] += a * n
                    sup[grp]["hold"] += n
                    sup[grp]["n"] += 1

    thin = np.array(thin_shares, dtype=float)
    heavy = np.array(heavy_shares, dtype=float)
    n_thin, n_heavy = len(thin), len(heavy)

    thin_mean = float(np.mean(thin)) if n_thin > 0 else None
    heavy_mean = float(np.mean(heavy)) if n_heavy > 0 else None
    diff = (thin_mean - heavy_mean) if (thin_mean is not None and heavy_mean is not None) else None

    t_val = None
    if n_thin >= 2 and n_heavy >= 2:
        t, _ = stats.ttest_ind(thin, heavy, equal_var=False)
        t_val = float(t) if np.isfinite(t) else None

    # supporting check: strategy gain before costs minus holding BTC, summed over each part's active bars
    ex_thin = sup["thin"]["strat"] - sup["thin"]["hold"] if sup["thin"]["n"] > 0 else None
    ex_heavy = sup["heavy"]["strat"] - sup["heavy"]["hold"] if sup["heavy"]["n"] > 0 else None
    if ex_thin is None or ex_heavy is None:
        sup_value, sup_passed = None, None
    else:
        sup_value = float(min(ex_thin, ex_heavy))
        sup_passed = bool(ex_thin > 0 and ex_heavy > 0)

    # decision
    if n_thin < 15 or n_heavy < 15:
        status = "inconclusive"
        decided_by = "Inconclusive: fewer than 15 thin cases or fewer than 15 heavy cases across the 6 windows."
    elif thin_mean >= heavy_mean:
        status = "rejected"
        decided_by = "Reject: the thin mean share is at or above the heavy mean share."
    else:
        tstat_ok = t_val is not None and (-t_val) >= 2.0
        if not tstat_ok:
            status = "inconclusive"
            decided_by = "Inconclusive: thin is below heavy but the Welch t-stat is under 2.0."
        elif thin_mean < 0:
            status = "confirmed"
            decided_by = ("Confirm: the thin mean share is below the heavy mean share with a Welch t-stat of at "
                          "least 2.0, and the thin mean share is below 0.")
        else:
            status = "inconclusive"
            decided_by = ("Thin is below heavy with a Welch t-stat of at least 2.0 but the thin mean share is not "
                          "below 0, so the confirm rule is not met and no reject rule applies; left inconclusive.")

    return {
        "status": status,
        "main_measure": {
            "name": "mean next-bar share of the move, thin minus heavy",
            "value": float(diff) if diff is not None else None,
            "statistic": ({"name": "Welch t (thin minus heavy)", "value": t_val} if t_val is not None else None),
            "threshold": ("thin mean share below heavy mean share with Welch t of at least 2.0 in magnitude "
                          "(thin below heavy), and thin mean share below 0"),
        },
        "supporting_check": {
            "name": "strategy minus BTC hold return on active bars, min of heavy-only and thin-only parts",
            "value": sup_value,
            "passed": sup_passed,
        },
        "counts": {
            "thin cases": int(n_thin),
            "heavy cases": int(n_heavy),
            "thin mean share": thin_mean,
            "heavy mean share": heavy_mean,
        },
        "decided_by": decided_by,
        "reading": ("Thin cases are bars labelled mean_reversion and heavy cases bars labelled trending, with the "
                    "move as close[t]/close[t-1]-1 and the next return close[t+1]/close[t]-1 inside the window. "
                    "The supporting check is read as the summed before-cost position gain minus BTC's summed return "
                    "on each part's bars, which must be above 0 in both parts. A t-stat of at least 2.0 with the "
                    "thin mean not below 0 meets neither the confirm nor the reject rule, so it is treated as "
                    "inconclusive."),
    }
