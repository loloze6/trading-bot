def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; hrs=[]
    for coin, ws in data["bars"].items():
        g=[]
        for w,b in ws.items():
            c=b["close"].values.astype(float)
            idx=np.arange(0,len(c)-24,24)
            g.append(c[idx+24]/c[idx]-1)
        allg=np.concatenate(g); drift=allg.mean(); u=allg.std()
        for w,b in ws.items():
            c=b["close"].astype(float); ts=pd.to_datetime(b["timestamp"])
            r24=c/c.shift(24)-1; r72=c/c.shift(72)-1; r168=c/c.shift(168)-1
            fwd=c.shift(-24)/c-1
            vola=c.pct_change().rolling(168,min_periods=100).std()
            vol=b["volume"].astype(float)
            vz=vol.rolling(24).sum()/vol.rolling(168,min_periods=100).sum()*7
            df=pd.DataFrame({"coin":coin,"w":w,"z24":r24/u,"z72":r72/u,"r168":r168,"s":(fwd-drift)/u,
                             "vola":vola,"vz":vz,"yr":ts.dt.year.values,"pos":np.arange(len(c))})
            rows.append(df[df.pos%24==0])
            r1=c.pct_change()
            sd=r1.std()
            hrs.append(pd.DataFrame({"coin":coin,"h":ts.dt.hour.values,"r":(r1/sd).values,"wd":ts.dt.weekday.values}))
    G=pd.concat(rows,ignore_index=True).dropna(subset=["z24","s","vola","vz"])
    G["vt"]=G.groupby("coin")["vola"].transform(lambda v:pd.qcut(v,3,labels=False,duplicates="drop"))
    def ct(d,a="z24"):
        n=len(d); r=np.corrcoef(d[a],d.s)[0,1] if n>5 else np.nan
        return pd.Series({"n":n,"corr":r,"t":r*np.sqrt(n-2)/np.sqrt(1-r*r) if n>5 else np.nan,
                          "fall_mean_s":d[d[a]<0].s.mean(),"rise_mean_s":d[d[a]>0].s.mean()})
    out={}
    out["all"]=ct(G).to_frame().T.round(4)
    out["by_coin"]=G.groupby("coin").apply(ct).round(4)
    out["by_year"]=G.groupby("yr").apply(ct).round(4)
    out["by_vol_tercile"]=G.groupby("vt").apply(ct).round(4)
    F=G[G.z24<0]
    out["falls_only_by_vol_tercile"]=F.groupby("vt").apply(ct).round(4)
    out["falls_only_by_vol_tercile_by_halfyear"]=F.assign(p=(F.yr>=2022).astype(int)).groupby(["p","vt"]).apply(ct).round(4)
    G["vzt"]=pd.qcut(G.vz,3,labels=False,duplicates="drop")
    out["falls_by_volume_tercile"]=G[G.z24<0].groupby("vzt").apply(ct).round(4)
    out["72h_by_vol_tercile"]=G.dropna(subset=["z72"]).groupby("vt").apply(lambda d:ct(d,"z72")).round(4)
    H=pd.concat(hrs).dropna()
    out["hour_of_day_scaled_1h"]=H.groupby("h").r.agg(["mean","count","std"]).assign(t=lambda t:t["mean"]/(t["std"]/np.sqrt(t["count"]))).round(4)[["mean","t"]]
    return out
