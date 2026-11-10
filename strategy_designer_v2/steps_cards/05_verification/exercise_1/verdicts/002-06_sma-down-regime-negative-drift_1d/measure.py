import numpy as np
import pandas as pd


def measure(bars):
    fc_col = "forecast"
    alloc_col = "postRebalance_current_allocation"

    # Coin selection: the plan is BTC only
    coins = [c for c in bars.keys() if "BTC" in str(c).upper()]
    if not coins:
        coins = list(bars.keys())

    all_rets = []                 # next-bar returns over all bars, pooled
    in_rets = []                  # next-bar returns of in-state bars
    in_cluster = []               # stretch id of each in-state bar
    strat_gain_all = []           # position gain on every bar (equity curve)
    strat_gain_in = []            # position gain on in-state bars
    stretch_id = 0

    for coin in coins:
        wins = bars[coin]
        for w in sorted(wins.keys()):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            ret = close.shift(-1) / close - 1.0          # inside this window only
            fc = pd.to_numeric(df[fc_col], errors="coerce") if fc_col in df else pd.Series(np.nan, index=df.index)
            alloc = pd.to_numeric(df[alloc_col], errors="coerce") if alloc_col in df else pd.Series(np.nan, index=df.index)

            # all-bars returns
            valid_ret = ret.notna()
            all_rets.extend(ret[valid_ret].tolist())

            # equity curve gains (all bars)
            g = alloc * ret
            strat_gain_all.extend(g[g.notna()].tolist())

            # stretches: consecutive runs of forecast < 0 within a window
            in_state = (fc < 0) & fc.notna()
            prev = False
            for i in range(len(df)):
                cur = bool(in_state.iloc[i])
                if cur and not prev:
                    stretch_id += 1
                if cur and valid_ret.iloc[i]:
                    in_rets.append(float(ret.iloc[i]))
                    in_cluster.append(stretch_id)
                    gi = g.iloc[i]
                    strat_gain_in.append((float(gi) if pd.notna(gi) else np.nan, float(ret.iloc[i])))
                prev = cur

    all_rets = np.asarray(all_rets, dtype=float)
    in_rets = np.asarray(in_rets, dtype=float)
    in_cluster = np.asarray(in_cluster)

    n_in = int(len(in_rets))
    stretches_used = int(len(np.unique(in_cluster))) if n_in > 0 else 0

    diff = None
    t_stat = None
    mean_all = float(np.mean(all_rets)) if len(all_rets) > 0 else None
    if n_in > 0 and mean_all is not None:
        mean_in = float(np.mean(in_rets))
        diff = mean_in - mean_all
        G = stretches_used
        if G >= 2:
            resid = in_rets - mean_in
            sums = pd.Series(resid).groupby(in_cluster).sum().values
            var = (G / (G - 1.0)) * np.sum(sums ** 2) / (n_in ** 2)
            se = float(np.sqrt(var))
            if se > 0:
                t_stat = diff / se

    # supporting check: share of down bars
    down_in = float(np.mean(in_rets < 0)) if n_in > 0 else None
    down_all = float(np.mean(all_rets < 0)) if len(all_rets) > 0 else None
    down_diff = (down_in - down_all) if (down_in is not None and down_all is not None) else None
    down_passed = (down_diff > 0) if down_diff is not None else None

    # equity-curve details (reported, before costs)
    sg_all = np.asarray(strat_gain_all, dtype=float)
    equity_end = float(np.prod(1.0 + sg_all)) if len(sg_all) > 0 else None
    pairs = [(a, b) for a, b in strat_gain_in if not np.isnan(a)]
    if pairs:
        strat_in = float(np.prod([1.0 + a for a, _ in pairs]) - 1.0)
        hold_in = float(np.prod([1.0 + b for _, b in pairs]) - 1.0)
    else:
        strat_in, hold_in = None, None
    equity_above_flat = (equity_end > 1.0) if equity_end is not None else None
    beats_hold = (strat_in > hold_in) if (strat_in is not None and hold_in is not None) else None

    # decision
    if stretches_used < 3 or n_in < 60 or diff is None:
        status = "inconclusive"
        decided_by = ("Inconclusive: fewer than 3 distinct down-cross stretches or fewer than 60 in-state bars "
                      "pooled across the windows.")
    elif diff >= 0:
        status = "rejected"
        decided_by = "Reject: the in-state mean next-bar return is at or above the all-bars mean."
    elif diff <= -0.001 and t_stat is not None and t_stat <= -2 and down_passed:
        status = "confirmed"
        decided_by = ("Confirm: in-state mean is at least 0.10% per day below the all-bars mean with "
                      "stretch-clustered t <= -2, and the down-bar share in the stretches is higher than over all bars.")
    else:
        status = "inconclusive"
        decided_by = ("Inconclusive: the difference is negative but t > -2, or it is smaller than 0.10% per day, "
                      "or the down-bar share condition of the confirm rule is not met.")

    return {
        "status": status,
        "main_measure": {
            "name": "in-state (forecast<0) mean next-bar return minus all-bars mean, pooled",
            "value": float(diff) if diff is not None else None,
            "threshold": "<= -0.10% per day with stretch-clustered t <= -2 to confirm; >= 0 to reject",
        },
        "supporting_check": {
            "name": "down-bar share in stretches minus down-bar share over all bars",
            "value": float(down_diff) if down_diff is not None else None,
            "passed": bool(down_passed) if down_passed is not None else None,
            "details": {
                "t_stat_clustered": float(t_stat) if t_stat is not None else None,
                "down_share_in_state": down_in,
                "down_share_all": down_all,
                "equity_end_multiple_before_costs": equity_end,
                "equity_above_flat": bool(equity_above_flat) if equity_above_flat is not None else None,
                "strategy_return_in_state": strat_in,
                "hold_return_in_state": hold_in,
                "beats_hold_in_state": bool(beats_hold) if beats_hold is not None else None,
            },
        },
        "cases": stretches_used,
        "decided_by": decided_by,
        "reading": ("A stretch is a run of consecutive bars with forecast < 0 inside one window, cases counts stretches "
                    "holding at least one in-state bar with a next-bar return, the clustered t treats the all-bars mean "
                    "as fixed with a G/(G-1) correction, a down bar is a negative next-bar return, and the equity-curve "
                    "parts of the supporting check are reported but only the down-share condition named in the confirm "
                    "rule enters the decision."),
    }
