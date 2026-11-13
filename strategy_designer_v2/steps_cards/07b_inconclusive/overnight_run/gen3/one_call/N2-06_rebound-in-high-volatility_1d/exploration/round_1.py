def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            d=df.copy().reset_index(drop=True)
            d["nxt"]=d["close"].shift(-1)/d["close"]-1
            d["ret"]=d["close"].pct_change()
            d["sma20"]=d["close"].rolling(20,min_periods=10).mean()
            d["above"]=(d["close"]>d["sma20"]).astype(float)
            d["ret5"]=d["close"]/d["close"].shift(5)-1
            d["coin"]=coin; d["w"]=w; d["year"]=pd.to_datetime(d["timestamp"]).dt.year
            d["wd"]=pd.to_datetime(d["timestamp"]).dt.weekday
            rows.append(d[["coin","w","year","wd","forecast","regime","nxt","ret","above","ret5"]])
    a=pd.concat(rows).dropna(subset=["nxt","forecast"])
    cm=a.groupby("coin")["nxt"].mean()
    a["ex"]=a["nxt"]-a["coin"].map(cm)
    a["up"]=(a["nxt"]>0).astype(float)-a["coin"].map(a.groupby("coin")["nxt"].apply(lambda s:(s>0).mean()))
    pos=a[a.forecast>0]
    thr=a.forecast.quantile(0.9)
    top=a[(a.forecast>=thr)&(a.forecast>0)].copy()
    def summ(g):
        return pd.Series({"n":len(g),"mean_ex":g.ex.mean(),"t":g.ex.mean()/(g.ex.std()/np.sqrt(len(g))) if len(g)>2 else np.nan,"netup":g.up.mean()})
    out={}
    out["thr"]=float(thr)
    out["top_by_regime"]=top.groupby("regime").apply(summ)
    out["top_by_coin_regime"]=top.groupby(["coin","regime"]).apply(summ)
    out["top_by_year"]=top.groupby(["year","regime"]).apply(summ)
    top["fq"]=pd.qcut(top.forecast.rank(method="first"),4,labels=["q1","q2","q3","q4"])
    out["top_by_fq_regime"]=top.groupby(["fq","regime"]).apply(summ)
    pos2=pos.copy(); pos2["fd"]=pd.qcut(pos2.forecast.rank(method="first"),5,labels=False)
    out["pos_by_quintile"]=pos2.groupby("fd").apply(summ)
    out["top_by_above_sma"]=top.groupby(["above","regime"]).apply(summ)
    top["r5neg"]=(top.ret5<-0.1)
    out["top_by_5d_drop"]=top.groupby(["r5neg"]).apply(summ)
    out["all_by_regime"]=a.groupby("regime").apply(summ)
    out["nontop_flat_by_regime"]=a[a.forecast<=0].groupby("regime").apply(summ)
    out["top_by_wd"]=top.groupby("wd").apply(summ)
    return out
