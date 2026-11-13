def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy().reset_index(drop=True)
            if len(b)<30: continue
            c=b["close"].astype(float)
            r1=c.pct_change()
            df=pd.DataFrame({
                "coin":coin,"w":w,
                "f":b["forecast"].astype(float),
                "raw":b["debug_info.components.sma_cross_down.last_history_value"].astype(float),
                "alloc":b["postRebalance_current_allocation"].astype(float),
                "r1":r1,
                "fwd1":c.shift(-1)/c-1,
                "fwd10":c.shift(-10)/c-1,
                "past10":c/c.shift(10)-1,
                "vol20":r1.rolling(20).std(),
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr":pd.to_datetime(b["timestamp"]).dt.year,
            })
            bv=b["postRebalance_total_value"].astype(float)
            df["book_fwd1"]=bv.shift(-1)/bv-1
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    d["short"]=d["f"]<0
    out={}
    def agg(g,col="fwd10"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(max(len(x),1)/10) if len(x)>2 else np.nan,"up_share":(x>0).mean()})
    out["fwd10 by state x coin"]=d.groupby(["coin","short"]).apply(agg).round(4)
    d["rawbin"]=pd.qcut(d["raw"],10,duplicates="drop")
    out["fwd10 by raw spread decile"]=d.groupby("rawbin").apply(agg).round(4)
    d["p10bin"]=pd.qcut(d["past10"],5)
    out["fwd10 by past10 quint x state"]=d.groupby(["p10bin","short"]).apply(agg).round(4)
    d["volq"]=d.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s,4,labels=False,duplicates="drop"))
    out["fwd10 by vol quartile x state"]=d.groupby(["volq","short"]).apply(agg).round(4)
    out["fwd1 by weekday"]=d.groupby("wd").apply(lambda g: agg(g,"fwd1")).round(4)
    out["fwd10 by year x state"]=d.groupby(["yr","short"]).apply(agg).round(4)
    # big daily moves
    d["z"]=d["r1"]/d["vol20"]
    d["zbin"]=pd.cut(d["z"],[-99,-3,-2,-1,1,2,3,99])
    out["fwd1 & fwd10 after z-move"]=pd.concat([d.groupby("zbin")["fwd1"].agg(["count","mean"]),d.groupby("zbin")["fwd10"].mean().rename("fwd10")],axis=1).round(4)
    # book
    out["book_fwd1 by state"]=d.groupby("short")["book_fwd1"].agg(["count","mean","std"]).round(5)
    out["alloc vs f"]=d.groupby(pd.cut(d["f"],[-21,-10,-5,-2,-0.001,0.001]))["alloc"].agg(["count","mean"]).round(3)
    # trades
    tr=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            if len(t): t=t.copy(); t["coin"]=coin; tr.append(t)
    T=pd.concat(tr,ignore_index=True)
    T["days"]=T["duration_minutes"]/1440
    out["trades by side"]=T.groupby("side").agg(n=("days","size"),dur=("days","median"),pl=("net_profit_loss_percent","mean"),win=("net_profit_loss_percent",lambda x:(x>0).mean())).round(3)
    T["durbin"]=pd.qcut(T["days"],4,duplicates="drop")
    out["trades by duration"]=T.groupby("durbin")["net_profit_loss_percent"].agg(["count","mean","median"]).round(3)
    out["trades by coin"]=T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","sum"]).round(3)
    # entry state: spread just after cross vs deep
    out["fwd10 short by days-since-cross"]=d[d.short].assign(k=d[d.short].groupby(["coin","w",(~d["short"]).cumsum()]).cumcount()).pipe(lambda x: x.groupby(pd.cut(x["k"],[-1,10,30,60,120,1000]))).apply(agg).round(4)
    return out
