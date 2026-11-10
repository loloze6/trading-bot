import numpy as np
import pandas as pd


def measure(bars):
    H = 1
    MIN_DIFF = -0.001
    T_MAX = -2.0
    MIN_STRETCHES = 3
    MIN_BARS = 60

    all_r = []
    in_r = []
    in_cluster = []
    strat_all = []
    strat_in = []
    hold_in = []
    cluster_id = 0

    for coin, windows in bars.items():
        for w, df in windows.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            if "postRebalance_current_allocation" in d.columns:
                alloc = pd.to_numeric(d["postRebalance_current_allocation"],
                                      errors="coerce").to_numpy(dtype=float)
            else:
                alloc = np.full(len(d), np.nan)
            n = len(d)
            r = np.full(n, np.nan)
            if n > H:
                r[:-H] = close[H:] / close[:-H] - 1.0

            # stretches: contiguous runs of forecast < 0 inside this window
            prev_in = False
            for t in range(n):
                is_in = (not np.isnan(fc[t])) and fc[t] < 0
                if is_in and not prev_in:
                    cluster_id += 1
                prev_in = is_in
                if np.isnan(r[t]) or not np.isfinite(r[t]):
                    continue
                all_r.append(r[t])
                if not np.isnan(alloc[t]):
                    strat_all.append(alloc[t] * r[t])
                if is_in:
                    in_r.append(r[t])
                    in_cluster.append(cluster_id)
                    if not np.isnan(alloc[t]):
                        strat_in.append(alloc[t] * r[t])
                        hold_in.append(r[t])

    all_r = np.asarray(all_r, dtype=float)
    in_r = np.asarray(in_r, dtype=float)
    in_cluster = np.asarray(in_cluster)

    n_in = len(in_r)
    n_stretches = int(len(np.unique(in_cluster))) if n_in > 0 else 0

    main_name = "pooled mean next-bar return on forecast<0 bars minus all-bars mean"
    main_thr = "at most -0.10% per day with stretch-clustered t <= -2; reject if >= 0"

    diff = None
    t_stat = None
    if n_in > 0 and len(all_r) > 0:
        mean_all = float(np.mean(all_r))
        mean_in = float(np.mean(in_r))
        diff = mean_in - mean_all
        # stretch-clustered standard error of the in-state mean (all-bars mean taken as the benchmark)
        G = n_stretches
        if G >= 2:
            resid = in_r - mean_in
            sums = pd.Series(resid).groupby(in_cluster).sum().to_numpy()
            var = (G / (G - 1.0)) * np.sum(sums ** 2) / (n_in ** 2)
            se = float(np.sqrt(var))
            if se > 0:
                t_stat = diff / se

    # supporting check
    down_in = float(np.mean(in_r < 0)) if n_in > 0 else None
    down_all = float(np.mean(all_r < 0)) if len(all_r) > 0 else None
    down_higher = None
    down_diff = None
    if down_in is not None and down_all is not None:
        down_diff = down_in - down_all
        down_higher = bool(down_in > down_all)

    eq_end = float(np.prod(1.0 + np.asarray(strat_all))) if len(strat_all) else None
    eq_above_flat = None if eq_end is None else bool(eq_end > 1.0)
    strat_in_end = float(np.prod(1.0 + np.asarray(strat_in))) if len(strat_in) else None
    hold_in_end = float(np.prod(1.0 + np.asarray(hold_in))) if len(hold_in) else None
    beats_hold = None
    if strat_in_end is not None and hold_in_end is not None:
        beats_hold = bool(strat_in_end > hold_in_end)

    parts = [down_higher, eq_above_flat, beats_hold]
    if any(p is None for p in parts):
        sup_passed = None
    else:
        sup_passed = bool(all(parts))

    supporting = {
        "name": "down-bar share in-state minus all bars (also: equity ends above flat, beats holding in-state)",
        "value": down_diff,
        "passed": sup_passed,
        "details": {
            "down_share_in_state": down_in,
            "down_share_all": down_all,
            "equity_end_multiple_all_bars": eq_end,
            "strategy_in_state_multiple": strat_in_end,
            "hold_in_state_multiple": hold_in_end,
        },
    }

    if n_stretches < MIN_STRETCHES or n_in < MIN_BARS or diff is None:
        status = "inconclusive"
        decided_by = ("Inconclusive: fewer than 3 distinct down-cross stretches or fewer than 60 "
                      "in-state bars pooled across the windows.")
    elif diff >= 0:
        status = "rejected"
        decided_by = "Reject: in-state mean return is at or above the all-bars mean."
    elif (diff <= MIN_DIFF and t_stat is not None and t_stat <= T_MAX
          and down_higher is True):
        status = "confirmed"
        decided_by = ("Confirm: in-state mean is at least 0.10% per day below the all-bars mean with "
                      "stretch-clustered t <= -2, and the down-bar share is higher inside the stretches.")
    else:
        status = "inconclusive"
        decided_by = ("Inconclusive: the difference is negative but t > -2, or it is smaller than "
                      "0.10% per day, or the down-bar share is not higher inside the stretches.")

    return {
        "status": status,
        "main_measure": {
            "name": main_name,
            "value": None if diff is None else float(diff),
            "threshold": main_thr,
            "t_stat_clustered": None if t_stat is None else float(t_stat),
        },
        "supporting_check": supporting,
        "cases": int(n_in),
        "stretches": int(n_stretches),
        "decided_by": decided_by,
        "reading": ("In-state bars are bars with forecast < 0 and stretches are their contiguous runs "
                    "within one window (a run cut by a window edge counts once per window); the "
                    "clustered SE treats the all-bars mean as fixed with a G/(G-1) correction; the "
                    "confirm rule uses only the down-bar share from the supporting check, while the "
                    "equity checks (pooled compounded before-cost gains) are reported in 'passed'."),
    }
