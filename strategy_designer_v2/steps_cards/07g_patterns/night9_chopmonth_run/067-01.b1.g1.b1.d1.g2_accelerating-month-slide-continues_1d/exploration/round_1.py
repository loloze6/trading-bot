import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            n=len(b)
            d=pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(n)})
            d["regime"]=b["regime"].values
            d["fc"]=b["forecast"].values
            d["alloc"]=b["postRebalance_current_allocation"].values
            d["r1"]=c.pct_change().values
            d["r5"]=(c/c.shift(5)-1).values
            d["r30"]=(c/c.shift(30)-1).values
            d["rng"]=((b["high"]-b["low"])/c).values
            d["clpos"]=((c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)).values
            for h in (1,3,5,10):
                d[f"f{h}"]=(c.shift(-h)/c-1).values
            d["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday.values
            d["yr"]=pd.to_datetime(b["timestamp"]).dt.year.values
            d["vol20"]=c.pct_change().rolling(20).std().values
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    # drift per coin on grid
    for h in (1,3,5,10):
        g=D[D.pos%h==0]
        dr=g.groupby("coin")[f"f{h}"].mean()
        D[f"u{h}"]=D[f"f{h}"]-D.coin.map(dr)
    D["z1"]=D.r1/D.vol20
    G=D[D.pos%10==0].copy()
    def summ(x,col):
        x=x.dropna(subset=[col])
        m=x[col].mean(); s=x[col].std(); n=len(x)
        return pd.Series({"n":n,"mean":m,"t":m/(s/np.sqrt(n)) if n>2 else np.nan})
    out={}
    out["regime_counts"]=D.regime.value_counts()
    G["choppy"]=G.regime!="chop"
    g2=G.dropna(subset=["r30","u10"])
    g2["q30"]=g2.groupby("choppy").r30.transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["u10_by_choppy_r30q"]=g2.groupby(["choppy","q30"]).apply(lambda x: summ(x,"u10"))
    g3=G.dropna(subset=["r5","u10"]).copy()
    g3["q5"]=g3.groupby("regime").r5.transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["u10_by_regime_r5q"]=g3.groupby(["regime","q5"]).apply(lambda x: summ(x,"u10"))
    # daily: next-day after large z move, by regime group
    D["zq"]=pd.cut(D.z1,[-99,-2,-1,1,2,99])
    D["chop2"]=np.where(D.regime=="chop","trend","choppy")
    G3=D[D.pos%3==0]
    out["u3_by_z_chop"]=G3.groupby(["chop2","zq"]).apply(lambda x: summ(x,"u3"))
    out["u1_by_weekday"]=D.groupby("wd").apply(lambda x: summ(x,"u1"))
    D["cq"]=pd.cut(D.clpos,[0,0.2,0.4,0.6,0.8,1.0],include_lowest=True)
    G5=D[D.pos%5==0]
    out["u5_by_closepos_chop"]=G5.groupby(["chop2","cq"]).apply(lambda x: summ(x,"u5"))
    G5=G5.copy(); G5["rq"]=G5.groupby("coin").rng.transform(lambda s: pd.qcut(s,4,labels=False,duplicates="drop"))
    out["u5_by_rangeq_chop"]=G5.groupby(["chop2","rq"]).apply(lambda x: summ(x,"u5"))
    # book days
    dd=[]
    for coin,wins in data["days"].items():
        for w,x in wins.items():
            x=x.copy(); x["win"]=w; x["coin"]=coin; dd.append(x)
    B=pd.concat(dd)
    bk=B.groupby(["win","day"]).book_return.mean().dropna()
    out["book_by_window"]=bk.groupby(level=0).agg(["count","mean","std"])
    return out
