def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            d=pd.DataFrame({"coin":coin,"win":w})
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float); o=b["open"].astype(float)
            d=pd.DataFrame({"coin":coin,"win":w,"ts":pd.to_datetime(b["timestamp"])})
            d["ret"]=c/c.shift(1)-1
            d["nxt"]=c.shift(-1)/c-1
            d["nxt3"]=c.shift(-3)/c-1
            rng=(h-l)
            d["nearlow"]=np.where(rng>0,(h-c)/rng,np.nan)
            d["rngpct"]=rng/c
            d["ret5"]=c/c.shift(5)-1
            d["vol20"]=d["ret"].rolling(20).std()
            d["tr60"]=c/c.shift(60)-1
            d["alloc"]=b["postRebalance_current_allocation"].astype(float)
            d["lowgap"]=(l/c.shift(1)-1)
            d["wd"]=d["ts"].dt.weekday
            d["year"]=d["ts"].dt.year
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["gain"]=D["alloc"]*D["nxt"]
    hold=D.groupby("coin")["nxt"].mean()
    D["ex"]=D["nxt"]-D["coin"].map(hold)
    def summ(g,col="ex"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    D["rq"]=D.groupby("coin")["ret"].transform(lambda s: pd.qcut(s.rank(method="first"),10,labels=False))
    out["next ex by day-return decile"]=D.groupby("rq").apply(summ)
    D["down"]=D["ret"]<0
    D["nlq"]=D.groupby(["coin","down"])["nearlow"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["next ex by down x nearlow quintile"]=D.groupby(["down","nlq"]).apply(summ)
    D["rgq"]=D.groupby("coin")["rngpct"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["down days next ex by range quintile"]=D[D.down].groupby("rgq").apply(summ)
    out["all days next ex by range quintile"]=D.groupby("rgq").apply(summ)
    out["down days nxt3 by nearlow q"]=D[D.down].groupby("nlq").apply(lambda g: summ(g.iloc[::1],"nxt3"))
    out["next ex by weekday"]=D.groupby("wd").apply(summ)
    D["vq"]=D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    out["down days next ex by vol tercile x nearlow top/bot"]=D[D.down&D.nlq.isin([0,4])].groupby(["vq","nlq"]).apply(summ)
    D["tr"]=pd.cut(D["tr60"],[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    out["down days ex by trend x nlq top/bot"]=D[D.down&D.nlq.isin([0,4])].groupby(["tr","nlq"]).apply(summ)
    D["r5q"]=D.groupby("coin")["ret5"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["next ex by 5d return quintile"]=D.groupby("r5q").apply(summ)
    out["by coin down nearlow top-bot"]=D[D.down&D.nlq.isin([0,4])].groupby(["coin","nlq"])["ex"].mean().unstack()*100
    out["by year down top quintile"]=D[D.down&(D.nlq==4)].groupby("year").apply(summ)
    return out
