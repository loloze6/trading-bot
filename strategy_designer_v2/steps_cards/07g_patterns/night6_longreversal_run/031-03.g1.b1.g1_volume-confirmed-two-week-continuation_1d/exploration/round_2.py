def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            n = len(b)
            for i in range(0, n - 14, 14):
                if i < 29: continue
                d = dict(coin=coin, win=w)
                d["fwd14"] = c[i+14]/c[i]-1
                d["fwd7"] = c[i+7]/c[i]-1
                d["vr"] = v[i-13:i+1].mean()/v[i-29:i+1].mean()
                d["vr7"] = v[i-6:i+1].mean()/v[i-29:i+1].mean()
                d["ret14"] = c[i]/c[i-14]-1
                d["vratio_ret"] = d["ret14"]
                d["ts"] = pd.Timestamp(b["timestamp"].iloc[i])
                d["regime"] = b["regime"].iloc[i]
                rows.append(d)
    g = pd.DataFrame(rows)
    # coin mean over all its grid cases (all windows)
    allr = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            for i in range(0, len(c)-14, 14):
                allr.append((coin, c[i+14]/c[i]-1, c[min(i+7,len(c)-1)]/c[i]-1))
    A = pd.DataFrame(allr, columns=["coin","f14","f7"])
    cm14 = A.groupby("coin")["f14"].mean(); cm7 = A.groupby("coin")["f7"].mean()
    g["ex"] = g["fwd14"] - g["coin"].map(cm14)
    g["ex7"] = g["fwd7"] - g["coin"].map(cm7)
    g["day"] = g["ts"].dt.floor("D"); g["year"] = g["ts"].dt.year
    g["lvr"] = np.log(g["vr"]); g["lvr7"] = np.log(g["vr7"])
    g["q"] = g.groupby("coin")["vr"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out = {}
    def dayt(s, col):
        d = s.groupby("day")[col].sum()
        return d.mean()/d.std()*np.sqrt(len(d)), len(d)
    # signed case: long when vr above coin median, size lvr centered
    g["lc"] = g["lvr"] - g.groupby("coin")["lvr"].transform("median")
    g["sx"] = g["ex"]*np.sign(g["lc"])
    g["sx7"] = g["ex7"]*np.sign(g["lc"])
    t, nd = dayt(g, "sx"); t7, _ = dayt(g, "sx7")
    out["vr sign-long/short: mean ex14, day-clustered t, days; ex7"] = pd.Series({"mean14": g["sx"].mean(), "t14": t, "days": nd, "mean7": g["sx7"].mean(), "t7": t7, "cases": len(g)})
    rows2 = {}
    for q, s in g.groupby("q"):
        tt, nd = dayt(s, "ex"); rows2[q] = (s["ex"].mean(), s["ex7"].mean(), len(s), nd, tt)
    out["ex14 by coin-quintile vr, day-clustered"] = pd.DataFrame(rows2, index=["ex14","ex7","n","days","t_day"]).T
    out["vr effect by year (mean sx, n)"] = g.groupby("year")["sx"].agg(["mean","count"])
    out["vr effect by window"] = g.groupby("win")["sx"].agg(["mean","count"]).T
    out["vr effect by coin"] = g.groupby("coin")["sx"].agg(["mean","count"])
    out["vr effect by regime"] = g.groupby("regime")["sx"].agg(["mean","count"])
    # cross-sectional control: demean ex by day across coins
    g["exd"] = g["ex"] - g.groupby("day")["ex"].transform("mean")
    g["nday"] = g.groupby("day")["ex"].transform("count")
    s = g[g["nday"] >= 3]
    out["spearman lvr vs ex, raw / day-demeaned"] = pd.Series({"raw": stats.spearmanr(g["lvr"], g["ex"])[0], "demeaned": stats.spearmanr(s["lvr"], s["exd"])[0], "n_dem": len(s), "lvr7_raw": stats.spearmanr(g["lvr7"], g["ex"])[0]})
    # vr is mostly market-wide? share of variance in lvr explained by day mean
    out["lvr within-day share"] = 1 - g.groupby("day")["lvr"].transform("mean").var()/g["lvr"].var()
    # daily: weekday and prev-day, clustered by day
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            d["prev"] = d["coin_return"].shift(1)
            d["sd"] = d["coin_return"].shift(1).rolling(30).std()
            dd.append(d)
    D = pd.concat(dd).dropna(subset=["coin_return"])
    D["day"] = pd.to_datetime(D["day"])
    dm = D.groupby("day")["coin_return"].mean().to_frame("r")
    dm["wd"] = dm.index.dayofweek; dm["year"] = dm.index.year
    out["day-mean coin return by weekday"] = dm.groupby("wd")["r"].agg(["mean","count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    out["weekday mean by year (Wed,Fri,Sat minus others)"] = dm.groupby("year").apply(lambda x: x[x.wd.isin([2,4,5])]["r"].mean() - x[~x.wd.isin([2,4,5])]["r"].mean())
    D2 = D.dropna(subset=["prev","sd"]).copy()
    D2["z"] = D2["prev"]/D2["sd"]
    D2["cmean"] = D2.groupby("coin")["coin_return"].transform("mean")
    D2["ex1"] = D2["coin_return"] - D2["cmean"]
    D2["zb"] = pd.cut(D2["z"], [-99,-2,-1,0,1,2,99])
    D2["exd"] = D2["ex1"] - D2.groupby("day")["ex1"].transform("mean")
    out["next-day ex by prev-day z (raw, day-demeaned)"] = D2.groupby("zb").agg(ex=("ex1","mean"), exd=("exd","mean"), n=("ex1","count"))
    dz = D2[D2.z < -1].groupby("day")["ex1"].sum()
    out["after z<-1: day-clustered t, days"] = pd.Series({"t": dz.mean()/dz.std()*np.sqrt(len(dz)), "days": len(dz)})
    return out
