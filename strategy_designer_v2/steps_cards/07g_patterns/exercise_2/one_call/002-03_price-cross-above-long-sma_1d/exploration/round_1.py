def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy()
            cl=b["close"].astype(float)
            d=pd.DataFrame({"coin":c,"win":w})
            d=pd.DataFrame(index=b.index)
            d["coin"]=c; d["win"]=w
            d["dist"]=b["debug_info.components.above_ma.last_history_value"].astype(float)
            d["fc"]=b["forecast"].astype(float)
            d["r1"]=cl.pct_change()
            d["f1"]=cl.shift(-1)/cl-1
            d["f5"]=cl.shift(-5)/cl-1
            d["f20"]=cl.shift(-20)/cl-1
            d["vol20"]=d["r1"].rolling(20).std()
            d["mom20"]=cl/cl.shift(20)-1
            d["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            d["yr"]=pd.to_datetime(b["timestamp"]).dt.year
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["r1"].mean()
    D["mu"]=D["coin"].map(mu)
    D["x20"]=D["f20"]-20*D["mu"]; D["x5"]=D["f5"]-5*D["mu"]; D["x1"]=D["f1"]-D["mu"]
    def summ(g,col):
        s=g[col].dropna()
        return pd.Series({"n":len(s),"mean":s.mean(),"t":s.mean()/s.std()*np.sqrt(len(s)/ (20 if col=="x20" else (5 if col=="x5" else 1))),"hit":(s>0).mean()})
    out={}
    D["distq"]=pd.qcut(D["dist"],10,labels=False,duplicates="drop")
    t=D.groupby("distq").apply(lambda g: pd.concat([summ(g,"x20").add_prefix("x20_"),summ(g,"x1").add_prefix("x1_")]))
    t["dist_mid"]=D.groupby("distq")["dist"].median()
    out["by_dist_decile"]=t
    D["volq"]=D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["by_vol_quint"]=D.groupby("volq").apply(lambda g: pd.concat([summ(g,"x20").add_prefix("x20_"),summ(g,"x5").add_prefix("x5_")]))
    D["momq"]=D.groupby("coin")["mom20"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["by_mom20_quint"]=D.groupby("momq").apply(lambda g: pd.concat([summ(g,"x20").add_prefix("x20_"),summ(g,"x5").add_prefix("x5_")]))
    z=D["r1"]/D["vol20"].shift(1) if False else None
    D["rz"]=D.groupby(["coin","win"])["r1"].transform(lambda s: s/s.rolling(20).std().shift(1))
    D["bigmv"]=pd.cut(D["rz"],[-99,-2.5,-1.5,1.5,2.5,99],labels=["vbigdn","dn","mid","up","vbigup"])
    out["after_big_moves"]=D.groupby("bigmv").apply(lambda g: pd.concat([summ(g,"x1").add_prefix("x1_"),summ(g,"x5").add_prefix("x5_")]))
    out["weekday"]=D.groupby("wd").apply(lambda g: summ(g,"x1"))
    out["year_x20_above_vs_below"]=D.assign(ab=D["dist"]>0).groupby(["yr","ab"]).apply(lambda g: summ(g,"x20")).unstack()["mean"]
    out["coin_above_below"]=D.assign(ab=D["dist"]>0).groupby(["coin","ab"]).apply(lambda g: summ(g,"x20")).unstack()
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items()])
    T["dd"]=T["duration_minutes"]/1440
    out["trades"]=pd.Series({"n":len(T),"mean_net":T["net_profit_loss_percent"].mean(),"med_net":T["net_profit_loss_percent"].median(),"win":(T["net_profit_loss_percent"]>0).mean(),"med_days":T["dd"].median(),"share_lt3d":(T["dd"]<3).mean()})
    return out
