def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    rows = []
    for c in bars:
        for w in bars[c]:
            b = bars[c][w].copy()
            b["ts"] = pd.to_datetime(b["timestamp"], utc=True)
            b["hour"] = b["ts"].dt.hour
            b["coin"] = c; b["w"] = w
            b["r72"] = b["close"] / b["close"].shift(72) - 1
            for h in [2, 8, 24, 72]:
                b[f"f{h}"] = b["close"].shift(-h) / b["close"] - 1
            b["pos_idx"] = np.arange(len(b))
            rows.append(b[["coin","w","hour","r72","forecast","pos_idx","f2","f8","f24","f72"]])
    B = pd.concat(rows, ignore_index=True)
    # coin mean returns per horizon on non-overlapping grid
    means = {}
    for h in [2, 8, 24, 72]:
        g = B[B["pos_idx"] % h == 0]
        means[h] = g.groupby("coin")[f"f{h}"].mean()
    # entry bars
    E = B[B["hour"].isin([23, 7, 15]) & (B["r72"] > 0)].copy()
    for h in [2, 8, 24, 72]:
        E[f"x{h}"] = E[f"f{h}"] - E["coin"].map(means[h])
    E["q"] = E.groupby("coin")["r72"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    tab = E.groupby("q")[["x2","x8","x24"]].mean() * 1e4
    tab["n"] = E.groupby("q").size()
    tab["t2"] = E.groupby("q")["x2"].apply(lambda s: s.mean() / (s.std() / np.sqrt(s.notna().sum())))
    out["entry_excess_bp_by_r72_quintile"] = tab
    out["entry_excess_bp_by_hour"] = E.groupby("hour")[["x2","x8"]].mean() * 1e4
    # 2-bar post-settle excess by hour within day, uptrend only, all hours (on grid of each hour)
    U = B[B["r72"] > 0].copy()
    U["x2"] = U["f2"] - U["coin"].map(means[2])
    out["x2_bp_any_hour_uptrend"] = (U.groupby("hour")["x2"].mean() * 1e4).round(2)
    # longer horizon: 24h and 72h excess grid sampled once a day at 00:00 by r72 quintile, all coins
    D0 = B[(B["hour"] == 0)].copy()
    D0["x24"] = D0["f24"] - D0["coin"].map(means[24])
    D0 = D0.dropna(subset=["r72", "x24"])
    D0["q"] = D0.groupby("coin")["r72"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    t = D0.groupby("q")["x24"].agg(["mean", "count", "std"])
    t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    t["mean"] *= 1e4
    out["daily_x24_bp_by_r72_quintile_all"] = t[["mean","count","t"]]
    out["by_window_x2_bp"] = (E.groupby("w")["x2"].mean() * 1e4).describe()
    return out
