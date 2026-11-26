def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=3
    rows=[]; drows=[]
    for coin, wins in data["bars"].items():
        # coin drift over all windows, nonoverlapping 3d
        allg=[]
        for w,b in wins.items():
            c=b["close"].values
            for i in range(0,len(c)-H,H): allg.append(c[i+H]/c[i]-1)
        drift=np.mean(allg); usual=np.std(allg)
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            sd30=r.rolling(30,min_periods=20).std()
            z7=(c/c.shift(7)-1)/(sd30*np.sqrt(7))
            z1=r/sd30
            r3=c/c.shift(3)-1
            tr60=c/c.shift(60)-1
            volrel=sd30/sd30.rolling(60,min_periods=30).median()
            rng=(b["high"]-b["low"])/c/sd30
            clv=(c-b["low"])/(b["high"]-b["low"])
            fwd=c.shift(-H)/c-1
            fwd1=c.shift(-1)/c-1
            ts=pd.to_datetime(b["timestamp"])
            for i in range(0,len(b)-H,H):
                rows.append(dict(coin=coin,w=w,day=ts[i].normalize(),z7=z7[i],z1=z1[i],r3z=r3[i]/(sd30[i]*np.sqrt(3)) if sd30[i]>0 else np.nan,
                                 tr60=tr60[i],volrel=volrel[i],rng=rng[i],clv=clv[i],fwd=fwd[i],ex=fwd[i]-drift,s=(fwd[i]-drift)/usual,fc=b["forecast"][i],wd=ts[i].dayofweek))
            for i in range(1,len(b)-1):
                drows.append(dict(coin=coin,day=ts[i].normalize(),wd=ts[i].dayofweek,z1=z1[i],r1=r[i],fwd1=fwd1[i],
                                  alloc=b["postRebalance_current_allocation"][i]))
    g=pd.DataFrame(rows).dropna(subset=["ex"])
    d=pd.DataFrame(drows)
    def ct(df,col="ex"):
        x=df.dropna(subset=[col]); dev=x[col]
        s=x.assign(v=dev).groupby("day")["v"].sum()
        n=len(s); m=dev.mean()
        se=np.sqrt((s**2).sum())/len(x) if len(x)>0 else np.nan
        # clustered se of mean: sqrt(sum_day (sum dev - n_d*m)^2)/N
        cnt=x.groupby("day").size()
        se=np.sqrt(((s-cnt*m)**2).sum())/len(x)
        return pd.Series(dict(n=len(x),days=n,mean=m,t=m/se if se>0 else np.nan,mean_s=x["s"].mean() if "s" in x else np.nan))
    out={}
    gz=g.dropna(subset=["z7"])
    gz["zb"]=pd.cut(gz["z7"],[-9,-1.5,-0.75,-0.25,0.25,0.75,1.5,9])
    out["fwd3_by_z7"]=gz.groupby("zb").apply(ct)
    dn=gz[gz.z7<0]; up=gz[gz.z7>0]
    out["slope_down_weeks"]=pd.Series(stats.linregress(dn.z7,dn.ex)[:4],index=["slope","int","r","p"])
    out["slope_up_weeks"]=pd.Series(stats.linregress(up.z7,up.ex)[:4],index=["slope","int","r","p"])
    gt=gz.dropna(subset=["tr60"]).copy()
    gt["trend"]=pd.cut(gt.tr60,[-9,-0.1,0.1,99],labels=["falling","choppy","rising"])
    gt["agit"]=np.where(gt.volrel>1,"agit","calm")
    gt["sgn"]=np.where(gt.z7>0,"upweek","downweek")
    out["fwd3_by_trend_sgn"]=gt.groupby(["trend","sgn"]).apply(ct)
    out["fwd3_by_agit_sgn"]=gt.dropna(subset=["volrel"]).groupby(["agit","sgn"]).apply(ct)
    g1=g.dropna(subset=["z1"]).copy(); g1["b"]=pd.qcut(g1.z1,6)
    out["fwd3_by_z1"]=g1.groupby("b").apply(ct)
    g3=g.dropna(subset=["volrel"]).copy(); g3["b"]=pd.qcut(g3.volrel,5)
    out["fwd3_by_volrel"]=g3.groupby("b").apply(ct)
    g4=g.dropna(subset=["rng"]).copy(); g4["b"]=pd.qcut(g4.rng,5)
    out["fwd3_by_range"]=g4.groupby("b").apply(ct)
    g5=g.dropna(subset=["clv"]).copy(); g5["b"]=pd.qcut(g5.clv,5)
    out["fwd3_by_closeloc"]=g5.groupby("b").apply(ct)
    out["fwd3_by_weekday"]=g.groupby("wd").apply(ct)
    dd=d.dropna(subset=["fwd1"]).copy(); dd["ex"]=dd.fwd1-dd.groupby("coin").fwd1.transform("mean"); dd["s"]=np.nan
    out["ret1_next_by_weekday"]=dd.groupby("wd").apply(ct)
    return out
