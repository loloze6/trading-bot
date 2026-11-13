def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy()
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(60,min_periods=20).std(); mu=r.rolling(60,min_periods=20).mean()
            z=(r-mu)/sd
            df=pd.DataFrame({"coin":coin,"w":w,"r":r,"z":z,"n1":r.shift(-1),
                             "n3":c.shift(-3)/c-1,"fc":b["forecast"].astype(float),
                             "reg":b["regime"],"wd":pd.to_datetime(b["timestamp"]).dt.dayofweek,
                             "yr":pd.to_datetime(b["timestamp"]).dt.year,
                             "rng":(b["high"]-b["low"])/c,"cl":(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan),
                             "vol":b["volume"].astype(float)})
            df["vrel"]=df["vol"]/df["vol"].rolling(20,min_periods=10).mean()
            df["mom20"]=c/c.shift(20)-1
            df["i"]=np.arange(len(df))
            rows.append(df)
    d=pd.concat(rows).dropna(subset=["z","n1"])
    d["n1x"]=d["n1"]-d.groupby("coin")["n1"].transform("mean")
    def agg(g,col="n1x"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan,"up":(g["n1"]>0).mean()})
    out={}
    d["zb"]=pd.cut(d["z"],[-99,-3,-2,-1.5,-1,0,1,1.5,2,3,99])
    out["by_zbin"]=d.groupby("zb").apply(agg)
    out["by_zbin_reg"]=d.groupby(["zb","reg"]).apply(agg)
    dd=d[d.z<-1.5]
    out["drop_by_coin"]=dd.groupby("coin").apply(agg)
    out["drop_by_year"]=dd.groupby("yr").apply(agg)
    out["drop_by_close_loc"]=dd.groupby(pd.cut(dd["cl"],[-0.01,0.2,0.5,1.01])).apply(agg)
    out["drop_by_vrel"]=dd.groupby(pd.qcut(dd["vrel"],3)).apply(agg)
    out["drop_by_mom20"]=dd.groupby(pd.qcut(dd["mom20"],3)).apply(agg)
    out["all_by_wd"]=d.groupby("wd").apply(agg)
    out["drop_by_wd"]=dd.groupby("wd").apply(agg)
    out["all_by_reg"]=d.groupby("reg").apply(agg)
    # 3-day non-overlap after drops events
    e=d[(d.z<-2)].dropna(subset=["n3"])
    e3=e.groupby(["coin","w"]).apply(lambda g:g[g["i"].diff().fillna(99)>=3]).reset_index(drop=True)
    out["drop_n3"]=pd.Series({"n":len(e3),"mean":e3["n3"].mean(),"t":e3["n3"].mean()/e3["n3"].std()*np.sqrt(len(e3))})
    # range quantile (intraday range) predictive
    d["rngq"]=d.groupby("coin")["rng"].transform(lambda x:pd.qcut(x,5,labels=False))
    out["all_by_rngq"]=d.groupby("rngq").apply(agg)
    # trades
    tr=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values()])
    out["trades"]=tr.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","median",lambda x:(x>0).mean()])
    tr["ef"]=pd.qcut(tr["entry_forecast"].rank(method="first"),4,labels=False)
    out["trades_by_ef"]=tr.groupby("ef")["net_profit_loss_percent"].agg(["count","mean",lambda x:(x>0).mean()])
    out["trades_dur"]=tr["duration_minutes"].describe()
    return out
