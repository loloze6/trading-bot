def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        allr=[]
        for w,df in wins.items():
            c=df["close"].astype(float).values
            allr.append(pd.Series(c).pct_change().dropna())
        mu=pd.concat(allr).mean()
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float)
            r=c.pct_change()
            z=r/r.rolling(20).std()
            ret20=c/c.shift(20)-1
            vol20=r.rolling(20).std()
            for h in (1,2,3,5,10):
                df[f"f{h}"]=c.shift(-h)/c-1-mu*h
            d=pd.DataFrame({"coin":coin,"win":w,"year":pd.to_datetime(df["timestamp"]).dt.year,
                            "fc":df["forecast"].astype(float),"z":z,"r":r,"ret20":ret20,"vol20":vol20,
                            **{f"f{h}":df[f"f{h}"] for h in (1,2,3,5,10)}})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    def tt(x):
        x=x.dropna(); 
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    D["fb"]=pd.cut(D["fc"],[-0.01,0,1,5,19.99,20.01],labels=["0","0-1","1-5","5-20","20"])
    out={}
    out["by_fc_bucket_h1"]=D.groupby("fb")["f1"].apply(tt).unstack()
    S=D[D["fc"]>=5]
    out["fc5_by_horizon"]=pd.DataFrame({h:tt(S[f"f{h}"]) for h in ("f1","f2","f3","f5","f10")}).T
    out["fc5_by_coin"]=S.groupby("coin")["f1"].apply(tt).unstack()
    out["fc5_by_year"]=S.groupby("year")["f1"].apply(tt).unstack()
    S=S.copy()
    S["trend"]=np.where(S["ret20"]>0,"up20","down20")
    out["fc5_by_trend20"]=S.groupby("trend")["f1"].apply(tt).unstack()
    S["volq"]=pd.qcut(S["vol20"],3,labels=["lowvol","mid","highvol"])
    out["fc5_by_vol"]=S.groupby("volq")["f1"].apply(tt).unstack()
    D["zb"]=pd.cut(D["z"],[-99,-3,-2,-1.5,-1,-0.5,0,99])
    out["by_raw_z_h1"]=D.groupby("zb")["f1"].apply(tt).unstack()
    out["by_raw_z_h3"]=D.groupby("zb")["f3"].apply(tt).unstack()
    out["fc5_up20_by_h"]=pd.DataFrame({h:tt(S.loc[S.trend=="up20",h]) for h in ("f1","f2","f3","f5")}).T
    out["fc5_down20_by_h"]=pd.DataFrame({h:tt(S.loc[S.trend=="down20",h]) for h in ("f1","f2","f3","f5")}).T
    return out
