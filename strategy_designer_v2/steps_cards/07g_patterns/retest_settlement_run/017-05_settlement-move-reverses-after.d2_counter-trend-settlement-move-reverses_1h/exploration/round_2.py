def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b[["timestamp","close","volume"]].copy().reset_index(drop=True)
            b["timestamp"] = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"]
            b["pos"] = np.arange(len(b))
            b["r24f"] = c.shift(-24)/c - 1
            b["r8f"] = c.shift(-8)/c - 1
            b["r24p"] = c/c.shift(24) - 1
            b["r2p"] = c/c.shift(2) - 1
            lr = np.log(c).diff()
            b["vol24"] = lr.rolling(24).std()
            b["vol720"] = lr.rolling(720).std()
            b["vratio"] = b["vol24"]/b["vol720"]
            b["year"] = b["timestamp"].dt.year
            b["coin"] = coin; b["win"] = w
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    def tt(x):
        x = x.dropna(); n=len(x)
        return pd.Series({"mean_bp": x.mean()*1e4, "t": x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan, "n": n})
    G = B[B["pos"] % 24 == 0].copy()
    drift = B[B["pos"] % 24 == 0].groupby("coin")["r24f"].mean()
    G["r24x"] = G["r24f"] - G["coin"].map(drift)
    d = G.dropna(subset=["r24p","r24x","vol24","vol720"]).copy()
    d["rev"] = -np.sign(d["r24p"])*d["r24x"]
    d["revtot"] = -np.sign(d["r24p"])*d["r24f"]
    d["absz"] = d["r24p"].abs()/(d["vol24"]*np.sqrt(24))
    d["absr"] = d["r24p"].abs()
    d["vq"] = pd.qcut(d["vratio"].rank(method="first"),5,labels=False)
    d["rq"] = d.groupby("coin")["absr"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["24h reversal by |24h return| quintile (per coin)"] = d.groupby("rq")["rev"].apply(tt).unstack()
    out["24h reversal total move by |24h return| quintile"] = d.groupby("rq")["revtot"].apply(tt).unstack()
    out["24h reversal by vol24/vol720 quintile"] = d.groupby("vq")["rev"].apply(tt).unstack()
    out["24h reversal, top |r24| quintile, by coin"] = d[d["rq"]==4].groupby("coin")["rev"].apply(tt).unstack()
    out["24h reversal, top |r24| quintile, by year"] = d[d["rq"]==4].groupby("year")["rev"].apply(tt).unstack()
    out["24h reversal, top |r24| quintile, by side of past move"] = d[d["rq"]==4].groupby(np.sign(d["r24p"]))["rev"].apply(tt).unstack()
    wm = d[d["rq"]==4].groupby("win")["rev"].mean()
    out["top quintile: share of windows with positive reversal"] = float((wm>0).mean())
    # graded slope of signed rev on |r24| in units of coin's usual 24h move
    usual = G.groupby("coin")["r24f"].std()
    d["absu"] = d["absr"]/d["coin"].map(usual)
    sl = stats.linregress(d["absu"], d["rev"])
    out["slope rev on |r24|/usual (bp per usual move)"] = pd.Series({"slope_bp": sl.slope*1e4, "t": sl.slope/sl.stderr, "n": len(d)})
    d["strength"] = d["rev"]/d["coin"].map(usual)
    out["strength by |r24| quintile"] = d.groupby("rq")["strength"].mean().to_frame("strength")
    # 8h reversal of 2h move by size quintile, on 8h grid
    G8 = B[B["pos"] % 8 == 0].copy()
    dr8 = G8.groupby("coin")["r8f"].mean()
    G8["r8x"] = G8["r8f"] - G8["coin"].map(dr8)
    e = G8.dropna(subset=["r2p","r8x"]).copy()
    e["rev"] = -np.sign(e["r2p"])*e["r8x"]
    e["q"] = e.groupby("coin")["r2p"].transform(lambda s: pd.qcut(s.abs().rank(method="first"),5,labels=False))
    out["8h reversal of 2h move by |2h| quintile"] = e.groupby("q")["rev"].apply(tt).unstack()
    out["8h reversal top |2h| quintile by year"] = e[e["q"]==4].groupby("year")["rev"].apply(tt).unstack()
    return out
