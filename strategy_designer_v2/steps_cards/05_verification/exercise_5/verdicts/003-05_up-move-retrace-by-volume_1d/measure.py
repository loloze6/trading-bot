import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    thin_shares, heavy_shares = [], []
    sup = {"trending": {"gain": [], "hold": []}, "mean_reversion": {"gain": [], "hold": []}}

    for coin in bars:
        for window, df in bars[coin].items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            move = close / close.shift(1) - 1.0
            nxt = close.shift(-1) / close - 1.0
            regime = df["regime"].astype(str)
            alloc = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce")

            for i in range(len(df)):
                r = regime.iloc[i]
                if r not in ("trending", "mean_reversion"):
                    continue
                m, n = move.iloc[i], nxt.iloc[i]
                if pd.notna(m) and pd.notna(n) and m > 0:
                    share = n / m
                    if r == "mean_reversion":
                        thin_shares.append(share)
                    else:
                        heavy_shares.append(share)
                a = alloc.iloc[i]
                if pd.notna(a) and pd.notna(n) and a != 0:
                    sup[r]["gain"].append(a * n)
                    sup[r]["hold"].append(n)

    n_thin, n_heavy = len(thin_shares), len(heavy_shares)
    thin_mean = float(np.mean(thin_shares)) if n_thin else None
    heavy_mean = float(np.mean(heavy_shares)) if n_heavy else None
    diff = thin_mean - heavy_mean if (thin_mean is not None and heavy_mean is not None) else None

    t = None
    if n_thin >= 2 and n_heavy >= 2:
        res = stats.ttest_ind(thin_shares, heavy_shares, equal_var=False)
        if np.isfinite(res.statistic):
            t = float(res.statistic)

    # supporting check
    parts = {}
    for k, name in (("trending", "heavy"), ("mean_reversion", "thin")):
        g = sup[k]["gain"]
        h = sup[k]["hold"]
        parts[name] = {
            "n": len(g),
            "mean_gain": float(np.mean(g)) if g else None,
            "mean_hold": float(np.mean(h)) if h else None,
        }
    if parts["heavy"]["mean_gain"] is None or parts["thin"]["mean_gain"] is None:
        sup_passed = None
        sup_value = None
    else:
        sup_value = float(min(parts["heavy"]["mean_gain"], parts["thin"]["mean_gain"]))
        sup_passed = bool(parts["heavy"]["mean_gain"] > 0 and parts["thin"]["mean_gain"] > 0)

    # decision
    if n_thin < 15 or n_heavy < 15 or diff is None:
        status = "inconclusive"
        decided_by = "Inconclusive: fewer than 15 thin cases or fewer than 15 heavy cases across the 6 windows."
    elif thin_mean >= heavy_mean:
        status = "rejected"
        decided_by = "Reject: the thin mean share is at or above the heavy mean share."
    elif t is None or t > -2.0:
        status = "inconclusive"
        decided_by = "Inconclusive: thin is below heavy but the Welch t-stat is under 2.0 in magnitude."
    elif thin_mean < 0:
        status = "confirmed"
        decided_by = "Confirm: thin mean share is below heavy with Welch t of at least 2.0 and the thin mean share is below 0."
    else:
        status = "inconclusive"
        decided_by = ("Thin is significantly below heavy but the thin mean share is at or above 0, so the confirm rule "
                      "fails and no reject rule is met literally; left inconclusive.")

    return {
        "status": status,
        "main_measure": {
            "name": "mean next-bar share of move, thin minus heavy",
            "value": diff,
            "statistic": {"name": "Welch t (thin minus heavy)", "value": t} if t is not None else None,
            "threshold": "thin mean below heavy mean with Welch t of at least 2.0 (t <= -2.0 for thin minus heavy), and thin mean below 0",
        },
        "supporting_check": {
            "name": "min of mean active-bar strategy return before costs over heavy-only and thin-only parts (vs holding BTC)",
            "value": sup_value,
            "passed": sup_passed,
            "details": {
                "thin_mean_share": thin_mean,
                "heavy_mean_share": heavy_mean,
                "heavy_part": parts["heavy"],
                "thin_part": parts["thin"],
            },
        },
        "counts": {"thin cases": n_thin, "heavy cases": n_heavy},
        "decided_by": decided_by,
        "reading": ("Sharp-move bars are those labelled mean_reversion (thin) or trending (heavy), with the move as close[t]/close[t-1]-1 "
                    "inside the window and only positive moves with a next bar in the same window kept. The supporting check passes when the "
                    "mean active-bar strategy return (allocation != 0) is positive in both the heavy and thin parts, with the BTC hold return "
                    "reported alongside. Thin significantly below heavy but not below 0 matches no rule literally and is reported as inconclusive."),
    }
