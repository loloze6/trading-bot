def explore(data):
    import numpy as np, pandas as pd
    out = {}
    b = data["bars"]["BTCUSD"]["w1"]
    f = b["forecast"].astype(float)
    raw = b["debug_info.components.rsi_high.last_history_value"].astype(float)
    rsi = 50 - raw
    fwd = b["close"].shift(-5) / b["close"] - 1
    grid = np.arange(len(b)) % 5 == 0
    out["blocks_possible"] = pd.Series({"bars": len(b), "grid_bars_with_fwd": int((grid & fwd.notna()).sum()),
        "max_cases_any_threshold": int((grid & fwd.notna()).sum())})
    bins = pd.cut(f, [-20.01, -10, -2, -1e-9, 1e-9])
    out["rsi_by_forecast_bin"] = rsi.groupby(bins, observed=False).agg(["count", "min", "mean", "max"])
    ext = f <= -10
    runid = (ext != ext.shift()).cumsum()
    runs = ext.groupby(runid).agg(["first", "size"])
    out["extreme_run_lengths"] = runs[runs["first"]]["size"].describe()
    out["rsi_thresholds_count"] = pd.Series({f"RSI>={t}": int((rsi >= t).sum()) for t in [55, 60, 65, 70]})
    # all bars any shift
    sel = fwd[ext].dropna(); m = fwd.mean()
    out["excess_all_extreme_bars_overlapping"] = pd.Series({"n": len(sel), "mean_excess": (sel - m).mean(),
        "sd": (sel - m).std()})
    # by grid offset
    rows = []
    for off in range(5):
        g = (np.arange(len(b)) % 5 == off) & ext & fwd.notna()
        rows.append({"offset": off, "n": int(g.sum()), "excess_mean": (fwd[g] - m).mean()})
    out["by_grid_offset"] = pd.DataFrame(rows)
    out["fwd1_sd"] = float((b["close"].pct_change()).std())
    return out
