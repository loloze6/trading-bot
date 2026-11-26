def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            r7=c/c.shift(7)-1
            base=r7.abs().rolling(30,min_periods=20).mean()
            sc=r7/base
            vol30=r1.rolling(30,min_periods=20).std()
            volr=vol30/vol30.rolling(60,min_periods=30).median()
            rng=(b["high"]-b["low"])/c
            clpos=(c-b["low"])/(b["high"]-b["low"])
            inprof=(b["regime"]!="chop")
            wd=pd.to_datetime(b["timestamp"]).dt.weekday
            for h in (1,3,7,14):
                fwd=c.shift(-h)/c-1
                idx=np.arange(0,len(b),h)
                d=pd.DataFrame({"coin":coin,"w":w,"h":h,"fwd":fwd.iloc[idx].values,
                    "sc":sc.iloc[idx].values,"r1":r1.iloc[idx].values,"r1s":(r1/vol30).iloc[idx].values,
                    "volr":volr.iloc[idx].values,"inprof":inprof.iloc[idx].values,
                    "regime":b["regime"].iloc[idx].values,"wd":wd.iloc[idx].values,
                    "rng":(rng/vol30).iloc[idx].values,"clpos":clpos.iloc[idx].values})
                rows.append(d)
    D=pd.concat(rows).dropna(subset=["fwd"])
    # drift per coin,h
    drift=D.groupby(["coin","h"])["fwd"].transform("mean")
    D["ex"]=D["fwd"]-drift
    def summ(g):
        x=g["ex"].dropna()
        n=len(x)
        return pd.Series({"n":n,"mean_ex":x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan,"mean_tot":g["fwd"].mean()})
    out={}
    D["scb"]=pd.cut(D["sc"],[-np.inf,-2,-1,-0.3,0.3,1,2,np.inf])
    for h in (3,14):
        s=D[D.h==h]
        out[f"scaled7_bins_h{h}_by_prof"]=s.groupby(["inprof","scb"],observed=True).apply(summ)
    D["r1b"]=pd.cut(D["r1s"],[-np.inf,-2,-1,-0.3,0.3,1,2,np.inf])
    for h in (1,3,7):
        s=D[D.h==h]
        out[f"r1scaled_bins_h{h}"]=s.groupby("r1b",observed=True).apply(summ)
    s=D[D.h==3]
    out["r1scaled_h3_by_prof"]=s.groupby(["inprof","r1b"],observed=True).apply(summ)
    s=D[D.h==1]
    out["weekday_h1"]=s.groupby("wd").apply(summ)
    D["volb"]=pd.qcut(D["volr"],4)
    for h in (1,7):
        out[f"volratio_q_h{h}"]=D[D.h==h].groupby("volb",observed=True).apply(summ)
    D["rngb"]=pd.qcut(D["rng"],4); D["clb"]=pd.cut(D["clpos"],[0,0.25,0.75,1],include_lowest=True)
    out["range_x_close_h3"]=D[D.h==3].groupby(["rngb","clb"],observed=True).apply(summ)
    # trades
    T=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            if len(t): T.append(t.assign(coin=coin))
    T=pd.concat(T)
    T["fb"]=pd.qcut(T["entry_forecast"],4,duplicates="drop")
    out["trades_by_entry_forecast"]=T.groupby("fb",observed=True)["net_profit_loss_percent"].agg(["count","mean","median"])
    out["trades_by_coin"]=T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean"])
    return out
