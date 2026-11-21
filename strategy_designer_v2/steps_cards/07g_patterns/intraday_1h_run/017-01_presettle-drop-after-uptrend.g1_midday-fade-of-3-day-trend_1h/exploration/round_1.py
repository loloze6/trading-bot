def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            d=b[["timestamp","close","volume","postRebalance_current_allocation"]].copy()
            d["ts"]=pd.to_datetime(d["timestamp"],utc=True)
            d["hour"]=d["ts"].dt.hour; d["wd"]=d["ts"].dt.weekday
            d["r1"]=d["close"].shift(-1)/d["close"]-1
            d["past1"]=d["close"]/d["close"].shift(1)-1
            d["past72"]=d["close"]/d["close"].shift(72)-1
            d["past24"]=d["close"]/d["close"].shift(24)-1
            d["vol24"]=d["past1"].rolling(24).std()
            d["lv"]=np.log(d["volume"].replace(0,np.nan))
            d["lvrel"]=d["lv"]-d["lv"].rolling(168,min_periods=48).mean()
            d["coin"]=c; d["win"]=w
            d["pos"]=np.arange(len(d))
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    A["r1x"]=A["r1"]-A.groupby("coin")["r1"].transform("mean")
    A["z1"]=A["past1"]/A["vol24"]
    A["r1n"]=A["r1x"]/A["vol24"]
    A["z72"]=A.groupby("coin")["past72"].transform(lambda s:(s-s.mean())/s.std())
    out={}
    g=A.groupby("hour")
    out["hour_ret"]=pd.DataFrame({"mean_bp":g["r1x"].mean()*1e4,"t":g["r1x"].apply(lambda s:s.mean()/s.std()*np.sqrt(s.count())),
        "relvol":g["lvrel"].mean(),"slope72_corr":g.apply(lambda x:x[["z72","r1n"]].dropna().corr().iloc[0,1]),"n":g["r1x"].count()})
    # reversal after 1h moves
    A["q1"]=pd.qcut(A["z1"],10,labels=False)
    g=A.groupby("q1")
    out["next1_by_past1_decile"]=pd.DataFrame({"mean_bp":g["r1x"].mean()*1e4,"t":g["r1x"].apply(lambda s:s.mean()/s.std()*np.sqrt(s.count())),"n":g["r1x"].count()})
    # per coin corr z1 vs next
    out["rev1_corr_by_coin"]=A.groupby("coin").apply(lambda x:pd.Series({"corr":x[["z1","r1n"]].dropna().corr().iloc[0,1],"n":x[["z1","r1n"]].dropna().shape[0]}))
    # 24h horizon non-overlapping: past72 and past24 vs next 24
    B=A.copy()
    B["f24"]=B.groupby(["coin","win"])["close"].shift(-24)/B["close"]-1
    S=B[B["pos"]%24==0].dropna(subset=["f24","past72","past24"])
    S["f24x"]=S["f24"]-S.groupby("coin")["f24"].transform("mean")
    out["24h_nonoverlap"]=pd.DataFrame({"corr_p72":[S[["past72","f24x"]].corr().iloc[0,1]],"corr_p24":[S[["past24","f24x"]].corr().iloc[0,1]],"n":[len(S)]})
    # weekday
    g=A.groupby("wd")
    out["weekday"]=pd.DataFrame({"mean_bp":g["r1x"].mean()*1e4,"t":g["r1x"].apply(lambda s:s.mean()/s.std()*np.sqrt(s.count()))})
    # trades gross vs net
    T=pd.concat([t for ws in data["trades"].values() for t in ws.values()])
    out["trades"]=pd.Series({"n":len(T),"gross_mean_pct":T["profit_loss_percent"].mean(),"net_mean_pct":T["net_profit_loss_percent"].mean(),"t_gross":T["profit_loss_percent"].mean()/T["profit_loss_percent"].std()*np.sqrt(len(T))})
    D=pd.concat([x for ws in data["days"].values() for x in ws.values()])
    out["book_daily"]=pd.Series({"mean":D["book_return"].mean(),"std":D["book_return"].std(),"n":D["book_return"].count()})
    return out
