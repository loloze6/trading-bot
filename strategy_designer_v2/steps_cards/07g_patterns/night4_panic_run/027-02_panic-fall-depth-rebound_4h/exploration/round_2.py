def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; allgrid={h:[] for h in [6,18,42,84]}
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; n=len(b)
            rng=(b["high"]-b["low"])/b["close"]
            ratio=(rng.rolling(6).mean()/rng.rolling(180).mean()).values
            r6=(b["close"]/b["close"].shift(6)-1).values
            r1=(b["close"]/b["close"].shift(1)-1).values
            vol180=pd.Series(r1).rolling(180).std().values
            for h in allgrid:
                for g0 in range(0,n-h,h):
                    allgrid[h].append(dict(coin=coin,h=h,fwd=c[g0+h]/c[g0]-1))
            for g0 in range(0,n-18,18):
                for t in range(g0,min(g0+18,n-18)):
                    if np.isnan(ratio[t]) or np.isnan(r6[t]) or np.isnan(vol180[t]): continue
                    if ratio[t]>=3 and r6[t]<0:
                        f={("f%d"%h):(c[t+h]/c[t]-1 if t+h<n else np.nan) for h in [3,6,12,18,42,84]}
                        rows.append(dict(coin=coin,w=w,t=t,ratio=ratio[t],r6=r6[t],zfall=-r6[t]/(vol180[t]*np.sqrt(6)),**f))
                        break
    G=pd.concat([pd.DataFrame(v) for v in allgrid.values()])
    st=G.groupby(["coin","h"])["fwd"].agg(["mean","std"])
    R=pd.DataFrame(rows)
    out={}
    res=[]
    for h in [3,6,12,18,42,84]:
        hh=h if h in allgrid else None
        mu=R["coin"].map(lambda k: st.loc[(k,84),"mean"]*h/84)
        sd=R["coin"].map(lambda k: st.loc[(k,84),"std"]*np.sqrt(h/84))
        R["x%d"%h]=R["f%d"%h]-mu; R["z%d"%h]=R["x%d"%h]/sd
        s=R["x%d"%h].dropna(); zz=R["z%d"%h].dropna()
        m=R[["zfall","z%d"%h]].dropna()
        sl=stats.linregress(m["zfall"],m["z%d"%h])
        res.append(dict(h=h,n=len(s),mean=s.mean(),median=s.median(),t=s.mean()/(s.std()/np.sqrt(len(s))),
                        strength=zz.mean(),share_pos=(s>0).mean(),slope_zfall=sl.slope,slope_t=sl.slope/sl.stderr))
    out["pf18grid_by_horizon"]=pd.DataFrame(res).set_index("h")
    out["pf_x18_by_coin"]=R.groupby("coin")["x18"].agg(["count","mean","median"])
    R["zq"]=pd.qcut(R["zfall"],4,labels=False)
    out["pf_by_zfall_quartile"]=R.groupby("zq")[["zfall","x6","x18","x84"]].mean().join(R.groupby("zq")["x18"].count().rename("n"))
    R["rq"]=pd.qcut(R["ratio"],4,labels=False)
    out["pf_by_ratio_quartile"]=R.groupby("rq")[["ratio","x6","x18","x84"]].mean()
    R["late"]=R["w"].str[1:].astype(int)>12
    out["pf_x18_by_half"]=R.groupby("late")["x18"].agg(["count","mean",lambda s: s.mean()/(s.std()/np.sqrt(len(s)))])
    q=R["x18"].dropna(); lo,hi=q.quantile([0.05,0.95])
    qt=q.clip(lo,hi)
    out["x18_winsor_t"]=pd.Series(dict(mean=qt.mean(),t=qt.mean()/(qt.std()/np.sqrt(len(qt)))))
    return out
