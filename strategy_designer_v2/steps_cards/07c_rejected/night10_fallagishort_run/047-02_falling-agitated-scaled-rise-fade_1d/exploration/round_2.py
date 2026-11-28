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
            raw=b["debug_info.components.scaled_rise.last_history_value"] if "debug_info.components.scaled_rise.last_history_value" in b else pd.Series(np.nan,index=b.index)
            # 2-day and 3-day scaled rise
            z2=(c/c.shift(2)-1)/(sd*np.sqrt(2)); z3=(c/c.shift(3)-1)/(sd*np.sqrt(3))
            for h in [1,2,3,5]:
                fwd=c.shift(-h)/c-1
                for i in range(0,len(b),h):
                    if i+h>=len(b): continue
                    rows.append(dict(coin=coin,w=w,h=h,z=z.iloc[i],z3=z3.iloc[i],fc=fc.iloc[i],raw=raw.iloc[i],
                        ret=fwd.iloc[i],inprof=b["regime"].iloc[i]=="unknown",
                        year=pd.Timestamp(b["timestamp"].iloc[i]).year))
    d=pd.DataFrame(rows)
    d=d.join(d.groupby(["coin","h"])["ret"].mean().rename("drift"),on=["coin","h"])
    d["unus"]=d["ret"]-d["drift"]
    d=d.dropna(subset=["z","unus"])
    def agg(g):
        m=g["unus"].mean(); s=g["unus"].std(); n=len(g)
        return pd.Series({"n":n,"mean_unus":m,"t":m/(s/np.sqrt(n)) if n>2 else np.nan})
    out={}
    P=d[d.inprof]
    up=P[P.z>0]
    sl=[]
    for h,g in up.groupby("h"):
        res=stats.linregress(g["z"],g["unus"]); sl.append(dict(h=h,n=len(g),slope=res.slope,t=res.slope/res.stderr,
            mean=g.unus.mean(),corr_fc_z=g[["fc","z"]].corr().iloc[0,1]))
    out["up_inprof_slope"]=pd.DataFrame(sl)
    dn=P[P.z<0]
    sl=[]
    for h,g in dn.groupby("h"):
        res=stats.linregress(g["z"],g["unus"]); sl.append(dict(h=h,n=len(g),slope=res.slope,t=res.slope/res.stderr,mean=g.unus.mean()))
    out["down_inprof_slope"]=pd.DataFrame(sl)
    up["zb"]=pd.cut(up["z"],[0,0.5,1,1.5,99])
    out["up_inprof_zb"]=up.groupby(["h","zb"]).apply(agg).unstack(0)
    up["fcb"]=pd.cut(up["fc"],[-21,-10,-2,0.01])
    out["up_inprof_fcb_h3"]=up[up.h==3].groupby("fcb").apply(agg)
    out["up_inprof_zbig_coin_h3"]=up[(up.h==3)&(up.z>1)].groupby("coin").apply(agg)
    out["up_inprof_zbig_year_h3"]=up[(up.h==3)&(up.z>1)].groupby("year").apply(agg)
    # 3-day scaled rise
    u3=P[(P.h==3)&(P.z3>0)].dropna(subset=["z3"])
    res=stats.linregress(u3["z3"],u3["unus"])
    out["up3day_inprof_h3"]=pd.Series({"n":len(u3),"slope":res.slope,"t":res.slope/res.stderr,"mean":u3.unus.mean()})
    # outside profile up days slope
    o=d[(~d.inprof)&(d.z>0)]
    sl=[]
    for h,g in o.groupby("h"):
        res=stats.linregress(g["z"],g["unus"]); sl.append(dict(h=h,n=len(g),slope=res.slope,t=res.slope/res.stderr))
    out["up_outprof_slope"]=pd.DataFrame(sl)
    return out
