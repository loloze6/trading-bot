import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]; drows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float)
            r=c.pct_change()
            sma=c.rolling(20).mean(); sd=r.rolling(20).std()
            b["z"]=(c/sma-1)/sd
            b["r1"]=r
            b["rz"]=r/sd
            b["tr60"]=c/c.shift(60)-1
            b["f5"]=c.shift(-5)/c-1
            b["f1"]=c.shift(-1)/c-1
            b["f10"]=c.shift(-10)/c-1
            b["inprof"]=(b["regime"]=="unknown").astype(int)
            b["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            b["yr"]=pd.to_datetime(b["timestamp"]).dt.year
            b["coin"]=coin; b["w"]=w; b["pos"]=np.arange(len(b))
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b[["coin","w","pos","day","z","r1","rz","tr60","f5","f1","f10","inprof","wd","yr","forecast","postRebalance_current_allocation"]])
    A=pd.concat(rows,ignore_index=True)
    m5=A[A.pos%5==0].groupby("coin")["f5"].mean()
    m1=A.groupby("coin")["f1"].mean()
    m10=A[A.pos%10==0].groupby("coin")["f10"].mean()
    A["x5"]=A["f5"]-A.coin.map(m5); A["x1"]=A["f1"]-A.coin.map(m1); A["x10"]=A["f10"]-A.coin.map(m10)
    G=A[(A.pos%5==0)].dropna(subset=["z","x5"]).copy()
    G["zb"]=pd.cut(G.z,[-99,-2,-1,0,1,2,99])
    def agg(g,col):
        return pd.Series({"n":len(g),"mean":g[col].mean(),"t":g[col].mean()/(g[col].std()/np.sqrt(len(g))) if len(g)>2 else np.nan})
    out={}
    out["x5 by zbin all"]=G.groupby("zb").apply(lambda g:agg(g,"x5"))
    out["x5 by zbin x inprof"]=G.groupby(["inprof","zb"]).apply(lambda g:agg(g,"x5"))
    G["trb"]=pd.cut(G.tr60,[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    out["x5 by trend x zsign"]=G.dropna(subset=["trb"]).groupby(["trb",G.z>0]).apply(lambda g:agg(g,"x5"))
    G10=A[(A.pos%10==0)].dropna(subset=["z","x10"]).copy()
    G10["zb"]=pd.cut(G10.z,[-99,-2,-1,0,1,2,99])
    out["x10 by zbin"]=G10.groupby("zb").apply(lambda g:agg(g,"x10"))
    D=A.dropna(subset=["rz","x1"]).copy()
    D["rb"]=pd.cut(D.rz,[-99,-2,-1,0,1,2,99])
    out["next1d by day move z"]=D.groupby("rb").apply(lambda g:agg(g,"x1"))
    out["next1d by day move z inprof"]=D[D.inprof==1].groupby("rb").apply(lambda g:agg(g,"x1"))
    out["x1 by weekday"]=D.groupby("wd").apply(lambda g:agg(g,"x1"))
    out["x5 corr z by coin"]=G.groupby("coin").apply(lambda g:pd.Series({"n":len(g),"rho":stats.spearmanr(g.z,g.x5)[0]}))
    out["share inprof"]=float(A.inprof.mean())
    return out
