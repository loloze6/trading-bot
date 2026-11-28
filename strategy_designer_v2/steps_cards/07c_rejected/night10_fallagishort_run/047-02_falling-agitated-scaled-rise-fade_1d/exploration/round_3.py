def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std().shift(1)
            z=r/sd
            fc=b["forecast"].astype(float)
            tr60=c/c.shift(60)-1
            rng=(b["high"]-b["low"])/c
            clpos=(c-b["low"])/(b["high"]-b["low"])
            h=3
            fwd=c.shift(-h)/c-1
            for off in [0,1,2]:
                for i in range(off,len(b),h):
                    if i+h>=len(b): continue
                    rows.append(dict(coin=coin,w=w,off=off,z=z.iloc[i],fc=fc.iloc[i],ret=fwd.iloc[i],
                        tr60=tr60.iloc[i],clpos=clpos.iloc[i],
                        inprof=b["regime"].iloc[i]=="unknown",day=str(b["timestamp"].iloc[i])[:10],
                        year=pd.Timestamp(b["timestamp"].iloc[i]).year))
    d=pd.DataFrame(rows)
    dr=d[d.off==0].groupby("coin")["ret"].mean().rename("drift")
    d=d.join(dr,on="coin"); d["unus"]=d["ret"]-d["drift"]
    d=d.dropna(subset=["z","unus"])
    out={}
    U=d[d.inprof&(d.z>0)]
    sl=[]
    for off,g in U.groupby("off"):
        res=stats.linregress(g["z"],g["unus"])
        sl.append(dict(off=off,n=len(g),slope=res.slope,t=res.slope/res.stderr,mean=g.unus.mean(),
            mean_zgt1=g[g.z>1].unus.mean(),n_zgt1=(g.z>1).sum(),mean_zle05=g[g.z<=0.5].unus.mean()))
    out["up_h3_by_offset"]=pd.DataFrame(sl)
    # pooled offsets, by year, slope
    sl=[]
    for y,g in U.groupby("year"):
        if len(g)<8: continue
        res=stats.linregress(g["z"],g["unus"]); sl.append(dict(year=y,n=len(g),slope=res.slope,t=res.slope/res.stderr))
    out["up_h3_slope_by_year_alloffsets"]=pd.DataFrame(sl)
    sl=[]
    for cn,g in U.groupby("coin"):
        res=stats.linregress(g["z"],g["unus"]); sl.append(dict(coin=cn,n=len(g),slope=res.slope,t=res.slope/res.stderr))
    out["up_h3_slope_by_coin_alloffsets"]=pd.DataFrame(sl)
    # close position within the day's range on up days, offset 0
    g=U[U.off==0].dropna(subset=["clpos"])
    g=g.assign(cb=pd.cut(g.clpos,[-0.01,0.5,0.8,1.01]))
    out["up_h3_by_closepos"]=g.groupby("cb").agg(n=("unus","size"),mean=("unus","mean"),z=("z","mean"))
    # day-clustered short-signed t, forecast<=-10 cases, offset 0
    g=U[(U.off==0)]
    for lab,gg in [("fc_le_-10",g[g.fc<=-10]),("fc_-10_-2",g[(g.fc>-10)&(g.fc<=-2)]),("z_gt_1",g[g.z>1])]:
        s=(-gg["unus"]).groupby(gg["day"]).sum(); G=len(s)
        m=(-gg["unus"]).mean()
        se=np.sqrt((s**2).sum()*G/(G-1))/len(gg) if G>1 else np.nan
        out["short_t_"+lab]=pd.Series({"cases":len(gg),"days":G,"mean_short":m,"t_day":m/se})
    return out
