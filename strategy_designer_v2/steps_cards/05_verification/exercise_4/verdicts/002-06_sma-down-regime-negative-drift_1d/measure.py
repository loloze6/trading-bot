import numpy as np
import pandas as pd


def measure(bars):
    coin = "BTCUSD" if "BTCUSD" in bars else (list(bars.keys())[0] if len(bars) else None)
    windows = bars.get(coin, {}) if coin is not None else {}

    all_rets = []
    in_rets = []
    in_cluster = []
    n_windows = 0
    stretch_id = 0

    for w in sorted(windows.keys()):
        df = windows[w]
        if df is None or len(df) == 0:
            continue
        n_windows += 1
        close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
        fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
        n = len(close)
        r = np.full(n, np.nan)
        if n > 1:
            r[:-1] = close[1:] / close[:-1] - 1.0
        in_state = np.where(np.isnan(fc), False, fc < 0)

        # contiguous runs of forecast < 0 within this window = stretches
        prev = False
        cur_id = None
        for i in range(n):
            if in_state[i]:
                if not prev:
                    stretch_id += 1
                    cur_id = stretch_id
                if np.isfinite(r[i]):
                    in_rets.append(r[i])
                    in_cluster.append(cur_id)
            if np.isfinite(r[i]):
                all_rets.append(r[i])
            prev = bool(in_state[i])

    all_rets = np.asarray(all_rets, dtype=float)
    in_rets = np.asarray(in_rets, dtype=float)
    in_cluster = np.asarray(in_cluster, dtype=int)

    n_in = int(len(in_rets))
    n_all = int(len(all_rets))
    clusters = np.unique(in_cluster) if n_in > 0 else np.array([], dtype=int)
    n_stretches = int(len(clusters))

    diff = None
    t_stat = None
    down_in = None
    down_all = None
    down_diff = None
    down_pass = None

    if n_in > 0 and n_all > 0:
        mean_in = float(np.mean(in_rets))
        mean_all = float(np.mean(all_rets))
        diff = mean_in - mean_all
        # stretch-clustered standard error of the pooled in-state mean
        if n_stretches >= 2:
            resid = in_rets - mean_in
            sums = np.array([resid[in_cluster == c].sum() for c in clusters])
            var = (n_stretches / (n_stretches - 1.0)) * np.sum(sums ** 2) / (n_in ** 2)
            se = float(np.sqrt(var))
            if se > 0 and np.isfinite(se):
                t_stat = float(diff / se)
        down_in = float(np.mean(in_rets < 0))
        down_all = float(np.mean(all_rets < 0))
        down_diff = down_in - down_all
        down_pass = bool(down_in > down_all)

    enough = (n_stretches >= 3) and (n_in >= 60)

    if not enough or diff is None:
        status = "inconclusive"
        decided_by = ("Inconclusive: fewer than 3 distinct down-cross stretches or fewer than 60 "
                      "in-state bars pooled across the windows.")
    elif diff >= 0:
        status = "rejected"
        decided_by = "Reject: the in-state mean return is at or above the all-bars mean."
    elif diff <= -0.001 and t_stat is not None and t_stat <= -2 and down_pass:
        status = "confirmed"
        decided_by = ("Confirm: in-state mean is at least 0.10% per day below the all-bars mean with "
                      "stretch-clustered t <= -2, and the down-bar share inside stretches is higher than over all bars.")
    else:
        status = "inconclusive"
        decided_by = ("Inconclusive: the difference is negative but t > -2, or smaller than 0.10% per day, "
                      "or the down-bar share inside stretches is not higher than over all bars.")

    return {
        "status": status,
        "main_measure": {
            "name": "in-state mean next-bar return minus all-bars mean",
            "value": None if diff is None else float(diff),
            "statistic": None if t_stat is None else {"name": "stretch-clustered t", "value": float(t_stat)},
            "threshold": "difference <= -0.10% per day with stretch-clustered t <= -2",
        },
        "supporting_check": {
            "name": "down-bar share in stretches minus down-bar share over all bars",
            "value": None if down_diff is None else float(down_diff),
            "passed": down_pass,
        },
        "counts": {
            "distinct down-cross stretches": n_stretches,
            "in-state bars pooled": n_in,
            "all bars pooled": n_all,
            "windows": n_windows,
        },
        "decided_by": decided_by,
        "reading": ("Stretches are contiguous runs of forecast < 0 inside one window (a run cut by a window edge counts "
                    "as its own stretch), the t is the pooled difference over a cluster-robust standard error of the in-state "
                    "mean with stretches as clusters (K/(K-1) correction, all-bars mean treated as fixed), a down bar is a "
                    "negative next-bar return, and the supporting check's pass is the down-share comparison the confirm rule "
                    "names (the equity-curve part is not used in the decision)."),
    }
