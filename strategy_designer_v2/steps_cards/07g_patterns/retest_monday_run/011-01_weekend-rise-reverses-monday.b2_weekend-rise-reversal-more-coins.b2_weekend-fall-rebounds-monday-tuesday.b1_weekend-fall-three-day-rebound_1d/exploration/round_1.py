def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        # coin mean 3-bar return on grid
        g=[]
        for w,df in wins.items():
            c=df["close"].values
            r=c[3::3]/c[:-3:3]-1 if len(c)>3 else []
            g.extend(list(r))
        m3=np.mean(g) if len(g) else np.nan
        g1=[]
        for w,df in wins.items():
            g1.extend(list(df["close"].pct_change().dropna().values))
        m1=np.mean(g1)
        for w,df in wins.items():
            d=df.copy()
            d["ts"]=pd.to_datetime(d["timestamp"],utc=True)
            d["wd"]=d["ts"].dt.weekday
            d["year"]=d["ts"].dt.year
            d["r1"]=d["close"].pct_change()
            mu=d["r1"].rolling(60,min_periods=20).mean(); sd=d["r1"].rolling(60,min_periods=20).std()
            d["z"]=(d["r1"]-mu)/sd
            d["r2"]=d["close"]/d["close"].shift(2)-1
            sd2=d["r2"].rolling(60,min_periods=20).std()
            d["z2"]=(d["r2"]-d["r2"].rolling(60,min_periods=20).mean())/sd2
            d["ex3"]=d["close"].shift(-3)/d["close"]-1-m3
            d["ex1"]=d["close"].shift(-1)/d["close"]-1-m1
            d["vr"]=d["volume"]/d["volume"].rolling(60,min_periods=20).mean()
            d["vol20"]=d["r1"].rolling(20).std()
            d["volrank"]=d["vol20"]/d["vol20"].rolling(120,min_periods=40).median()
            d["tr30"]=d["close"]/d["close"].shift(30)-1
            d["coin"]=coin; d["win"]=w
            rows.append(d[["coin","win","wd","year","r1","z","z2","ex3","ex1","vr","volrank","tr30","volume"]])
    A=pd.concat(rows).dropna(subset=["z","ex3"])
    out={}
    def tt(x):
        x=np.asarray(x); x=x[~np.isnan(x)]
        return pd.Series({"n":len(x),"mean%":100*x.mean() if len(x) else np.nan,"t":x.mean()/(x.std(ddof=1)/np.sqrt(len(x))) if len(x)>2 else np.nan})
    # 1 falls/rises by weekday
    res=[]
    for wd in range(7):
        s=A[A.wd==wd]
        f=s[s.z<=-1]; f2=s[s.z<=-2]; u=s[s.z>=1]
        sl=stats.linregress(-s.z.clip(upper=0)*-1*-1 if False else s.z.clip(upper=0).abs(), s.ex3)
        res.append({"wd":wd,"n_fall1":len(f),"ex3_fall1%":100*f.ex3.mean(),"t_f1":tt(f.ex3)["t"],
                    "n_fall2":len(f2),"ex3_fall2%":100*f2.ex3.mean(),"t_f2":tt(f2.ex3)["t"],
                    "n_rise1":len(u),"ex3_rise1%":100*u.ex3.mean(),"t_r1":tt(u.ex3)["t"],
                    "slope_fall":sl.slope*100,"t_slope":sl.slope/sl.stderr})
    out["by_weekday_z_fwd3"]=pd.DataFrame(res).round(3)
    # weekday mean next-day excess return (all bars)
    out["weekday_next1"]=A.groupby("wd")["ex1"].apply(tt).unstack().round(3)
    S=A[(A.wd==6)&(A.z<=-1)].copy()
    S["vq"]=pd.qcut(S.vr,3,labels=["lowvol","mid","highvol"])
    out["sunfall_by_volume"]=S.groupby("vq")["ex3"].apply(tt).unstack().round(3)
    S["volq"]=pd.qcut(S.volrank,3,labels=["calm","mid","wild"])
    out["sunfall_by_volatility"]=S.groupby("volq")["ex3"].apply(tt).unstack().round(3)
    S["trend"]=np.where(S.tr30>0,"up30","down30")
    out["sunfall_by_trend"]=S.groupby("trend")["ex3"].apply(tt).unstack().round(3)
    out["sunfall_by_year"]=S.groupby("year")["ex3"].apply(tt).unstack().round(3)
    # two-day weekend (Fri close->Sun close)
    S2=A[(A.wd==6)&(A.z2<=-1)]
    out["sun_2day_fall"]=tt(S2.ex3).round(3)
    S2r=A[(A.wd==6)&(A.z2>=1)]
    out["sun_2day_rise"]=tt(S2r.ex3).round(3)
    # all-weekday large falls by vol tercile
    F=A[A.z<=-2].copy()
    F["volq"]=pd.qcut(F.volrank,3,labels=["calm","mid","wild"])
    out["allday_fall2_by_volatility"]=F.groupby("volq")["ex3"].apply(tt).unstack().round(3)
    # book
    D=[]
    for coin,wins in data["days"].items():
        for w,df in wins.items():
            x=df.copy(); x["coin"]=coin; x["win"]=w; D.append(x)
    D=pd.concat(D)
    D["day"]=pd.to_datetime(D["day"],utc=True)
    D["wd"]=D.day.dt.weekday; D["year"]=D.day.dt.year
    out["book_by_weekday_pct"]=(D.groupby("wd")["book_return"].mean()*100).round(4)
    out["book_by_year"]=D.groupby("year")["book_return"].apply(tt).unstack().round(4)
    br=D.dropna(subset=["book_return"])
    q=br.book_return.quantile([0.01,0.99])
    big_l=br[br.book_return<=q.iloc[0]]; big_g=br[br.book_return>=q.iloc[1]]
    out["book_extreme_coinret_pct"]=pd.Series({"n_loss":len(big_l),"loss_book%":100*big_l.book_return.mean(),"loss_coin%":100*big_l.coin_return.mean(),
        "n_gain":len(big_g),"gain_book%":100*big_g.book_return.mean(),"gain_coin%":100*big_g.coin_return.mean(),
        "share_sum_top1pct":big_g.book_return.sum()/br.book_return.sum(),"share_sum_bot1pct":big_l.book_return.sum()/br.book_return.sum()}).round(3)
    return out
