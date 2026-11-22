def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            c=b["close"].astype(float)
            r=c.pct_change()
            vol=r.rolling(20,min_periods=15).std()
            c90=c/c.shift(90)-1
            d=pd.DataFrame({"coin":coin,"win":w,"r":r,"z":r/vol,
                            "fall":(b["regime"]=="mean_reversion").values,
                            "f1":c.shift(-1)/c-1,"f2":c.shift(-2)/c-1,
                            "r90":c90,
                            "ts":pd.to_datetime(b["timestamp"]),"pos":np.arange(len(b))})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for h in ["f1","f2"]:
        mu=D.groupby("coin")[h].mean(); sd=D.groupby("coin")[h].std()
        D["x"+h]=D[h]-D["coin"].map(mu)
        D["s"+h]=D["x"+h]/D["coin"].map(sd)
    D["year"]=D.ts.dt.year
    D["wd"]=D.ts.dt.dayofweek
    out={}
    def reg(df,x,y):
        df=df.dropna(subset=[x,y]); df=df[np.isfinite(df[x])]
        if len(df)<30: return pd.Series({"n":len(df)})
        s=stats.linregress(df[x].clip(-5,5),df[y])
        return pd.Series({"n":len(df),"slope":round(s.slope,4),"t":round(s.slope/s.stderr,2)})
    # slope of next-day strength on z, by regime, by year
    out["slope sf1~z by fall"]=D.groupby("fall").apply(lambda g:reg(g,"z","sf1"))
    out["slope sf1~z falling by year"]=D[D.fall].groupby("year").apply(lambda g:reg(g,"z","sf1"))
    out["slope sf1~z falling by coin"]=D[D.fall].groupby("coin").apply(lambda g:reg(g,"z","sf1"))
    out["slope sf1~z not falling by coin"]=D[~D.fall].groupby("coin").apply(lambda g:reg(g,"z","sf1"))
    # down days only: graded rebound?
    dn=D[D.z<0]
    out["down days: slope sf1~z by fall"]=dn.groupby("fall").apply(lambda g:reg(g,"z","sf1"))
    up=D[D.z>0]
    out["up days: slope sf1~z by fall"]=up.groupby("fall").apply(lambda g:reg(g,"z","sf1"))
    # deeper fall interacts? within falling, by r90 tercile
    F=D[D.fall].copy()
    F["r90q"]=pd.qcut(F.r90,3,labels=False)
    out["falling: slope sf1~z by r90 tercile"]=F.groupby("r90q").apply(lambda g:reg(g,"z","sf1"))
    # 2-day horizon, non-overlapping
    D2=D[D.pos%2==0]
    out["slope sf2~z by fall (nonoverlap)"]=D2.groupby("fall").apply(lambda g:reg(g,"z","sf2"))
    # weekday by year robustness: Thu+Fri minus Mon+Wed
    D["wg"]=np.where(D.wd.isin([3,4]),"ThuFri",np.where(D.wd.isin([0,2]),"MonWed","other"))
    a=D.groupby(["year","wg"])["sf1"].mean().unstack()
    out["weekday group mean sf1 by year"]=a.round(4)
    # raw unusual move per case size for z<-1 falling and z>1 falling
    out["raw xf1 by sign falling"]=pd.Series({"z<-1 mean xf1":D[D.fall&(D.z<-1)].xf1.mean(),
        "z>1 mean -xf1":-D[D.fall&(D.z>1)].xf1.mean(),
        "z<-1 n":int((D.fall&(D.z<-1)).sum()),"z>1 n":int((D.fall&(D.z>1)).sum())})
    return out
