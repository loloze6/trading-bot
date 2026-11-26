def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            sma=c.rolling(20).mean()
            dist=c/sma-1
            r1=c.pct_change()
            vol=r1.rolling(20).std()
            ret5=c/c.shift(5)-1
            ret20=c/c.shift(20)-1
            fwd10=c.shift(-10)/c-1
            fwd3=c.shift(-3)/c-1
            ts=pd.to_datetime(b["timestamp"])
            n=len(b)
            for i in range(0,n,10):
                rows.append(dict(coin=coin,w=w,dist=dist[i],vol=vol[i],ret5=ret5[i],ret20=ret20[i],
                    fwd10=fwd10[i],fwd3=fwd3[i],r1=r1[i],regime=b["regime"][i],
                    fc=b["forecast"][i],alloc=b["postRebalance_current_allocation"][i],
                    rv=b["sizing_realised_vol"][i] if "sizing_realised_vol" in b else np.nan,
                    wd=ts[i].weekday(),yr=ts[i].year,day=ts[i].normalize()))
    d=pd.DataFrame(rows)
    drift=d.groupby("coin")["fwd10"].transform("mean")
    d["ex10"]=d["fwd10"]-drift
    d["inprof"]=(d["regime"]=="unknown")
    out={}
    def tab(g):
        x=g["ex10"].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    dd=d.dropna(subset=["dist","ex10"]).copy()
    dd["dq"]=dd.groupby("coin")["dist"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["ex10 by dist quintile x inprofile"]=dd.groupby(["inprof","dq"]).apply(tab).reset_index()
    # 20d return quintiles
    e=d.dropna(subset=["ret20","ex10"]).copy()
    e["q"]=e.groupby("coin")["ret20"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["ex10 by ret20 quintile x inprof"]=e.groupby(["inprof","q"]).apply(tab).reset_index()
    # vol terciles relative to coin median
    v=d.dropna(subset=["vol","ex10","dist"]).copy()
    v["vrel"]=v["vol"]/v.groupby("coin")["vol"].transform("median")
    v["vt"]=pd.qcut(v["vrel"],3,labels=False)
    v["sx"]=np.sign(v["dist"])*v["ex10"]
    out["signed (dist-follow) ex10 by vol tercile x inprof"]=v.groupby(["inprof","vt"])["sx"].agg(["count","mean",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))]).reset_index()
    # spearman dist vs ex10 per regime
    out["spearman dist~ex10"]=pd.DataFrame({k:stats.spearmanr(g["dist"],g["ex10"])[:2] for k,g in dd.groupby("inprof")},index=["rho","p"])
    out["spearman ret5~fwd3ex"]=pd.Series(stats.spearmanr(d.dropna(subset=["ret5","fwd3"])["ret5"],d.dropna(subset=["ret5","fwd3"])["fwd3"])[:2],index=["rho","p"])
    # daily: weekday of book & coin
    days=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w; days.append(x)
    D=pd.concat(days); D["day"]=pd.to_datetime(D["day"])
    D["wd"]=D["day"].dt.weekday
    out["coin ret by weekday"]=D.groupby("wd")["coin_return"].agg(["count","mean",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))])
    out["book ret by weekday"]=D.groupby("wd")["book_return"].agg(["count","mean",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))])
    # next-day after large daily moves (by coin-standardised daily return decile)
    D=D.sort_values(["coin","w","day"])
    D["nxt"]=D.groupby(["coin","w"])["coin_return"].shift(-1)
    D["z"]=D.groupby("coin")["coin_return"].transform(lambda s:(s-s.mean())/s.std())
    D2=D.dropna(subset=["z","nxt"]).copy()
    D2["zq"]=pd.qcut(D2["z"],10,labels=False)
    out["next day ret by today z decile"]=D2.groupby("zq")["nxt"].agg(["count","mean",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))])
    # by year: forecast-follow excess
    out["follow ex10 by year inprof"]=v[v.inprof].groupby("yr")["sx"].agg(["count","mean"])
    # trades
    tr=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            t=t.copy();t["coin"]=coin;tr.append(t)
    T=pd.concat(tr)
    out["trades by side"]=T.groupby("side")["net_profit_loss_percent"].agg(["count","mean","median",lambda x:(x>0).mean()])
    T["af"]=T["entry_forecast"].abs()
    T["afq"]=pd.qcut(T["af"].rank(method="first"),4,labels=False)
    out["trades by |entry fc| quartile x side"]=T.groupby(["side","afq"])["net_profit_loss_percent"].agg(["count","mean"]).reset_index()
    return out
