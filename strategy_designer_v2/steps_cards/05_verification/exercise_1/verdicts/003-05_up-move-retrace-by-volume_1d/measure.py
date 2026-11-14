import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    alloc_col = "postRebalance_current_allocation"
    thin_shares, heavy_shares = [], []
    sup = {"trending": {"strat": 0.0, "hold": 0.0, "n": 0},
           "mean_reversion": {"strat": 0.0, "hold": 0.0, "n": 0}}

    for coin, windows in bars.items():
        for w in sorted(windows.keys()):
            df = windows[w]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            move = close / close.shift(1) - 1.0          # the sharp move on bar t, within window
            nxt = close.shift(-1) / close - 1.0          # next bar close-to-close return, within window
            regime = df["regime"].astype(str)
            alloc = pd.to_numeric(df[alloc_col], errors="coerce") if alloc_col in df.columns else pd.Series(np.nan, index=df.index)

            for i in range(len(df)):
                r = regime.iloc[i]
                if r not in ("trending", "mean_reversion"):
                    continue
                # main measure: share kept / given back
                m, n = move.iloc[i], nxt.iloc[i]
                if np.isfinite(m) and np.isfinite(n) and m != 0:
                    share = n / m
                    if r == "mean_reversion":
                        thin_shares.append(share)
                    else:
                        heavy_shares.append(share)
                # supporting check: active bars, gain before costs vs holding BTC
                a = alloc.iloc[i]
                if np.isfinite(a) and a != 0 and np.isfinite(n):
                    sup[r]["strat"] += a * n
                    sup[r]["hold"] += n
                    sup[r]["n"] += 1

    n_thin, n_heavy = len(thin_shares), len(heavy_shares)
    thin_mean = float(np.mean(thin_shares)) if n_thin else None
    heavy_mean = float(np.mean(heavy_shares)) if n_heavy else None
    diff = (heavy_mean - thin_mean) if (thin_mean is not None and heavy_mean is not None) else None

    t_stat = None
    if n_thin >= 2 and n_heavy >= 2:
        res = stats.ttest_ind(np.array(heavy_shares), np.array(thin_shares), equal_var=False)
        if np.isfinite(res.statistic):
            t_stat = float(res.statistic)  # positive when thin mean is below heavy mean

    # supporting check
    ex_heavy = sup["trending"]["strat"] - sup["trending"]["hold"] if sup["trending"]["n"] > 0 else None
    ex_thin = sup["mean_reversion"]["strat"] - sup["mean_reversion"]["hold"] if sup["mean_reversion"]["n"] > 0 else None
    if ex_heavy is None or ex_thin is None:
        sup_passed = None
        sup_value = None
    else:
        sup_passed = bool(ex_heavy > 0 and ex_thin > 0)
        sup_value = float(min(ex_heavy, ex_thin))

    # decision
    if n_thin < 15 or n_heavy < 15:
        status = "inconclusive"
        decided_by = f"Inconclusive: fewer than 15 thin ({n_thin}) or heavy ({n_heavy}) cases across the 6 windows."
    elif thin_mean >= heavy_mean:
        status = "rejected"
        decided_by = "Reject: the thin mean share is at or above the heavy mean share."
    elif t_stat is None or t_stat < 2.0:
        status = "inconclusive"
        decided_by = "Inconclusive: thin mean share is below heavy but the Welch t-stat is under 2.0."
    elif thin_mean < 0:
        status = "confirmed"
        decided_by = "Confirm: thin mean share below heavy with Welch t-stat >= 2.0, and thin mean share below 0."
    else:
        status = "inconclusive"
        decided_by = ("No plan rule is met: thin is below heavy with t >= 2.0 but the thin mean share is not "
                      "below 0, so neither confirm nor reject applies; left inconclusive.")

    return {
        "status": status,
        "main_measure": {
            "name": "thin minus heavy mean next-bar share of move (heavy mean - thin mean), Welch t",
            "value": None if diff is None else float(diff),
            "threshold": "thin mean share below heavy mean share with Welch t >= 2.0, and thin mean share below 0",
            "thin_mean_share": thin_mean,
            "heavy_mean_share": heavy_mean,
            "welch_t": t_stat,
        },
        "supporting_check": {
            "name": "active-bar gain before costs minus holding BTC, heavy-only and thin-only parts (min of the two)",
            "value": sup_value,
            "passed": sup_passed,
            "heavy_excess": None if ex_heavy is None else float(ex_heavy),
            "thin_excess": None if ex_thin is None else float(ex_thin),
        },
        "cases": int(n_thin + n_heavy),
        "decided_by": decided_by,
        "reading": ("Sharp-move bars are those labelled regime 'trending' (heavy) or 'mean_reversion' (thin); the move is "
                    "close[t]/close[t-1]-1 within the window (so a window's first bar and last bar drop out); the supporting "
                    "check sums per-bar position gain minus BTC return over active bars (non-zero held allocation) split by the "
                    "bar's regime label, and does not change the status; thin below heavy with t >= 2 but thin share >= 0 "
                    "meets no stated rule and is reported inconclusive."),
    }
