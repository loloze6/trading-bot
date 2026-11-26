def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); n = len(b)
            r1 = c.pct_change()
            hh20 = b["high"].rolling(20).max(); ll20 = b["low"].rolling(20).min()
            ts = pd.to_datetime(b["timestamp"])
            sd30 = r1.rolling(30).std()
            rows.append(pd.DataFrame({"coin":coin,"win":w,"wn":int(w[1:]),"pos":np.arange(n),"r1":r1,
                "fwd1":c.shift(-1)/c-1,"fwd2":c.shift(-2)/c-1,
                "sd20":r1.rolling(20).std(),"sd30":sd30,
                "p20":(c-ll20)/(hh20-ll20),
                "clv":(c-b["low"])/(b["high"]-b["low"]),
                "tr60":c/c.shift(60)-1,
                "day":ts.dt.floor("D"),"yr":ts.dt.year}))
    d = pd.concat(rows, ignore_index=True)
    # agitation proxy: 30-day swing vs the coin's median 30-day swing over all its windows
    d["ag"] = np.where(d.sd30 > d.coin.map(d.groupby("coin").sd30.median()), "agit", "calm")
    d["tr"] = pd.cut(d.tr60, [-10,-0.1,0.1,10], labels=["falling","choppy","rising"])
    d["ex1"] = d.fwd1 - d.coin.map(d.groupby("coin").fwd1.mean())
    d["s1"] = d.ex1/d.coin.map(d.groupby("coin").fwd1.std())
    d["half"] = np.where(d.wn <= 12, "w7-w12", "w13-w18")
    d = d.dropna(subset=["ex1","p20","r1","clv"])
    def ct(x, col="ex1"):
        m = x[col].mean(); D = x["day"].nunique(); N = len(x)
        dev = (x[col]-m).groupby(x["day"]).sum()
        se = np.sqrt((dev**2).sum()*D/(D-1))/N
        return pd.Series({"n":N,"days":D,"mean%":100*m,"t_day":m/se})
    def slope(x, xc, col="s1"):
        x = x.dropna(subset=[xc, col]); X = x[xc]-x[xc].mean()
        if len(x) < 30: return pd.Series({"n":len(x),"slope":np.nan,"t_day":np.nan})
        b = (X*x[col]).sum()/(X**2).sum(); res = x[col]-x[col].mean()-b*X
        dev = (X*res).groupby(x["day"]).sum(); D = dev.shape[0]
        se = np.sqrt((dev**2).sum()*D/(D-1))/(X**2).sum()
        return pd.Series({"n":len(x),"slope":b,"t_day":b/se})
    up = d[d.r1>0].copy(); dn = d[d.r1<0].copy()
    up["q"] = pd.qcut(up.p20, 5, labels=False)
    out["up days ex1 by p20 quintile x half"] = up.groupby(["half","q"]).apply(ct)
    out["up days slope s1 on p20 by half"] = up.groupby("half").apply(lambda z: slope(z,"p20"))
    # 2-day for comparison, non-overlapping grid
    g = up[up.pos % 2 == 0].copy()
    g["ex2"] = g.fwd2 - g.coin.map(d[d.pos%2==0].groupby("coin").fwd2.mean())
    out["up days ex2 by p20 quintile (grid)"] = g.dropna(subset=["ex2"]).groupby(pd.qcut(g.p20,5,labels=False)).apply(lambda z: ct(z,"ex2"))
    # profile: all bars next-day by trend x agit
    out["all bars ex1 by trend x agit"] = d.dropna(subset=["tr"]).groupby(["tr","ag"],observed=True).apply(ct)
    # close location on the day: slope by profile (s1 on clv) all days
    out["slope s1 on clv by trend x agit"] = d.dropna(subset=["tr"]).groupby(["tr","ag"],observed=True).apply(lambda z: slope(z,"clv"))
    # choppy agitated: clv quintiles and half split
    ca = d[(d.tr=="choppy")&(d.ag=="agit")].copy()
    ca["cq"] = pd.qcut(ca.clv, 3, labels=["low","mid","high"])
    out["choppy agit ex1 by clv tercile"] = ca.groupby("cq",observed=True).apply(ct)
    out["choppy agit slope on clv by half"] = ca.groupby("half").apply(lambda z: slope(z,"clv"))
    out["all slope s1 on clv by half"] = d.groupby("half").apply(lambda z: slope(z,"clv"))
    return out
