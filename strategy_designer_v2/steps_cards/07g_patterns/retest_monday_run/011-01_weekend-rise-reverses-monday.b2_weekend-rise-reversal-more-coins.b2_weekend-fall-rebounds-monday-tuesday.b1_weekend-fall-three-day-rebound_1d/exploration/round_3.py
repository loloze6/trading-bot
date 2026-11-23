def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        g=[]
        for w,df in wins.items():
            c=df["close"].values
            if len(c)>3: g.extend(list(c[3::3]/c[:-3:3]-1))
        m3=np.mean(g)
        for w,df in wins.items():
            d=df.copy()
            d["ts"]=pd.to_datetime(d["timestamp"],utc=True)
            d["wd"]=d["ts"].dt.weekday; d["year"]=d["ts"].dt.year
            d["date"]=d["ts"].dt.floor("D")
            d["r1"]=d["close"].pct_change()
            mu=d["r1"].rolling(60,min_periods=20).mean(); sd=d["r1"].rolling(60,min_periods=20).std()
            d["z"]=(d["r1"]-mu)/sd
            d["vol20"]=d["r1"].rolling(20).std()
            d["volrank"]=d["vol20"]/d["vol20"].rolling(120,min_periods=40).median()
            d["ex3"]=d["close"].shift(-3)/d["close"]-1-m3
            d["coin"]=coin; d["win"]=w
            rows.append(d[["coin","win","wd","year","date","z","ex3","volrank"]])
    A=pd.concat(rows).dropna(subset=["z","ex3"])
    out={}
    def tt(x):
        x=np.asarray(x,dtype=float); x=x[~np.isnan(x)]
        if len(x)<3: return pd.Series({"n":len(x),"mean%":np.nan,"t":np.nan})
        return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/(x.std(ddof=1)/np.sqrt(len(x)))})
    # Thursday: per coin fall product, share of coins positive
    T=A[A.wd==3].copy(); T["pf"]=(-T.z).clip(lower=0)*T.ex3
    pc=T.groupby("coin")["pf"].mean()
    out["thu_fall_per_coin"]=pd.Series({"coins":len(pc),"share_pos":(pc>0).mean(),"median%":100*pc.median()}).round(3)
    # Thursday clustered by date, z<=-1 vs rest
    T["big"]=T.z<=-1
    cl=T[T.big].groupby("date")["ex3"].mean()
    out["thu_fall1_clustered"]=tt(cl).round(3)
    # all days, falls z<=-1 clustered, by weekday group
    F=A[A.z<=-1].copy()
    F["grp"]=np.where(F.wd==6,"sun",np.where(F.wd==3,"thu","other"))
    out["fall1_clustered_by_grp"]=F.groupby(["grp","date"])["ex3"].mean().reset_index().groupby("grp")["ex3"].apply(tt).unstack().round(3)
    # Sunday rises clustered, by size
    S=A[(A.wd==6)&(A.z>0)].copy()
    S["zb"]=pd.cut(S.z,[0,0.5,1,99])
    out["sun_rise_clustered"]=S.groupby(["zb","date"],observed=True)["ex3"].mean().reset_index().groupby("zb",observed=True)["ex3"].apply(tt).unstack().round(3)
    # Sunday fall clustered by volatility tercile
    SF=A[(A.wd==6)&(A.z<=-0.5)].dropna(subset=["volrank"]).copy()
    SF["vq"]=pd.qcut(SF.volrank,3,labels=["calm","mid","wild"])
    out["sun_fall05_clust_by_vol"]=SF.groupby(["vq","date"],observed=True)["ex3"].mean().reset_index().groupby("vq",observed=True)["ex3"].apply(tt).unstack().round(3)
    # Sunday fall z<=-0.5 by year clustered
    out["sun_fall05_clust_by_year"]=SF.groupby(["year","date"])["ex3"].mean().reset_index().groupby("year")["ex3"].apply(tt).unstack().round(3)
    return out
