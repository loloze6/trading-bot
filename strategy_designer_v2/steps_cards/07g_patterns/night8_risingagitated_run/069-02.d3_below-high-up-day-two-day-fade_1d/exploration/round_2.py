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
            hh10 = b["high"].rolling(10).max(); ll10 = b["low"].rolling(10).min()
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(n),"r1":r1,
                "fwd1":c.shift(-1)/c-1,"fwd2":c.shift(-2)/c-1,
                "sd20":r1.rolling(20).std(),
                "p20":(c-ll20)/(hh20-ll20),"p10":(c-ll10)/(hh10-ll10),
                "tr30":c/c.shift(30)-1,"vr":r1.rolling(20).std()/r1.rolling(60,min_periods=40).std(),
                "day":ts.dt.floor("D"),"yr":ts.dt.year}))
    d = pd.concat(rows, ignore_index=True)
    d["ex1"] = d.fwd1 - d.coin.map(d.groupby("coin").fwd1.mean())
    d["s1"] = d.ex1/d.coin.map(d.groupby("coin").fwd1.std())
    d = d.dropna(subset=["ex1","p20","r1"])
    def ct(x, col="ex1"):
        g = x.groupby("day")[col].sum(); m = x[col].mean(); D = len(g); N = len(x)
        dev = (x[col]-m).groupby(x["day"]).sum()
        se = np.sqrt((dev**2).sum()*D/(D-1))/N
        return pd.Series({"n":N,"days":D,"mean%":100*m,"t_day":m/se})
    def slope(x, xc, col="s1"):
        x = x.dropna(subset=[xc, col]); X = x[xc]-x[xc].mean()
        b = (X*x[col]).sum()/(X**2).sum(); res = x[col]-x[col].mean()-b*X
        dev = (X*res).groupby(x["day"]).sum(); D = dev.shape[0]
        se = np.sqrt((dev**2).sum()*D/(D-1))/(X**2).sum()
        return pd.Series({"n":len(x),"slope":b,"t_day":b/se})
    up = d[d.r1>0].copy(); dn = d[d.r1<0].copy()
    for nm, x in [("up", up), ("down", dn)]:
        x["q"] = pd.qcut(x.p20, 5, labels=False)
        out[f"{nm} days ex1 by p20 quintile (day-clustered)"] = x.groupby("q").apply(ct)
        out[f"{nm} days slope s1 on p20, by year"] = x.groupby("yr").apply(lambda z: slope(z,"p20"))
        out[f"{nm} days slope s1 on p20, by coin"] = x.groupby("coin").apply(lambda z: slope(z,"p20"))
        out[f"{nm} days slope s1 on p10 all"] = slope(x,"p10").to_frame().T
        x["tr"] = pd.cut(x.tr30,[-10,-0.1,0.1,10],labels=["falling","choppy","rising"])
        x["ag"] = np.where(x.vr>1,"agit","calm")
        out[f"{nm} days slope s1 on p20 by trend x agit"] = x.dropna(subset=["tr"]).groupby(["tr","ag"],observed=True).apply(lambda z: slope(z,"p20"))
    # down day size grading near top: within top two p20 quintiles, ex1 by scaled fall size
    top = dn[dn.p20 > dn.p20.quantile(0.6)].copy()
    top["fz"] = pd.qcut(top.r1/top.sd20, 3, labels=["big fall","mid","small fall"])
    out["down days high in range: ex1 by fall size"] = top.groupby("fz", observed=True).apply(ct)
    return out
