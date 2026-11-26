def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]
            r=c.pct_change()
            sd30=r.rolling(30,min_periods=20).std()
            hi14=c.rolling(14).max()
            df=pd.DataFrame({
                "coin":coin,"win":w,
                "fc":b["forecast"],"reg":b["regime"],
                "alloc":b["postRebalance_current_allocation"],
                "r1":r,"r1z":r/sd30,
                "ret14z":(c/c.shift(14)-1)/sd30,
                "depth":(c-hi14)/hi14/sd30,
                "ret5z":(c/c.shift(5)-1)/sd30,
                "sd30":sd30,
                "rng":(b["high"]-b["low"])/c/sd30,
                "clv":(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan),
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr":pd.to_datetime(b["timestamp"]).dt.year,
                "f5":c.shift(-5)/c-1,
            })
            df["pos"]=np.arange(len(df))
            df["grid"]=(df["pos"]%5==0)
            df["sdq"]=sd30/ r.rolling(len(df),min_periods=20).std()
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    drift=A[A.grid].groupby("coin")["f5"].mean()
    usual=A[A.grid].groupby("coin")["f5"].std()
    A["u5"]=(A["f5"]-A["coin"].map(drift))
    A["u5s"]=A["u5"]/A["coin"].map(usual)
    G=A[A.grid].dropna(subset=["u5"])
    out={}
    def tab(g,col,q=5):
        g=g.dropna(subset=[col]).copy()
        g["b"]=pd.qcut(g[col],q,labels=False,duplicates="drop")
        t=g.groupby("b").agg(n=("u5","size"),lo=(col,"min"),hi=(col,"max"),
            u5=("u5","mean"),u5s=("u5s","mean"))
        t["t"]=g.groupby("b")["u5"].apply(lambda x: x.mean()/(x.std()/np.sqrt(len(x))))
        return t.round(4)
    out["regime counts grid"]=G["reg"].value_counts()
    out["by regime u5"]=G.groupby("reg")["u5"].agg(["size","mean","std"]).assign(t=lambda d:d["mean"]/(d["std"]/np.sqrt(d["size"]))).round(4)
    out["depth quint, unknown(falling calm)"]=tab(G[G.reg=="unknown"],"depth")
    out["depth quint, chop(other)"]=tab(G[G.reg=="chop"],"depth")
    out["r1z quint all"]=tab(G,"r1z")
    out["ret5z quint all"]=tab(G,"ret5z")
    out["ret14z quint all"]=tab(G,"ret14z")
    out["rng quint all"]=tab(G,"rng")
    out["clv quint all"]=tab(G,"clv")
    out["ret14z quint chop"]=tab(G[G.reg=="chop"],"ret14z")
    out["weekday"]=G.groupby("wd")["u5"].agg(["size","mean"]).round(4)
    out["year"]=G.groupby("yr")["u5"].agg(["size","mean"]).round(4)
    out["coin"]=G.groupby("coin")["u5"].agg(["size","mean"]).round(4)
    # book daily
    D=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            d=d.copy(); d["coin"]=coin; d["win"]=w; D.append(d)
    D=pd.concat(D)
    out["book ret by window"]=D.groupby("win").agg(book=("book_return","mean"),coin=("coin_return","mean")).round(5)
    out["book ret by coin"]=D.groupby("coin").agg(book=("book_return","mean"),coin=("coin_return","mean")).round(5)
    # active short positions: unusual by depth quint
    act=G[G.alloc<0]
    out["active short cases depth quint"]=tab(act,"depth",4)
    return out
