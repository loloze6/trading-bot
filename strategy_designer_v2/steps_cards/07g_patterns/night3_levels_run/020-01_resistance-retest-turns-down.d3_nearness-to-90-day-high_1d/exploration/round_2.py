def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    D = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol20 = r1.rolling(20, min_periods=10).std()
            ts = pd.to_datetime(b["timestamp"])
            rawp = b["debug_info.components.high_prox.last_history_value"]
            d = pd.DataFrame({"coin": coin, "win": w, "r1": r1, "vol20": vol20,
                              "fwd1": c.shift(-1)/c-1, "fwd2": c.shift(-2)/c-1, "fwd5": c.shift(-5)/c-1,
                              "wd": ts.dt.weekday, "year": ts.dt.year, "ts": ts, "rawp": rawp,
                              "pos": b["postRebalance_current_allocation"], "i": np.arange(len(b))})
            D.append(d)
    D = pd.concat(D)
    for h in ["fwd1", "fwd2", "fwd5"]:
        D["ex" + h[3:]] = D[h] - D.groupby("coin")[h].transform("mean")
    D["z"] = D["r1"] / D["vol20"]
    out = {}
    y = D.dropna(subset=["z", "ex1"])
    # per coin: slope of next-day excess on z, down days only
    def sl(s, col="ex1"):
        s = s.dropna(subset=[col])
        r = stats.linregress(s["z"], s[col])
        return pd.Series({"slope": r.slope, "t": r.slope/r.stderr, "n": len(s), "mean": s[col].mean()})
    dn = y[y["z"] < 0]
    out["down_slope_by_coin"] = dn.groupby("coin").apply(sl).round(5)
    out["down_slope_by_year"] = dn.groupby("year").apply(sl).round(5)
    out["up_slope_by_coin"] = y[y["z"] > 0].groupby("coin").apply(sl).round(5)
    # date-clustered: average across coins per date
    dd = dn.copy(); dd["zb"] = pd.cut(dd["z"], [-99, -2, -1.5, -1, -0.5, 0])
    a = dd.groupby("zb")[["ex1", "ex2"]].mean()
    a["n"] = dd.groupby("zb").size()
    # cluster t by date
    def ct(s, col):
        m = s.groupby("ts")[col].mean()
        return m.mean() / (m.std() / np.sqrt(len(m)))
    a["t1_dateclust"] = [ct(dd[dd["zb"] == k], "ex1") for k in a.index]
    a["t2_dateclust"] = [ct(dd[dd["zb"] == k].dropna(subset=["ex2"]), "ex2") for k in a.index]
    out["down_buckets"] = a.round(5)
    # non-overlapping 2-day grid version
    g2 = D[D["i"] % 2 == 0].dropna(subset=["z", "ex2"])
    g2 = g2[g2["z"] < 0]
    out["down_slope_2d_grid"] = sl(g2, "ex2").round(5)
    # weekday per year (date-clustered mean of ex1)
    W = y.groupby(["ts"]).agg(ex1=("ex1", "mean"), wd=("wd", "first"), year=("year", "first"))
    out["thu_fri_minus_other_by_year"] = W.groupby("year").apply(
        lambda s: s[s["wd"].isin([3, 4])]["ex1"].mean() - s[~s["wd"].isin([3, 4])]["ex1"].mean()).round(5)
    a = W.groupby("wd")["ex1"].agg(["mean", "std", "count"]); a["t"] = a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["weekday_dateclust"] = a.round(5)
    # raw proximity top region: fine deciles on 5-day grid
    G = D[D["i"] % 5 == 0].dropna(subset=["rawp", "ex5"]).copy()
    G["dq"] = G.groupby("coin")["rawp"].transform(lambda s: pd.qcut(s.rank(method="first"), 10, labels=False))
    a = G.groupby("dq")["ex5"].agg(["mean", "std", "count"]); a["t"] = a["mean"]/(a["std"]/np.sqrt(a["count"]))
    a["rawp_med"] = G.groupby("dq")["rawp"].median()
    out["rawp_deciles"] = a.round(4)
    out["top_decile_by_coin"] = G[G["dq"] == 9].groupby("coin")["ex5"].agg(["mean", "count"]).round(4)
    # book position after down days
    out["pos_after_down_z"] = dd.groupby("zb")["pos"].mean().round(3)
    return out
