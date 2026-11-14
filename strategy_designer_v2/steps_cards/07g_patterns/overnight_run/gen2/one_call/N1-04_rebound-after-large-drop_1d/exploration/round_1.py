def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            ma=r.abs().rolling(20,min_periods=20).mean().shift(1)
            z=r/ma
            vol=r.rolling(20,min_periods=20).std()
            volrank=vol.rolling(120,min_periods=60).rank(pct=True)
            mom=c/c.shift(20)-1
            d=pd.DataFrame({"coin":coin,"w":w,"r":r,"z":z,"n1":r.shift(-1),"n3":c.shift(-3)/c-1,
                            "f":b["forecast"].astype(float),"wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                            "year":pd.to_datetime(b["timestamp"]).dt.year,"volrank":volrank,"mom":mom,
                            "rng":(b["high"]-b["low"])/c,"clo":(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)})
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["z","n1"])
    def summ(g):
        return pd.Series({"n":len(g),"hit":(g.n1>0).mean(),"mean":g.n1.mean(),"t":g.n1.mean()/g.n1.std()*np.sqrt(len(g))})
    out={}
    D["zb"]=pd.cut(D.z,[-np.inf,-3,-2,-1.5,-1,0,1,1.5,2,3,np.inf])
    out["by_zbucket"]=D.groupby("zb").apply(summ)
    big=D[D.z<=-1.88]
    out["bigdrop_by_coin"]=big.groupby("coin").apply(summ)
    out["bigdrop_by_year"]=big.groupby("year").apply(summ)
    out["bigdrop_by_mom"]=big.groupby(pd.cut(big.mom,[-np.inf,-0.15,0,0.15,np.inf])).apply(summ)
    out["bigdrop_by_volrank"]=big.groupby(pd.cut(big.volrank,[0,0.33,0.66,1.01])).apply(summ)
    out["bigdrop_by_closeloc"]=big.groupby(pd.cut(big.clo,[-0.01,0.2,0.5,1.01])).apply(summ)
    bigup=D[D.z>=1.88]
    out["bigup_by_mom"]=bigup.groupby(pd.cut(bigup.mom,[-np.inf,-0.15,0,0.15,np.inf])).apply(summ)
    out["all_by_weekday"]=D.groupby("wd").apply(summ)
    out["all_by_volrank"]=D.groupby(pd.cut(D.volrank,[0,0.33,0.66,1.01])).apply(summ)
    # 3-day after big drop, non-overlap approx (events)
    out["bigdrop_n3"]=pd.Series({"n":big.n3.notna().sum(),"mean":big.n3.mean(),"hit":(big.n3>0).mean()})
    # trades
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values()])
    out["trades"]=T.groupby("coin").agg(n=("net_profit_loss_percent","size"),mean=("net_profit_loss_percent","mean"),
        hit=("net_profit_loss_percent",lambda x:(x>0).mean()),worst=("net_profit_loss_percent","min"),best=("net_profit_loss_percent","max"))
    return out
