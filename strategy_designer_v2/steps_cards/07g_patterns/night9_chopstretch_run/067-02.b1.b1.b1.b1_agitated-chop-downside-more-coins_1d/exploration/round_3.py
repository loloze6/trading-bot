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
            ts=pd.to_datetime(b["timestamp"])
            n=len(b)
            for h in (5,10):
                for i in range(0,n-h,h):
                    rows.append(dict(h=h,coin=coin,w=w,wn=int(w[1:]),reg=str(b["regime"].iloc[i]),z=z.iloc[i],
                        tr60=tr60.iloc[i],fwd=c.iloc[i+h]/c.iloc[i]-1,day=ts.iloc[i].normalize()))
    d=pd.DataFrame(rows)
    d["u"]=d["fwd"]-d.groupby(["h","coin"])["fwd"].transform("mean")
    d=d.dropna(subset=["z","tr60","u"]).copy()
    d["trend"]=np.where(d.tr60>0.1,"rising",np.where(d.tr60<-0.1,"falling","choppy"))
    d["prof"]=np.where(d.reg!="chop","agit_inprof","other")
    d["fold"]=np.where(d.wn<=12,"B","C")
    def slope(g):
        # graded: regression of u on z, day-clustered t
        if len(g)<10: return pd.Series(dict(n=len(g),days=np.nan,slope=np.nan,t=np.nan,spear=np.nan))
        x=g.z.values; y=g.u.values
        xm=x-x.mean(); b=(xm*(y-y.mean())).sum()/(xm**2).sum()
        e=(y-y.mean()-b*xm)
        s=pd.Series(xm*e).groupby(g.day.values).sum()
        G=len(s); se=np.sqrt((s**2).sum()*G/(G-1))/(xm**2).sum()
        return pd.Series(dict(n=len(g),days=G,slope=b,t=b/se,spear=stats.spearmanr(x,y)[0]))
    out={}
    out["slope_by_trend_prof_h"]=d.groupby(["h","trend","prof"]).apply(slope)
    out["slope_by_trend_h_fold"]=d.groupby(["h","trend","fold"]).apply(slope)
    ch=d[(d.trend=="choppy")&(d.prof=="other")]
    out["choppy_calm_slope_by_side_h"]=ch.assign(zs=np.where(ch.z>0,"above","below")).groupby(["h","zs"]).apply(slope)
    out["all_slope_by_h_fold"]=d.groupby(["h","fold"]).apply(slope)
    fa=d[(d.trend=="falling")]
    out["falling_slope_by_side_h"]=fa.assign(zs=np.where(fa.z>0,"above","below")).groupby(["h","zs"]).apply(slope)
    return out
