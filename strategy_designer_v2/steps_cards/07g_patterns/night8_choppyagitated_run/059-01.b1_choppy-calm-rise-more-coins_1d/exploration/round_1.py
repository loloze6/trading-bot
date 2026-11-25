def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; daily=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float)
            r1=c.pct_change()
            vol30=r1.rolling(30,min_periods=20).std()
            z=(c/c.shift(7)-1)/(vol30*np.sqrt(7))
            z1=r1/vol30
            r60=c/c.shift(60)-1
            fwd7=c.shift(-7)/c-1
            fwd1=c.shift(-1)/c-1
            vrank=vol30.rolling(60,min_periods=30).rank(pct=True)
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"z":z,"z1":z1,"r60":r60,
              "fwd7":fwd7,"fwd1":fwd1,"inprof":(b["regime"]=="unknown"),"vrank":vrank,
              "fc":b["forecast"],"alloc":b["postRebalance_current_allocation"],"wd":ts.dt.weekday,"yr":ts.dt.year})
            rows.append(df)
    A=pd.concat(rows)
    A["mean7"]=A.groupby("coin")["fwd7"].transform(lambda s: s[A.loc[s.index,"pos"]%7==0].mean() if False else np.nan)
    G=A[(A.pos%7==0)&A.fwd7.notna()].copy()
    cm=G.groupby("coin")["fwd7"].mean()
    G["ex7"]=G.fwd7-G.coin.map(cm)
    def summ(g,col="ex7"):
        x=g[col].dropna(); n=len(x)
        return pd.Series({"n":n,"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    out={}
    G["zq"]=pd.qcut(G.z,5,labels=False)
    out["ex7 by z quintile, in profile"]=G[G.inprof].groupby("zq").apply(summ)
    out["ex7 by z quintile, outside profile"]=G[~G.inprof].groupby("zq").apply(summ)
    G["trend"]=pd.cut(G.r60,[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    G["agit"]=np.where(G.vrank>0.5,"hi","lo")
    out["ex7 by trend x zq"]=G.groupby(["trend","zq"]).apply(summ).unstack()["t"]
    out["ex7 by trend x zq mean"]=G.groupby(["trend","zq"]).apply(summ).unstack()["mean"]
    out["ex7 by agit x zq t"]=G.groupby(["agit","zq"]).apply(summ).unstack()["t"]
    out["ex7 by agit x zq mean"]=G.groupby(["agit","zq"]).apply(summ).unstack()["mean"]
    G["z1q"]=pd.qcut(G.z1,5,labels=False)
    out["ex7 by 1-day scaled move quintile"]=G.groupby("z1q").apply(summ)
    D=A[A.fwd1.notna()].copy()
    cm1=D.groupby("coin")["fwd1"].mean(); D["ex1"]=D.fwd1-D.coin.map(cm1)
    D["z1q"]=pd.qcut(D.z1,5,labels=False)
    out["next-day ex by 1-day scaled move q"]=D.groupby("z1q").apply(lambda g:summ(g,"ex1"))
    out["next-day ex by weekday"]=D.groupby("wd").apply(lambda g:summ(g,"ex1"))
    out["ex7 by year, in profile z>0"]=G[G.inprof&(G.z>0)].groupby("yr").apply(summ)
    out["ex7 by coin, in profile z>0"]=G[G.inprof&(G.z>0)].groupby("coin").apply(summ)
    return out
