import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H=84
    bars=data["bars"]
    out={}
    hourly=[]; pans=[]; grid=[]
    for coin,wins in bars.items():
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float); hi=df["high"].astype(float); lo=df["low"].astype(float)
            rng6=(hi.rolling(6).max()-lo.rolling(6).min())/c
            mult=rng6/rng6.rolling(180,min_periods=30).mean()
            r6=c/c.shift(6)-1
            r42=c/c.shift(42)-1
            r1=np.log(c/c.shift(1)); vol=r1.rolling(180,min_periods=60).std()
            fwd=c.shift(-H)/c-1
            fwd36=c.shift(-36)/c-1
            f1=c.shift(-1)/c-1
            ts=pd.to_datetime(df["timestamp"])
            hourly.append(pd.DataFrame({"coin":coin,"w":w,"year":ts.dt.year,"hour":ts.dt.hour,"wd":ts.dt.weekday,"f1":f1,"day":ts.dt.floor("D")}))
            n=len(df)
            for s in range(0,n,H):
                grid.append(dict(coin=coin,fwd=fwd.iloc[s]))
            pan=(mult>=3)&(r6<0)
            for s in range(0,n,H):
                idx=np.where(pan.iloc[s:s+H].values)[0]
                if len(idx):
                    i=s+idx[0]
                    pans.append(dict(coin=coin,w=w,year=ts.iloc[i].year,day=ts.iloc[i].floor("D"),
                        fwd=fwd.iloc[i],fwd36=fwd36.iloc[i],r6=r6.iloc[i],r42=r42.iloc[i],
                        r6z=r6.iloc[i]/(vol.iloc[i]*np.sqrt(6)),mult=mult.iloc[i]))
    G=pd.DataFrame(grid).dropna(); cm=G.groupby("coin")["fwd"].mean()
    P=pd.DataFrame(pans).dropna(subset=["fwd","r6"]); P["ex"]=P["fwd"]-P["coin"].map(cm)
    # slopes
    def ols(x,y):
        r=stats.linregress(x,y); return pd.Series({"n":len(x),"slope":r.slope,"t":r.slope/r.stderr})
    out["panic ex on r6 (pooled)"]=ols(P.r6,P.ex).round(4)
    Pz=P.dropna(subset=["r6z"])
    out["panic ex on r6z (pooled)"]=ols(Pz.r6z,Pz.ex).round(4)
    out["panic ex on r42 (pooled)"]=ols(P.r42,P.ex).round(4)
    # clustered by day: average per day then slope
    Dg=P.groupby("day")[["ex","r6","r42"]].mean()
    out["day-clustered ex on r6"]=ols(Dg.r6,Dg.ex).round(4)
    out["day-clustered ex on r42"]=ols(Dg.r42,Dg.ex).round(4)
    # depth slope by year halves and by coin sign
    yr=[]
    for y,g in P.groupby("year"):
        if len(g)>10: s=ols(g.r6,g.ex); s["year"]=y; yr.append(s)
    out["panic ex~r6 slope by year"]=pd.DataFrame(yr).set_index("year").round(3)
    cs=[]
    for co,g in P.groupby("coin"):
        if len(g)>10: s=ols(g.r6,g.ex); s["coin"]=co; cs.append(s)
    C=pd.DataFrame(cs)
    out["per-coin r6 slope: share negative, n coins"]=pd.Series({"share_neg":(C.slope<0).mean(),"n":len(C)}).round(3)
    # deepest quartile by year
    P["dq"]=pd.qcut(P.r6,4,labels=False)
    out["deepest quartile ex by year"]=P[P.dq==0].groupby("year")["ex"].agg(["count","mean"]).round(3)
    out["panic ex 6d (36 bars) by depth q"]=P.assign(ex36=P.fwd36).groupby("dq")["ex36"].agg(["count","mean"]).round(4)
    # hourly: robust
    Hh=pd.concat(hourly).dropna(subset=["f1"])
    # per coin: mean f1 by hour, then share of coins positive and t across coins
    pc=Hh.groupby(["coin","hour"])["f1"].mean().unstack()
    res=pd.DataFrame({"mean_across_coins":pc.mean(),"share_pos":(pc>0).mean(),
                      "t_across_coins":pc.mean()/(pc.std()/np.sqrt(len(pc)))})
    out["hour: across coins"]=res.round(5)
    py=Hh.groupby(["year","hour"])["f1"].mean().unstack()
    out["hour mean by year"]=(py*1e4).round(1)
    # day-clustered: average across coins at same timestamp-hour-day, t across days
    dc=Hh.groupby(["day","hour"])["f1"].mean().reset_index()
    g=dc.groupby("hour")["f1"].agg(["count","mean","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["hour: cross-coin averaged, t over days"]=g.round(5)
    dw=Hh.groupby(["day"]).agg(f1=("f1","mean"),wd=("wd","first")).reset_index()
    # weekday: sum per day of the six bars, averaged across coins
    dd=Hh.groupby(["coin","w","day"]).agg(r=("f1",lambda x: np.prod(1+x)-1),wd=("wd","first")).reset_index()
    dd2=dd.groupby(["day","wd"])["r"].mean().reset_index()
    g=dd2.groupby("wd")["r"].agg(["count","mean","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["weekday: cross-coin averaged, t over days"]=g.round(5)
    return out
