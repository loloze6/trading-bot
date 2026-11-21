def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        # coin drift over all windows (non-overlapping 5-bar grid)
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - H, H):
                allr.append(c[i + H] / c[i] - 1)
        drift = np.mean(allr); usual = np.std(allr)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            lr = np.log(c)
            vol20 = pd.Series(r1).rolling(20, min_periods=10).std().values
            ret5past = np.r_[[np.nan] * 5, c[5:] / c[:-5] - 1]
            ts = pd.to_datetime(b["timestamp"])
            nh = b.get("debug_info.components.near_high.post_pipeline_value")
            rt = b.get("debug_info.components.ret20.post_pipeline_value")
            alloc = b["postRebalance_current_allocation"].values
            for i in range(0, len(c) - H, H):
                fr = c[i + H] / c[i] - 1
                rows.append(dict(coin=coin, w=w, f=b["forecast"].iloc[i],
                                 nh=nh.iloc[i] if nh is not None else np.nan,
                                 rt=rt.iloc[i] if rt is not None else np.nan,
                                 r1=r1[i], r1z=r1[i] / vol20[i] if vol20[i] > 0 else np.nan,
                                 r5=ret5past[i], vol=vol20[i], wd=ts.iloc[i].dayofweek,
                                 yr=ts.iloc[i].year, alloc=alloc[i],
                                 ex=(fr - drift), exu=(fr - drift) / usual))
    df = pd.DataFrame(rows)
    out = {}
    def tq(g):
        x = g["ex"].dropna()
        return pd.Series({"n": len(x), "mean_ex_%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    for col in ["f", "nh", "rt", "r1z", "r5", "vol"]:
        d = df.dropna(subset=[col, "ex"]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        out["quint_" + col] = d.groupby("q").apply(tq)
    # slopes of components jointly, per coin
    res = []
    for coin, g in df.dropna(subset=["nh", "rt", "r1z", "ex"]).groupby("coin"):
        for col in ["nh", "rt", "r1z"]:
            s = stats.linregress(g[col], g["ex"])
            res.append(dict(coin=coin, var=col, slope=s.slope, t=s.slope / s.stderr, n=len(g)))
    out["slopes_per_coin"] = pd.DataFrame(res)
    out["by_weekday"] = df.groupby("wd").apply(tq)
    out["by_year"] = df.groupby("yr").apply(tq)
    # near-high conditional on vol regime
    d = df.dropna(subset=["nh", "vol", "ex"]).copy()
    d["volhi"] = d.groupby("coin")["vol"].transform(lambda s: s > s.median())
    d["nhq"] = d.groupby("coin")["nh"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["nh_tercile_by_vol"] = d.groupby(["volhi", "nhq"]).apply(tq)
    # side performance
    df["side"] = np.sign(df["alloc"])
    out["by_side"] = df.groupby("side").apply(tq)
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    T = pd.concat(tr)
    out["trades_by_side"] = T.groupby("side").agg(n=("net_profit_loss_percent", "size"),
        mean_net=("net_profit_loss_percent", "mean"), mean_gross=("profit_loss_percent", "mean"),
        win=("net_profit_loss_percent", lambda s: (s > 0).mean()),
        days=("duration_minutes", lambda s: s.mean() / 1440))
    return out
