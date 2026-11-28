def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]; v=b["volume"]
            b["ret1"]=c.pct_change()
            b["ret5p"]=c/c.shift(5)-1
            b["ret10p"]=c/c.shift(10)-1
            b["vr"]=v/v.shift(1).rolling(20,min_periods=15).mean()
            rng=(b["high"]-b["low"])
            b["clv"]=(c-b["low"])/rng.replace(0,np.nan)
            b["rngr"]=rng/c
            b["rngrel"]=b["rngr"]/b["rngr"].shift(1).rolling(20,min_periods=15).mean()
            b["fwd5"]=c.shift(-5)/c-1
            b["fwd2"]=c.shift(-2)/c-1
            b["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            b["grid"]=(np.arange(len(b))%5==0)
            b["inprof"]=b["regime"].isin(["mean_reversion","unknown"])
            b["coin"]=coin; b["win"]=w
            rows.append(b)
    B=pd.concat(rows,ignore_index=True)
    G=B[B.grid & B.fwd5.notna()].copy()
    drift=G.groupby("coin")["fwd5"].mean()
    G["unus"]=G["fwd5"]-G["coin"].map(drift)
    P=G[G.inprof].copy()
    def summ(df,key):
        g=df.groupby(key)["unus"]
        out=pd.DataFrame({"n":g.size(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
        return out.round(4)
    res={}
    res["regime_counts"]=B.groupby("regime").size()
    res["drift5_by_coin"]=drift.round(4)
    res["inprof_all"]=summ(P.assign(a="all"),"a")
    for f in ["ret1","ret5p","ret10p","vr","clv","rngrel"]:
        d=P.dropna(subset=[f]).copy()
        d["q"]=pd.qcut(d[f],5,labels=False,duplicates="drop")
        res["q_"+f]=summ(d,"q")
    d=P.dropna(subset=["vr","ret1"]).copy()
    d["up"]=d.ret1>0; d["heavy"]=d.vr>1
    res["up_x_heavy"]=summ(d,["up","heavy"])
    res["wd"]=summ(P,"wd")
    res["coin"]=summ(P,"coin")
    res["win"]=summ(P,"win")
    # outside profile for contrast
    O=G[~G.inprof].dropna(subset=["ret5p"]).copy()
    O["q"]=pd.qcut(O["ret5p"],5,labels=False)
    res["outprof_q_ret5p"]=summ(O,"q")
    T=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            if len(t): T.append(t.assign(coin=coin))
    if T:
        T=pd.concat(T)
        res["trades"]=T.groupby("coin")["net_profit_loss_percent"].agg(["size","mean","median"]).round(3)
    return res
