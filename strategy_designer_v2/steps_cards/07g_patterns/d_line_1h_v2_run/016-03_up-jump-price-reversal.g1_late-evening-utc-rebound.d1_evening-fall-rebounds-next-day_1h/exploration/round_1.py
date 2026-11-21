def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        # coin mean 24-bar return over grid
        g=[]
        for w,df in ws.items():
            c=df["close"].values
            idx=np.arange(0,len(c)-24,24)
            g+=list(c[idx+24]/c[idx]-1)
        mu=np.mean(g)
        for w,df in ws.items():
            d=pd.DataFrame({"close":df["close"].values,"vol":df["volume"].values})
            ts=pd.to_datetime(df["timestamp"])
            d["hour"]=ts.dt.hour.values; d["wd"]=ts.dt.weekday.values
            r1=d.close.pct_change()
            d["r24"]=d.close/d.close.shift(24)-1
            d["fwd"]=d.close.shift(-24)/d.close-1-mu
            sd=r1.rolling(24*30,min_periods=200).std()
            d["z"]=d.r24/(sd*np.sqrt(24))
            ab=r1.abs()
            d["jump"]=ab.rolling(24).max()/ab.rolling(24).sum()
            vs=d.vol.rolling(24).sum()
            d["vjump"]=d.vol.rolling(24).max()/vs
            d["volreg"]=sd/sd.rolling(24*90,min_periods=200).median()
            d["fwd72"]=d.close.shift(-72)/d.close-1
            d["coin"]=coin; d["w"]=w; d["pos"]=np.arange(len(d))
            rows.append(d)
    A=pd.concat(rows).dropna(subset=["z","fwd","jump"])
    out={}
    # by hour slope of fwd on -z
    res=[]
    for h,s in A.groupby("hour"):
        r=stats.linregress(-s.z,s.fwd)
        res.append((h,len(s),r.slope*1e4,r.slope/r.stderr))
    out["slope_by_hour (bp per z, t)"]=pd.DataFrame(res,columns=["hour","n","slope_bp","t"])
    # grid sample positions 0,24.. to be independent
    G=A[A.pos%24==0].copy()
    G["zj"]=G.z*(G.jump-G.jump.mean())
    G["zv"]=G.z*(G.vjump-G.vjump.mean())
    import numpy.linalg as la
    def ols(y,X):
        X=np.column_stack([np.ones(len(X)),X]); b=la.lstsq(X,y,rcond=None)[0]
        e=y-X@b; s2=e@e/(len(y)-X.shape[1]); se=np.sqrt(np.diag(s2*la.inv(X.T@X)))
        return pd.Series(b/se,index=["c"]+[f"x{i}" for i in range(X.shape[1]-1)])
    out["grid t: fwd ~ z, jump, z*jump, z*vjump"]=ols(G.fwd.values,G[["z","jump","zj","zv"]].values)
    out["n grid"]=len(G)
    G["zq"]=pd.qcut(G.z,5,labels=False); G["jq"]=pd.qcut(G.jump,3,labels=False)
    out["fwd24 bp by z quintile x jump tercile"]=(G.groupby(["zq","jq"]).fwd.mean()*1e4).unstack()
    G["vq"]=pd.qcut(G.volreg,3,labels=False)
    out["fwd24 bp by z quintile x volregime"]=(G.groupby(["zq","vq"]).fwd.mean()*1e4).unstack()
    wd=G.groupby("wd").fwd.agg(["mean","std","count"]); wd["t"]=wd["mean"]/(wd["std"]/np.sqrt(wd["count"])); wd["mean"]*=1e4
    out["fwd24 by weekday"]=wd
    hh=A.groupby("hour").fwd.agg(["mean","count"]); 
    # next-hour return by hour
    B=pd.concat(rows); B["r1n"]=B.close.shift(-1)/B.close-1
    B.loc[B.w!=B.w.shift(-1),"r1n"]=np.nan
    hr=B.groupby("hour").r1n.agg(["mean","std","count"]); hr["t"]=hr["mean"]/(hr["std"]/np.sqrt(hr["count"])); hr["mean"]*=1e4
    out["next 1h ret by hour bp"]=hr
    # per coin z slope at grid
    pc=[]
    for c,s in G.groupby("coin"):
        r=stats.linregress(s.z,s.fwd); pc.append((c,len(s),r.slope*1e4,r.slope/r.stderr))
    out["per coin slope fwd~z"]=pd.DataFrame(pc,columns=["coin","n","bp","t"])
    return out
