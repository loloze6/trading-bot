def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            allr.append(b["close"].pct_change().dropna())
        mu=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.copy().reset_index(drop=True)
            c,h,l,o=b["close"],b["high"],b["low"],b["open"]
            rng=(h-l)
            d=pd.DataFrame({"coin":coin,"win":w})
            d["clv"]=(2*c-h-l)/rng.replace(0,np.nan)
            d["rm"]=rng/rng.shift(1).rolling(20).mean()
            d["r1"]=c.pct_change()
            d["r5p"]=c/c.shift(5)-1
            d["r20p"]=c/c.shift(20)-1
            d["vol20"]=d["r1"].rolling(20).std()
            d["low30"]=(c<=c.rolling(30).min()).astype(float)
            d["high30"]=(c>=c.rolling(30).max()).astype(float)
            d["pos30"]=(c-l.rolling(30).min())/(h.rolling(30).max()-l.rolling(30).min())
            d["body"]=(c-o)/rng.replace(0,np.nan)
            d["f"]=b["forecast"]
            d["alloc"]=b["postRebalance_current_allocation"]
            for k in [1,2,3,5]:
                d[f"n{k}"]=(c.shift(-k)/c-1)-k*mu
            d["n1raw"]=c.shift(-1)/c-1
            d["gain"]=d["alloc"]*d["n1raw"]
            d["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            d["pos"]=np.arange(len(d))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    def tab(g,col="n1"):
        x=D.dropna(subset=[col]).groupby(g,observed=True)[col]
        r=x.agg(["mean","count","std"]); r["t"]=r["mean"]/(r["std"]/np.sqrt(r["count"]))
        r["mean"]=r["mean"]*100
        return r.drop(columns="std").round(3)
    D["clvq"]=pd.qcut(D["clv"],5,labels=False)
    D["rmq"]=pd.qcut(D["rm"],3,labels=False)
    D["r1q"]=pd.qcut(D["r1"],5,labels=False)
    D["r5q"]=pd.qcut(D["r5p"],5,labels=False)
    D["r20q"]=pd.qcut(D["r20p"],3,labels=False)
    D["volq"]=D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s,3,labels=False))
    D["fq"]=pd.qcut(D["f"],5,labels=False,duplicates="drop")
    D["posq"]=pd.qcut(D["pos30"],5,labels=False)
    out={}
    out["clv quint x rm tercile n1"]=tab(["rmq","clvq"])
    out["r1 quint n1"]=tab("r1q")
    out["r5 quint n1"]=tab("r5q")
    out["r20 tercile x clv quint n1"]=tab(["r20q","clvq"])
    out["pos30 quint n1"]=tab("posq")
    out["low30 / high30 n1"]=tab(["low30","high30"])
    out["vol tercile x clvq n1"]=tab(["volq","clvq"])
    out["weekday n1"]=tab("wd")
    out["forecast quint n1"]=tab("fq")
    # longer horizons on grid
    for k in [3,5]:
        G=D[D["pos"]%k==0].dropna(subset=[f"n{k}","clv"])
        x=G.groupby("clvq")[f"n{k}"].agg(["mean","count","std"]); x["t"]=x["mean"]/(x["std"]/np.sqrt(x["count"])); x["mean"]*=100
        out[f"clvq n{k} grid"]=x.drop(columns="std").round(3)
    out["book gain by weekday %"]=D.groupby("wd")["gain"].mean().mul(100).round(4)
    out["book gain by clvq %"]=D.groupby("clvq")["gain"].mean().mul(100).round(4)
    return out
