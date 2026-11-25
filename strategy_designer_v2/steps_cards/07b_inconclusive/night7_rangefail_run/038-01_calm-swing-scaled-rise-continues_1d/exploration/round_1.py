def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(20).std()
            x=(c/c.shift(5)-1)/(sd*np.sqrt(5))
            tr60=c/c.shift(60)-1
            yr=pd.to_datetime(df["timestamp"]).dt.year
            for h in [1,3,5,10,20]:
                fwd=c.shift(-h)/c-1
                idx=np.arange(0,len(df),h)
                for i in idx:
                    if np.isnan(fwd.iloc[i]) or np.isnan(x.iloc[i]): continue
                    rows.append(dict(coin=coin,w=w,h=h,x=x.iloc[i],f=fwd.iloc[i],reg=df["regime"].iloc[i],
                                     fc=df["forecast"].iloc[i],tr=tr60.iloc[i],yr=yr.iloc[i],day=str(df["timestamp"].iloc[i])[:10]))
    d=pd.DataFrame(rows)
    d["drift"]=d.groupby(["coin","h"])["f"].transform("mean")
    d["ex"]=d["f"]-d["drift"]
    d["calm"]=d["reg"]!="chop"
    d["side"]=np.where(d["x"]>0,"up","down")
    d["dex"]=np.where(d["x"]>0,d["ex"],-d["ex"])
    def summ(g):
        dd=g.groupby("day")["dex"].sum()
        t=dd.mean()/(dd.std()/np.sqrt(len(dd))) if len(dd)>2 else np.nan
        sl=stats.linregress(g["x"].abs(),g["dex"]) if len(g)>5 else None
        return pd.Series(dict(n=len(g),mean_dex=g["dex"].mean(),t_day=t,slope_t=(sl.slope/sl.stderr) if sl else np.nan))
    out={}
    out["by_h_calm_side"]=d.groupby(["h","calm","side"]).apply(summ)
    d5=d[d.h==5].copy()
    d5["q"]=d5.groupby(["calm","side"])["x"].transform(lambda s: pd.qcut(s.abs(),4,labels=False,duplicates="drop"))
    out["h5_quartile"]=d5.groupby(["calm","side","q"]).apply(summ)
    d5["trend"]=pd.cut(d5["tr"],[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    out["h5_trend"]=d5.groupby(["calm","side","trend"]).apply(summ)
    out["h5_year_calm_up"]=d5[d5.calm&(d5.side=="up")].groupby("yr").apply(summ)
    out["h5_coin_calm_up"]=d5[d5.calm&(d5.side=="up")].groupby("coin").apply(summ)
    return out
