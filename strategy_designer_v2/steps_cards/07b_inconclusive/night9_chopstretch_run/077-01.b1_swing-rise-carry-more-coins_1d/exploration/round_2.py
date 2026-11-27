def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            vsr=(c/c.shift(14)-1)/(r.rolling(30).std()*np.sqrt(14))
            yr=pd.to_datetime(b["timestamp"]).dt.year
            n=len(b)
            for h in (3,5,7,10):
                for i in range(0,n-h,h):
                    rows.append(dict(coin=coin,w=w,h=h,ret=c[i+h]/c[i]-1,vsr=vsr[i],reg=b["regime"][i],yr=yr[i],ts=str(b["timestamp"][i])[:10]))
    d=pd.DataFrame(rows)
    d["drift"]=d.groupby(["coin","h"])["ret"].transform("mean")
    d["un"]=d["ret"]-d["drift"]
    d=d.dropna(subset=["vsr"])
    d["inprof"]=d["reg"]!="chop"
    def slope(g):
        g=g.copy()
        if len(g)<8: return pd.Series(dict(n=len(g),days=g.ts.nunique(),beta=np.nan,t=np.nan,sp=np.nan))
        x=g.vsr-g.vsr.mean(); y=g.un
        beta=(x*y).sum()/(x*x).sum()
        e=y-y.mean()-beta*x
        s=(x*e).groupby(g.ts).sum(); D=len(s)
        se=np.sqrt((s**2).sum()*D/max(D-1,1))/(x*x).sum()
        return pd.Series(dict(n=len(g),days=D,beta=beta,t=beta/se,sp=g[["vsr","un"]].corr("spearman").iloc[0,1]))
    def tclu(g):
        m=g.un.mean(); s=(g.un-m).groupby(g.ts).sum(); D=len(s); n=len(g)
        se=np.sqrt((s**2).sum()*D/max(D-1,1))/n
        return pd.Series(dict(n=n,days=D,mean=m,t=m/se if D>2 else np.nan))
    out={}
    a=d[d.inprof]
    out["in_slope_by_h"]=a.groupby("h").apply(slope)
    out["out_slope_by_h"]=d[~d.inprof].groupby("h").apply(slope)
    out["in_slope_pos_side_by_h"]=a[a.vsr>0].groupby("h").apply(slope)
    out["in_slope_neg_side_by_h"]=a[a.vsr<0].groupby("h").apply(slope)
    a7=a[a.h==7]
    out["in_h7_slope_by_year"]=a7.groupby("yr").apply(slope)
    out["in_h7_slope_by_coin"]=a7.groupby("coin").apply(slope)
    out["in_vsr_gt1_by_h"]=a[a.vsr>1].groupby("h").apply(tclu)
    out["in_vsr_lt_m05_by_h"]=a[a.vsr<-0.5].groupby("h").apply(tclu)
    out["in_vsr_dist"]=a7.vsr.describe()
    return out
