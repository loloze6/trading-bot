import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    LOOK = 30

    # ---------- 1. Situation check: close below every one of the prior 30 closes, side short ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            for i in range(len(df)):
                if not np.isfinite(fc[i]) or fc[i] == 0:
                    continue
                if i == 0:
                    continue  # no prior close in the window to check against
                prior = close[max(0, i - LOOK):i]
                prior = prior[np.isfinite(prior)]
                if len(prior) == 0 or not np.isfinite(close[i]):
                    continue
                n_active += 1
                in_sit = close[i] < prior.min()
                if in_sit and fc[i] < 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("The new-low situation is recomputed inside each window as the close below every one of the prior 30 closes, "
               "using the available prior closes for bars with fewer than 30 in-window predecessors and skipping each window's "
               "first bar; the coin's mean 10-bar return is taken on the non-overlapping grid (positions 0, 10, 20, ...) of all "
               "its windows pooled; the median split uses the pooled cases of both coins; and fewer than 20 cases per group or "
               "40 in total is reported as 'not observable' as the workflow requires.")

    main_name = "Welch t of mild minus deep excess 10-bar return"
    threshold = "confirm if t <= -2 (with mild mean excess < 0); reject if t >= +2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are short bars on which the close is below every one of the "
                           "prior 30 closes, so the config does not trade the plan's new-low situation on the short side."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    # coin mean 10-bar return over all windows (non-overlapping grid)
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            for i in range(0, len(df) - H, H):
                r = close[i + H] / close[i] - 1
                if np.isfinite(r):
                    rets.append(r)
        coin_mean[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            last = None
            for i in range(len(df)):
                if reg[i] != "trending":
                    continue
                if i + H > len(df) - 1:
                    continue
                if last is not None and i - last < H:
                    continue
                r = close[i + H] / close[i] - 1
                if not (np.isfinite(r) and np.isfinite(fc[i]) and np.isfinite(coin_mean[coin])):
                    continue
                last = i
                cases.append((fc[i], r - coin_mean[coin]))

    n_total = len(cases)
    if n_total > 0:
        f = np.array([c[0] for c in cases])
        x = np.array([c[1] for c in cases])
        med = float(np.median(f))
        mild = x[f <= med]
        deep = x[f > med]
    else:
        mild = np.array([])
        deep = np.array([])
    n_mild, n_deep = len(mild), len(deep)
    counts = {"cases in total": int(n_total), "mild group cases": int(n_mild), "deep group cases": int(n_deep)}

    t_val = None
    diff = None
    if n_mild >= 2 and n_deep >= 2:
        t_val = float(stats.ttest_ind(mild, deep, equal_var=False).statistic)
        diff = float(mild.mean() - deep.mean())
        if not np.isfinite(t_val):
            t_val = None
    mild_mean = float(mild.mean()) if n_mild > 0 else None
    sup_pass = (mild_mean < 0) if mild_mean is not None else None

    main = {"name": main_name,
            "value": diff,
            "statistic": {"name": "Welch t", "value": t_val} if t_val is not None else None,
            "threshold": threshold}
    sup = {"name": "mild group mean excess 10-bar return below 0", "value": mild_mean, "passed": sup_pass}

    if n_mild < 20 or n_deep < 20 or n_total < 40:
        status = "not observable"
        decided = (f"The plan's minimum of 20 cases per group (40 in total) is not reached "
                   f"(mild {n_mild}, deep {n_deep}, total {n_total}).")
    elif t_val is None:
        status = "inconclusive"
        decided = "The Welch t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_val <= -2 and sup_pass:
        status = "confirmed"
        decided = "The Welch t of mild minus deep is -2 or less and the mild group's mean excess return is below 0."
    elif t_val >= 2:
        status = "rejected"
        decided = "The Welch t of mild minus deep is +2 or more."
    elif t_val <= -2:
        status = "inconclusive"
        decided = "The Welch t is -2 or less but the mild group's mean excess return is not below 0."
    else:
        status = "inconclusive"
        decided = "The Welch t of mild minus deep lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
