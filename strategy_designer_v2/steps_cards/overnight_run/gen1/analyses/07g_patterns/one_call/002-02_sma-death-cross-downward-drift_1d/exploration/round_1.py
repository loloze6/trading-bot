def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy()
            c=b["close"].astype(float)
            r1=np.log(c).diff()
            f10=np.log(c.shift(-10))-np.log(c)
            vol=r1.rolling(20).std()
            sp=b["debug_info.components.sma_cross_down.last_history_value"].astype(float)
            d=pd.DataFrame({"coin":coin,"w":w,"r1":r1,"f10":f10,"f1":r1.shift(-1),
                            "vol":vol,"fc":b["forecast"].astype(float),"sp":sp,
                            "z":r1/vol.shift(1),"ret20":np.log(c)-np.log(c.shift(20)),
                            "wd":pd.to_datetime(b["timestamp"]).dt.dayofweek,
                            "yr":pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["f10x"]=D["f10"]-D.groupby("coin")["f10"].transform("mean")
    D["f1x"]=D["f1"]-D.groupby("coin")["f1"].transform("mean")
    def summ(g,col="f10x"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)/ (10 if col=="f10x" else 1)) if len(x)>2 else np.nan,"up":(x>0).mean()})
    out={}
    D["spb"]=pd.qcut(D["sp"],8,duplicates="drop")
    out["fwd10 excess by raw spread octile"]=D.groupby("spb").apply(summ)
    D["zb"]=pd.cut(D["z"],[-99,-2.5,-1.5,-0.5,0.5,1.5,2.5,99])
    out["fwd1 excess by today's z-move"]=D.groupby("zb").apply(lambda g:summ(g,"f1x"))
    out["fwd10 excess by today's z-move"]=D.groupby("zb").apply(summ)
    D["vq"]=D.groupby("coin")["vol"].transform(lambda s:pd.qcut(s,4,labels=False,duplicates="drop"))
    out["fwd10 excess by vol quartile"]=D.groupby("vq").apply(summ)
    D["r20q"]=D.groupby("coin")["ret20"].transform(lambda s:pd.qcut(s,5,labels=False,duplicates="drop"))
    out["fwd10 excess by 20d return quintile"]=D.groupby("r20q").apply(summ)
    out["fwd1 excess by weekday"]=D.groupby("wd").apply(lambda g:summ(g,"f1x"))
    out["fwd10 excess by coin, short vs flat"]=D.groupby(["coin",D["fc"]<0]).apply(summ)
    out["fwd10 by year short vs flat"]=D.groupby(["yr",D["fc"]<0]).apply(summ)
    # trades
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items()],ignore_index=True)
    T["days"]=T["duration_minutes"]/1440
    out["trades"]=T.groupby("coin").agg(n=("side","size"),mean_pl=("net_profit_loss_percent","mean"),win=("net_profit_loss_percent",lambda x:(x>0).mean()),med_days=("days","median"))
    return out
