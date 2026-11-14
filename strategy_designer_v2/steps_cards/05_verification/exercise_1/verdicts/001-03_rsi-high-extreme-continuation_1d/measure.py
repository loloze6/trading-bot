import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    MIN_CASES = 30
    FC, AL = "forecast", "postRebalance_current_allocation"

    # 1) Extreme cut-off: 80th percentile of non-zero forecasts, pooled over all coins and windows.
    nz = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = pd.to_numeric(df[FC], errors="coerce").to_numpy(dtype=float)
            f = f[np.isfinite(f) & (f != 0)]
            nz.extend(f.tolist())
    q80 = float(np.quantile(np.array(nz), 0.8)) if len(nz) > 0 else np.nan

    # 2) Non-overlapping 5-bar forward returns, on a fixed grid t = 0, 5, 10, ... inside each window.
    ext_all, neu_all = [], []
    per_coin = {}
    for coin, wins in bars.items():
        ce, cn = [], []
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(d[FC], errors="coerce").to_numpy(dtype=float)
            n = len(d)
            for t in range(0, n - H, H):
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and np.isfinite(f[t]) and c[t] != 0):
                    continue
                r = c[t + H] / c[t] - 1.0
                if np.isfinite(q80) and f[t] != 0 and f[t] >= q80:
                    ce.append(r)
                elif f[t] < 1:
                    cn.append(r)
        per_coin[coin] = (ce, cn)
        ext_all.extend(ce)
        neu_all.extend(cn)

    n_ext, n_neu = len(ext_all), len(neu_all)
    diff, tstat = None, None
    if n_ext >= 2 and n_neu >= 2:
        e, nn = np.array(ext_all), np.array(neu_all)
        diff = float(e.mean() - nn.mean())
        tt = stats.ttest_ind(e, nn, equal_var=False)
        tstat = float(tt.statistic) if np.isfinite(tt.statistic) else None
    elif n_ext >= 1 and n_neu >= 1:
        diff = float(np.mean(ext_all) - np.mean(neu_all))

    coins_pos = 0
    coin_diffs = {}
    for coin, (ce, cn) in per_coin.items():
        if len(ce) > 0 and len(cn) > 0:
            dd = float(np.mean(ce) - np.mean(cn))
            coin_diffs[coin] = dd
            if dd > 0:
                coins_pos += 1
        else:
            coin_diffs[coin] = None

    # 3) Supporting check: strategy return minus buy-and-hold scaled to average exposure, per coin, pooled.
    excess_total = 0.0
    have_support = False
    for coin, wins in bars.items():
        strat_sum, coin_sum, allocs = 0.0, 0.0, []
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            a = pd.to_numeric(d[AL], errors="coerce").to_numpy(dtype=float)
            for t in range(len(d) - 1):
                if not (np.isfinite(c[t]) and np.isfinite(c[t + 1]) and np.isfinite(a[t]) and c[t] != 0):
                    continue
                r = c[t + 1] / c[t] - 1.0
                strat_sum += a[t] * r
                coin_sum += r
                allocs.append(a[t])
        if allocs:
            have_support = True
            excess_total += strat_sum - float(np.mean(allocs)) * coin_sum
    support_val = float(excess_total) if have_support else None
    support_pass = (support_val > 0) if support_val is not None else None

    # 4) Decision
    if n_ext < MIN_CASES or n_neu < MIN_CASES or diff is None or tstat is None:
        status = "inconclusive"
        decided = (f"Inconclusive: fewer than 30 non-overlapping extreme ({n_ext}) or neutral ({n_neu}) cases pooled.")
    elif diff <= 0 or tstat <= 0:
        status = "rejected"
        decided = ("Rejected: pooled extreme-minus-neutral difference is zero or negative (t <= 0)"
                   + ("; t <= -2 points to reversal." if tstat <= -2 else "."))
    elif tstat >= 2 and coins_pos >= 2 and support_pass:
        status = "confirmed"
        decided = ("Confirmed: pooled difference positive with t >= 2, positive in at least 2 coins, "
                   "and pooled supporting excess positive.")
    else:
        status = "inconclusive"
        if tstat < 2:
            decided = "Inconclusive: t is between 0 and 2."
        else:
            decided = ("Inconclusive: t >= 2 but the confirm rule's coin count (>= 2 positive coins) "
                       "or positive pooled supporting excess is not met.")

    return {
        "status": status,
        "main_measure": {
            "name": "mean 5-bar fwd return after extreme minus after neutral bars (pooled)",
            "value": diff,
            "threshold": "positive with t-statistic >= 2 (reject if t <= 0)",
        },
        "supporting_check": {
            "name": "strategy return minus exposure-scaled buy-and-hold, pooled over coins",
            "value": support_val,
            "passed": support_pass,
        },
        "cases": int(n_ext),
        "decided_by": decided + f" (t={tstat}, extreme n={n_ext}, neutral n={n_neu}, coins positive={coins_pos}/{len(per_coin)})",
        "reading": ("Non-overlapping returns are taken on a fixed grid t=0,5,10,... within each window; the top-20% "
                    "cut-off is the 80th percentile of non-zero forecasts pooled over all coins and windows; t is "
                    "Welch's two-sample t; with only 2 coins present the 'at least 2 of 3 coins' rule requires both "
                    "positive; the supporting excess sums per-bar returns with exposure = mean allocation per coin, "
                    "and 'cases' counts the non-overlapping extreme cases."),
    }
