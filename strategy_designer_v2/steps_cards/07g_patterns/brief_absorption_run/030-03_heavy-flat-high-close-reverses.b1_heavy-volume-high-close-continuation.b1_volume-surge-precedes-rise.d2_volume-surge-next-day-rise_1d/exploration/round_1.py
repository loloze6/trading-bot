def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            c=b["close"].astype(float)
            allr.append((c.shift(-1)/c-1).dropna())
        mu=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.copy()
            c=b["close"].astype(float); v=b["volume"].astype(float)
            d=pd.DataFrame({"coin":coin,"win":w})
            d["fwd"]=(c.shift(-1)/c-1)
            d["ex"]=d["fwd"]-mu
            d["fwd3"]=c.shift(-3)/c-1
            d["vr"]=v/v.shift(1).rolling(20).mean()
            rng=(b["high"]-b["low"]).astype(float)
            d["clv"]=((c-b["low"])/rng).where(rng>0)
            d["r0"]=c/c.shift(1)-1
            d["r5"]=c/c.shift(5)-1
            d["vol20"]=d["r0"].rolling(20).std()
            d["rngp"]=rng/c
            d["fc"]=b["forecast"].astype(float)
            d["alloc"]=b["postRebalance_current_allocation"].astype(float)
            d["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            d["yr"]=pd.to_datetime(b["timestamp"]).dt.year
            d["pos3"]=np.arange(len(d))%3
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    def g(df,key):
        x=df.dropna(subset=["ex"])
        r=x.groupby(key,observed=True)["ex"].agg(["count","mean","std"])
        r["t"]=r["mean"]/(r["std"]/np.sqrt(r["count"]))
        r["mean"]*=100
        return r.drop(columns="std").round(3)
    D["vrq"]=pd.qcut(D["vr"],5,labels=False)
    D["clvt"]=pd.cut(D["clv"],[-.01,1/3,2/3,1.01],labels=False)
    D["r0q"]=D.groupby("coin")["r0"].transform(lambda s: pd.qcut(s,5,labels=False))
    D["r5q"]=D.groupby("coin")["r5"].transform(lambda s: pd.qcut(s,5,labels=False))
    D["volt"]=D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s,3,labels=False))
    D["rngz"]=D["rngp"]/D["vol20"]
    D["rngq"]=pd.qcut(D["rngz"],5,labels=False)
    out={}
    out["vrq"]=g(D,"vrq")
    out["vrq_x_clv"]=g(D,["vrq","clvt"])
    out["r0q"]=g(D,"r0q")
    out["r0q_x_vrtop"]=g(D[D.vrq==4],"r0q")
    out["r5q"]=g(D,"r5q")
    out["volt"]=g(D,"volt")
    out["vrq_x_volt"]=g(D,["volt","vrq"])
    out["wd"]=g(D,"wd")
    out["yr_vrtop"]=g(D[D.vrq>=3],"yr")
    out["rngq"]=g(D,"rngq")
    out["coin_vrtop"]=g(D[D.vrq==4],"coin")
    # 3-day non-overlapping
    x=D[(D.pos3==0)].dropna(subset=["fwd3","vrq"])
    r=x.groupby("vrq")["fwd3"].agg(["count","mean","std"]);r["t"]=r["mean"]/(r["std"]/np.sqrt(r["count"]));r["mean"]*=100
    out["fwd3_by_vrq"]=r.drop(columns="std").round(3)
    return out
