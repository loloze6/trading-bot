import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        allnext=[]
        frames=[]
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            vol=r.rolling(20).std().shift(1)
            z=r/vol
            nxt=c.shift(-1)/c-1
            f3=c.shift(-3)/c-1
            hi20=b["high"].rolling(20).max()
            dist=c/hi20-1
            vr=b["volume"]/b["volume"].rolling(20).mean().shift(1)
            r5=c/c.shift(5)-1
            d=pd.DataFrame({"z":z,"nxt":nxt,"f3":f3,"dist":dist,"vr":vr,"vol":vol,"r5":r5,
                            "fc":b["forecast"],"alloc":b["postRebalance_current_allocation"],
                            "wd":pd.to_datetime(b["timestamp"]).dt.dayofweek,"pos":np.arange(len(b)),
                            "year":pd.to_datetime(b["timestamp"]).dt.year})
            d["coin"]=coin; d["win"]=w
            frames.append(d)
        D=pd.concat(frames)
        D["ex"]=D["nxt"]-D["nxt"].mean()
        D["ex3"]=D["f3"]-D.loc[D.pos%3==0,"f3"].mean()
        D["volq"]=D.groupby("coin")["vol"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop")) if False else np.nan
        rows.append(D)
    A=pd.concat(rows)
    A["volq"]=A.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    def summ(g,col="ex"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    A["zb"]=pd.cut(A["z"],[-np.inf,-2.5,-1.5,-0.75,0,0.75,1.5,2.5,np.inf])
    out["next1 by z bucket"]=A.groupby("zb").apply(summ)
    A3=A[A.pos%3==0]
    out["next3 by z bucket (grid)"]=A3.groupby("zb").apply(lambda g: summ(g,"ex3"))
    A["db"]=pd.qcut(A["dist"],5)
    out["next1 by dist to 20d high"]=A.groupby("db").apply(summ)
    out["down-day (z<0) next1 by volq"]=A[A.z<0].groupby("volq").apply(summ)
    out["up-day (z>0) next1 by volq"]=A[A.z>0].groupby("volq").apply(summ)
    out["next1 by weekday"]=A.groupby("wd").apply(summ)
    A["vrb"]=pd.qcut(A["vr"],4)
    out["z<-1 next1 by volume ratio"]=A[A.z<-1].groupby("vrb").apply(summ)
    out["z>1 next1 by volume ratio"]=A[A.z>1].groupby("vrb").apply(summ)
    A["r5b"]=pd.qcut(A["r5"],5)
    out["next1 by 5d return"]=A.groupby("r5b").apply(summ)
    out["z<0 slope t by coin"]=A[A.z<0].groupby("coin").apply(lambda g: pd.Series({"n":g[["z","ex"]].dropna().shape[0],"slope_t":stats.linregress(g[["z","ex"]].dropna()["z"],g[["z","ex"]].dropna()["ex"]).slope/stats.linregress(g[["z","ex"]].dropna()["z"],g[["z","ex"]].dropna()["ex"]).stderr}))
    out["z<0 next1 by year"]=A[A.z<0].groupby("year").apply(summ)
    # book
    bd=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            d=d.copy(); d["coin"]=coin; d["win"]=w; bd.append(d)
    B=pd.concat(bd)
    P=B.groupby(["win","day"])[["book_return","coin_return"]].mean().dropna()
    P["wd"]=pd.to_datetime(P.index.get_level_values("day")).dayofweek
    out["book daily by weekday"]=P.groupby("wd")["book_return"].agg(["count","mean"])
    q=P["book_return"].quantile([0.02,0.98])
    out["coin_ret on book worst2%/best2%"]=pd.Series({"worst_book_mean":P.loc[P.book_return<=q.iloc[0],"book_return"].mean(),"worst_coin":P.loc[P.book_return<=q.iloc[0],"coin_return"].mean(),"best_book":P.loc[P.book_return>=q.iloc[1],"book_return"].mean(),"best_coin":P.loc[P.book_return>=q.iloc[1],"coin_return"].mean()})
    out["book by window"]=P.groupby(level="win")["book_return"].agg(["count","mean"]).T
    return out
