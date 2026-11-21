def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin, wins in data["bars"].items():
        allr=[]
        for w,df in wins.items():
            allr.append(df["close"].astype(float).pct_change().dropna())
        mu=pd.concat(allr).mean()
        sd=pd.concat(allr).std()
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float)
            r=c.pct_change()
            vol20=r.rolling(20).std()
            d=pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(len(df)),
                            "year":pd.to_datetime(df["timestamp"]).dt.year,
                            "fc":df["forecast"].astype(float),"z":r/vol20,"r":r,
                            "ret20":c/c.shift(20)-1,"vol20":vol20,"mu":mu,"sd":sd})
            for h in (1,2,3,5,10):
                d[f"f{h}"]=c.shift(-h)/c-1-mu*h
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    def tt(x):
        x=x.dropna()
        n=len(x)
        return pd.Series({"n":n,"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    def grid(S,h):
        return S.loc[S["pos"]%h==0,f"f{h}"]
    out={}
    out["coins_present"]=", ".join(sorted(D["coin"].unique()))
    D["fb"]=pd.cut(D["fc"],[-0.01,0,1,5,19.99,20.01],labels=["0","0-1","1-5","5-20","20"])
    out["by_fc_bucket_h1"]=D.groupby("fb",observed=True)["f1"].apply(tt).unstack()
    S=D[D["fc"]>=5].copy()
    out["fc5_by_horizon_nonoverlap"]=pd.DataFrame({h:tt(grid(S,h)) for h in (1,2,3,5,10)}).T
    out["fc5_by_coin"]=S.groupby("coin")["f1"].apply(tt).unstack()
    out["fc5_by_year"]=S.groupby("year")["f1"].apply(tt).unstack()
    S["trend"]=np.where(S["ret20"]>0,"up20","down20")
    out["fc5_by_trend20"]=S.groupby("trend")["f1"].apply(tt).unstack()
    S["volq"]=pd.qcut(S["vol20"],3,labels=["lowvol","mid","highvol"])
    out["fc5_by_vol"]=S.groupby("volq",observed=True)["f1"].apply(tt).unstack()
    D["zb"]=pd.cut(D["z"],[-99,-3,-2,-1.5,-1,-0.5,0,99])
    out["by_raw_z_h1"]=D.groupby("zb",observed=True)["f1"].apply(tt).unstack()
    out["by_raw_z_h3_grid"]=D[D["pos"]%3==0].groupby("zb",observed=True)["f3"].apply(tt).unstack()
    out["by_raw_z_h5_grid"]=D[D["pos"]%5==0].groupby("zb",observed=True)["f5"].apply(tt).unstack()
    out["fc5_up20_by_h"]=pd.DataFrame({h:tt(grid(S[S.trend=="up20"],h)) for h in (1,2,3,5)}).T
    out["fc5_down20_by_h"]=pd.DataFrame({h:tt(grid(S[S.trend=="down20"],h)) for h in (1,2,3,5)}).T
    # spearman of fall size vs next day on down days
    dn=D[(D["z"]<0)].dropna(subset=["z","f1"])
    out["down_days_corr_negz_f1"]=float(np.corrcoef(-dn["z"],dn["f1"])[0,1])
    out["down_days_n"]=len(dn)
    out["fc5_share_win_positive"]=float((S["f1"]>0).mean())
    return out
