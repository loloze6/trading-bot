def explore(data):
    import numpy as np, pandas as pd
    H=18
    bars_all=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float); v=b["volume"].astype(float).replace(0,np.nan)
            r1=c.pct_change()
            sd1=r1.rolling(180,min_periods=45).std()
            z18=(c/c.shift(18)-1)/(sd1*np.sqrt(18))
            z6=(c/c.shift(6)-1)/(sd1*np.sqrt(6))
            vz=np.log(v/v.rolling(180,min_periods=45).median())
            vz18=np.log(v.rolling(18).mean()/v.rolling(180,min_periods=45).median())
            f18=c.shift(-H)/c-1
            ts=pd.to_datetime(b["timestamp"])
            bars_all.append(pd.DataFrame(dict(coin=coin,w=w,wn=int(w[1:]),yr=ts.dt.year,z18=z18,z6=z6,vz=vz,vz18=vz18,
                f18=f18,r1n=r1.shift(-1),hour=ts.dt.hour,wd=ts.dt.weekday,pos=np.arange(len(b)),
                fc=b["forecast"],alloc=b["postRebalance_current_allocation"])))
    A=pd.concat(bars_all,ignore_index=True)
    out={}
    def tt(s):
        s=s.dropna(); return pd.Series(dict(mean=s.mean(),t=s.mean()/(s.std()/np.sqrt(len(s))),n=len(s)))
    A["r1z"]=A.r1n/A.groupby("coin")["r1n"].transform("std")
    h16=A[A.hour==16]
    out["hour16 next-bar z by coin"]=h16.groupby("coin")["r1z"].apply(tt).unstack().round(3)
    out["hour16 next-bar z by year"]=h16.groupby("yr")["r1z"].apply(tt).unstack().round(3)
    h20=A[A.hour==20]
    out["hour20 next-bar z by year"]=h20.groupby("yr")["r1z"].apply(tt).unstack().round(3)
    fr=A[A.wd==4]
    out["friday next-bar z by year"]=fr.groupby("yr")["r1z"].apply(tt).unstack().round(3)
    out["friday x hour next-bar z"]=fr.groupby("hour")["r1z"].apply(tt).unstack().round(3)
    G=A[A.pos%H==0].dropna(subset=["f18"]).copy()
    st=G.groupby("coin")["f18"].agg(["mean","std"])
    G["ex"]=(G.f18-G.coin.map(st["mean"]))/G.coin.map(st["std"])
    G=G.dropna(subset=["z18","vz18"])
    G["z18b"]=pd.cut(G.z18,[-99,-2,-1,0,1,2,99])
    out["z18 bins -> ex18"]=G.groupby("z18b")["ex"].apply(tt).unstack().round(3)
    hi=G[G.z18>1]
    out["z18>1 ex18 by coin"]=hi.groupby("coin")["ex"].apply(tt).unstack().round(3)
    hi["vzq"]=pd.qcut(hi.vz18,3,labels=False)
    out["z18>1 by 18-bar volume tercile"]=hi.groupby("vzq")["ex"].apply(tt).unstack().round(3)
    out["corr z18*vz18 with ex (up side z18>0)"]=float(np.corrcoef((G.z18.clip(0)*G.vz18.clip(0))[G.z18>0],G.ex[G.z18>0])[0,1])
    G["vzq"]=pd.qcut(G.vz,5,labels=False)
    out["vz quintile ex18 by up/down last 6 bars"]=G.groupby([G.vzq,np.sign(G.z6)])["ex"].mean().unstack().round(3)
    # book: share of time short and drift vs timing
    D=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            D.append(d.assign(coin=coin))
    D=pd.concat(D)
    out["book daily mean, coin daily mean"]=pd.Series(dict(book=D.book_return.mean(),coin=D.coin_return.mean()))
    out["mean alloc, share short"]=pd.Series(dict(mean_alloc=A.alloc.mean(),short=(A.alloc<0).mean()))
    return out
