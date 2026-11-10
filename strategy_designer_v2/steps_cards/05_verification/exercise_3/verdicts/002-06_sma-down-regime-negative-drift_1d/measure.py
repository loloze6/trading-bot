import numpy as np
import pandas as pd


def measure(bars):
    H = 1
    MIN_STRETCHES = 3
    MIN_BARS = 60
    DIFF_THR = -0.001
    T_THR = -2.0

    coin = None
    for c in bars:
        if "BTC" in str(c).upper():
            coin = c
            break
    if coin is None and len(bars) > 0:
        coin = list(bars.keys())[0]

    all_r = []
    in_r = []
    in_cluster = []
    strat_logs_all = []
    strat_logs_in = []
    hold_logs_in = []
    stretch_id = 0

    if coin is not None:
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            alloc = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce")
            r = close.shift(-H) / close - 1.0

            prev_in = False
            for i in range(len(df)):
                ri = r.iloc[i]
                fi = fc.iloc[i]
                ai = alloc.iloc[i]
                valid_r = pd.notna(ri) and np.isfinite(ri)
                if valid_r:
                    all_r.append(float(ri))
                    if pd.notna(ai):
                        strat_logs_all.append(np.log1p(float(ai) * float(ri)))
                is_in = bool(pd.notna(fi) and fi < 0)
                if is_in and not prev_in:
                    stretch_id += 1
                if is_in and valid_r:
                    in_r.append(float(ri))
                    in_cluster.append(stretch_id)
                    hold_logs_in.append(np.log1p(float(ri)))
                    if pd.notna(ai):
                        strat_logs_in.append(np.log1p(float(ai) * float(ri)))
                prev_in = is_in

    all_r = np.array(all_r, dtype=float)
    in_r = np.array(in_r, dtype=float)
    in_cluster = np.array(in_cluster)

    n_in = int(len(in_r))
    n_all = int(len(all_r))
    n_stretches = int(len(np.unique(in_cluster))) if n_in > 0 else 0

    diff = None
    t_stat = None
    if n_in > 0 and n_all > 0:
        mean_in = float(in_r.mean())
        mean_all = float(all_r.mean())
        diff = mean_in - mean_all
        if n_stretches >= 2:
            e = in_r - mean_in
            G = n_stretches
            sums = pd.Series(e).groupby(in_cluster).sum().values
            var = (G / (G - 1.0)) * np.sum(sums ** 2) / (n_in ** 2)
            se = float(np.sqrt(var))
            if se > 0:
                t_stat = float(diff / se)

    down_in = float(np.mean(in_r < 0)) if n_in > 0 else None
    down_all = float(np.mean(all_r < 0)) if n_all > 0 else None
    down_diff = (down_in - down_all) if (down_in is not None and down_all is not None) else None
    down_passed = (down_diff > 0) if down_diff is not None else None

    strat_total = float(np.expm1(np.sum(strat_logs_all))) if strat_logs_all else None
    strat_in_total = float(np.expm1(np.sum(strat_logs_in))) if strat_logs_in else None
    hold_in_total = float(np.expm1(np.sum(hold_logs_in))) if hold_logs_in else None
    equity_above_flat = (strat_total > 0) if strat_total is not None else None
    beats_hold_in = ((strat_in_total > hold_in_total)
                     if (strat_in_total is not None and hold_in_total is not None) else None)

    if n_stretches < MIN_STRETCHES or n_in < MIN_BARS or diff is None:
        status = "inconclusive"
        decided_by = ("Inconclusive: fewer than 3 distinct down-cross stretches or fewer than 60 in-state bars "
                      "pooled across the windows.")
    elif diff >= 0:
        status = "rejected"
        decided_by = "Reject: the in-state mean return is at or above the all-bars mean."
    elif diff <= DIFF_THR and t_stat is not None and t_stat <= T_THR and down_passed:
        status = "confirmed"
        decided_by = ("Confirm: in-state mean is at least 0.10% per day below the all-bars mean with "
                      "stretch-clustered t <= -2, and the share of down bars inside stretches is higher.")
    else:
        status = "inconclusive"
        if diff > DIFF_THR or t_stat is None or t_stat > T_THR:
            decided_by = ("Inconclusive: the difference is negative but t > -2 or it is smaller than "
                          "0.10% per day.")
        else:
            decided_by = ("Inconclusive: the difference and t meet the confirm thresholds but the share of "
                          "down bars inside the stretches is not higher than over all bars, so the confirm "
                          "rule is not fully met.")

    return {
        "status": status,
        "main_measure": {
            "name": "in-state minus all-bars mean next-bar return",
            "value": diff,
            "statistic": ({"name": "stretch-clustered t", "value": t_stat} if t_stat is not None else None),
            "threshold": "difference <= -0.10% per day with stretch-clustered t <= -2",
        },
        "supporting_check": {
            "name": "share of down bars in stretches minus share over all bars",
            "value": down_diff,
            "passed": down_passed,
            "details": {
                "down_share_in_state": down_in,
                "down_share_all": down_all,
                "strategy_equity_return_before_costs": strat_total,
                "equity_ends_above_flat": equity_above_flat,
                "strategy_return_in_state": strat_in_total,
                "hold_return_in_state": hold_in_total,
                "beats_holding_in_state": beats_hold_in,
            },
        },
        "counts": {
            "distinct down-cross stretches": n_stretches,
            "in-state bars pooled": n_in,
            "all bars pooled": n_all,
        },
        "decided_by": decided_by,
        "reading": ("In-state bars are those with forecast < 0, a stretch is each contiguous run of such bars "
                    "within one window (a run open at a window's start counts as one stretch), the t uses a "
                    "cluster-robust standard error of the pooled in-state mean by stretch with the all-bars mean "
                    "taken as fixed, a down bar is a negative next-bar return, and only the down-bar share enters "
                    "the confirm rule while the equity checks are reported but not decisive."),
    }
