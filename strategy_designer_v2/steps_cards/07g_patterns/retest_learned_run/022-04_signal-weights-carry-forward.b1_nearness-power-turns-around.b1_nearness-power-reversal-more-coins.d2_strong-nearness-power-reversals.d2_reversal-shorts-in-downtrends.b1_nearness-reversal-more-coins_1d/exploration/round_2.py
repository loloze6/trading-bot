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
            d=pd.DataFrame(index=b.index)
            d["coin"]=coin; d["win"]=w
            d["fwd"]=c.shift(-H)/c-1
            d["r1"]=r1
            d["r5"]=c/c.shift(5)-1
            d["r20"]=c/c.shift(20)-1
            d["vol20"]=r1.rolling(20,min_periods=15).std()
            d["vol60"]=r1.rolling(60,min_periods=40).std()
            d["volratio"]=d["vol20"]/d["vol60"]
            d["r1z"]=r1/d["vol20"].shift(1)
            d["r5z"]=d["r5"]/(d["vol20"]*np.sqrt(5))
            d["r20z"]=d["r20"]/(d["vol60"]*np.sqrt(20))
            d["near"]=c/c.rolling(90,min_periods=30).max()
            d["rng"]=(b["high"].astype(float)-b["low"].astype(float))/c/d["vol20"]
            vol=b["volume"].astype(float).replace(0,np.nan)
            d["volu"]=np.log(vol/vol.rolling(20,min_periods=15).mean())
            d["fc"]=b["forecast"].astype(float)
            d["alloc"]=b["postRebalance_current_allocation"].astype(float)
            ts=pd.to_datetime(b["timestamp"])
            d["wd"]=ts.dt.dayofweek.values
            d["yr"]=ts.dt.year.values
            d["grid"]=(np.arange(len(b))%H==0)
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    G=D[D.grid & D.fwd.notna()].copy()
    G["drift"]=G.groupby("coin")["fwd"].transform("mean")
    G["ex"]=G["fwd"]-G["drift"]
    G["usd"]=G.groupby("coin")["fwd"].transform("std")
    G["exs"]=G["ex"]/G["usd"]
    out={}
    def tab(g,key):
        a=g.groupby(key)["exs"].agg(["mean","count","std"])
        a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
        a["ex_pct"]=g.groupby(key)["ex"].mean()*100
        return a.round(4)
    def bucket(col,g0=None,q=5):
        g=(G if g0 is None else g0)
        g=g[g[col].notna()].copy()
        g["b"]=g.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"),q,labels=False))
        a=tab(g,"b")
        sp=stats.spearmanr(g[col],g["exs"])
        a.loc["rho","mean"]=sp.correlation; a.loc["rho","t"]=sp.correlation*np.sqrt(len(g)); a.loc["rho","count"]=len(g)
        return a.round(4)
    for col in ["r1z","r5z","r20z","near","vol20","volratio","rng","volu"]:
        try: out["fwd5 by "+col]=bucket(col)
        except Exception as e: out["err "+col]=str(e)[:80]
    try: out["by weekday"]=tab(G,"wd")
    except Exception as e: out["err wd"]=str(e)[:80]
    try:
        g=G[G.r20<0]
        for col in ["r5z","near","volratio"]:
            out["r20<0: by "+col]=bucket(col,g)
        g=G[G.r20>=0]
        out["r20>=0: by r5z"]=bucket("r5z",g)
    except Exception as e: out["err cond"]=str(e)[:80]
    try:
        g=G.copy(); g["fb"]=np.where(g.fc==0,"flat",np.where(g.fc>-0.5,"weak","strong"))
        g["neg20"]=g.r20<0
        out["fwd by r20<0 & forecast"]=tab(g,["neg20","fb"])
        g2=g[g.fc<0].copy()
        out["active cases by year"]=tab(g2,"yr")
    except Exception as e: out["err fc"]=str(e)[:80]
    try:
        dd=[]
        for coin,wins in data["days"].items():
            for w,x in wins.items():
                x=x.copy(); x["coin"]=coin; x["win"]=w; dd.append(x)
        DD=pd.concat(dd)
        B=DD.groupby(["win","day"])["book_return"].mean().dropna()
        out["book daily mean,std,n"]=pd.Series({"mean":B.mean(),"std":B.std(),"n":float(len(B))})
        C=DD.groupby(["win","day"])["coin_return"].mean().reindex(B.index)
        k=max(1,int(len(B)*0.02))
        top=B.nlargest(k).index; bot=B.nsmallest(k).index
        out["coins' mean return on book's best/worst 2% days"]=pd.Series({"best_book":B.loc[top].mean(),"coin_on_best":C.loc[top].mean(),"worst_book":B.loc[bot].mean(),"coin_on_worst":C.loc[bot].mean()})
    except Exception as e: out["err book"]=str(e)[:80]
    try:
        T=[]
        for coin,wins in data["trades"].items():
            for w,t in wins.items():
                if len(t): t=t.copy(); t["coin"]=coin; T.append(t)
        T=pd.concat(T,ignore_index=True)
        T["dur_d"]=T.duration_minutes/1440
        T["db"]=pd.cut(T.dur_d,[0,5.5,10,20,1000]).astype(str)
        out["trades by duration"]=T.groupby(["side","db"])["net_profit_loss_percent"].agg(["mean","count","median"]).round(3)
        T["ef"]=pd.qcut(T.entry_forecast.rank(method="first"),3,labels=False)
        out["trades by entry fc tercile"]=T.groupby("ef")["net_profit_loss_percent"].agg(["mean","count","median"]).round(3)
    except Exception as e: out["err trades"]=str(e)[:80]
    return out
