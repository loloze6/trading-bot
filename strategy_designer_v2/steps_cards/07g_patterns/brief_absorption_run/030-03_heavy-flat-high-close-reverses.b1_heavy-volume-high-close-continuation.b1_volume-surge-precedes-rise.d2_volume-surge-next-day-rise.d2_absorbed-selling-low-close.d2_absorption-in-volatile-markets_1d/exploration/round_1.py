def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            d=pd.DataFrame({"coin":coin,"win":w})
            d["dist_high"]=(b["high"]-c)/rng
            d["volr"]=b["volume"]/b["volume"].shift(1).rolling(20).mean()
            v20=r.rolling(20).std()
            d["vr"]=v20/v20.rolling(60).mean()
            d["v20"]=v20
            d["r1"]=r
            d["r5p"]=c/c.shift(5)-1
            d["f1"]=c.shift(-1)/c-1
            d["f3"]=c.shift(-3)/c-1
            d["pos3"]=(np.arange(len(b))%3==0)
            d["active"]=(b["regime"]=="mean_reversion").values
            d["fc"]=b["forecast"].values
            d["alloc"]=b["postRebalance_current_allocation"].values
            d["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            d["yr"]=pd.to_datetime(b["timestamp"]).dt.year
            d["absr"]=(c/b["open"]-1).abs()
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["f1"].transform("mean")
    D["x1"]=D["f1"]-mu
    mu3=D[D.pos3].groupby("coin")["f3"].mean()
    D["x3"]=D["f3"]-D["coin"].map(mu3)
    D["ux"]=D["x1"]/D.groupby("coin")["f1"].transform("std")
    out={}
    def tab(g,col="x1",sub=None):
        S=D if sub is None else sub
        a=S.dropna(subset=[col]).groupby(g)[col].agg(["mean","count","std"])
        a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
        return a.drop(columns="std")
    D["clq"]=pd.qcut(D["dist_high"],5,labels=False)
    D["vq"]=pd.qcut(D["volr"],3,labels=False)
    D["vrq"]=pd.qcut(D["vr"],3,labels=False)
    out["dist_high quint x act"]=tab(["active","clq"])
    out["dist_high quint x volr terc"]=tab(["vq","clq"]).unstack(0)["t"]
    out["dist_high quint x vr terc, t"]=tab(["vrq","clq"]).unstack(0)["t"]
    out["dist_high quint x vr terc, mean"]=tab(["vrq","clq"]).unstack(0)["mean"]
    out["3d after, dist_high quint (grid)"]=tab(["active","clq"],"x3",D[D.pos3])
    D["r1q"]=pd.qcut(D["r1"],5,labels=False)
    out["after day return quint x vr terc t"]=tab(["vrq","r1q"]).unstack(0)["t"]
    D["absq"]=pd.qcut(D["absr"],3,labels=False)
    out["clq x |body| terc t"]=tab(["absq","clq"]).unstack(0)["t"]
    out["weekday"]=tab("wd")
    out["weekday active long"]=tab("wd",sub=D[D.alloc>0])
    D["r5q"]=pd.qcut(D["r5p"],5,labels=False)
    out["after 5d return quint x act"]=tab(["active","r5q"])
    out["year x active long"]=tab(["yr"],sub=D[D.alloc>0])
    out["coin clq slope t"]=pd.Series({c:stats.linregress(g.dropna(subset=["dist_high","x1"])["dist_high"],g.dropna(subset=["dist_high","x1"])["x1"]).slope/ stats.linregress(g.dropna(subset=["dist_high","x1"])["dist_high"],g.dropna(subset=["dist_high","x1"])["x1"]).stderr for c,g in D.groupby("coin")})
    return out
