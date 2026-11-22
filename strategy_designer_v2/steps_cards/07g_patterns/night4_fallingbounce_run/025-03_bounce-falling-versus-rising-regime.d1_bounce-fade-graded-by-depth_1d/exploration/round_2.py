def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            vol=r.rolling(20,min_periods=15).std()
            z=r/vol
            r30=c/c.shift(30)-1
            r90=c/c.shift(90)-1
            f5=c.shift(-5)/c-1
            f3=c.shift(-3)/c-1
            f1=c.shift(-1)/c-1
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"z":z,"r30z":r30/(vol*np.sqrt(30)),"r90":r90,"vol":vol,
                            "f5":f5,"f3":f3,"f1":f1,"wd":ts.dt.dayofweek,"yr":ts.dt.year})
            d["grid"]=(np.arange(len(d))%5==0)
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    tt=lambda s:s.mean()/s.std()*np.sqrt(len(s)) if len(s)>2 else np.nan
    out={}
    G=D[D.grid].dropna(subset=["f5","z","r30z"]).copy()
    drift=G.groupby("coin")["f5"].mean()
    G["ab"]=G["f5"]-G["coin"].map(drift)
    up=G[G.r30z>0]
    out["r30z>0: ab by z"]=up.groupby(pd.cut(up.z,[-99,-1,0,0.5,1,1.5,2,99]))["ab"].agg(["count","mean",tt])
    dn=G[G.r30z<=0]
    out["r30z<=0: ab by z"]=dn.groupby(pd.cut(dn.z,[-99,-1,0,0.5,1,1.5,2,99]))["ab"].agg(["count","mean",tt])
    u1=G[(G.z>1)&(G.r30z>0)]
    out["z>1 & r30z>0 by year"]=u1.groupby("yr")["ab"].agg(["count","mean",tt])
    out["z>1 & r30z>0 by coin"]=u1.groupby("coin")["ab"].agg(["count","mean",tt])
    u1=u1.assign(prod=u1.z.clip(upper=4)*u1.r30z.clip(upper=4))
    rr,p=stats.spearmanr(u1["prod"],u1["ab"]); out["z>1&r30z>0 spearman prod vs ab"]=pd.Series({"n":len(u1),"rho":rr,"p":p})
    # interaction across all grid bars
    G["zx"]=G.z.clip(-4,4)*np.sign(G.r30z)
    rr,p=stats.spearmanr(G["zx"],G["ab"]); out["all: spearman z*sign(r30) vs ab"]=pd.Series({"n":len(G),"rho":rr,"p":p})
    # weekday robustness
    D1=D.dropna(subset=["f1"]).copy()
    cm=D1.groupby("coin")["f1"].mean(); D1["ab1"]=D1.f1-D1.coin.map(cm)
    D1["thufri"]=D1.wd.isin([3,4])
    out["thu/fri minus rest by year"]=D1.groupby("yr").apply(lambda g:pd.Series({"n":len(g),"diff":g[g.thufri].ab1.mean()-g[~g.thufri].ab1.mean(),"t":stats.ttest_ind(g[g.thufri].ab1,g[~g.thufri].ab1,equal_var=False).statistic}))
    out["thu/fri minus rest by coin"]=D1.groupby("coin").apply(lambda g:pd.Series({"n":len(g),"diff":g[g.thufri].ab1.mean()-g[~g.thufri].ab1.mean(),"t":stats.ttest_ind(g[g.thufri].ab1,g[~g.thufri].ab1,equal_var=False).statistic}))
    out["weekday ab1 median"]=D1.groupby("wd")["ab1"].agg(["median",lambda s:(s>0).mean()])
    # bounce in falling 90d (theory) graded
    fb=G[(G.r90<0)&(G.z>=1)]
    out["r90<0 & z>=1 ab by r30z"]=fb.groupby(pd.cut(fb.r30z,[-99,-1.5,-0.5,0,99]))["ab"].agg(["count","mean",tt])
    return out
