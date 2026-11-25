def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            allr.append(b["close"].pct_change().dropna())
        mu=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c,h,l,o=b["close"],b["high"],b["low"],b["open"]
            rng=(h-l)
            d=pd.DataFrame(index=b.index)
            d["coin"]=coin; d["win"]=w
            d["clv"]=(2*c-h-l)/rng.replace(0,np.nan)
            d["rm"]=rng/rng.shift(1).rolling(20).mean()
            d["r1"]=c.pct_change()
            d["r5p"]=c/c.shift(5)-1
            d["r20p"]=c/c.shift(20)-1
            d["vol20"]=d["r1"].rolling(20).std()
            d["low30"]=(c<=c.rolling(30).min()).astype(float)
            d["pos30"]=(c-l.rolling(30).min())/(h.rolling(30).max()-l.rolling(30).min())
            d["f"]=b["forecast"].values
            d["alloc"]=b["postRebalance_current_allocation"].values
            for k in [1,3,5]:
                d[f"n{k}"]=(c.shift(-k)/c-1)-k*mu
            d["n1raw"]=c.shift(-1)/c-1
            d["gain"]=d["alloc"]*d["n1raw"]
            d["turn"]=(b["postRebalance_current_allocation"]-b["previous_allocation"]).abs().values
            d["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday.values
            d["pos"]=np.arange(len(d))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    def tab(df,g,col="n1"):
        x=df.dropna(subset=[col]).groupby(g,observed=True)[col]
        r=x.agg(["mean","count","std"]); r["t"]=r["mean"]/(r["std"]/np.sqrt(r["count"]))
        r["mean"]=r["mean"]*100
        return r.drop(columns="std").round(3)
    D["clvq"]=pd.qcut(D["clv"],5,labels=False)
    D["rmq"]=pd.qcut(D["rm"],3,labels=False)
    D["r1q"]=pd.qcut(D["r1"],5,labels=False)
    D["r5q"]=pd.qcut(D["r5p"],5,labels=False)
    D["r20q"]=pd.qcut(D["r20p"],3,labels=False)
    D["volq"]=D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s,3,labels=False))
    D["posq"]=pd.qcut(D["pos30"],5,labels=False)
    out={}
    out["rm tercile x clv quint n1"]=tab(D,["rmq","clvq"])
    out["r1 quint n1"]=tab(D,"r1q")
    out["r5 quint n1"]=tab(D,"r5q")
    out["r20 tercile x clv quint n1"]=tab(D,["r20q","clvq"])
    out["pos30 quint n1"]=tab(D,"posq")
    out["vol tercile x clvq n1"]=tab(D,["volq","clvq"])
    out["weekday n1"]=tab(D,"wd")
    out["coin x clv extreme n1"]=tab(D[D["clvq"].isin([0,4])],["coin","clvq"])
    for k in [3,5]:
        G=D[D["pos"]%k==0]
        out[f"clvq n{k} grid"]=tab(G,"clvq",f"n{k}")
        out[f"r5q n{k} grid"]=tab(G,"r5q",f"n{k}")
    # volatile decline: r20 bottom tercile & vol top tercile, by pos30
    V=D[(D["r20q"]==0)&(D["volq"]==2)]
    out["volatile decline: pos30 quint n1"]=tab(V,"posq")
    G5=V[V["pos"]%5==0]
    out["volatile decline: pos30 quint n5 grid"]=tab(G5,"posq","n5")
    B=D.dropna(subset=["gain"])
    out["book gain % by clvq"]=B.groupby("clvq").agg(gain=("gain","mean"),turn=("turn","mean")).mul(100).round(4)
    out["book gain % by coin"]=B.groupby("coin").agg(gain=("gain","mean"),turn=("turn","mean")).mul(100).round(4)
    out["book gain % by window"]=B.groupby("win")["gain"].mean().mul(100).round(4)
    out["mean turnover %/bar"]=float(B["turn"].mean()*100)
    return out
