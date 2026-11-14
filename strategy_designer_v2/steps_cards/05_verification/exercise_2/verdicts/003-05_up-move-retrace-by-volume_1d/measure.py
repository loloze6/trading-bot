import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    MIN_CASES = 15
    T_MIN = 2.0
    alloc_col = "postRebalance_current_allocation"

    thin_shares, heavy_shares = [], []
    part = {"heavy": {"strat": [], "hold": []}, "thin": {"strat": [], "hold": []}}

    for coin, windows in bars.items():
        for w, df in windows.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            move = close / close.shift(1) - 1.0          # sharp-move bar's own return, same window only
            nxt = close.shift(-1) / close - 1.0           # next bar's close-to-close return, same window only
            regime = d["regime"].astype(str)
            alloc = pd.to_numeric(d[alloc_col], errors="coerce") if alloc_col in d else pd.Series(np.nan, index=d.index)

            for i in range(len(d)):
                r = regime.iloc[i]
                if r == "trending":
                    grp = "heavy"
                elif r == "mean_reversion":
                    grp = "thin"
                else:
                    continue
                m, n = move.iloc[i], nxt.iloc[i]
                # main measure: next return as a share of the (up) move
                if np.isfinite(m) and np.isfinite(n) and m > 0:
                    share = n / m
                    (heavy_shares if grp == "heavy" else thin_shares).append(float(share))
                # supporting check: active bars, gain before costs vs holding BTC
                a = alloc.iloc[i]
                if np.isfinite(a) and np.isfinite(n) and a != 0:
                    part[grp]["strat"].append(float(a * n))
                    part[grp]["hold"].append(float(n))

    n_thin, n_heavy = len(thin_shares), len(heavy_shares)
    thin_mean = float(np.mean(thin_shares)) if n_thin else None
    heavy_mean = float(np.mean(heavy_shares)) if n_heavy else None

    t_stat = None
    if n_thin >= 2 and n_heavy >= 2:
        t, _ = stats.ttest_ind(heavy_shares, thin_shares, equal_var=False)
        t_stat = float(t) if np.isfinite(t) else None

    diff = (thin_mean - heavy_mean) if (thin_mean is not None and heavy_mean is not None) else None

    # supporting check
    excess = {}
    for g in ("heavy", "thin"):
        if part[g]["strat"]:
            excess[g] = float(np.sum(part[g]["strat"]) - np.sum(part[g]["hold"]))
        else:
            excess[g] = None
    if excess["heavy"] is None or excess["thin"] is None:
        sup_passed, sup_value = None, None
    else:
        sup_passed = bool(excess["heavy"] > 0 and excess["thin"] > 0)
        sup_value = float(min(excess["heavy"], excess["thin"]))

    # decision
    if n_thin < MIN_CASES or n_heavy < MIN_CASES or diff is None:
        status = "inconclusive"
        decided_by = (f"Inconclusive: fewer than {MIN_CASES} thin cases ({n_thin}) or fewer than "
                      f"{MIN_CASES} heavy cases ({n_heavy}) across the windows.")
    elif thin_mean >= heavy_mean:
        status = "rejected"
        decided_by = "Rejected: the thin mean share is at or above the heavy mean share."
    elif t_stat is None or t_stat < T_MIN:
        status = "inconclusive"
        decided_by = "Inconclusive: thin is below heavy but the Welch t-stat is under 2.0."
    elif thin_mean < 0:
        status = "confirmed"
        decided_by = ("Confirmed: thin mean share is below heavy with Welch t-stat >= 2.0, "
                      "and the thin mean share is below 0.")
    else:
        status = "inconclusive"
        decided_by = ("Inconclusive: thin is below heavy with t-stat >= 2.0 but the thin mean share is not "
                      "below 0, a case no confirm or reject rule covers.")

    return {
        "status": status,
        "main_measure": {
            "name": "thin minus heavy mean next-bar share of move",
            "value": diff,
            "threshold": "thin mean below heavy mean with Welch t >= 2.0 and thin mean below 0",
        },
        "supporting_check": {
            "name": "min over heavy/thin parts of strategy gain minus BTC hold on active bars",
            "value": sup_value,
            "passed": sup_passed,
        },
        "cases": int(n_thin + n_heavy),
        "decided_by": decided_by,
        "reading": ("Heavy and thin cases are the bars labelled trending and mean_reversion, the move is "
                    "close[t]/close[t-1]-1 within the window (first row of a window and non-positive moves "
                    "excluded), the supporting check compares summed position gains with summed BTC returns "
                    "on bars with nonzero allocation in each part, and thin<heavy with t>=2 but thin>=0, "
                    "covered by no rule, is treated as inconclusive."),
        "details": {
            "thin_mean_share": thin_mean,
            "heavy_mean_share": heavy_mean,
            "welch_t_heavy_minus_thin": t_stat,
            "n_thin": n_thin,
            "n_heavy": n_heavy,
            "excess_heavy": excess["heavy"],
            "excess_thin": excess["thin"],
        },
    }
