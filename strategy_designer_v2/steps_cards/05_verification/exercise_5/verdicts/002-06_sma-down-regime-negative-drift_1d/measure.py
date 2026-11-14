import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    POS = "postRebalance_current_allocation"
    THRESH = 0.001  # 0.10% per day
    T_CUT = -2.0
    MIN_STRETCHES = 3
    MIN_INSTATE = 60

    all_rets = []
    in_rets = []
    in_cluster = []
    strat_log_all = 0.0
    strat_ok = False
    strat_log_in = 0.0
    hold_log_in = 0.0
    n_stretches = 0

    for coin in sorted(bars.keys()):
        for window in sorted(bars[coin].keys()):
            df = bars[coin][window].reset_index(drop=True)
            if df.empty or "close" not in df or FC not in df:
                continue
            close = df["close"].astype(float).values
            fc = df[FC].astype(float).values
            pos = df[POS].astype(float).values if POS in df else np.full(len(df), np.nan)
            n = len(df)
            nxt = np.full(n, np.nan)
            if n > 1:
                nxt[:-1] = close[1:] / close[:-1] - 1.0

            # stretches: consecutive runs of forecast < 0 within this window
            in_state = np.where(np.isnan(fc), False, fc < 0)
            stretch_id = np.full(n, -1)
            prev = False
            for i in range(n):
                if in_state[i]:
                    if not prev:
                        n_stretches += 1
                    stretch_id[i] = n_stretches
                prev = in_state[i]

            for i in range(n):
                r = nxt[i]
                if np.isnan(r):
                    continue
                all_rets.append(r)
                p = pos[i]
                if not np.isnan(p):
                    g = p * r
                    if 1.0 + g > 0:
                        strat_log_all += np.log1p(g)
                        strat_ok = True
                if in_state[i]:
                    in_rets.append(r)
                    in_cluster.append(stretch_id[i])
                    if not np.isnan(p) and 1.0 + p * r > 0:
                        strat_log_in += np.log1p(p * r)
                    hold_log_in += np.log1p(r)

    all_rets = np.asarray(all_rets, dtype=float)
    in_rets = np.asarray(in_rets, dtype=float)
    in_cluster = np.asarray(in_cluster)
    n_in = int(len(in_rets))
    n_clusters_with_returns = int(len(np.unique(in_cluster))) if n_in else 0

    diff = None
    t_stat = None
    if n_in > 0 and len(all_rets) > 0:
        mean_all = float(np.mean(all_rets))
        mean_in = float(np.mean(in_rets))
        diff = mean_in - mean_all
        G = n_clusters_with_returns
        if G >= 2:
            resid = in_rets - mean_in
            sums = pd.Series(resid).groupby(in_cluster).sum().values
            var = (G / (G - 1.0)) * np.sum(sums ** 2) / (n_in ** 2)
            se = float(np.sqrt(var))
            if se > 0:
                t_stat = diff / se

    # supporting check
    down_in = float(np.mean(in_rets < 0)) if n_in else None
    down_all = float(np.mean(all_rets < 0)) if len(all_rets) else None
    down_diff = (down_in - down_all) if (down_in is not None and down_all is not None) else None
    down_ok = (down_diff is not None) and (down_diff > 0)
    equity_end = float(np.exp(strat_log_all)) if strat_ok else None
    equity_ok = equity_end is not None and equity_end > 1.0
    beat_hold_ok = n_in > 0 and strat_log_in > hold_log_in
    supp_passed = None if down_diff is None else bool(down_ok and equity_ok and beat_hold_ok)

    # decision
    if n_stretches < MIN_STRETCHES or n_in < MIN_INSTATE or diff is None:
        status = "inconclusive"
        decided = (f"Inconclusive: fewer than {MIN_STRETCHES} distinct down-cross stretches "
                   f"or fewer than {MIN_INSTATE} in-state bars pooled across the windows.")
    elif diff >= 0:
        status = "rejected"
        decided = "Rejected: the in-state mean return is at or above the all-bars mean."
    elif diff <= -THRESH and t_stat is not None and t_stat <= T_CUT and down_ok:
        status = "confirmed"
        decided = ("Confirmed: in-state mean is at least 0.10% per day below the all-bars mean with "
                   "stretch-clustered t <= -2, and the down-bar share is higher inside the stretches.")
    else:
        status = "inconclusive"
        decided = ("Inconclusive: the difference is negative but t > -2, or it is smaller than 0.10% per day, "
                   "or the down-bar share inside the stretches is not higher than over all bars.")

    return {
        "status": status,
        "main_measure": {
            "name": "in-state mean next-bar return minus all-bars mean (% per day)",
            "value": None if diff is None else float(diff * 100.0),
            "statistic": None if t_stat is None else {"name": "stretch-clustered t", "value": float(t_stat)},
            "threshold": "at least 0.10% per day below the all-bars mean with stretch-clustered t <= -2",
        },
        "supporting_check": {
            "name": "down-bar share in stretches minus over all bars; equity above flat and beats holding in-state",
            "value": None if down_diff is None else float(down_diff),
            "passed": supp_passed,
        },
        "counts": {
            "distinct down-cross stretches": int(n_stretches),
            "in-state bars": n_in,
        },
        "decided_by": decided,
        "reading": ("In-state bars are bars with forecast < 0 that have a next close in the same window, a stretch is "
                    "each run of consecutive such bars within one window, the t uses a cluster-robust (by stretch, "
                    "G/(G-1) corrected) standard error of the in-state mean taking the all-bars mean as the reference, "
                    "and the confirm rule uses only the down-bar share comparison while 'passed' also requires the "
                    "pre-cost equity (compounded over all bars) to end above 1 and to beat holding over in-state bars."),
    }
