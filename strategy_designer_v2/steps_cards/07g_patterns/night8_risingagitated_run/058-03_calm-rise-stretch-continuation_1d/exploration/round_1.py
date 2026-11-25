def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            n=len(b)
            sma=c.rolling(20,min_periods=20).mean()
            dist=c/sma-1
            r1=c.pct_change()
            vol10=r1.rolling(10,min_periods=10).std()
            vol30=r1.rolling(30,min_periods=30).std()
            tr30=c/c.shift(30)-1
            tr60=c/c.shift(60)-1
            ret1=r1
            ret3=c/c.shift(3)-1
            fwd5=c.shift(-5)/c-1
            fwd1=c.shift(-1)/c-1
            fwd2=c.shift(-2)/c-1
            rng=(b["high"]-b["low"])/c
            clpos=(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(n),"ts":pd.to_datetime(b["timestamp"]),
               "dist":dist,"vol10":vol10,"vol30":vol30,"tr30":tr30,"tr60":tr60,"ret1":ret1,"ret3":ret3,
               "fwd5":fwd5,"fwd1":fwd1,"fwd2":fwd2,"rng":rng,"clpos":clpos,"regime":b["regime"],
               "fc":b["forecast"],"alloc":b["postRebalance_current_allocation"],
               "volrel":vol10/vol30})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["day"]=D["ts"].dt.floor("D")
    # coin mean 5-bar return on grid
    g5=D[D.pos%5==0].copy()
    m5=g5.groupby("coin")["fwd5"].mean()
    g5["ex5"]=g5["fwd5"]-g5["coin"].map(m5)
    g1=D.copy(); m1=g1.groupby("coin")["fwd1"].mean(); g1["ex1"]=g1["fwd1"]-g1["coin"].map(m1)
    g2=D[D.pos%2==0].copy(); m2=g2.groupby("coin")["fwd2"].mean(); g2["ex2"]=g2["fwd2"]-g2["coin"].map(m2)
    def dt(df,col):
        df=df.dropna(subset=[col])
        s=df.groupby("day")[col].sum(); k=df.groupby("day")[col].size()
        mu=df[col].mean(); dev=(df[col]-mu).groupby(df["day"]).sum()
        se=np.sqrt((dev**2).sum())/len(df) if len(df)>1 else np.nan
        return pd.Series({"n":len(df),"days":df["day"].nunique(),"mean%":100*mu,"t_day":mu/se if se>0 else np.nan})
    def slope(df,x,y):
        df=df.dropna(subset=[x,y])
        if len(df)<30: return pd.Series({"n":len(df),"slope":np.nan,"t":np.nan})
        X=df[x]-df[x].mean(); Y=df[y]-df[y].mean()
        b=(X*Y).sum()/(X*X).sum(); e=Y-b*X
        sc=(X*e).groupby(df["day"]).sum()
        se=np.sqrt((sc**2).sum())/(X*X).sum()
        return pd.Series({"n":len(df),"slope":b,"t":b/se})
    out={}
    # trend groups by 60d (within window) and 30d
    def tg(v): return np.where(v>0.10,"rising",np.where(v<-0.10,"falling","choppy"))
    g5["tg30"]=tg(g5["tr30"]); g5["tg60"]=np.where(g5.tr60.isna(),"na",tg(g5["tr60"]))
    g5["agit"]=np.where(g5["vol10"]>g5.groupby("coin")["vol10"].transform("median"),"agit","calm")
    out["dist_slope_by_tg30_agit"]=g5.groupby(["tg30","agit"]).apply(lambda d: slope(d,"dist","ex5"))
    out["dist_slope_by_regime"]=g5.groupby("regime").apply(lambda d: slope(d,"dist","ex5"))
    g5["dq"]=g5.groupby("coin")["dist"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["ex5_by_dist_quint"]=g5.groupby("dq").apply(lambda d: dt(d,"ex5"))
    out["ex5_by_dist_quint_x_tg30"]=g5.groupby(["tg30","dq"]).apply(lambda d: dt(d,"ex5")).reset_index().pivot(index="dq",columns="tg30",values=["mean%","t_day"])
    # after large moves 1 day
    g1["rq"]=g1.groupby("coin")["ret1"].transform(lambda s: pd.qcut(s,10,labels=False,duplicates="drop"))
    out["ex1_by_ret1_decile"]=g1.groupby("rq").apply(lambda d: dt(d,"ex1"))
    g5["r3q"]=g5.groupby("coin")["ret3"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["ex5_by_ret3_quint"]=g5.groupby("r3q").apply(lambda d: dt(d,"ex5"))
    g1["wd"]=g1["ts"].dt.dayofweek
    out["ex1_by_weekday"]=g1.groupby("wd").apply(lambda d: dt(d,"ex1"))
    g5["vq"]=g5.groupby("coin")["volrel"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["ex5_by_volrel_quint"]=g5.groupby("vq").apply(lambda d: dt(d,"ex5"))
    out["ex5_by_tg30_agit"]=g5.groupby(["tg30","agit"]).apply(lambda d: dt(d,"ex5"))
    # trades
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values()],ignore_index=True)
    out["trades"]=pd.Series({"n":len(T),"mean_net%":T["net_profit_loss_percent"].mean(),"win":(T["net_profit_loss_percent"]>0).mean(),"med_dur_days":T["duration_minutes"].median()/1440})
    out["trades_by_coin"]=T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","median"])
    return out
