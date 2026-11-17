import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    frames=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            vol=r.rolling(20).std().shift(1)
            vol60=r.rolling(60).std().shift(1)
            z=r/vol
            nxt=c.shift(-1)/c-1
            vr=b["volume"]/b["volume"].rolling(20).mean().shift(1)
            d=pd.DataFrame({"z":z,"nxt":nxt,"vr":vr,"vol":vol,"volrel":vol/vol60,
                            "year":pd.to_datetime(b["timestamp"]).dt.year})
            d["coin"]=coin; d["win"]=w
            frames.append(d)
    A=pd.concat(frames)
    A["ex"]=A["nxt"]-A.groupby("coin")["nxt"].transform("mean")
    A["volq"]=A.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    A["vrq"]=A.groupby("coin")["vr"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    def summ(g):
        x=g["ex"].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    dn=A[A.z<0].dropna(subset=["z","ex","vr","vol"]).copy()
    dn["fall"]=-dn["z"]; dn["lvr"]=np.log(dn["vr"])
    X=np.column_stack([np.ones(len(dn)),dn["fall"],dn["lvr"],dn["fall"]*dn["lvr"]])
    beta,res,_,_=np.linalg.lstsq(X,dn["ex"].values,rcond=None)
    resid=dn["ex"].values-X@beta; s2=resid@resid/(len(dn)-4)
    se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["down days: ex ~ fall + logvr + fall*logvr"]=pd.DataFrame({"beta":beta,"t":beta/se},index=["c","fall","logvr","fall_x_logvr"])
    out["down days next1 by volq x vrq"]=dn.groupby(["volq","vrq"]).apply(summ)
    out["down days high-vol tercile by coin"]=dn[dn.volq==2].groupby("coin").apply(summ)
    out["down days high-vol-ratio tercile by coin"]=dn[dn.vrq==2].groupby("coin").apply(summ)
    dn["dollar_fall"]=-dn["z"]*dn["vol"]
    out["down days: slope t of ex on raw fall vs scaled"]=pd.Series({
        "raw_t":stats.linregress(dn["dollar_fall"],dn["ex"]).slope/stats.linregress(dn["dollar_fall"],dn["ex"]).stderr,
        "scaled_t":stats.linregress(dn["fall"],dn["ex"]).slope/stats.linregress(dn["fall"],dn["ex"]).stderr})
    dn["vb"]=pd.qcut(dn["dollar_fall"],5)
    out["down days by raw fall quintile"]=dn.groupby("vb").apply(summ)
    up=A[A.z>0].dropna(subset=["ex","vol"])
    out["up days high-vol tercile by coin"]=up[up.volq==2].groupby("coin").apply(summ)
    up2=up.copy(); up2["rise"]=up2["z"]*up2["vol"]
    lr=stats.linregress(up2["rise"],up2["ex"])
    out["up days slope ex on raw rise"]=pd.Series({"slope":lr.slope,"t":lr.slope/lr.stderr,"n":len(up2)})
    out["down days high-vol tercile by year"]=dn[dn.volq==2].groupby("year").apply(summ)
    out["down days by volrel tercile"]=dn.assign(q=pd.qcut(dn["volrel"],3,labels=False)).groupby("q").apply(summ)
    return out
