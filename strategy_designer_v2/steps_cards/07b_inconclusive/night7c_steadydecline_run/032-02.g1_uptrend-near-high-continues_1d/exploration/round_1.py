def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            r28 = pd.Series(c).pct_change(28).values
            hi28 = pd.Series(c).rolling(28, min_periods=28).max().values
            for h in (1, 3, 5, 10, 20):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i,
                                     year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                     fc=b["forecast"].iloc[i], reg=b["regime"].iloc[i],
                                     r28=r28[i], dist=(hi28[i]/c[i]-1) if not np.isnan(hi28[i]) else np.nan,
                                     ret=c[i+h]/c[i]-1))
    df = pd.DataFrame(rows)
    df["ex"] = df["ret"] - df.groupby(["coin","h"])["ret"].transform("mean")
    tr = df[(df.reg == "trending")]
    def slope_t(g, x="fc"):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 20 or g[x].std() == 0: return pd.Series({"n": len(g), "t": np.nan})
        res = stats.linregress(g[x], g["ex"])
        return pd.Series({"n": len(g), "slope": res.slope, "t": res.slope/res.stderr})
    out = {}
    out["by_horizon_fc"] = tr.groupby("h").apply(slope_t)
    out["by_horizon_dist"] = tr.groupby("h").apply(lambda g: slope_t(g, "dist"))
    t5 = tr[tr.h == 5]
    out["h5_by_coin"] = t5.groupby("coin").apply(slope_t)
    out["h5_by_year"] = t5.groupby("year").apply(slope_t)
    out["h5_by_window"] = t5.groupby("w").apply(slope_t)
    t5 = t5.copy()
    t5["fq"] = pd.qcut(t5["fc"].rank(method="first"), 5, labels=False)
    out["h5_fc_quintile_mean_ex"] = t5.groupby("fq")["ex"].agg(["count","mean"])
    t5["dq"] = pd.qcut(t5["dist"].rank(method="first"), 5, labels=False)
    out["h5_dist_quintile_mean_ex"] = t5.groupby("dq").agg(n=("ex","count"), mean=("ex","mean"), dist=("dist","mean"))
    t5["rq"] = pd.qcut(t5["r28"].rank(method="first"), 3, labels=False)
    out["h5_by_r28_tercile"] = t5.groupby("rq").apply(slope_t)
    a5 = df[df.h == 5].dropna(subset=["dist","r28"]).copy()
    a5["up"] = a5.r28 > 0
    out["h5_all_dist_by_updown"] = a5.groupby("up").apply(lambda g: slope_t(g, "dist"))
    return out
