def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        allr=[]
        for w,b in wins.items():
            b=b.reset_index(drop=True).copy()
            rng=(b.high-b.low)
            b["rr"]=rng/rng.rolling(20,min_periods=20).mean()
            b["r5"]=b.close/b.close.shift(5)-1
            b["r1"]=b.close/b.close.shift(1)-1
            b["vol20"]=b.r1.rolling(20).std()
            b["z1"]=b.r1/b.vol20.shift(1)
            b["body"]=(b.close-b.open)/rng.replace(0,np.nan)
            b["cl"]=(b.close-b.low)/rng.replace(0,np.nan)
            b["fwd"]=b.close.shift(-3)/b.close-1
            b["fwd1"]=b.close.shift(-1)/b.close-1
            g=b.iloc[::3].copy()
            g["coin"]=coin; g["win"]=w
            g["wd"]=pd.to_datetime(g.timestamp).dt.weekday
            g["day"]=pd.to_datetime(g.timestamp).dt.floor("D")
            allr.append(g)
        d=pd.concat(allr)
        d["ex"]=d.fwd-d.fwd.mean()
        d["sdc"]=d.fwd.std()
        d["volq"]=pd.qcut(d.vol20.rank(method="first"),3,labels=["lowvol","midvol","highvol"])
        rows.append(d)
    d=pd.concat(rows).dropna(subset=["ex","rr","r5"])
    def summ(gb):
        x=gb["ex"].agg(["mean","count","std"])
        x["t"]=x["mean"]/(x["std"]/np.sqrt(x["count"]))
        return x.round(4)
    out={}
    d["up"]=np.where(d.r5>0,"up5","down5")
    d["rrq"]=pd.qcut(d.rr,5,labels=False)
    out["rr quintile x run dir"]=summ(d.groupby(["up","rrq"]))
    d["flat"]=pd.cut(d.body.abs(),[-.01,.25,.6,1.01],labels=["flatclose","mid","bigbody"])
    out["wide(rr top q) by body, run"]=summ(d[d.rrq==4].groupby(["up","flat"]))
    d["clq"]=pd.cut(d.cl,[-.01,.33,.66,1.01],labels=["closeLow","closeMid","closeHigh"])
    out["wide by closeloc, run"]=summ(d[d.rrq==4].groupby(["up","clq"]))
    d["z1q"]=pd.qcut(d.z1,7,labels=False)
    out["1d z-move septile"]=summ(d.groupby("z1q"))
    d["r5q"]=pd.qcut(d.r5/ d.vol20,5,labels=False)
    out["r5/vol quintile"]=summ(d.groupby("r5q"))
    out["vol tercile"]=summ(d.groupby("volq"))
    out["weekday"]=summ(d.groupby("wd"))
    d["fq"]=pd.qcut(d.forecast.rank(method="first"),10,labels=False)
    out["forecast decile (all grid)"]=summ(d[d.forecast>0].groupby(pd.qcut(d[d.forecast>0].forecast.rank(method="first"),5,labels=False)))
    out["coin"]=summ(d.groupby("coin"))
    return out
