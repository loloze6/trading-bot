import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    FC = "forecast"
    ALLOC = "postRebalance_current_allocation"

    # Each coin's 80th-percentile cut-off of its non-zero forecasts, over all its bars and windows.
    cutoffs = {}
    for coin, wins in bars.items():
        vals = []
        for w, df in wins.items():
            f = pd.to_numeric(df[FC], errors="coerce").dropna()
            vals.append(f[f != 0].values)
        allv = np.concatenate(vals) if vals else np.array([])
        cutoffs[coin] = float(np.quantile(allv, 0.8)) if allv.size else np.nan

    ext_all, neu_all = [], []
    per_coin_diff = {}
    excess_total = 0.0
    excess_any = False

    for coin, wins in bars.items():
        ext_c, neu_c = [], []
        gains_sum, coin_ret_sum, alloc_vals = 0.0, 0.0, []
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d[FC], errors="coerce").values
            n = len(d)

            # Non-overlapping 5-bar forward returns on the grid 0, 5, 10, ... of the window.
            for t in range(0, n - H, H):
                c0, c1, f = close[t], close[t + H], fc[t]
                if np.isnan(c0) or np.isnan(c1) or np.isnan(f) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                if f != 0 and not np.isnan(cutoffs[coin]) and f >= cutoffs[coin]:
                    ext_c.append(r)
                elif f < 1:
                    neu_c.append(r)

            # Supporting check: position gains and coin returns, bar by bar inside the window.
            alloc = pd.to_numeric(d[ALLOC], errors="coerce").values
            for t in range(n - 1):
                a, c0, c1 = alloc[t], close[t], close[t + 1]
                if np.isnan(a) or np.isnan(c0) or np.isnan(c1) or c0 == 0:
                    continue
                r1 = c1 / c0 - 1.0
                gains_sum += a * r1
                coin_ret_sum += r1
                alloc_vals.append(a)

        if alloc_vals:
            avg_exp = float(np.mean(alloc_vals))
            excess_total += gains_sum - avg_exp * coin_ret_sum
            excess_any = True

        per_coin_diff[coin] = (float(np.mean(ext_c) - np.mean(neu_c))
                               if ext_c and neu_c else None)
        ext_all += ext_c
        neu_all += neu_c

    n_ext, n_neu = len(ext_all), len(neu_all)
    diff, t = None, None
    if n_ext > 0 and n_neu > 0:
        diff = float(np.mean(ext_all) - np.mean(neu_all))
    if n_ext >= 2 and n_neu >= 2:
        tt = stats.ttest_ind(ext_all, neu_all, equal_var=False).statistic
        t = float(tt) if np.isfinite(tt) else None

    coins_positive = sum(1 for v in per_coin_diff.values() if v is not None and v > 0)
    support_val = float(excess_total) if excess_any else None
    support_pass = (support_val > 0) if support_val is not None else None

    if n_ext < 30 or n_neu < 30:
        status = "inconclusive"
        decided = (f"Inconclusive: fewer than 30 non-overlapping extreme cases ({n_ext}) "
                   f"or fewer than 30 neutral cases ({n_neu}) pooled.")
    elif diff is None or t is None:
        status = "inconclusive"
        decided = "Inconclusive: the t-statistic could not be computed."
    elif diff <= 0 or t <= 0:
        status = "rejected"
        decided = ("Rejected: the pooled difference is negative with t <= -2, which points to reversal."
                   if t <= -2 else
                   "Rejected: the pooled extreme-minus-neutral difference is zero or negative (t <= 0).")
    elif t >= 2 and coins_positive >= 2 and support_pass:
        status = "confirmed"
        decided = ("Confirmed: the difference is positive with t >= 2, positive in at least 2 coins, "
                   "and the pooled supporting excess is positive.")
    elif t >= 2:
        status = "inconclusive"
        decided = ("Inconclusive: t >= 2, but the other confirm conditions are not met "
                   "(positive in at least 2 coins and a positive pooled supporting excess).")
    else:
        status = "inconclusive"
        decided = "Inconclusive: t is between 0 and 2."

    return {
        "status": status,
        "main_measure": {
            "name": "mean 5-bar forward return, extreme minus neutral bars",
            "value": diff,
            "statistic": {"name": "Welch t", "value": t} if t is not None else None,
            "threshold": "positive with t >= 2 to confirm; t <= 0 rejects",
        },
        "supporting_check": {
            "name": "strategy return minus exposure-scaled buy-and-hold, pooled, before costs",
            "value": support_val,
            "passed": support_pass,
        },
        "counts": {
            "non-overlapping extreme cases pooled": n_ext,
            "neutral cases pooled": n_neu,
            "coins with positive difference": coins_positive,
            "coins present": len(per_coin_diff),
        },
        "decided_by": decided,
        "reading": ("Extreme bars are those whose forecast is at or above the 80th percentile of that coin's "
                    "non-zero forecasts over all its bars and windows, and neutral bars have forecast < 1. "
                    "Returns are sampled on the grid 0, 5, 10, ... of each window. "
                    "With only 2 coins present, 'at least 2 of the 3 coins' is read literally as at least 2 coins, "
                    "so both must be positive. "
                    "The supporting excess is computed per coin as the sum of bar gains minus the coin's mean "
                    "allocation times the sum of the coin's bar returns, then summed over coins."),
    }
