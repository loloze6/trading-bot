def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            d=df.copy()
            d["ts"]=pd.to_datetime(d["timestamp"])
            d=d.sort_values("ts").reset_index(drop=True)
            c=d["close"]
            d["r"]=c.pct_change()
            d["f1"]=c.shift(-1)/c-1
            d["vol"]=d["r"].rolling(20,min_periods=15).std()
            d["z"]=d["r"]/d["vol"]
            d["volpct"]=d["vol"]/d["vol"].rolling(60,min_periods=30).mean()
            d["vrel"]=d["volume"]/d["volume"].rolling(20,min_periods=15).mean()
            d["wd"]=d["ts"].dt.weekday; d["yr"]=d["ts"].dt.year
            d["coin"]=coin; d["w"]=w
            rows.append(d[["coin","w","yr","wd","r","f1","z","vol","volpct","vrel","regime"]])
    A=pd.concat(rows)
    mu=A.groupby("coin")["r"].mean()
    A["f1x"]=A["f1"]-A["coin"].map(mu)
    B=A.dropna(subset=["z","f1x","volpct"]).copy()
    B["fz"]=B["f1x"]/B["vol"]
    B["vlq"]=pd.qcut(B["volpct"],3,labels=False)
    out={}
    def reg(g):
        if len(g)<30: return pd.Series({"n":len(g),"slope":np.nan,"t":np.nan})
        r=stats.linregress(g["z"].clip(-5,5),g["fz"])
        return pd.Series({"n":len(g),"slope":r.slope,"t":r.slope/r.stderr})
    out["slope fz~z by vol tercile"]=B.groupby("vlq").apply(reg)
    H=B[B["vlq"]==2].copy()
    H["sgn"]=np.where(H["z"]<0,"down","up")
    out["high-vol slope by sign"]=H.groupby("sgn").apply(reg)
    H["zq"]=pd.qcut(H["z"],5,labels=False)
    g=H.groupby("zq")["f1x"].agg(["mean","count","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["high-vol f1x by z quintile"]=g.drop(columns="std")
    out["high-vol slope by coin"]=H.groupby("coin").apply(reg)
    out["high-vol slope by year"]=H.groupby("yr").apply(reg)
    out["slope by weekday"]=B.groupby("wd").apply(reg)
    out["Sat slope by year"]=B[B["wd"]==5].groupby("yr").apply(reg)
    out["Mon slope by year"]=B[B["wd"]==0].groupby("yr").apply(reg)
    B["vq"]=pd.qcut(B["vrel"],3,labels=False)
    out["slope by rel-volume tercile"]=B.groupby("vq").apply(reg)
    out["high-vol slope by rel-volume tercile"]=H.assign(vq=pd.qcut(H["vrel"],3,labels=False)).groupby("vq").apply(reg)
    return out
