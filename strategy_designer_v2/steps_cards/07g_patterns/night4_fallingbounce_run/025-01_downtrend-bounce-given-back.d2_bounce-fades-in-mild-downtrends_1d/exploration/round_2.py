def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            vol=r.rolling(20).std()
            z=r/vol
            r90=c/c.shift(90)-1
            f5=c.shift(-5)/c-1
            f1=c.shift(-1)/c-1
            f2=c.shift(-2)/c-1
            ts=pd.to_datetime(b["timestamp"])
            idx=np.arange(len(b))
            rows.append(pd.DataFrame(dict(coin=coin,w=w,z=z,r=r,r90=r90,f5=f5,f1=f1,f2=f2,
                wd=ts.dt.weekday,yr=ts.dt.year,hr=ts.dt.hour,g5=(idx%5==0),g2=(idx%2==0),
                pos=b["postRebalance_current_allocation"].astype(float))))
    D=pd.concat(rows,ignore_index=True)
    out={}
    out["bar hour values"]=D.hr.value_counts().to_frame()
    def tt(x):
        x=x.dropna(); return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x)))))
    out["next1d ret by weekday (bar of close)"]=D.groupby("wd")["f1"].apply(tt).unstack()
    G=D[D.g5]
    out["f5 by weekday"]=G.groupby("wd")["f5"].apply(tt).unstack()
    S=G[G.wd==6]
    out["sunday f5 by year"]=S.groupby("yr")["f5"].apply(tt).unstack()
    out["sunday f5 by coin"]=S.groupby("coin")["f5"].apply(tt).unstack()
    out["sunday f5 share windows negative"]=float((S.groupby("w")["f5"].mean()<0).mean())
    out["next1d by weekday by year t (mon-sun diffs)"]=D.groupby(["yr","wd"])["f1"].mean().unstack()
    # down-day reversal, graded, by regime
    A=D.dropna(subset=["z","f1","r90"]).copy()
    A["reg"]=np.where(A.r90<0,"down90","up90")
    A["zb"]=pd.cut(A.z,[-99,-3,-2,-1.5,-1,-0.5,0.5,1,2,99])
    out["f1 by z bucket x regime"]=A.groupby(["reg","zb"])["f1"].apply(tt).unstack()
    N=A[A.z<0]
    for reg in ["down90","up90"]:
        g=N[N.reg==reg]; s=stats.linregress(-g.z,g.f1)
        out[f"slope f1 on -z down days {reg}"]=f"slope {s.slope:.5f} t {s.slope/s.stderr:.2f} n {len(g)}"
    B=D[D.g2].dropna(subset=["z","f2"])
    Bn=B[B.z<-1]
    out["f2 after z<-1 by year"]=Bn.groupby("yr")["f2"].apply(tt).unstack()
    out["f2 after z<-1 by coin"]=Bn.groupby("coin")["f2"].apply(tt).unstack()
    out["f2 all grid mean"]=float(B.f2.mean())
    # book gain on sundays vs position
    D["gain"]=D.pos*D.f1
    out["position gain by weekday"]=D.groupby("wd")["gain"].apply(tt).unstack()
    return out
