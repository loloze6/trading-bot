def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd30=r.rolling(30).std()
            volr=sd30/sd30.rolling(60).mean()
            er=(c-c.shift(30)).abs()/(c.diff().abs().rolling(30).sum())
            r7=c/c.shift(7)-1
            z7=r7/(sd30*np.sqrt(7))
            f7=c.shift(-7)/c-1
            ts=pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"z7":z7,"volr":volr,"er":er,
                                      "f7":f7,"day":ts.dt.floor("D"),"year":ts.dt.year}))
    d=pd.concat(rows)
    drift=d[d.pos%7==0].groupby("coin")["f7"].mean()
    d["u7"]=d["f7"]-d["coin"].map(drift)
    d=d.dropna(subset=["z7","volr","er","u7"]).copy()
    d["reg"]=np.where(d.volr>=1,"agit","calm")+"_"+np.where(d.er>=0.3,"trend","chop")
    def slope_cl(x):
        # slope of u7 on z7, t clustered by day
        X=x.z7.values; Y=x.u7.values
        if len(x)<10: return pd.Series({"n":len(x),"slope":np.nan,"t_day":np.nan})
        Xc=X-X.mean(); b=(Xc*(Y-Y.mean())).sum()/(Xc**2).sum()
        e=Y-Y.mean()-b*Xc
        sc=pd.Series(Xc*e).groupby(x.day.values).sum()
        se=np.sqrt((sc**2).sum())/(Xc**2).sum()
        return pd.Series({"n":len(x),"slope":b,"t_day":b/se})
    out={}
    # offsets of grid
    off={}
    for o in range(7):
        g=d[d.pos%7==o]
        for k,x in g.groupby("reg"):
            off[(o,k)]=slope_cl(x)
        off[(o,"all")]=slope_cl(g)
    out["offset_slopes"]=pd.DataFrame(off).T.unstack(1)["t_day"]
    g=d[d.pos%7==0]
    out["calmchop_by_coin"]=g[g.reg=="calm_chop"].groupby("coin").apply(slope_cl)
    out["calmchop_by_year"]=g[g.reg=="calm_chop"].groupby("year").apply(slope_cl)
    out["all_by_year"]=g.groupby("year").apply(slope_cl)
    out["all_by_window"]=g.groupby("w").apply(slope_cl)
    # graded by calm: slope in volr quintiles and er quintiles (all grid 0)
    out["slope_by_volq"]=g.assign(q=pd.qcut(g.volr,4,labels=False)).groupby("q").apply(slope_cl)
    out["slope_by_erq"]=g.assign(q=pd.qcut(g.er,4,labels=False)).groupby("q").apply(slope_cl)
    # signed: z7 times u7 sign split in calm chop
    cc=g[g.reg=="calm_chop"]
    out["calmchop_up_down"]=pd.DataFrame({"up":[ (cc.z7>0).sum(), cc[cc.z7>0].u7.mean()],
                                          "down":[(cc.z7<=0).sum(), cc[cc.z7<=0].u7.mean()]},index=["n","mean_u7"])
    return out
