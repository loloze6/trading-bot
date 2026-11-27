import numpy as np, pandas as pd

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); h = b["high"].astype(float)
            r1 = c.pct_change()
            sd20 = r1.rolling(20).std()
            sd30 = r1.rolling(30).std()
            hh20 = h.rolling(20).max()
            depth = (c - hh20) / hh20 / sd20
            tr60 = c / c.shift(60) - 1
            n = len(b)
            fwd = c.shift(-1) / c - 1
            for i in range(0, n - 1):
                rows.append(dict(coin=coin, w=w, i=i, r1=r1[i], depth=depth[i], fwd=fwd[i],
                                 regime=b["regime"][i], tr60=tr60[i], sd20=sd20[i], sd30=sd30[i],
                                 day=pd.Timestamp(b["timestamp"][i]).floor("D"),
                                 yr=pd.Timestamp(b["timestamp"][i]).year))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby("coin")["fwd"].transform("mean")
    d["un"] = d["fwd"] - d["drift"]
    d = d.dropna(subset=["depth","un","r1"])
    d["prof"] = np.where(d["regime"]=="chop","trend","choppy")
    d["agit"] = d.groupby("coin")["sd30"].transform(lambda s: (s > s.median()).astype(int))
    d["trd"] = np.where(d.tr60 > 0.10, "rising", np.where(d.tr60 < -0.10, "falling", "choppy"))
    up = d[d.r1 > 0].copy()
    def clus(g, x="depth"):
        # slope of un on x, day-clustered t
        X = g[x].values; Y = g["un"].values
        Xc = X - X.mean(); b = (Xc*Y).sum()/(Xc**2).sum()
        e = Y - Y.mean() - b*Xc
        s = pd.Series(Xc*e).groupby(g["day"].values).sum()
        se = np.sqrt((s**2).sum())/(Xc**2).sum()
        # mean un clustered
        dm = (g["un"]).groupby(g["day"]).sum()
        nd = len(dm)
        tmean = g["un"].sum()/np.sqrt(((dm - dm.mean()*0 - g["un"].mean()*g.groupby("day").size())**2).sum())
        return pd.Series(dict(n=len(g), days=nd, mean_un=g["un"].mean(), t_mean_day=tmean, slope=b, t_slope=b/se))
    out = {}
    out["up days: un on depth, all"] = clus(up)
    out["up days by trend x agitation"] = up.groupby(["trd","agit"]).apply(clus)
    out["up days by window"] = up.groupby("w").apply(clus)
    out["up days by year"] = up.groupby("yr").apply(clus)
    up["dq"] = pd.qcut(up["depth"], 5, labels=False)
    out["up days depth quintile x agit"] = up.groupby(["agit","dq"]).apply(lambda g: pd.Series(dict(n=len(g), mean_un=g.un.mean(), t=g.un.mean()/(g.un.std()/np.sqrt(len(g))), depth=g.depth.mean())))
    # up-day size in sd units graded?
    up["mv"] = up.r1/up.sd20
    out["up days: un on move/sd"] = clus(up, "mv")
    out["up days: un on move/sd by agit"] = up.groupby("agit").apply(lambda g: clus(g, "mv"))
    dn = d[d.r1 <= 0].copy()
    out["down days: un on depth by agit"] = dn.groupby("agit").apply(clus)
    # book around largest gains/losses
    dd=[]
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            dd.append(t.assign(coin=coin, w=w))
    dd = pd.concat(dd)
    br = dd.groupby(["w","day"])["book_return"].mean().dropna()
    out["book return quantiles"] = br.quantile([0.01,0.05,0.5,0.95,0.99])
    return out
