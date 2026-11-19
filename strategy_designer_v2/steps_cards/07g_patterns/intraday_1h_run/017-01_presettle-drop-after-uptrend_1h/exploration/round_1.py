def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            d=df[["timestamp","close","volume","postRebalance_current_allocation","total_portfolio_value","postRebalance_total_value"]].copy()
            ts=pd.to_datetime(d["timestamp"],utc=True)
            d["hour"]=ts.dt.hour.values; d["wd"]=ts.dt.weekday.values
            c=d["close"]
            d["r1"]=c.shift(-1)/c-1
            d["r2"]=c.shift(-2)/c-1
            d["rpast1"]=c/c.shift(1)-1
            d["tr72"]=c/c.shift(72)-1
            d["tr24"]=c/c.shift(24)-1
            d["vol24"]=d["rpast1"].rolling(24).std()
            d["lv"]=np.log(d["volume"].replace(0,np.nan))
            d["lvrel"]=d["lv"]-d["lv"].rolling(168,min_periods=48).mean()
            d["gross"]=d["postRebalance_current_allocation"]*d["r1"]
            d["fee"]=(d["total_portfolio_value"]-d["postRebalance_total_value"])/d["total_portfolio_value"]
            d["pos"]=np.arange(len(d))
            d["coin"]=coin; d["w"]=w
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    out={}
    # standardise tr72 per coin
    A["z72"]=A.groupby("coin")["tr72"].transform(lambda s:(s-s.mean())/s.std())
    A["exr1"]=A["r1"]-A.groupby("coin")["r1"].transform("mean")
    h=A.groupby("hour")["exr1"].agg(["mean","count","std"])
    h["t"]=h["mean"]/(h["std"]/np.sqrt(h["count"]))
    out["excess 1h fwd ret by hour"]=h[["mean","t","count"]]
    # slope of next-1h return on z72 by hour
    def sl(g):
        g=g.dropna(subset=["exr1","z72"])
        r=stats.linregress(g["z72"],g["exr1"])
        return pd.Series({"slope_bp":r.slope*1e4,"t":r.slope/r.stderr,"n":len(g)})
    out["slope of 1h fwd ret on z72 by hour"]=A.groupby("hour").apply(sl)
    v=A.groupby("hour")["lvrel"].agg(["mean","count"])
    out["log volume rel 7d by hour"]=v
    # big moves: past 1h return per-coin vol-scaled deciles -> next 1h
    A["sc"]=A["rpast1"]/A["vol24"]
    A["dec"]=pd.qcut(A["sc"],10,labels=False,duplicates="drop")
    g=A.groupby("dec")["exr1"].agg(["mean","count","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["next1h by past1h scaled decile"]=g[["mean","t","count"]]
    # 24h trend deciles -> next 24h nonoverlap
    G=A[A["pos"]%24==0].copy()
    G["r24f"]=G.groupby(["coin","w"])["close"].shift(-1)/G["close"]-1
    G["ex"]=G["r24f"]-G.groupby("coin")["r24f"].transform("mean")
    G["d"]=pd.qcut(G["tr24"]/G["vol24"],5,labels=False,duplicates="drop")
    g=G.groupby("d")["ex"].agg(["mean","count","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["next24h by past24h quintile (nonoverlap)"]=g[["mean","t","count"]]
    # vol level -> next 1h abs and mean
    A["vq"]=A.groupby("coin")["vol24"].transform(lambda s:pd.qcut(s,5,labels=False,duplicates="drop"))
    g=A.groupby("vq")["exr1"].agg(["mean","count","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["next1h by vol quintile"]=g[["mean","t","count"]]
    g=A.groupby("wd")["exr1"].agg(["mean","count","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["next1h by weekday"]=g[["mean","t","count"]]
    out["book gross vs fee per bar (mean bp)"]=pd.Series({"gross_bp":A["gross"].mean()*1e4,"fee_bp":A["fee"].mean()*1e4,"gross_t":A["gross"].mean()/(A["gross"].std()/np.sqrt(A["gross"].notna().sum()))})
    act=A[A["postRebalance_current_allocation"].abs()>0]
    out["active bars by hour gross bp"]=act.groupby("hour")["gross"].agg(["mean","count"]).assign(mean=lambda x:x["mean"]*1e4)
    return out
