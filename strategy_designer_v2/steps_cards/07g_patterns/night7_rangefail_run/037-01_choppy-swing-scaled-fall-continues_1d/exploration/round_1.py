def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd20=r.rolling(20).std()
            ret5=c/c.shift(5)-1
            ret1=r
            ret20=c/c.shift(20)-1
            fwd5=c.shift(-5)/c-1
            fwd1=c.shift(-1)/c-1
            rng=(b["high"]-b["low"])/c
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"z5":ret5/(sd20*np.sqrt(5)),
                             "z1":ret1/sd20,"z20":ret20/(sd20*np.sqrt(20)),"sd20":sd20,"fwd5":fwd5,"fwd1":fwd1,
                             "regime":b["regime"].values,"fc":b["forecast"].values,
                             "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                             "rngz":rng/sd20,
                             "alloc":b["postRebalance_current_allocation"].values})
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    G=A[(A.pos%5==0)&A.fwd5.notna()].copy()
    drift=G.groupby("coin").fwd5.mean()
    G["u"]=G.fwd5-G.coin.map(drift)
    G["sdrel"]=G.sd20/G.groupby("coin").sd20.transform("median")
    G["choppy"]=G.regime=="unknown"
    def tab(g,key):
        o=g.groupby(key).u.agg(["mean","count","std"])
        o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
        return o[["mean","count","t"]].round(4)
    H=G.dropna(subset=["z5"]).copy()
    H["z5q"]=pd.qcut(H.z5,5,labels=False)
    H["z1q"]=pd.qcut(H.z1,5,labels=False)
    H["z20q"]=pd.qcut(H.z20,5,labels=False)
    H["volq"]=pd.qcut(H.sdrel,3,labels=False)
    H["rngq"]=pd.qcut(H.rngz,5,labels=False)
    out={}
    out["z5 quintile x choppy"]=tab(H,["choppy","z5q"])
    out["z1 quintile x choppy"]=tab(H,["choppy","z1q"])
    out["z20 quintile x choppy"]=tab(H,["choppy","z20q"])
    out["vol tercile x choppy"]=tab(H,["choppy","volq"])
    out["range quintile"]=tab(H,"rngq")
    out["z5q x volq"]=tab(H,["volq","z5q"])
    out["weekday"]=tab(H,"wd")
    out["window"]=tab(H,"w")
    # daily book
    D=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            dd=d.copy(); dd["coin"]=coin; dd["w"]=w; D.append(dd)
    D=pd.concat(D)
    D["wd"]=pd.to_datetime(D["day"]).dt.weekday
    out["book by weekday"]=D.groupby("wd").book_return.agg(["mean","count"])
    out["book by window"]=D.groupby("w").book_return.agg(["mean","count"])
    # correlation of fc with fwd in choppy all bars nonoverlap
    C=H[H.choppy]
    out["spearman z5 vs u choppy"]=float(stats.spearmanr(C.z5,C.u).correlation)
    out["spearman z5 vs u nonchoppy"]=float(stats.spearmanr(H[~H.choppy].z5,H[~H.choppy].u).correlation)
    out["n choppy/non"]=f"{len(C)}/{(~H.choppy).sum()}"
    return out
