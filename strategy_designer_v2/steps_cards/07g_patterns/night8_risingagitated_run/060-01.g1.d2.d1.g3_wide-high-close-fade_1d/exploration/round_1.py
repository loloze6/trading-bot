def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            d=pd.DataFrame()
            d["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            o,h,l,c=b["open"],b["high"],b["low"],b["close"]
            rng=(h-l)
            d["cl"]=np.where(rng>0,(c-l)/rng,np.nan)
            d["rm"]=rng/rng.rolling(20,min_periods=20).mean()
            d["ret"]=c.pct_change()
            d["ret5"]=c/c.shift(5)-1
            d["tr60"]=c/c.shift(60)-1
            d["vol20"]=d["ret"].rolling(20).std()
            d["z"]=d["ret"]/d["vol20"].shift(1)
            d["body"]=np.where(rng>0,(c-o)/rng,np.nan)
            d["nxt"]=c.shift(-1)/c-1
            d["fa"]=b["regime"].isin(["mean_reversion","unknown"])
            d["pos"]=b["postRebalance_current_allocation"]
            d["wd"]=d["day"].dt.dayofweek
            d["coin"]=coin; d["w"]=w
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["ex"]=D["nxt"]-D.groupby("coin")["nxt"].transform("mean")
    def summ(g):
        x=g.dropna(subset=["ex"])
        if len(x)<5: return pd.Series({"n":len(x)})
        pd_=x.groupby("day")["ex"].mean()
        t=pd_.mean()/(pd_.std()/np.sqrt(len(pd_)))
        return pd.Series({"n":len(x),"days":len(pd_),"mean_ex%":x["ex"].mean()*100,"t_day":t})
    out={}
    out["regime counts"]=D["fa"].value_counts()
    F=D[D["fa"]]
    out["fa by cl quintile"]=F.groupby(pd.qcut(F["cl"],5)).apply(summ)
    out["fa by rm tercile x cl>0.5"]=F.groupby([pd.qcut(F["rm"],3),F["cl"]>0.5]).apply(summ)
    out["fa by body sign x cl>0.5"]=F.groupby([F["body"]>0,F["cl"]>0.5]).apply(summ)
    out["fa by z quintile"]=F.groupby(pd.qcut(F["z"],5)).apply(summ)
    out["fa by 5d ret quintile"]=F.groupby(pd.qcut(F["ret5"],5)).apply(summ)
    out["fa weekday"]=F.groupby("wd").apply(summ)
    N=D[~D["fa"]]
    out["nonfa by cl quintile"]=N.groupby(pd.qcut(N["cl"],5)).apply(summ)
    tr=pd.cut(N["tr60"],[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    out["nonfa trend x cl>0.5"]=N.groupby([tr,N["cl"]>0.5]).apply(summ)
    out["nonfa z quintile"]=N.groupby(pd.qcut(N["z"],5)).apply(summ)
    out["all weekday"]=D.groupby("wd").apply(summ)
    # book
    bd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy();x["coin"]=coin;x["w"]=w;bd.append(x)
    B=pd.concat(bd)
    B["day"]=pd.to_datetime(B["day"]).dt.floor("D")
    bk=B.groupby("day")["book_return"].mean().dropna()
    out["book by year"]=bk.groupby(bk.index.year).agg(["count","mean","std","sum"])
    out["book by window"]=B.groupby("w")["book_return"].agg(["mean","sum"])
    T=[]
    for coin,ws in data["trades"].items():
        for w,x in ws.items():
            if len(x): x=x.copy();x["coin"]=coin;T.append(x)
    T=pd.concat(T)
    out["trades by coin"]=T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","median","sum"])
    out["trades dur"]=T["duration_minutes"].describe()
    return out
