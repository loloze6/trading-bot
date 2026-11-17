def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,df in ws.items():
            c=df["close"].astype(float).reset_index(drop=True)
            allr.append(c.pct_change())
        mu=pd.concat(allr).mean()
        for w,df in ws.items():
            d=df.reset_index(drop=True)
            c=d["close"].astype(float)
            r1=c.pct_change()
            vol=r1.rolling(20,min_periods=15).std()
            z=r1/vol
            r5=c/c.shift(5)-1
            z5=r5/(vol*np.sqrt(5))
            vr=d["volume"]/d["volume"].rolling(20,min_periods=15).mean()
            volrel=vol/vol.rolling(120,min_periods=40).mean()
            ts=pd.to_datetime(d["timestamp"])
            f1=c.shift(-1)/c-1-mu
            f3=c.shift(-3)/c-1-3*mu
            pos=d["postRebalance_current_allocation"].astype(float)
            t=pd.DataFrame({"coin":coin,"w":w,"i":np.arange(len(d)),"z":z,"z5":z5,"vr":vr,"volrel":volrel,
                            "wd":ts.dt.dayofweek,"yr":ts.dt.year,"f1":f1,"f3":f3,"pos":pos,"pnl":pos*(c.shift(-1)/c-1)})
            rows.append(t)
    A=pd.concat(rows,ignore_index=True)
    def summ(g,col="f1"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    B=A.dropna(subset=["z","f1"]).copy()
    B["zd"]=pd.qcut(B["z"],10,labels=False)
    out={}
    out["f1 by z decile"]=B.groupby("zd").apply(summ)
    G3=A[A["i"]%3==0].dropna(subset=["z","f3"]).copy()
    G3["zd"]=pd.qcut(G3["z"],10,labels=False)
    out["f3 by z decile (nonoverlap)"]=G3.groupby("zd").apply(lambda g:summ(g,"f3"))
    B["z5d"]=pd.qcut(B["z5"],5,labels=False)
    out["f1 by 5d z quintile"]=B.dropna(subset=["z5"]).groupby("z5d").apply(summ)
    out["f1 by weekday"]=B.groupby("wd").apply(summ)
    falls=B[B["zd"]<=1]
    out["f1 big falls by weekday"]=falls.groupby("wd").apply(summ)
    B["vrq"]=pd.qcut(B["vr"],3,labels=False)
    out["f1 big falls by volume tercile"]=B[B["zd"]<=1].groupby("vrq").apply(summ)
    out["f1 big rises by volume tercile"]=B[B["zd"]>=8].groupby("vrq").apply(summ)
    B["vlq"]=pd.qcut(B["volrel"],3,labels=False)
    out["f1 big falls by vol regime"]=B[B["zd"]<=1].groupby("vlq").apply(summ)
    out["f1 by vol regime all"]=B.groupby("vlq").apply(summ)
    out["f1 big falls by coin"]=falls.groupby("coin").apply(summ)
    out["f1 big falls by year"]=falls.groupby("yr").apply(summ)
    out["pnl by weekday"]=A.groupby("wd").apply(lambda g:summ(g,"pnl"))
    return out
