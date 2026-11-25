import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    H=[1,5,10,20]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"].values
            n=len(df)
            for h in H:
                for i in range(0,n-h,h):
                    rows.append(dict(coin=coin,w=w,h=h,i=i,year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                        day=str(pd.Timestamp(df["timestamp"].iloc[i]).date()),
                        ret=c[i+h]/c[i]-1,reg=df["regime"].iloc[i],fc=df["forecast"].iloc[i],
                        raw=df.get("debug_info.components.near_high.last_history_value",pd.Series([np.nan]*n)).iloc[i]))
    R=pd.DataFrame(rows)
    R["drift"]=R.groupby(["coin","h"])["ret"].transform("mean")
    R["ex"]=R["ret"]-R["drift"]
    P=R[(R.reg=="unknown")&R.fc.notna()].copy()
    def slope(d):
        if len(d)<20 or d.fc.std()==0: return pd.Series(dict(n=len(d),slope=np.nan,t=np.nan))
        x=d.fc-d.fc.mean(); b=(x*d.ex).sum()/(x*x).sum()
        e=d.ex-d.ex.mean()-b*x
        g=(x*e).groupby(d.day).sum(); se=np.sqrt((g**2).sum())/(x*x).sum()
        return pd.Series(dict(n=len(d),slope=b,t=b/se))
    out={}
    out["by_h"]=P.groupby("h").apply(slope)
    P5=P[P.h==5]
    out["by_coin"]=P5.groupby("coin").apply(slope)
    out["by_window"]=P5.groupby("w").apply(slope)
    out["by_year"]=P5.groupby("year").apply(slope)
    P5=P5.copy()
    P5["fq"]=pd.qcut(P5.fc,6,duplicates="drop")
    out["fc_bins"]=P5.groupby("fq")["ex"].agg(["count","mean",lambda s:s.mean()/s.std()*np.sqrt(len(s))])
    P5["rq"]=pd.qcut(P5.raw,6,duplicates="drop")
    out["raw_bins"]=P5.groupby("rq")["ex"].agg(["count","mean",lambda s:s.mean()/s.std()*np.sqrt(len(s))])
    out["raw_slope"]=slope(P5.assign(fc=P5.raw))
    for h in H:
        Ph=P[P.h==h]
        out[f"raw_slope_h{h}"]=slope(Ph.assign(fc=Ph.raw))
    out["all_bars_mean_ex_inprofile"]=P5.ex.mean()
    return out
