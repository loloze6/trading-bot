def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    drift={}
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            allr.append((b["close"].shift(-1)/b["close"]-1).dropna())
        drift[coin]=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(30).std()
            width=((b["high"]-b["low"])/c)/sd
            loc=(c-b["low"])/(b["high"]-b["low"])
            ret=c.pct_change()
            for i in range(len(b)):
                d=dict(coin=coin,w=w,yr=pd.Timestamp(b["timestamp"].iloc[i]).year,
                       case=b["forecast"].iloc[i]<0,regime=b["regime"].iloc[i],
                       width=width.iloc[i],loc=loc.iloc[i],dayret=ret.iloc[i],sd=sd.iloc[i],
                       wd=pd.Timestamp(b["timestamp"].iloc[i]).weekday(),
                       ts=str(b["timestamp"].iloc[i])[:10])
                for h in (1,2,3,5):
                    d[f"f{h}"]=c.iloc[i+h]/c.iloc[i]-1 if i+h<len(b) else np.nan
                rows.append(d)
    df=pd.DataFrame(rows)
    df["dr"]=df.coin.map(drift)
    for h in (1,2,3,5):
        df[f"u{h}"]=-(df[f"f{h}"]-h*df["dr"])
    cs=df[df.case].copy()
    out={}
    def summ(g):
        x=g["u1"].dropna()
        return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,
                              pos=(x>0).mean(),med=x.median()))
    out["all_h"]=pd.DataFrame({f"u{h}":[cs[f"u{h}"].mean(),cs[f"u{h}"].count(),
        cs[f"u{h}"].mean()/(cs[f"u{h}"].std()/np.sqrt(cs[f"u{h}"].count()))] for h in (1,2,3,5)},index=["mean","n","t"])
    out["by_coin"]=cs.groupby("coin").apply(summ)
    out["by_window"]=cs.groupby("w").apply(summ)
    out["by_year"]=cs.groupby("yr").apply(summ)
    cs["wq"]=pd.qcut(cs["width"],3,labels=False,duplicates="drop")
    out["by_width_tercile"]=cs.groupby("wq").apply(summ).join(cs.groupby("wq")["width"].mean())
    cs["lq"]=pd.qcut(cs["loc"],3,labels=False,duplicates="drop")
    out["by_loc_tercile"]=cs.groupby("lq").apply(summ).join(cs.groupby("lq")["loc"].mean())
    cs["rq"]=pd.qcut(cs["dayret"],3,labels=False,duplicates="drop")
    out["by_dayret_tercile"]=cs.groupby("rq").apply(summ).join(cs.groupby("rq")["dayret"].mean())
    out["corr"]=pd.Series(dict(width_u1=cs[["width","u1"]].corr().iloc[0,1],loc_u1=cs[["loc","u1"]].corr().iloc[0,1],
                               dayret_u1=cs[["dayret","u1"]].corr().iloc[0,1]))
    out["by_weekday"]=cs.groupby("wd").apply(summ)
    # outliers
    x=cs["u1"].dropna()
    out["trim"]=pd.Series(dict(mean=x.mean(),trim5=stats.trim_mean(x,0.05),top3_share=x.nlargest(3).sum()/x.sum(),std=x.std()))
    # same situation outside profile
    sit=(df.width>=2)&(df["loc"]>=0.9)
    out["sit_by_regime"]=df[sit].groupby("regime").apply(summ)
    return out
