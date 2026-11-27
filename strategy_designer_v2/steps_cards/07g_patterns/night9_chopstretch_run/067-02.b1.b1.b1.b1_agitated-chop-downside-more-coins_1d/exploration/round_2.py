import numpy as np, pandas as pd

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
                    rows.append(dict(h=h,coin=coin,w=w,reg=str(b["regime"].iloc[i]),z=z.iloc[i],
                        tr60=tr60.iloc[i],fc=b["forecast"].iloc[i],
                        raw=b["debug_info.components.stretch.last_history_value"].iloc[i] if "debug_info.components.stretch.last_history_value" in b else np.nan,
                        fwd=c.iloc[i+h]/c.iloc[i]-1,day=ts.iloc[i].normalize(),yr=ts.iloc[i].year))
    d=pd.DataFrame(rows)
    d["u"]=d["fwd"]-d.groupby(["h","coin"])["fwd"].transform("mean")
    def agg(g):
        g=g.dropna(subset=["u"])
        if len(g)<3: return pd.Series(dict(n=len(g),days=0,mean=np.nan,tcl=np.nan))
        dev=(g["u"]-g["u"].mean()).groupby(g["day"]).sum()
        G=len(dev); se=np.sqrt((dev**2).sum()*G/(G-1))/len(g)
        return pd.Series(dict(n=len(g),days=G,mean=g["u"].mean(),tcl=g["u"].mean()/se))
    out={}
    out["regime_counts"]=d[d.h==5]["reg"].value_counts()
    dt=d.dropna(subset=["tr60","z"]).copy()
    dt["trend"]=np.where(dt.tr60>0.1,"rising",np.where(dt.tr60<-0.1,"falling","choppy"))
    dt["agit"]=np.where(dt.reg!="chop","agitated_inprof","other")
    dt["zs"]=np.where(dt.z>0,"above","below")
    ch=dt[dt.trend=="choppy"].copy()
    out["choppy_by_agit_side_h"]=ch.groupby(["h","agit","zs"]).apply(agg)
    ch["zb"]=pd.cut(ch.z,[-99,-2,-1,0,1,2,99])
    out["choppy_h5_by_zbin"]=ch[ch.h==5].groupby("zb").apply(agg)
    out["choppy_h10_by_zbin"]=ch[ch.h==10].groupby("zb").apply(agg)
    out["choppy_h5_side_by_year"]=ch[ch.h==5].groupby(["yr","zs"]).apply(agg)
    d5=dt[dt.h==5].copy()
    d5["zb"]=pd.cut(d5.z,[-99,-2,-1,0,1,2,99])
    out["all_h5_by_zbin_clustered"]=d5.groupby("zb").apply(agg)
    out["all_h10_by_zbin_clustered"]=dt[dt.h==10].assign(zb=lambda x:pd.cut(x.z,[-99,-2,-1,0,1,2,99])).groupby("zb").apply(agg)
    ip=d[(d.h==5)&(d.reg!="chop")].dropna(subset=["z"])
    out["inprof_corr_fc_vs_z"]=float(ip[["fc","z"]].corr().iloc[0,1]) if len(ip)>3 else np.nan
    out["inprof_corr_raw_vs_z"]=float(ip[["raw","z"]].dropna().corr().iloc[0,1]) if ip["raw"].notna().sum()>3 else np.nan
    ip2=ip.copy(); ip2["fcneg"]=ip2.fc<0
    out["inprof_by_fc_short"]=ip2.groupby("fcneg").apply(agg)
    return out
