def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        g=np.concatenate([ (lambda c:(c[np.arange(0,len(c)-24,24)+24]/c[np.arange(0,len(c)-24,24)]-1))(b["close"].values.astype(float)) for b in ws.values()])
        drift=g.mean(); sd=g.std()
        for w,b in ws.items():
            ts=pd.to_datetime(b["timestamp"]); c=b["close"].astype(float).reset_index(drop=True)
            d=pd.DataFrame({"hour":ts.dt.hour.values,"year":ts.dt.year.values})
            r1=c.pct_change(); d["r1"]=r1
            d["r24"]=c/c.shift(24)-1; d["fr"]=c.shift(-24)/c-1; d["f24"]=d["fr"]-drift
            d["vol24"]=r1.rolling(24).std(); d["vol30d"]=r1.rolling(720,min_periods=240).std()
            d["vr"]=d["vol24"]/d["vol30d"]
            d["z"]=d["r24"]/sd; d["sd"]=sd; d["coin"]=coin
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["vt"]=D.groupby("coin")["vol24"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    D["vrt"]=D.groupby("coin")["vr"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    def slope(x):
        x=x.dropna(subset=["z","f24"])
        if len(x)<50: return pd.Series({"n":len(x)})
        r=stats.linregress(-x["z"],x["f24"])
        u=-np.sign(x["z"])*x["f24"]; tot=-np.sign(x["z"])*x["fr"]
        return pd.Series({"n":len(x),"slope":r.slope,"t":r.slope/r.stderr,"unusual":u.mean(),"t_u":u.mean()/(u.std()/np.sqrt(len(u))),"total":tot.mean(),"strength":(u/x["sd"]).mean()})
    h0=D[D.hour==0].copy()
    out={}
    out["h0 by vol24 tercile"]=h0.groupby("vt").apply(slope)
    out["h0 by vol ratio (24h/30d) tercile"]=h0.groupby("vrt").apply(slope)
    hv=h0[h0.vt==2].dropna(subset=["z","f24"]).copy()
    hv["q"]=pd.qcut(hv["z"],5,labels=False)
    out["h0 high vol: f24 by r24 quintile"]=hv.groupby("q")["f24"].agg(["mean","count"])
    out["h0 high vol: by sign of r24"]=hv.groupby(np.sign(hv["z"])).apply(slope)
    out["h0 high vol by year"]=hv.groupby("year").apply(slope)
    out["h0 high vol by coin"]=hv.groupby("coin").apply(slope)
    out["h12 high vol"]=D[(D.hour==12)&(D.vt==2)].pipe(lambda x: slope(x)).to_frame("h12hv")
    out["h0 low vol by year"]=h0[h0.vt==0].groupby("year").apply(slope)
    # hour 21-22 drift persistence
    e=D[D.hour.isin([21,22])]
    a=e.groupby("year")["r1"].agg(["mean","std","count"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["hours 21-22 ret by year"]=a[["mean","t","count"]]
    b2=e.groupby("coin")["r1"].agg(["mean","std","count"]); b2["t"]=b2["mean"]/(b2["std"]/np.sqrt(b2["count"]))
    out["hours 21-22 ret by coin"]=b2[["mean","t"]]
    f=D[D.hour==14]; c3=f.groupby("year")["r1"].agg(["mean","std","count"]); c3["t"]=c3["mean"]/(c3["std"]/np.sqrt(c3["count"]))
    out["hour 14 ret by year"]=c3[["mean","t"]]
    return out
