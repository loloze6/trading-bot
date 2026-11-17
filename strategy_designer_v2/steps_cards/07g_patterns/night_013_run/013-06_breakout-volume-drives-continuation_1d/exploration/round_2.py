def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    days=data["days"]; bars=data["bars"]
    out={}
    D=[]
    for c in days:
        for w,df in days[c].items():
            d=df.copy().reset_index(drop=True); d["coin"]=c; d["w"]=w
            r=d.coin_return
            d["prev"]=r.shift(1)
            d["sd20"]=r.shift(1).rolling(20,min_periods=15).std()
            d["z"]=d.prev/d.sd20
            d["prev3"]=(1+r).shift(1).rolling(3).apply(np.prod,raw=True)-1
            # 3-day forward return non-overlapping later
            cl=d.close
            d["f3"]=cl.shift(-3)/cl-1
            d["pos"]=np.arange(len(d))
            D.append(d)
    D=pd.concat(D,ignore_index=True)
    D["yr"]=pd.to_datetime(D.day).dt.year; D["wd"]=pd.to_datetime(D.day).dt.weekday
    D["ex"]=D.coin_return-D.groupby("coin").coin_return.transform("mean")
    dd=D.dropna(subset=["z","ex"])
    res=[]
    for c,g in dd.groupby("coin"):
        s1=stats.linregress(g.prev,g.ex); s2=stats.linregress(g.z,g.ex)
        res.append(dict(coin=c,n=len(g),t_prev=s1.slope/s1.stderr,t_z=s2.slope/s2.stderr,spear=stats.spearmanr(g.z,g.ex).correlation))
    out["reversal_per_coin"]=pd.DataFrame(res)
    res=[]
    for y,g in dd.groupby("yr"):
        s2=stats.linregress(g.z,g.ex); res.append(dict(yr=y,n=len(g),t_z=s2.slope/s2.stderr))
    out["reversal_per_year"]=pd.DataFrame(res)
    dd=dd.copy(); dd["zq"]=pd.qcut(dd.z,10,labels=False)
    out["next_day_by_z_decile"]=dd.groupby("zq").agg(z=("z","mean"),ex=("ex","mean"),n=("ex","count"),sd=("ex","std")).assign(t=lambda x:x.ex/(x.sd/np.sqrt(x.n)))
    # trimmed: drop days with |ex|>3sd to see if outliers drive
    tr=dd[(dd.ex.abs()<dd.groupby("coin").ex.transform("std")*3)]
    s=stats.linregress(tr.z,tr.ex); out["reversal_trimmed_t"]=float(s.slope/s.stderr)
    # 3-day horizon non-overlapping after 3-day past return
    g3=D[(D.pos%3==0)].dropna(subset=["prev3","f3","sd20"]).copy()
    g3["ex3"]=g3.f3-g3.groupby("coin").f3.transform("mean"); g3["z3"]=g3.prev3/(g3.sd20*np.sqrt(3))
    s=stats.linregress(g3.z3,g3.ex3); out["reversal_3d_t_n"]=f"t={s.slope/s.stderr:.2f} n={len(g3)}"
    # weekday per coin and per year
    D2=D.dropna(subset=["ex"])
    out["sat_ex_by_coin"]=D2[D2.wd==5].groupby("coin").ex.agg(["mean","count"])
    out["sat_ex_by_year"]=D2[D2.wd==5].groupby("yr").ex.agg(["mean","count"])
    out["weekday_ex_pooled"]=D2.groupby("wd").ex.agg(["mean","std","count"]).assign(t=lambda x:x["mean"]/(x["std"]/np.sqrt(x["count"])))
    # volume ratio predicting 7d, per year (non-overlapping)
    rows=[]
    for c in bars:
        for w,df in bars[c].items():
            d=df.reset_index(drop=True); cl=d.close.astype(float); v=d.volume.astype(float)
            for i in range(30,len(d)-7,7):
                rows.append(dict(coin=c,yr=pd.Timestamp(d.timestamp.iloc[i]).year,fwd=cl.iloc[i+7]/cl.iloc[i]-1,
                    vr=np.log(v.iloc[i]/v.iloc[i-30:i].mean()),r1=cl.iloc[i]/cl.iloc[i-1]-1))
    S=pd.DataFrame(rows); S["ex"]=S.fwd-S.groupby("coin").fwd.transform("mean")
    S=S.replace([np.inf,-np.inf],np.nan).dropna()
    res=[]
    for y,g in S.groupby("yr"):
        s=stats.linregress(g.vr,g.ex); res.append(dict(yr=y,n=len(g),t=s.slope/s.stderr))
    out["logvr_7d_by_year"]=pd.DataFrame(res)
    S["up"]=(S.r1>0).astype(int)
    res=[]
    for u,g in S.groupby("up"):
        s=stats.linregress(g.vr,g.ex); res.append(dict(up=u,n=len(g),slope=s.slope,t=s.slope/s.stderr))
    out["logvr_7d_by_dayside"]=pd.DataFrame(res)
    return out
