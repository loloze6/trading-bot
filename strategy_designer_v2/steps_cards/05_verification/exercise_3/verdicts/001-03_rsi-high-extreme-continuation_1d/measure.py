import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    rows = []          # (coin, forecast, fwd_ret) on the non-overlapping grid
    all_nonzero = []   # all non-zero forecasts, every bar, every coin and window
    bar_gain = {}      # coin -> list of (alloc, next-bar return)

    for coin, wins in bars.items():
        bar_gain.setdefault(coin, [])
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            alloc = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce").to_numpy(dtype=float)
            n = len(df)

            nz = fc[np.isfinite(fc) & (fc != 0)]
            all_nonzero.extend(nz.tolist())

            for t in range(0, n, H):
                if t + H >= n:
                    break
                if not (np.isfinite(fc[t]) and np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] != 0):
                    continue
                rows.append((coin, fc[t], close[t + H] / close[t] - 1.0))

            for t in range(n - 1):
                if np.isfinite(alloc[t]) and np.isfinite(close[t]) and np.isfinite(close[t + 1]) and close[t] != 0:
                    bar_gain[coin].append((alloc[t], close[t + 1] / close[t] - 1.0))

    if len(all_nonzero) > 0:
        thr = float(np.percentile(np.asarray(all_nonzero), 80))
    else:
        thr = np.nan

    grid = pd.DataFrame(rows, columns=["coin", "fc", "ret"])
    if len(grid) and np.isfinite(thr):
        ext_mask = (grid["fc"] != 0) & (grid["fc"] >= thr)
    else:
        ext_mask = pd.Series(False, index=grid.index)
    neu_mask = grid["fc"] < 1 if len(grid) else pd.Series(False, index=grid.index)

    ext = grid.loc[ext_mask, "ret"].to_numpy(dtype=float)
    neu = grid.loc[neu_mask, "ret"].to_numpy(dtype=float)
    n_ext, n_neu = int(len(ext)), int(len(neu))

    diff = float(ext.mean() - neu.mean()) if (n_ext > 0 and n_neu > 0) else None
    t_stat = None
    if n_ext >= 2 and n_neu >= 2:
        tt = stats.ttest_ind(ext, neu, equal_var=False)
        t_stat = float(tt.statistic) if np.isfinite(tt.statistic) else None

    # per-coin differences
    coin_diffs = {}
    for coin in bars.keys():
        g = grid[grid["coin"] == coin] if len(grid) else grid
        e = g.loc[ext_mask.loc[g.index], "ret"] if len(g) else pd.Series(dtype=float)
        nn = g.loc[neu_mask.loc[g.index], "ret"] if len(g) else pd.Series(dtype=float)
        coin_diffs[coin] = float(e.mean() - nn.mean()) if (len(e) > 0 and len(nn) > 0) else None
    n_coins_pos = int(sum(1 for v in coin_diffs.values() if v is not None and v > 0))
    coin_ok = n_coins_pos >= 2

    # supporting check: strategy minus exposure-scaled buy-and-hold, per coin, summed
    total_excess = 0.0
    any_bar = False
    per_coin_excess = {}
    for coin, lst in bar_gain.items():
        if not lst:
            continue
        a = np.array([x[0] for x in lst])
        r = np.array([x[1] for x in lst])
        avg_exp = a.mean()
        ex = float(np.sum(a * r) - avg_exp * np.sum(r))
        per_coin_excess[coin] = ex
        total_excess += ex
        any_bar = True
    sup_val = float(total_excess) if any_bar else None
    sup_pass = (sup_val > 0) if sup_val is not None else None

    if n_ext < 30 or n_neu < 30 or t_stat is None or diff is None:
        status = "inconclusive"
        decided = "Fewer than 30 non-overlapping extreme or neutral cases pooled (or no t-statistic computable), so the plan's inconclusive rule applies."
    elif t_stat <= -2:
        status = "rejected"
        decided = "The t-statistic is -2 or below, which rejects and points to reversal."
    elif t_stat <= 0 or diff <= 0:
        status = "rejected"
        decided = "The pooled extreme-minus-neutral difference is zero or negative (t <= 0), which rejects."
    elif t_stat >= 2 and diff > 0 and coin_ok and sup_pass:
        status = "confirmed"
        decided = "The difference is positive with t >= 2, positive in at least 2 coins, and the pooled supporting excess is positive, so it confirms."
    elif t_stat < 2:
        status = "inconclusive"
        decided = "The t-statistic is between 0 and 2, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t >= 2 but the per-coin (at least 2 coins positive) or pooled supporting-excess condition fails, so neither confirm nor reject is met."

    return {
        "status": status,
        "main_measure": {
            "name": "mean 5-bar forward return, extreme minus neutral bars",
            "value": diff,
            "statistic": {"name": "Welch t", "value": t_stat} if t_stat is not None else None,
            "threshold": "positive with t >= 2 confirms; t <= 0 rejects (t <= -2 rejects as reversal); 0 < t < 2 inconclusive",
        },
        "supporting_check": {
            "name": "strategy minus exposure-scaled buy-and-hold, pooled, before costs",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {
            "non-overlapping extreme cases pooled": n_ext,
            "neutral cases": n_neu,
            "coins with positive difference": n_coins_pos,
            "coins in record": int(len(bars)),
        },
        "decided_by": decided,
        "reading": (
            "The top-20% cut is the 80th percentile of all non-zero forecasts pooled over every bar of all coins and windows "
            "(extreme = forecast >= it), neutral = forecast < 1 including zeros, both sampled on the 0,5,10,... grid of each window; "
            "'at least 2 of the 3 coins' is applied literally as at least 2 positive coins among those present; the supporting excess "
            "is, per coin, the summed per-bar strategy gain minus that coin's mean allocation times its summed per-bar return, added over coins; "
            "t >= 2 with a failing coin or supporting condition is treated as inconclusive."
        ),
    }
