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
            nxt2=c.shift(-2)/c-1
            d=pd.DataFrame({"coin":coin,"w":w,"ret":r,"loc":loc,"width":width,"nxt":nxt,
                            "nxt2":nxt2,"inprof":(b["regime"]!="chop"),"regime":b["regime"],
                            "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                            "rz":r/sd,"vol":sd,"year":pd.to_datetime(b["timestamp"]).dt.year,"ts":b["timestamp"]})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["nxt"].mean()
    D["ex"]=D["nxt"]-D["coin"].map(mu)
    D=D.dropna(subset=["ex","loc","width"])
    def summ(g):
        x=g["ex"]
        return pd.Series({"n":len(x),"mean%":x.mean()*100,"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    D["locb"]=pd.cut(D["loc"],[0,.2,.4,.6,.8,1.0001],include_lowest=True)
    D["widthb"]=pd.qcut(D["width"],4)
    out={}
    out["regime counts"]=D["regime"].value_counts()
    out["prof x loc"]=D.groupby(["inprof","locb"]).apply(summ)
    out["prof x width x lowclose"]=D[D["loc"]<0.2].groupby(["inprof","widthb"]).apply(summ)
    out["prof x width x highclose"]=D[D["loc"]>0.8].groupby(["inprof","widthb"]).apply(summ)
    D["rzb"]=pd.cut(D["rz"],[-99,-2,-1,0,1,2,99])
    out["prof x rz"]=D.groupby(["inprof","rzb"]).apply(summ)
    out["all rz"]=D.groupby("rzb").apply(summ)
    out["weekday"]=D.groupby("wd").apply(summ)
    D["volb"]=D.groupby("coin")["vol"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    out["vol tercile x rz sign"]=D.groupby(["volb",np.sign(D["rz"])]).apply(summ)
    # graded corr within profile
    P=D[D["inprof"]]
    P2=P.assign(sig=(P["loc"]-0.5)*P["width"])
    out["corr sig nxt prof"]=float(stats.spearmanr(P2["sig"],P2["ex"]).correlation)
    out["n prof"]=len(P2)
    A=D.assign(sig=(D["loc"]-0.5)*D["width"])
    out["corr sig nxt all"]=float(stats.spearmanr(A["sig"],A["ex"]).correlation)
    out["corr sig nxt out"]=float(stats.spearmanr(A[~A.inprof]["sig"],A[~A.inprof]["ex"]).correlation)
    return out
