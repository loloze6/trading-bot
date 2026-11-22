import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H=5
    rows=[]; allgrid={}
    for coin,ws in data["bars"].items():
        g=[]
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; hi=b["high"]; lo=b["low"]
            r10=b["close"]/b["close"].shift(10)-1
            ext=r10/r10.abs().rolling(60).mean()
            hh=hi.rolling(30).max(); ll=lo.rolling(30).min()
            nmr=(b["close"]-b["close"].shift(30)).abs()/(hh-ll)
            pos=(b["close"]-(hh+ll)/2)/(hh-ll)
            year=pd.to_datetime(b["timestamp"]).dt.year
            for i in range(0,len(b)-H,H):
                ret=c[i+H]/c[i]-1
                g.append(ret)
                f=b["forecast"].iloc[i]
                if f<0:
                    rows.append(dict(coin=coin,w=w,year=year.iloc[i],f=abs(f),ret=ret,ext=ext.iloc[i],nmr=nmr.iloc[i],pos=pos.iloc[i],r10=r10.iloc[i]))
        allgrid[coin]=np.mean(g)
    d=pd.DataFrame(rows)
    d["u"]=-(d["ret"]-d["coin"].map(allgrid))
    def agg(x):
        return pd.Series(dict(n=len(x),mean_u=x.u.mean(),t=x.u.mean()/(x.u.std()/np.sqrt(len(x))) if len(x)>2 else np.nan, mean_total=-x.ret.mean()))
    out={}
    out["all"]=agg(d)
    d["fq"]=pd.qcut(d.f.rank(method="first"),4,labels=["q1","q2","q3","q4"])
    out["by_forecast_quartile"]=d.groupby("fq").apply(agg)
    out["by_coin"]=d.groupby("coin").apply(agg)
    out["by_year"]=d.groupby("year").apply(agg)
    d["extq"]=pd.qcut(d.ext.rank(method="first"),4,labels=["deep","mid1","mid2","shallow"])
    out["by_ext_quartile"]=d.groupby("extq").apply(agg)
    d["nmrq"]=pd.qcut(d.nmr.rank(method="first"),3,labels=["low","mid","high"])
    out["by_nmr_tercile"]=d.groupby("nmrq").apply(agg)
    d["posq"]=pd.qcut(d.pos.rank(method="first"),3,labels=["lowest","mid","nearmid"])
    out["by_range_pos_tercile"]=d.groupby("posq").apply(agg)
    d["r10s"]=np.where(d.r10<0,"r10neg","r10pos")
    out["by_r10_sign"]=d.groupby("r10s").apply(agg)
    out["corr_f_u"]=pd.Series(stats.spearmanr(d.f,d.u)[:2],index=["rho","p"])
    out["coin_mean5"]=pd.Series(allgrid)
    return out
