import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sma=c.rolling(20).mean()
            sd=r.rolling(20).std()
            z=(c-sma)/sma/sd
            tr60=c/c.shift(60)-1
            r1=r
            r3=c/c.shift(3)-1
            vol30=r.rolling(30).std()
            ts=pd.to_datetime(b["timestamp"])
            n=len(b)
            for i in range(0,n-5,5):
                rows.append(dict(coin=coin,w=w,inprof=b["regime"].iloc[i]!="chop",z=z.iloc[i],
                    tr60=tr60.iloc[i],r1=r1.iloc[i],r3=r3.iloc[i],vol30=vol30.iloc[i],
                    fc=b["forecast"].iloc[i],alloc=b["postRebalance_current_allocation"].iloc[i],
                    fwd=c.iloc[i+5]/c.iloc[i]-1,wd=ts.iloc[i].weekday(),yr=ts.iloc[i].year))
    d=pd.DataFrame(rows)
    drift=d.groupby("coin")["fwd"].mean()
    d["u"]=d["fwd"]-d["coin"].map(drift)
    def agg(g):
        x=g["u"].dropna()
        return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    out={}
    dz=d.dropna(subset=["z"]).copy()
    dz["zq"]=pd.qcut(dz["z"],5,labels=False)
    out["all_by_zquint"]=dz.groupby("zq").apply(agg)
    out["inprof_by_zquint"]=dz[dz.inprof].groupby("zq").apply(agg)
    dt=dz.dropna(subset=["tr60"]).copy()
    dt["trend"]=np.where(dt.tr60>0.1,"rising",np.where(dt.tr60<-0.1,"falling","choppy"))
    dt["zs"]=np.where(dt.z>0,"above","below")
    out["trend_x_side"]=dt.groupby(["trend","zs"]).apply(agg)
    dt["zq"]=pd.qcut(dt["z"],5,labels=False)
    out["choppy_by_zq"]=dt[dt.trend=="choppy"].groupby("zq").apply(agg)
    out["rising_by_zq"]=dt[dt.trend=="rising"].groupby("zq").apply(agg)
    out["falling_by_zq"]=dt[dt.trend=="falling"].groupby("zq").apply(agg)
    d1=d.dropna(subset=["r3","vol30"]).copy()
    d1["s3"]=d1.r3/(d1.vol30*np.sqrt(3))
    d1["s3q"]=pd.qcut(d1["s3"],5,labels=False)
    out["by_3day_scaled_move_q"]=d1.groupby("s3q").apply(agg)
    out["by_weekday"]=d.groupby("wd").apply(agg)
    out["by_year"]=d.groupby("yr").apply(agg)
    # book daily
    dd=[]
    for coin,wins in data["days"].items():
        for w,x in wins.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    D=pd.concat(dd)
    D["wd"]=pd.to_datetime(D["day"]).dt.weekday
    out["book_by_window"]=D.groupby("w")["book_return"].agg(["mean","std","count"])
    out["book_by_coin"]=D.groupby("coin")["book_return"].agg(["mean","count"])
    T=[]
    for coin,wins in data["trades"].items():
        for w,x in wins.items():
            if len(x): x=x.copy(); x["coin"]=coin; T.append(x)
    T=pd.concat(T)
    T["fq"]=pd.qcut(T.entry_forecast.abs().rank(method="first"),4,labels=False)
    out["trades_by_fc_quart"]=T.groupby("fq")["profit_loss_percent"].agg(["mean","count","median"])
    out["trades_side"]=T.groupby("side")["profit_loss_percent"].agg(["mean","count"])
    return out
