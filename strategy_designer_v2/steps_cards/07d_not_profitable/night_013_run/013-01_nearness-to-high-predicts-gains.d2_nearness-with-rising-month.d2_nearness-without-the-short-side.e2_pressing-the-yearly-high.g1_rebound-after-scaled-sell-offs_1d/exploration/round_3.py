import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    br=[]
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.copy()
            r=b.close.pct_change()
            b["r"]=r
            b["nxt"]=b.close.shift(-1)/b.close-1
            b["f3"]=b.close.shift(-3)/b.close-1
            b["pos"]=b.postRebalance_current_allocation
            b["gain"]=b.pos*b.nxt
            b["vol30"]=r.rolling(30).std()
            b["vol90"]=r.rolling(90).std()
            b["volratio"]=b.vol30/b.vol90
            b["z"]=r/b.vol30.shift(1)
            b["r5p"]=b.close.shift(1)/b.close.shift(6)-1
            b["r5pz"]=b.r5p/(b.vol30.shift(1)*np.sqrt(5))
            b["day"]=pd.to_datetime(b.timestamp).dt.floor("D")
            b["coin"]=c; b["wn"]=int(w[1:])
            b["grid"]=(np.arange(len(b))%3==0)
            br.append(b)
    X=pd.concat(br)
    G=X[X.grid].dropna(subset=["f3","volratio","r5pz"]).copy()
    G["ex"]=G.f3-G.groupby("coin").f3.transform("mean")
    P=G[G.forecast>0].copy()
    P["vq"]=pd.qcut(P.volratio,4,labels=False)
    def slope(df):
        if len(df)<30: return pd.Series({"n":len(df)})
        s=stats.linregress(df.forecast,df.ex)
        return pd.Series({"n":len(df),"ex":df.ex.mean(),"slope":s.slope,"t":s.slope/s.stderr})
    out["grid fc>0 by volratio q"]=P.groupby("vq").apply(slope)
    P["pq"]=pd.qcut(P.r5pz,4,labels=False)
    out["grid fc>0 by prior 5d z q"]=P.groupby("pq").apply(slope)
    H=X[X.pos>0].dropna(subset=["volratio","r5pz"]).copy()
    H["vq"]=pd.qcut(H.volratio,4,labels=False)
    H["pq"]=pd.qcut(H.r5pz,4,labels=False)
    tot=H.gain.sum()
    out["held by volratio q"]=H.groupby("vq").agg(lo=("volratio","min"),hi=("volratio","max"),n=("gain","size"),gain=("gain","mean"),sd=("gain","std"),pos=("pos","mean"),worst=("gain",lambda x:(x<-0.03).mean()))
    out["held by prior 5d z q"]=H.groupby("pq").agg(lo=("r5pz","min"),hi=("r5pz","max"),n=("gain","size"),gain=("gain","mean"),sd=("gain","std"),pos=("pos","mean"),worst=("gain",lambda x:(x<-0.03).mean()))
    L=H.nsmallest(100,"gain")
    out["worst 100 held bars"]=pd.Series({"gain":L.gain.mean(),"nxt":L.nxt.mean(),"pos":L.pos.mean(),"z":L.z.mean(),"vr":L.volratio.mean(),"r5pz":L.r5pz.mean(),
        "all z":H.z.mean(),"all vr":H.volratio.mean(),"all r5pz":H.r5pz.mean(),"all pos":H.pos.mean()})
    return out
