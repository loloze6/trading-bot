def explore(data):
    import numpy as np, pandas as pd
    H=18; out={}
    hb=[]; rows=[]
    for coin,ws in data["bars"].items():
        g=[]
        for w,df in ws.items():
            c=df["close"].values; idx=np.arange(0,len(c)-H,H); g.append(c[idx+H]/c[idx]-1)
        g=np.concatenate(g); drift=g.mean(); sd=g.std()
        for w,df in ws.items():
            df=df.reset_index(drop=True); c=df["close"]; v=df["volume"]
            r1=c.pct_change(); ts=pd.to_datetime(df["timestamp"])
            ma=r1.abs().rolling(180,min_periods=60).mean()
            nxt=c.shift(-1)/c-1
            hb.append(pd.DataFrame(dict(coin=coin,yr=ts.dt.year,hour=ts.dt.hour,wd=ts.dt.weekday,
                nb=nxt.values,nbs=(nxt/ma).values)))
            ret18=c/c.shift(18)-1
            vrel18=v.rolling(18).mean()/v.rolling(180,min_periods=60).mean()
            fwd=c.shift(-H)/c-1
            for i in np.arange(0,len(c)-H,H):
                rows.append(dict(coin=coin,yr=ts[i].year,f18=ret18[i]/ma[i] if ma[i] else np.nan,
                    vr=vrel18[i],s=(fwd[i]-drift)/sd))
    HB=pd.concat(hb).dropna()
    # bar starting hour+4: label by the bar whose return is measured
    HB["next_bar_hour"]=(HB["hour"]+4)%24
    HB["next_wd"]=np.where(HB["hour"]==20,(HB["wd"]+1)%7,HB["wd"])
    def tt(x): return x.mean()/(x.std()/np.sqrt(len(x)))
    a=HB.groupby("next_bar_hour")["nb"].agg(["mean","count"]); a["mean"]*=1e4; a["t"]=HB.groupby("next_bar_hour")["nb"].apply(tt)
    out["bar return bp by the bar's start hour (pooled)"]=a.round(2)
    p=HB.pivot_table(index="coin",columns="next_bar_hour",values="nbs",aggfunc=tt); out["t by coin x bar start hour (scaled)"]=p.round(2)
    p=HB.pivot_table(index="yr",columns="next_bar_hour",values="nbs",aggfunc=tt); out["t by year x bar start hour (scaled)"]=p.round(2)
    p=HB.pivot_table(index="coin",columns="next_wd",values="nbs",aggfunc=tt); out["t by coin x weekday of measured bar"]=p.round(2)
    p=HB.pivot_table(index="yr",columns="next_wd",values="nbs",aggfunc=tt); out["t by year x weekday of measured bar"]=p.round(2)
    # 20h bar strength vs previous bars' (12h,16h) return on same day? graded: prior 12-20h move
    R=pd.DataFrame(rows).dropna()
    R["fq"]=R.groupby("coin")["f18"].transform(lambda x: pd.qcut(x.rank(method="first"),3,labels=False))
    R["vq"]=R.groupby("coin")["vr"].transform(lambda x: pd.qcut(x.rank(method="first"),3,labels=False))
    out["strength f18 tercile x 3d volume tercile"]=R.pivot_table(index="fq",columns="vq",values="s",aggfunc="mean").round(4)
    out["t f18 x vol"]=R.pivot_table(index="fq",columns="vq",values="s",aggfunc=tt).round(2)
    out["count f18 x vol"]=R.pivot_table(index="fq",columns="vq",values="s",aggfunc="count")
    top=R[R.fq==2]
    out["top f18 tercile strength t by coin"]=top.groupby("coin")["s"].agg(["mean","count",tt]).round(3)
    out["top f18 tercile strength by year"]=top.groupby("yr")["s"].agg(["mean","count"]).round(3)
    out["corr f18 with strength, by coin (spearman)"]=R.groupby("coin").apply(lambda d: d["f18"].corr(d["s"],method="spearman")).round(3)
    return out
