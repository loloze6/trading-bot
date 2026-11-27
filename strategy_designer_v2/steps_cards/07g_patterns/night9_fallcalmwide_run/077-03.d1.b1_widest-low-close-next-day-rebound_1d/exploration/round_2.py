import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            rng=(b["high"]-b["low"])
            loc=(b["close"]-b["low"])/rng.replace(0,np.nan)
            width=(rng/b["close"].shift(1))/sd
            nxt=c.shift(-1)/c-1
            tr60=(c/c.shift(60)-1)*100
            tr20=(c/c.shift(20)-1)*100
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"ret":r,"loc":loc,"width":width,"nxt":nxt,
                            "tr60":tr60,"tr20":tr20,"rz":r/sd,"vol":sd,"day":ts.dt.floor("D"),
                            "wd":ts.dt.weekday,"year":ts.dt.year})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["nxt"].mean()
    D["ex"]=D["nxt"]-D["coin"].map(mu)
    D=D.dropna(subset=["ex","loc","width"])
    D["volb"]=D.groupby("coin")["vol"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    D["trend"]=pd.cut(D["tr60"],[-1e9,-10,10,1e9],labels=["falling","choppy","rising"])
    D["agit"]=np.where(D["volb"]==2,"hi","lo")
    def summ(g):
        x=g["ex"]
        ds=g.groupby("day")["ex"].sum()
        tday=ds.mean()/(ds.std()/np.sqrt(len(ds))) if len(ds)>2 else np.nan
        return pd.Series({"n":len(x),"days":len(ds),"mean%":x.mean()*100,"t_day":tday})
    D["sig_low"]=(0.5-D["loc"]).clip(lower=0)*D["width"]
    D["sig_high"]=(D["loc"]-0.5).clip(lower=0)*D["width"]
    out={}
    HC=D[(D["loc"]>0.8)]
    HC=HC.assign(wb=pd.qcut(HC["width"],2,labels=["narrow","wide"]))
    out["highclose trend x agit x width"]=HC.groupby(["trend","agit","wb"]).apply(summ)
    LC=D[(D["loc"]<0.2)]
    LC=LC.assign(wb=pd.qcut(LC["width"],2,labels=["narrow","wide"]))
    out["lowclose trend x agit x width"]=LC.groupby(["trend","agit","wb"]).apply(summ)
    UP=D[D["rz"]>0]
    UP=UP.assign(rb=pd.cut(UP["rz"],[0,1,2,99]))
    out["upday trend x agit x size"]=UP.groupby(["trend","agit","rb"]).apply(summ)
    out["upday hi-vol by window"]=UP[UP["agit"]=="hi"].groupby("w").apply(summ)
    out["upday hi-vol by year"]=UP[UP["agit"]=="hi"].groupby("year").apply(summ)
    out["weekday by year wed"]=D[D["wd"]==2].groupby("year").apply(summ)
    # graded corr up-day size vs next in hi vol
    U=UP[UP["agit"]=="hi"]
    out["spearman rz vs ex, hi-vol upday"]=float(stats.spearmanr(U["rz"],U["ex"]).correlation)
    out["spearman sig_high vs ex, hi-vol"]=float(stats.spearmanr(D[D.agit=="hi"]["sig_high"],D[D.agit=="hi"]["ex"]).correlation)
    out["spearman ret vs ex hi-vol all"]=float(stats.spearmanr(D[D.agit=="hi"]["rz"],D[D.agit=="hi"]["ex"]).correlation)
    out["spearman ret vs ex lo-vol all"]=float(stats.spearmanr(D[D.agit=="lo"]["rz"],D[D.agit=="lo"]["ex"]).correlation)
    out["hi-vol up by coin"]=UP[UP["agit"]=="hi"].groupby("coin").apply(summ)
    return out
