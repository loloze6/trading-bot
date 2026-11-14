import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    POS = "postRebalance_current_allocation"

    in_rets, all_rets, cluster_ids = [], [], []
    strat_gains, hold_in = [], []
    n_stretches = 0
    cid = 0

    for coin in bars:
        for window in bars[coin]:
            df = bars[coin][window]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            ret = close.shift(-1) / close - 1.0
            fc = df[FC].astype(float)

            # all bars of the window with a valid next-bar return
            valid_all = ret.notna()
            all_rets.extend(ret[valid_all].tolist())

            # strategy gain before costs, over all bars
            if POS in df.columns:
                pos = df[POS].astype(float)
                g = pos * ret
                strat_gains.extend(g[g.notna()].tolist())

            # stretches: contiguous runs of forecast < 0 inside this window
            prev_in = False
            cur_cluster = None
            for i in range(len(df)):
                f = fc.iloc[i]
                is_in = (not pd.isna(f)) and f < 0
                if is_in and not prev_in:
                    cid += 1
                    n_stretches += 1
                    cur_cluster = cid
                if is_in and not pd.isna(ret.iloc[i]):
                    in_rets.append(float(ret.iloc[i]))
                    cluster_ids.append(cur_cluster)
                    hold_in.append(float(ret.iloc[i]))
                prev_in = is_in

    in_rets = np.asarray(in_rets, dtype=float)
    all_rets = np.asarray(all_rets, dtype=float)
    cluster_ids = np.asarray(cluster_ids)
    n_in = int(len(in_rets))
    n_clusters_used = int(len(np.unique(cluster_ids))) if n_in else 0

    diff = None
    t_stat = None
    down_in = down_all = down_diff = None
    passed = None

    if n_in > 0 and len(all_rets) > 0:
        mean_in = float(in_rets.mean())
        mean_all = float(all_rets.mean())
        diff = mean_in - mean_all

        # stretch-clustered SE of the in-state mean (CR1 small-sample factor G/(G-1))
        G = n_clusters_used
        if G >= 2:
            resid = in_rets - mean_in
            sums = pd.Series(resid).groupby(cluster_ids).sum().values
            var = (G / (G - 1)) * np.sum(sums ** 2) / (n_in ** 2)
            se = float(np.sqrt(var))
            if se > 0:
                t_stat = diff / se

        down_in = float(np.mean(in_rets < 0))
        down_all = float(np.mean(all_rets < 0))
        down_diff = down_in - down_all
        passed = bool(down_in > down_all)

    # informational equity checks
    strat_end = float(np.prod(1.0 + np.asarray(strat_gains))) if strat_gains else None
    hold_end = float(np.prod(1.0 + np.asarray(hold_in))) if hold_in else None

    counts = {
        "distinct down-cross stretches": int(n_stretches),
        "in-state bars pooled": n_in,
    }

    if n_stretches < 3 or n_in < 60 or diff is None:
        status = "inconclusive"
        decided = ("Inconclusive: fewer than 3 distinct down-cross stretches or fewer than 60 "
                   "in-state bars pooled across the windows.")
    elif diff >= 0:
        status = "rejected"
        decided = "Reject: in-state mean next-bar return is at or above the all-bars mean."
    elif diff <= -0.001 and t_stat is not None and t_stat <= -2 and passed:
        status = "confirmed"
        decided = ("Confirm: in-state mean is at least 0.10% per day below the all-bars mean with "
                   "stretch-clustered t <= -2, and the down-bar share in stretches exceeds the all-bars share.")
    else:
        status = "inconclusive"
        decided = ("Inconclusive: the difference is negative but t > -2, or smaller than 0.10% per day, "
                   "or the down-bar share in stretches is not higher than over all bars.")
    decided += (f" (Info: strategy equity end {strat_end}, holding over in-state bars end {hold_end}.)")

    return {
        "status": status,
        "main_measure": {
            "name": "in-state mean next-bar return minus all-bars mean",
            "value": None if diff is None else float(diff),
            "statistic": None if t_stat is None else {"name": "stretch-clustered t", "value": float(t_stat)},
            "threshold": "difference <= -0.10% per day (-0.001) with stretch-clustered t <= -2",
        },
        "supporting_check": {
            "name": "down-bar share in stretches minus share over all bars",
            "value": None if down_diff is None else float(down_diff),
            "passed": passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("In-state bars are bars with forecast < 0 and a next-bar return in the same window, "
                    "stretches are contiguous runs of such bars per window (a run open at a window edge counts "
                    "as a stretch), t is the difference divided by the cluster-robust (CR1) SE of the in-state "
                    "mean over stretches treating the all-bars mean as fixed, and only the down-share comparison "
                    "enters the confirm rule while the equity checks are reported for information."),
    }
