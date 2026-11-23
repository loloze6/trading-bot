def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            r1=c/c.shift(1)-1
            r2b=c/c.shift(2)-1
            scale=r1.abs().shift(1).rolling(60,min_periods=20).mean()
            vr=v/v.shift(1).rolling(60,min_periods=20).mean()
            vr2=(v+v.shift(1))/(2*v.shift(2).rolling(60,min_periods=20).mean())
            vol=r1.rolling(20,min_periods=10).std()
            volrank=vol/r1.rolling(60,min_periods=20).std().shift(20)
            f1=c.shift(-1)/c-1; f2=c.shift(-2)/c-1; d2=c.shift(-2)/c.shift(-1)-1
            f5=c.shift(-5)/c-1
            df=pd.DataFrame(dict(coin=coin,w=w,wd=ts.dt.weekday,year=ts.dt.year,r1=r1,r2b=r2b,z=r1/scale,z2=r2b/scale,
                vr=vr,vr2=vr2,volrank=volrank,f1=f1,f2=f2,d2=d2,f5=f5,
                fc=b["forecast"].astype(float),alloc=b["postRebalance_current_allocation"].astype(float)))
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    # drift per coin: mean f2 on grid -> approx by mean of f2 overall/ use daily mean*2
    dm=d.groupby("coin")["r1"].mean()
    d["drift1"]=d["coin"].map(dm)
    d["a1"]=d.f1-d.drift1; d["a2"]=d.f2-2*d.drift1; d["ad2"]=d.d2-d.drift1; d["a5"]=d.f5-5*d.drift1
    d["zc"]=d.z.clip(-2,2)
    out={}
    def summ(g,col,x="zc"):
        g=g.dropna(subset=[col,x])
        y=-g[x]*g[col]
        s=-np.sign(g[x])*g[col]
        return pd.Series(dict(n=len(g),mean_prod=y.mean(),t_prod=y.mean()/(y.std()/np.sqrt(len(g))),
                              mean_signed=s.mean(),t_signed=s.mean()/(s.std()/np.sqrt(len(g)))))
    # by weekday of the bar (0=Mon..6=Sun): reversal of that day's move over next 2 days
    out["by_bar_weekday_2d"]=pd.DataFrame({wd:summ(d[d.wd==wd],"a2") for wd in range(7)}).T
    out["by_bar_weekday_1d"]=pd.DataFrame({wd:summ(d[d.wd==wd],"a1") for wd in range(7)}).T
    s=d[d.wd==6]
    out["sun_split_days"]=pd.DataFrame({"mon":summ(s,"a1"),"tue":summ(s,"ad2"),"5d":summ(s,"a5")}).T
    # 2-day weekend move (Sat+Sun)
    s2=s.copy(); s2["z2c"]=s2.z2.clip(-3,3)
    out["sun_2dmove"]=pd.DataFrame({"z2_a2":summ(s2,"a2","z2c"),"z2_a5":summ(s2,"a5","z2c")}).T
    # volume tercile on Sunday
    s=s.dropna(subset=["vr2","a2","zc"]).copy()
    s["vq"]=pd.qcut(s.vr2,3,labels=["lowvol","mid","highvol"])
    out["sun_by_weekendvolume"]=s.groupby("vq").apply(lambda g:summ(g,"a2"))
    s["sz"]=pd.qcut(s.z.abs(),5,labels=False)
    out["sun_by_absz_quint"]=s.groupby("sz").apply(lambda g:summ(g,"a2"))
    s["up"]=np.where(s.z>0,"rise","fall")
    out["sun_by_sign"]=s.groupby("up").apply(lambda g:summ(g,"a2"))
    s2=s.dropna(subset=["volrank"]).copy()
    s2["vq"]=pd.qcut(s2.volrank,3,labels=["calm","mid","wild"])
    out["sun_by_volregime"]=s2.groupby("vq").apply(lambda g:summ(g,"a2"))
    out["sun_by_year"]=s.groupby("year").apply(lambda g:summ(g,"a2"))
    return out
