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
            r30=c/c.shift(30)-1
            hl=(b["high"]-b["low"])/c
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"z7":z7,"volr":volr,"er":er,"f7":f7,
                             "r30":r30,"sd30":sd30,"r1":r,"wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                             "alloc":b["postRebalance_current_allocation"],"fc":b["forecast"],
                             "year":pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
    d=pd.concat(rows)
    drift=d[d.pos%7==0].groupby("coin")["f7"].mean()
    d["u7"]=d["f7"]-d["coin"].map(drift)
    g=d[(d.pos%7==0)].dropna(subset=["z7","volr","er","u7"]).copy()
    g["agit"]=np.where(g.volr>=1,"agit","calm")
    g["trend"]=np.where(g.er>=0.3,"trend","chop")
    g["zq"]=pd.qcut(g.z7,5,labels=False)
    def summ(x):
        return pd.Series({"n":len(x),"mean_u7":x.u7.mean(),"t":x.u7.mean()/(x.u7.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    out["by_zq"]=g.groupby("zq").apply(summ)
    out["by_regime_zq"]=g.groupby(["agit","trend","zq"]).apply(summ)
    # slope of u7 on z7 per regime
    res={}
    for k,x in g.groupby(["agit","trend"]):
        s=stats.linregress(x.z7,x.u7); res[str(k)]=pd.Series({"n":len(x),"slope":s.slope,"t":s.slope/s.stderr})
    out["slope_regime"]=pd.DataFrame(res).T
    # 30d return momentum
    g["r30q"]=pd.qcut(g.r30,5,labels=False)
    out["by_r30q"]=g.groupby("r30q").apply(summ)
    out["by_volq"]=g.assign(vq=pd.qcut(g.volr,5,labels=False)).groupby("vq").apply(summ)
    s=stats.linregress(g.z7,g.u7); out["slope_all"]=pd.Series({"n":len(g),"slope":s.slope,"t":s.slope/s.stderr})
    # 1-day: large daily moves next day
    dd=d.dropna(subset=["r1","sd30"]).copy()
    dd["z1"]=dd.r1/dd.sd30
    dd["n1"]=dd.groupby(["coin","w"])["r1"].shift(-1)
    dd=dd.dropna(subset=["n1"])
    dd["z1q"]=pd.qcut(dd.z1,5,labels=False)
    out["next_day_by_z1q"]=dd.groupby("z1q")["n1"].agg(["count","mean","std"])
    out["weekday"]=dd.groupby("wd")["r1"].agg(["count","mean","std"])
    out["by_coin_slope"]=pd.DataFrame({c:pd.Series({"n":len(x),"slope":stats.linregress(x.z7,x.u7).slope,"t":stats.linregress(x.z7,x.u7).slope/stats.linregress(x.z7,x.u7).stderr}) for c,x in g.groupby("coin")}).T
    return out
