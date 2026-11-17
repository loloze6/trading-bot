def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = pd.Series(b["close"].values); n = len(b)
            r1 = cl.pct_change(); vol = r1.rolling(30).std()
            hi30 = pd.Series(b["high"].values).rolling(30).max()
            near = cl / hi30 - 1
            v = pd.Series(b["volume"].values)
            volr = np.log(v / v.rolling(30).mean())
            vol7 = np.log(v.rolling(7).mean() / v.rolling(30).mean())
            r30 = cl.pct_change(30)
            for i in range(0, n - 7, 7):
                rows.append(dict(coin=c, w=w, wi=int(w[1:]), f=b["forecast"].iloc[i], reg=b["regime"].iloc[i],
                                 z=r1.iloc[i] / vol.iloc[i], near=near.iloc[i], nearv=near.iloc[i] / vol.iloc[i],
                                 volr=volr.iloc[i], vol7=vol7.iloc[i], r30=r30.iloc[i],
                                 wd=pd.Timestamp(b["timestamp"].iloc[i]).dayofweek,
                                 fwd=cl.iloc[i + 7] / cl.iloc[i] - 1))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g["half"] = np.where(g["wi"] <= 12, "early", "late")
    out = {}
    def slope(d, x):
        d = d.dropna(subset=[x, "ex"])
        d = d[np.isfinite(d[x])]
        if len(d) < 20: return (np.nan, np.nan, len(d))
        r = stats.linregress(d[x], d["ex"])
        return (r.slope, r.slope / r.stderr, len(d))
    res = {}
    for x in ["near", "nearv", "volr", "vol7", "r30", "z"]:
        for lab, sub in [("all", g), ("trend", g[g.reg == "trending"]), ("nontrend", g[g.reg != "trending"]),
                         ("early", g[g.half == "early"]), ("late", g[g.half == "late"])]:
            s, t, nn = slope(sub, x); res[(x, lab)] = dict(slope=s, t=t, n=nn)
    out["slopes"] = pd.DataFrame(res).T
    cres = {}
    for x in ["near", "volr", "vol7"]:
        for c, sub in g.groupby("coin"):
            s, t, nn = slope(sub, x); cres[(x, c)] = dict(slope=s, t=t, n=nn)
    out["slopes_by_coin"] = pd.DataFrame(cres).T
    # near x volume interaction: within top near tercile, does low/high volume matter
    d = g.dropna(subset=["near", "vol7"]).copy()
    d["nb"] = d.groupby("coin")["near"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    d["vb"] = d.groupby("coin")["vol7"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["near_x_vol7"] = d.groupby(["nb", "vb"])["ex"].mean().unstack()
    out["near_x_vol7_n"] = d.groupby(["nb", "vb"])["ex"].count().unstack()
    # Friday robustness by half
    out["wd_by_half"] = g.groupby(["wd", "half"])["ex"].mean().unstack()
    # book: position gain decomposition per side, daily bars
    sl = []
    for c in bars:
        for w, b in bars[c].items():
            a = b["postRebalance_current_allocation"].values
            r = b["close"].shift(-1).values / b["close"].values - 1
            sl.append(pd.DataFrame(dict(a=a, r=r, coin=c, f=b["forecast"].values)))
    s = pd.concat(sl).dropna()
    mu = s.groupby("coin")["r"].transform("mean")
    s["drift"] = s["a"] * mu; s["timing"] = s["a"] * (s["r"] - mu)
    s["side"] = np.sign(s["a"])
    out["side_drift_timing"] = s.groupby("side")[["drift", "timing"]].sum()
    s["fb"] = pd.cut(s["f"], [-20.1, -10, -5, -1e-9, 1e-9, 5, 10, 20.1])
    out["next1d_ret_by_fc"] = s.groupby("fb")["r"].agg(["mean", "count"])
    return out
