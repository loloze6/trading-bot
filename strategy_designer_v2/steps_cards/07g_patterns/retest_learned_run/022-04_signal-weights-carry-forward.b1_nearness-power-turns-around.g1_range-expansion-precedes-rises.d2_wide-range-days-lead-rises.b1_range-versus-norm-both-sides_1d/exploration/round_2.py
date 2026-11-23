def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"]; rng=(b["high"]-b["low"])
            ratio=rng/rng.rolling(30,min_periods=10).mean()
            r1=c/c.shift(1)-1
            r5=c/c.shift(5)-1
            hi30=c/b["high"].rolling(30,min_periods=10).max()-1
            sd=r1.rolling(30,min_periods=10).std()
            f3=c.shift(-3)/c-1
            idx=np.arange(0,len(b)-3,3)
            ts=pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin":coin,"w":w,"ratio":ratio.values[idx],"r1":r1.values[idx],
                "r1z":(r1/sd).values[idx],"r5":r5.values[idx],"hi30":hi30.values[idx],"f3":f3.values[idx],
                "yr":ts.dt.year.values[idx]}))
    g=pd.concat(rows)
    g["ex"]=g["f3"]-g.groupby("coin")["f3"].transform("mean")
    g["sdh"]=g.groupby("coin")["f3"].transform("std")
    g["str"]=g["ex"]/g["sdh"]
    out={}
    def st(t):
        t=t.agg(["mean","count","std"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"])); return t[["mean","count","t"]]
    x=g.dropna(subset=["ratio","r1","ex","hi30","r5"]).copy()
    x["rq"]=x.groupby("coin")["ratio"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    # signed range: ratio x sign of day -> down-wide
    x["sr"]=-np.sign(x["r1"])*(x["ratio"]-1)
    # graded: within down days, ratio quintiles
    dn=x[x["r1"]<0].copy()
    dn["q"]=dn.groupby("coin")["ratio"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["down_days_by_ratio_q"]=st(dn.groupby("q")["ex"])
    up=x[x["r1"]>0].copy()
    up["q"]=up.groupby("coin")["ratio"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["up_days_by_ratio_q"]=st(up.groupby("q")["ex"])
    # down-day size z quintiles
    out["down_days_by_r1z_q"]=st(dn.assign(q=dn.groupby("coin")["r1z"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))).groupby("q")["ex"])
    # regressions
    def sl(d,col):
        d=d.dropna(subset=[col,"ex"]); r=stats.linregress(d[col],d["ex"]); return pd.Series({"slope":r.slope,"t":r.slope/r.stderr,"n":len(d)})
    dn["dr"]=dn["ratio"]
    out["down_slope_ratio_by_coin"]=dn.groupby("coin").apply(lambda d: sl(d,"dr"))
    out["down_slope_ratio_by_yr"]=dn.groupby("yr").apply(lambda d: sl(d,"dr"))
    out["down_slope_all"]=sl(dn,"dr").to_frame().T
    out["up_slope_all"]=sl(up,"ratio").to_frame().T
    out["down_strength_top_q"]=dn[dn["q"]==4]["str"].mean()
    # hi30 graded and overlap with ratio top
    x["hq"]=x.groupby("coin")["hi30"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["hi30_slope_by_coin"]=x.groupby("coin").apply(lambda d: sl(d,"hi30"))
    out["hi30_slope_by_yr"]=x.groupby("yr").apply(lambda d: sl(d,"hi30"))
    out["corr_ratio_hi30"]=float(x[["ratio","hi30"]].corr().iloc[0,1])
    out["hq_x_rq_top"]=st(x.assign(top=(x["rq"]==4).astype(int)).groupby(["hq","top"])["ex"])
    return out
