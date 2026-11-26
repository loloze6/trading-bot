def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=10
    out={}
    rows=[]
    gridrows=[]
    for coin,wins in data["bars"].items():
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float); hi=df["high"].astype(float); lo=df["low"].astype(float)
            n=len(df)
            ch=c.diff().abs()
            er=(c-c.shift(60)).abs()/ch.rolling(60).sum()
            er=er.rolling(5).mean()
            ph=hi.shift(1).rolling(60).max(); pl=lo.shift(1).rolling(60).min()
            dup=c/ph-1; ddn=c/pl-1
            r1=c.pct_change()
            vol20=r1.rolling(20).std()
            ret5=c/c.shift(5)-1
            fwd=c.shift(-H)/c-1
            ts=pd.to_datetime(df["timestamp"])
            for i in range(n):
                rows.append((coin,w,i,i//H,ts.iloc[i].normalize(),er.iloc[i],dup.iloc[i],ddn.iloc[i],r1.iloc[i],vol20.iloc[i],ret5.iloc[i],fwd.iloc[i],ts.iloc[i].dayofweek))
    d=pd.DataFrame(rows,columns=["coin","w","i","cell","day","er","dup","ddn","r1","vol20","ret5","fwd","dow"])
    g=d[d.i%H==0].dropna(subset=["fwd"])
    drift=g.groupby("coin").fwd.mean(); usual=g.groupby("coin").fwd.std()
    d["unus"]=d.fwd-d.coin.map(drift)
    d["str"]=d.unus/d.coin.map(usual)
    out["drift_usual"]=pd.DataFrame({"drift":drift,"usual":usual})
    def summ(ev,sign=1):
        ev=ev.dropna(subset=["fwd"]).groupby(["coin","w","cell"]).head(1)
        if len(ev)<3: return pd.Series({"n":len(ev)})
        x=sign*ev.unus
        ds=(x).groupby(ev.day).sum()
        t=ds.mean()/(ds.std(ddof=1)/np.sqrt(len(ds))) if len(ds)>1 else np.nan
        return pd.Series({"n":len(ev),"days":len(ds),"mean_unus":x.mean(),"t_day":t,"strength":(sign*ev["str"]).mean(),"hit":(x>0).mean()})
    res={}
    d["erb"]=pd.cut(d.er,[0,0.15,0.3,0.5,1.01])
    for b,sub in d.groupby("erb",observed=True):
        res[("up",str(b))]=summ(sub[sub.dup>0])
        res[("dn",str(b))]=summ(sub[sub.ddn<0])
    out["breakouts_by_er_longside"]=pd.DataFrame(res).T
    # graded overshoot in trendless upside
    up=d[(d.dup>0)&(d.er<=0.3)].dropna(subset=["fwd"]).groupby(["coin","w","cell"]).head(1)
    up["q"]=pd.qcut(up.dup,3,labels=False,duplicates="drop")
    out["trendless_up_by_overshoot_tercile"]=up.groupby("q").agg(n=("unus","size"),mean_unus=("unus","mean"),dup=("dup","mean"))
    dn=d[(d.ddn<0)&(d.er<=0.3)].dropna(subset=["fwd"]).groupby(["coin","w","cell"]).head(1)
    dn["q"]=pd.qcut(dn.ddn,3,labels=False,duplicates="drop")
    out["trendless_dn_by_overshoot_tercile"]=dn.groupby("q").agg(n=("unus","size"),mean_unus=("unus","mean"),ddn=("ddn","mean"))
    # grid-level graded: position in 60d range
    gg=d[d.i%H==0].dropna(subset=["fwd","dup","ddn","er"]).copy()
    gg["pos"]=(np.log(1+gg.ddn))/(np.log(1+gg.ddn)-np.log(1+gg.dup))
    gg["pq"]=pd.qcut(gg.pos,5,labels=False,duplicates="drop")
    out["grid_by_range_position_q"]=gg.groupby("pq").agg(n=("unus","size"),pos=("pos","mean"),mean_unus=("unus","mean"),t=("unus",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))))
    gg["r5q"]=gg.groupby("coin").ret5.transform(lambda x:pd.qcut(x,5,labels=False,duplicates="drop"))
    out["grid_by_ret5_q"]=gg.groupby("r5q").agg(n=("unus","size"),mean_unus=("unus","mean"),t=("unus",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))))
    gg["vq"]=gg.groupby("coin").vol20.transform(lambda x:pd.qcut(x,3,labels=False,duplicates="drop"))
    out["grid_by_vol_q"]=gg.groupby("vq").agg(n=("unus","size"),mean_unus=("unus","mean"),t=("unus",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))))
    out["grid_by_coin_pos_corr"]=gg.groupby("coin").apply(lambda s:pd.Series(stats.spearmanr(s.pos,s.unus),index=["rho","p"]))
    # daily next-day after big moves
    dd=d.dropna(subset=["r1","vol20"]).copy()
    dd["nxt"]=dd.groupby(["coin","w"]).r1.shift(-1)
    dd["z"]=dd.r1/dd.vol20
    dd["zq"]=pd.cut(dd.z,[-99,-2,-1,0,1,2,99])
    out["nextday_by_z"]=dd.groupby("zq",observed=True).agg(n=("nxt","count"),mean=("nxt","mean"),t=("nxt",lambda x:x.mean()/(x.std()/np.sqrt(x.count()))))
    out["dow_r1"]=dd.groupby("dow").agg(n=("r1","count"),mean=("r1","mean"),t=("r1",lambda x:x.mean()/(x.std()/np.sqrt(x.count()))))
    return out
