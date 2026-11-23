def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            d=pd.DataFrame({"coin":coin,"win":w})
            d["fwd"]=c.shift(-H)/c-1
            d["r1"]=r1
            d["r5"]=c/c.shift(5)-1
            d["r20"]=c/c.shift(20)-1
            d["vol20"]=r1.rolling(20,min_periods=15).std()
            d["vol60"]=r1.rolling(60,min_periods=40).std()
            d["volratio"]=d["vol20"]/d["vol60"]
            d["r1z"]=r1/d["vol20"].shift(1)
            d["r5z"]=d["r5"]/(d["vol20"]*np.sqrt(5))
            d["near"]=c/c.rolling(90,min_periods=30).max()
            d["rng"]=(b["high"]-b["low"])/c/d["vol20"]
            vol=b["volume"].astype(float)
            d["volu"]=np.log(vol/vol.rolling(20,min_periods=15).mean())
            d["fc"]=b["forecast"].astype(float)
            d["wd"]=pd.to_datetime(b["timestamp"]).dt.dayofweek
            d["yr"]=pd.to_datetime(b["timestamp"]).dt.year
            d["grid"]=(np.arange(len(b))%H==0)
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    G=D[D.grid & D.fwd.notna()].copy()
    G["drift"]=G.groupby("coin")["fwd"].transform("mean")
    G["ex"]=G["fwd"]-G["drift"]
    G["usd"]=G.groupby("coin")["fwd"].transform("std")
    G["exs"]=G["ex"]/G["usd"]
    out={}
    def bucket(col,q=5):
        g=G[G[col].notna()].copy()
        g["b"]=g.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"),q,labels=False))
        a=g.groupby("b")["exs"].agg(["mean","count","std"])
        a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
        a["ex_mean_pct"]=g.groupby("b")["ex"].mean()*100
        sp=stats.spearmanr(g[col],g["exs"])
        a.loc["rho","mean"]=sp.correlation; a.loc["rho","t"]=sp.correlation*np.sqrt(len(g))
        return a.round(4)
    for col in ["r1z","r5z","r20","near","vol20","volratio","rng","volu"]:
        out["fwd5 by "+col]=bucket(col)
    a=G.groupby("wd")["exs"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["by weekday"]=a.round(4)
    # forecast groups
    g=G.copy(); g["fb"]=np.where(g.fc==0,"flat",np.where(g.fc>-0.5,"weak","strong"))
    g["neg20"]=g.r20<0
    a=g.groupby(["neg20","fb"])["exs"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["fwd by forecast & r20<0"]=a.round(4)
    # r20 negative interaction with r5z
    g=G[G.r20<0].copy()
    g["b"]=pd.qcut(g["r5z"].rank(method="first"),5,labels=False)
    a=g.groupby("b")["exs"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["r20<0: by r5z"]=a.round(4)
    # book daily
    dd=[]
    for coin,wins in data["days"].items():
        for w,x in wins.items():
            x=x.copy(); x["coin"]=coin; x["win"]=w; dd.append(x)
    DD=pd.concat(dd)
    B=DD.groupby(["win","day"])["book_return"].mean().dropna()
    out["book daily mean,std,n"]=pd.Series({"mean":B.mean(),"std":B.std(),"n":len(B)})
    T=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            if len(t): t=t.copy(); t["coin"]=coin; T.append(t)
    T=pd.concat(T)
    T["dur_d"]=T.duration_minutes/1440
    T["db"]=pd.cut(T.dur_d,[0,5.5,10,20,1000])
    out["trades by duration"]=T.groupby(["side","db"])["net_profit_loss_percent"].agg(["mean","count","median"]).round(3)
    T["ef"]=pd.qcut(T.entry_forecast.rank(method="first"),3,labels=False)
    out["trades by entry fc tercile"]=T.groupby("ef")["net_profit_loss_percent"].agg(["mean","count","median"]).round(3)
    return out
