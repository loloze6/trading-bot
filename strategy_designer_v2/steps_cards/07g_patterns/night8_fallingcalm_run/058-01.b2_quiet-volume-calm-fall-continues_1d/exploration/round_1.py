def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r1=c.pct_change()
            b["fwd"]=c.shift(-H)/c-1
            b["fwd1"]=c.shift(-1)/c-1
            b["r1"]=r1
            b["r5"]=c/c.shift(5)-1
            b["r30"]=c/c.shift(30)-1
            b["r60"]=c/c.shift(60)-1
            b["vol30"]=r1.rolling(30).std()
            b["vrat"]=np.log(v.rolling(30).mean()/v.rolling(90).mean())
            b["vrat5"]=np.log(v.rolling(5).mean()/v.rolling(30).mean())
            b["rng"]=(b["high"]-b["low"])/c
            b["clpos"]=(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            b["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            b["yr"]=pd.to_datetime(b["timestamp"]).dt.year
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["coin"]=coin; b["win"]=w
            g=b.iloc[::H].copy()
            rows.append(g)
    G=pd.concat(rows).dropna(subset=["fwd"])
    drift=G.groupby("coin")["fwd"].transform("mean")
    G["ex"]=G["fwd"]-drift
    G["vol30n"]=G.groupby("coin")["vol30"].transform(lambda s:s.rank(pct=True))
    def summ(df,key):
        o=df.groupby(key)["ex"].agg(["count","mean","std"])
        o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
        return o.round(4)
    out={}
    out["by_regime"]=summ(G,"regime")
    T=G[G.regime=="trending"].copy()
    T["r30q"]=pd.qcut(T["r30"],4,labels=False,duplicates="drop")
    out["trend_by_r30q"]=summ(T,"r30q")
    T["vq"]=pd.qcut(T["vrat"],4,labels=False,duplicates="drop")
    out["trend_by_vrat_q"]=summ(T,"vq")
    for k in ["r30","r5","vrat","vrat5","rng","clpos","vol30n","r1"]:
        out[f"all_q_{k}"]=summ(G.assign(q=pd.qcut(G[k],5,labels=False,duplicates="drop")),"q")
    out["by_wd"]=summ(G,"wd")
    out["by_year"]=summ(G,"yr")
    # trend 60 profile among non-trending
    G["tr"]=np.where(G.r60>0.10,"rising",np.where(G.r60<-0.10,"falling","choppy"))
    G.loc[G.r60.isna(),"tr"]="na"
    out["by_trend60"]=summ(G,"tr")
    out["trend60_x_r5q"]=G.assign(q=pd.qcut(G.r5,3,labels=False)).groupby(["tr","q"])["ex"].agg(["count","mean"]).round(4)
    # book
    D=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            d=d.copy(); d["coin"]=coin; d["win"]=w; D.append(d)
    D=pd.concat(D)
    bk=D.groupby(["win","day"])[["book_return","coin_return"]].mean().dropna()
    out["book"]=pd.Series({"mean":bk.book_return.mean(),"sd":bk.book_return.std(),"n":len(bk),
        "corr_coin":bk.book_return.corr(bk.coin_return)}).round(5)
    out["book_by_win"]=bk.groupby(level=0)["book_return"].agg(["count","mean","sum"]).round(5)
    return out
