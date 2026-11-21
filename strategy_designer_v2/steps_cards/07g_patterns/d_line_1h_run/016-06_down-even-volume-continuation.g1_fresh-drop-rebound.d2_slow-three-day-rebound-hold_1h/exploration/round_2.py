def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    def tt(s): s=s.dropna(); return s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan
    # Grids per horizon h: reversal of past 24h move over next h, non-overlapping grid of h
    res=[]
    for h in [6,12,24,48,72]:
        rows=[]
        for coin,wins in data["bars"].items():
            for w,b in wins.items():
                c=b["close"].values; n=len(c)
                r1=np.r_[np.nan,c[1:]/c[:-1]-1]
                for t in range(0,n,h):
                    if t<72 or t+h>=n: continue
                    rows.append(dict(coin=coin,p24=c[t]/c[t-24]-1,p72=c[t]/c[t-72]-1,f=c[t+h]/c[t]-1,
                                     vol=np.nanstd(r1[t-23:t+1])))
        d=pd.DataFrame(rows)
        d["fx"]=d["f"]-d.groupby("coin")["f"].transform("mean")
        d["z"]=d.groupby("coin")["p24"].transform(lambda s:(s-s.mean())/s.std())
        d["qv"]=d.groupby("coin")["vol"].transform(lambda s:pd.qcut(s,3,labels=False))
        for nm,sub in [("all",d),("down72",d[d.p72<0]),("up72",d[d.p72>=0]),("lowvol",d[d.qv==0]),("highvol",d[d.qv==2]),
                       ("p24<0",d[d.p24<0]),("p24>0",d[d.p24>0])]:
            sl=stats.linregress(sub["z"],sub["fx"])
            res.append(dict(h=h,grp=nm,n=len(sub),slope=sl.slope,t=sl.slope/sl.stderr))
    out["reversal slope of fwd excess on past24 z, by horizon h (grid h)"]=pd.DataFrame(res).set_index(["h","grp"])
    # hour 21-22 effect by year and coin
    hrs=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            ts=pd.to_datetime(b["timestamp"]); r=b["close"].pct_change()
            hrs.append(pd.DataFrame({"h":ts.dt.hour,"y":ts.dt.year,"r":r,"coin":coin,"absr":r.abs()}))
    H=pd.concat(hrs).dropna()
    H["rx"]=H["r"]-H.groupby("coin")["r"].transform("mean")
    e=H[H.h.isin([21,22])]
    g=e.groupby("y")["rx"].agg(["mean","count"]); g["t"]=e.groupby("y")["rx"].apply(tt); out["hours 21-22 by year"]=g
    g=e.groupby("coin")["rx"].agg(["mean","count"]); g["t"]=e.groupby("coin")["rx"].apply(tt); out["hours 21-22 by coin"]=g
    # daily 24h return measured from 21:00 to 23:00 close vs rest: sum of mean
    out["hour abs return mean"]=H.groupby("h")["absr"].mean().to_frame().T
    # book: gain by position held into hours 21-22
    B=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            ts=pd.to_datetime(b["timestamp"]); c=b["close"].values
            nxt=np.r_[c[1:]/c[:-1]-1,np.nan]
            B.append(pd.DataFrame({"h":ts.dt.hour,"pos":b["postRebalance_current_allocation"].values,"g":b["postRebalance_current_allocation"].values*nxt,
                                   "chg":(b["postRebalance_current_allocation"]-b["previous_allocation"]).abs().values}))
    B=pd.concat(B).dropna()
    out["book: mean gain/turnover by entry age"]=pd.Series({"mean_pos":B.pos.mean(),"mean_gain_per_bar":B.g.mean(),"mean_turnover_per_bar":B.chg.mean(),
        "gross_gain_t":tt(B.g)})
    return out
