def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        allr=[]
        for w,df in wins.items():
            c=df["close"].values
            allr.append(c[1:]/c[:-1]-1)
        cmean=np.concatenate(allr).mean()
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            ts=pd.to_datetime(df["timestamp"],utc=True)
            c=df["close"].astype(float)
            r1=c.shift(-1)/c-1
            r4=c.shift(-4)/c-1
            ret72=c/c.shift(72)-1
            pos=df["postRebalance_current_allocation"].astype(float)
            d=pd.DataFrame({"coin":coin,"w":w,"hour":ts.dt.hour,"year":ts.dt.year,
                            "r1x":r1-cmean,"r4x":r4-4*cmean,"ret72":ret72,"pos":pos,"regime":df["regime"]})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    # actual main measure pieces
    T=D[D.regime=="trending"].dropna(subset=["r1x"])
    T=T.assign(g=T.pos*T.r1x)
    def tt(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    out["main_by_coin"]=T.groupby("coin")["g"].apply(tt).unstack()
    out["main_by_year"]=T.groupby("year")["g"].apply(tt).unstack()
    T2=T.assign(side=np.where(T.pos>0,"long_after_fall",np.where(T.pos<0,"short_after_rise","flat")))
    out["main_by_side"]=T2.groupby("side")["g"].apply(tt).unstack()
    T2=T2.assign(q=pd.qcut(T2.pos.abs().rank(method="first"),5,labels=False))
    out["main_by_possize_q"]=T2.groupby("q")["g"].apply(tt).unstack()
    # all hours: fade signal sign(-ret72) * next 1h excess; t per hour (one per coin-day => independent)
    A=D.dropna(subset=["r1x","ret72"])
    A=A.assign(f=-np.sign(A.ret72)*A.r1x, fz=-A.ret72*A.r1x)
    out["fade_sign_by_hour(bar start)"]=A.groupby("hour")["f"].apply(tt).unstack()
    # 4h horizon from 11:00 bar, non-overlapping per day
    B=D[D.hour==11].dropna(subset=["r4x","ret72"])
    out["h11_fade4h"]=tt(-np.sign(B.ret72)*B.r4x)
    # quintile of ret72 at hour 11, mean next 1h excess
    H=D[D.hour==11].dropna(subset=["r1x","ret72"])
    H=H.assign(q=pd.qcut(H.ret72,5,labels=False))
    out["h11_next1h_by_ret72_quintile"]=H.groupby("q").agg(n=("r1x","size"),mean_ret72=("ret72","mean"),mean_r1x=("r1x","mean"))
    return out
