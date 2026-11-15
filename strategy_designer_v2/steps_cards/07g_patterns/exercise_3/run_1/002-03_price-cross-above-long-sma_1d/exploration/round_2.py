def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            d = df.reset_index(drop=True).copy()
            c = d["close"].values; n = len(d)
            d["coin"] = coin; d["win"] = w; d["pos"] = np.arange(n)
            f1 = np.full(n, np.nan); f1[:n-1] = c[1:]/c[:-1]-1
            f5 = np.full(n, np.nan)
            if n > 5: f5[:n-5] = c[5:]/c[:-5]-1
            r1 = np.full(n, np.nan); r1[1:] = c[1:]/c[:-1]-1
            d["f1"]=f1; d["f5"]=f5; d["r1"]=r1
            d["vol20"] = pd.Series(r1).rolling(20).std().values
            d["z1"] = d["r1"]/d["vol20"]
            d["r20past"] = pd.Series(c).pct_change(20).values
            ts = pd.to_datetime(d["timestamp"])
            d["wd"] = ts.dt.dayofweek; d["year"] = ts.dt.year
            d["alloc"] = d["postRebalance_current_allocation"]
            rows.append(d[["coin","win","pos","f1","f5","r1","z1","vol20","r20past","wd","year","alloc"]])
    B = pd.concat(rows, ignore_index=True)
    mu = B.groupby("coin")["f1"].mean(); B["mu"]=B["coin"].map(mu)
    B["x1"]=B["f1"]-B["mu"]; B["x5"]=B["f5"]-5*B["mu"]
    b1 = B.dropna(subset=["x1"])
    # weekday per coin t
    def tt(s): return s.mean()/(s.std()/np.sqrt(len(s)))
    out["weekday t per coin"] = b1.groupby(["coin","wd"])["x1"].apply(tt).unstack().round(2)
    out["weekday t per year"] = b1.groupby(["year","wd"])["x1"].apply(tt).unstack().round(2)
    # cross-sectional averaged per day (removes cross-coin correlation): mean across coins per (win,pos)? use timestamp-independent: group by year+pos is not day; use weekday of each day averaged
    # Fri minus rest, Wed minus rest per coin Welch
    r = []
    for coin, g in b1.groupby("coin"):
        r.append([coin, stats.ttest_ind(g[g.wd==4].x1, g[g.wd!=4].x1, equal_var=False).statistic,
                  stats.ttest_ind(g[g.wd==2].x1, g[g.wd!=2].x1, equal_var=False).statistic,
                  stats.ttest_ind(g[g.wd==0].x1, g[g.wd!=0].x1, equal_var=False).statistic])
    out["Welch t Fri/Wed/Mon vs rest per coin"] = pd.DataFrame(r, columns=["coin","fri","wed","mon"]).set_index("coin").round(2)
    # z-scored 1-day move -> next 5-day excess, per coin, non-overlap grid
    g5 = B[B.pos%5==0].dropna(subset=["x5","z1"]).copy()
    g5["zb"] = pd.cut(g5["z1"], [-np.inf,-1.5,-0.5,0,0.5,1.5,np.inf])
    z = g5.groupby("zb")["x5"].agg(["mean","count","std"]); z["t"]=z["mean"]/(z["std"]/np.sqrt(z["count"]))
    out["z1 bin -> x5"] = z.round(4)
    out["spearman z1 vs x5 per coin"] = g5.groupby("coin").apply(lambda g: stats.spearmanr(g.z1,g.x5)[0]).round(3)
    g5["vb"] = g5.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    out["spearman z1 vs x5 by vol tercile"] = g5.groupby("vb").apply(lambda g: pd.Series({"rho":stats.spearmanr(g.z1,g.x5)[0],"n":len(g)})).round(3)
    # book: largest gain/loss days and their prior position/coin past move
    D = pd.concat([df.assign(coin=c, win=w) for c, ws in data["days"].items() for w, df in ws.items()], ignore_index=True).dropna(subset=["book_return"])
    D["absb"]=D.book_return.abs()
    q = D.book_return.quantile([0.01,0.99])
    out["book tails"] = pd.DataFrame({"worst1pct_mean":[D[D.book_return<=q.iloc[0]].book_return.mean()],
        "best1pct_mean":[D[D.book_return>=q.iloc[1]].book_return.mean()],
        "share_days_invested":[(D.book_return!=0).mean()]}).round(4)
    # book daily return by weekday
    D["wd"]=pd.to_datetime(D["day"]).dt.dayofweek
    out["book by weekday"] = D.groupby("wd")["book_return"].agg(["mean","count"]).round(5)
    return out
