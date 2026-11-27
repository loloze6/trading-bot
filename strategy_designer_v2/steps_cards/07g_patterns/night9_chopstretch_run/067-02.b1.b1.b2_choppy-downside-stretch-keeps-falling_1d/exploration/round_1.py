import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            cl=b["close"]; r=cl.pct_change()
            sma=cl.rolling(20).mean(); sd=r.rolling(20).std()
            z=(cl-sma)/sma/sd
            r1=r; r5b=cl/cl.shift(5)-1
            rng=(b["high"]-b["low"])/cl
            clpos=(cl-b["low"])/(b["high"]-b["low"])
            f5=cl.shift(-5)/cl-1; f1=cl.shift(-1)/cl-1
            n=len(b)
            d=pd.DataFrame({"coin":c,"win":w,"pos":np.arange(n),"z":z,"r1":r1,"r5b":r5b,
              "rs":r1/sd,"rng":rng/sd,"clpos":clpos,"f5":f5,"f1":f1,
              "choppy":(b["regime"]=="unknown").values,
              "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
              "yr":pd.to_datetime(b["timestamp"]).dt.year,
              "vol":b["volume"]/b["volume"].rolling(20).mean(),
              "alloc":b["postRebalance_current_allocation"]})
            rows.append(d)
    D=pd.concat(rows)
    dr=D.groupby("coin")["f5"].apply(lambda s: s[D.loc[s.index,"pos"]%5==0].mean()) if False else None
    G=D[D["pos"]%5==0].dropna(subset=["f5"]).copy()
    drift=G.groupby("coin")["f5"].mean()
    G["u5"]=G["f5"]-G["coin"].map(drift)
    out={}
    def tab(df,key):
        g=df.groupby(key)["u5"]
        return pd.DataFrame({"n":g.size(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    G["zq"]=pd.qcut(G["z"],5,labels=False)
    out["u5 by z quintile, choppy"]=tab(G[G.choppy],"zq")
    out["u5 by z quintile, not choppy"]=tab(G[~G.choppy],"zq")
    G["rq"]=pd.qcut(G["rs"],5,labels=False)
    out["u5 by 1d scaled return quintile, choppy"]=tab(G[G.choppy],"rq")
    out["u5 by 1d scaled return quintile, not choppy"]=tab(G[~G.choppy],"rq")
    G["cq"]=pd.qcut(G["clpos"],5,labels=False)
    out["u5 by close position quintile all"]=tab(G,"cq")
    G["gq"]=pd.qcut(G["rng"],5,labels=False)
    out["u5 by range/sd quintile all"]=tab(G,"gq")
    G["vq"]=pd.qcut(G["vol"],5,labels=False)
    out["u5 by rel volume quintile all"]=tab(G,"vq")
    out["u5 by year choppy z<0"]=tab(G[G.choppy&(G.z<0)],"yr")
    out["u5 by coin choppy z<0"]=tab(G[G.choppy&(G.z<0)],"coin")
    # daily: f1 by weekday
    A=D.dropna(subset=["f1"]).copy()
    m=A.groupby("coin")["f1"].mean(); A["u1"]=A["f1"]-A["coin"].map(m)
    g=A.groupby("wd")["u1"]
    out["next-day unusual by weekday"]=pd.DataFrame({"n":g.size(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    # book daily
    bd=[]
    for c,ws in data["days"].items():
        for w,d in ws.items():
            bd.append(d.assign(coin=c,win=w))
    B=pd.concat(bd).dropna(subset=["book_return"])
    out["book mean daily by coin"]=B.groupby("coin")["book_return"].agg(["mean","std","size"])
    out["book by window"]=B.groupby("win")["book_return"].agg(["mean","size"])
    out["share choppy"]=float(D.choppy.mean())
    return out
