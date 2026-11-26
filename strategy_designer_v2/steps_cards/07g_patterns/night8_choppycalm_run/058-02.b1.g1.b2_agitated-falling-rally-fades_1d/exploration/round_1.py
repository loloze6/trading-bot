def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            d=pd.DataFrame({"coin":coin,"win":w,"ts":pd.to_datetime(b["timestamp"]),
                "ret":r,"nxt":c.shift(-1)/c-1,"nxt3":c.shift(-3)/c-1,
                "sd20":r.rolling(20).std(),"tr60":c/c.shift(60)-1,
                "rng":(b["high"]-b["low"])/c,"clpos":(c-b["low"])/(b["high"]-b["low"]),
                "reg":b["regime"].astype(str),"alloc":b["postRebalance_current_allocation"].astype(float),
                "pos":np.arange(len(b))})
            d["z"]=d["ret"]/d["sd20"]
            d["vol_rel"]=d["sd20"]/r.rolling(60).std()
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["mu"]=D.groupby("coin")["nxt"].transform("mean")
    D["ex"]=D["nxt"]-D["mu"]
    D["fa"]=D["reg"]=="unknown"
    def tab(g,col="ex"):
        a=g[col].dropna()
        return pd.Series({"n":len(a),"mean%":a.mean()*100,"t":a.mean()/(a.std()/np.sqrt(len(a))) if len(a)>2 else np.nan})
    out={}
    D["zq"]=pd.cut(D["z"],[-99,-2,-1,-0.3,0.3,1,2,99])
    out["regime_share"]=D["reg"].value_counts(normalize=True)
    out["z_bucket_by_FA"]=D.groupby(["fa","zq"]).apply(tab).reset_index()
    D["tr"]=pd.cut(D["tr60"],[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    out["z_bucket_by_trend60"]=D.groupby(["tr","zq"]).apply(tab).reset_index()
    D["wd"]=D["ts"].dt.dayofweek
    out["weekday_all"]=D.groupby("wd").apply(tab)
    D["cq"]=pd.cut(D["clpos"],[-0.01,0.2,0.4,0.6,0.8,1.01])
    out["closepos_by_trend"]=D.groupby(["tr","cq"]).apply(tab).reset_index()
    # 3-day grid
    G=D[D["pos"]%3==0].copy()
    G["ex3"]=G["nxt3"]-G.groupby("coin")["nxt3"].transform("mean")
    out["z_bucket_3d_FA"]=G.groupby(["fa","zq"]).apply(lambda g:tab(g,"ex3")).reset_index()
    # book
    dd=[]
    for coin,wins in data["days"].items():
        for w,x in wins.items():
            x=x.copy();x["coin"]=coin;x["win"]=w;dd.append(x)
    Y=pd.concat(dd)
    Y["yr"]=pd.to_datetime(Y["day"]).dt.year
    out["book_by_year"]=Y.groupby("yr").agg(br=("book_return","mean"),cr=("coin_return","mean"),n=("book_return","count"))
    out["book_by_coin"]=Y.groupby("coin").agg(br=("book_return","mean"),sd=("book_return","std"))
    return out
