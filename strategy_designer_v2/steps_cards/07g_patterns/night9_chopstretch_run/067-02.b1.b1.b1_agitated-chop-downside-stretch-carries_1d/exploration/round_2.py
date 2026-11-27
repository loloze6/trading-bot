import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float); r=c.pct_change()
            sma=c.rolling(20).mean(); sd=r.rolling(20).std()
            b["z"]=(c/sma-1)/sd
            b["tr60"]=c/c.shift(60)-1
            b["f5"]=c.shift(-5)/c-1
            b["rz"]=r/sd
            b["f1"]=c.shift(-1)/c-1
            b["coin"]=coin; b["w"]=w; b["pos"]=np.arange(len(b))
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["yr"]=pd.to_datetime(b["timestamp"]).dt.year
            b["inprof"]=(b["regime"]=="unknown").astype(int)
            rows.append(b[["coin","w","pos","day","yr","z","tr60","f5","rz","f1","inprof"]])
    A=pd.concat(rows,ignore_index=True)
    m5=A[A.pos%5==0].groupby("coin")["f5"].mean(); A["x5"]=A.f5-A.coin.map(m5)
    m1=A.groupby("coin")["f1"].mean(); A["x1"]=A.f1-A.coin.map(m1)
    G=A[A.pos%5==0].dropna(subset=["z","x5","tr60"]).copy()
    G["s"]=np.sign(G.z)*G.x5  # signed continuation
    G["trb"]=pd.cut(G.tr60,[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    def cl(g,col="s",wcol=None):
        v=g[col] if wcol is None else g[col]*g[wcol]/g[wcol].mean()
        d=v.groupby(g.day).sum(); n=len(g)
        mu=v.mean(); G_=len(d)
        se=np.sqrt((d-mu*g.groupby("day").size()).pow(2).sum()*G_/(G_-1))/n if G_>1 else np.nan
        return pd.Series({"n":n,"days":G_,"mean":mu,"t_cl":mu/se})
    G["az"]=G.z.abs()
    out={}
    out["signed cont by trend, weighted |z|"]=G.groupby("trb").apply(lambda g:cl(g,"s","az"))
    out["signed cont by trend unweighted"]=G.groupby("trb").apply(lambda g:cl(g))
    G["azb"]=pd.cut(G.az,[0,1,2,99])
    out["chop: by |z| bin x side"]=G[G.trb=="chop"].groupby(["azb",G.z>0]).apply(lambda g:cl(g,"x5"))
    out["all: by |z| bin signed"]=G.groupby("azb").apply(lambda g:cl(g))
    out["all signed weighted by window"]=G.groupby("w").apply(lambda g:pd.Series({"n":len(g),"mean":(g.s*g.az).sum()/g.az.sum()}))
    out["chop signed weighted by window"]=G[G.trb=="chop"].groupby("w").apply(lambda g:pd.Series({"n":len(g),"mean":(g.s*g.az).sum()/g.az.sum()}))
    out["all signed by coin"]=G.groupby("coin").apply(lambda g:cl(g,"s","az"))
    out["chop inprof vs not"]=G[G.trb=="chop"].groupby("inprof").apply(lambda g:cl(g,"s","az"))
    D=A.dropna(subset=["rz","x1"]).copy()
    D["rev"]=-np.sign(D.rz)*D.x1
    D["arz"]=D.rz.abs()
    D["rb"]=pd.cut(D.arz,[0,1,2,99])
    out["1d reversal signed by |day z|"]=D.groupby(["rb",D.rz>0]).apply(lambda g:cl(g,"x1"))
    return out
