def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r=c.pct_change()
            vol20=r.rolling(20).std()
            z=r/vol20.shift(1)
            vr=v/v.rolling(30).mean().shift(1)
            ts=pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"z":z,"vr":vr,
                "f1":c.shift(-1)/c-1,"f2_5":c.shift(-5)/c.shift(-1)-1,"f3":c.shift(-3)/c-1,
                "f5":c.shift(-5)/c-1,"wd":ts.dt.weekday,"yr":ts.dt.year}))
    D=pd.concat(rows,ignore_index=True)
    for col in ["f1","f2_5","f3","f5"]:
        D["x"+col]=D[col]-D.groupby("coin")[col].transform("mean")
    D=D.dropna(subset=["z","vr"])
    def tt(s):
        s=s.dropna(); return pd.Series({"n":len(s),"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s)))})
    res={}
    # down moves: 3-day rebound graded by volume ratio, grid 3
    g3=D[D.pos%3==0].copy()
    dn=g3[g3.z<-1].copy()
    dn["vq"]=pd.qcut(dn.vr,4,labels=["q1","q2","q3","q4"])
    res["down z<-1 xf3 grid3 by vr quartile"]=dn.groupby("vq",observed=True).xf3.apply(tt).unstack()
    res["down spearman vr vs xf3"]=float(stats.spearmanr(dn.vr,dn.xf3,nan_policy="omit")[0])
    dn["s"]=-dn.z*dn.vr
    res["down spearman (-z*vr) vs xf3"]=float(stats.spearmanr(dn.s,dn.xf3,nan_policy="omit")[0])
    res["down z<-1 xf3 by year"]=dn[dn.vr>1].groupby("yr").xf3.mean()
    res["down z<-1 vr>1 xf3 by coin"]=dn[dn.vr>1].groupby("coin").xf3.apply(tt).unstack()
    # up moves: days 2-5 on grid 5, graded by vr
    g5=D[D.pos%5==0].copy()
    up=g5[g5.z>1].copy()
    up["vq"]=pd.qcut(up.vr,4,labels=["q1","q2","q3","q4"])
    res["up z>1 grid5 xf1 & xf2_5 by vr quartile"]=pd.concat({"xf1":up.groupby("vq",observed=True).xf1.apply(tt).unstack(),
        "xf2_5":up.groupby("vq",observed=True).xf2_5.apply(tt).unstack()},axis=1)
    res["up spearman vr vs xf2_5"]=float(stats.spearmanr(up.vr,up.xf2_5,nan_policy="omit")[0])
    res["up z>1 vr>1 xf2_5 by coin"]=up[up.vr>1].groupby("coin").xf2_5.mean()
    # wednesday by year
    res["xf1 wednesday by year"]=D[D.wd==2].groupby("yr").xf1.apply(tt).unstack()
    return res
