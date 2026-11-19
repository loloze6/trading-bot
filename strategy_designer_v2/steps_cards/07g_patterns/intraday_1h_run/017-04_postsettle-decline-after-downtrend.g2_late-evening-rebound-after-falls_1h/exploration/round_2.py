def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            d=df.copy()
            ts=pd.to_datetime(d["timestamp"],utc=True)
            d["hr"]=(ts+pd.Timedelta(hours=1)).dt.hour
            d["yr"]=(ts+pd.Timedelta(hours=1)).dt.year
            c=d["close"]
            d["r1"]=c.shift(-1)/c-1
            d["r2"]=c.shift(-2)/c-1
            d["r4"]=c.shift(-4)/c-1
            d["rpast1"]=c/c.shift(1)-1
            d["r72"]=c/c.shift(72)-1
            d["vol24"]=d["rpast1"].rolling(24).std()
            d["pos"]=np.arange(len(d))
            d["coin"]=coin; d["w"]=w
            rows.append(d[["coin","w","hr","yr","pos","r1","r2","r4","rpast1","r72","vol24"]])
    A=pd.concat(rows,ignore_index=True)
    for k in ["r1","r2","r4"]:
        A["ex"+k[1:]]=A[k]-A.groupby("coin")[k].transform("mean")
    A["z"]=A["rpast1"]/A["vol24"]
    out={}
    def tt(s): return s.mean()/(s.std()/np.sqrt(s.count()))
    B=A.dropna(subset=["ex1","z"])
    # reversal slope: regression of ex1 on z, per coin and per year
    def slope(g):
        x=g["z"].clip(-6,6); y=g["ex1"]
        r=stats.linregress(x,y)
        return pd.Series({"slope_bp":r.slope*1e4,"t":r.slope/r.stderr,"n":len(g)})
    out["rev_slope_by_coin"]=B.groupby("coin").apply(slope)
    out["rev_slope_by_year"]=B.groupby("yr").apply(slope)
    # graded by vol quintile
    B=B.copy()
    B["vq"]=B.groupby("coin")["vol24"].transform(lambda x: pd.qcut(x,5,labels=False,duplicates="drop"))
    out["rev_slope_by_volq"]=B.groupby("vq").apply(slope)
    # reversal horizon: 2h and 4h non-overlapping grids
    res=[]
    for h,col in [(2,"ex2"),(4,"ex4")]:
        s=A[(A["pos"]%h==0)].dropna(subset=[col,"z"])
        r=stats.linregress(s["z"].clip(-6,6),s[col])
        res.append((h,r.slope*1e4,r.slope/r.stderr,len(s)))
    out["rev_slope_by_horizon_h"]=pd.DataFrame(res,columns=["h","slope_bp","t","n"]).set_index("h")
    # 21:00 unconditional 2h excess by coin and by year
    s=A[A["hr"]==21].dropna(subset=["ex2"])
    out["ex2_21_by_coin"]=s.groupby("coin")["ex2"].agg(mean_bp=lambda x:x.mean()*1e4,t=tt,n="count")
    out["ex2_21_by_year"]=s.groupby("yr")["ex2"].agg(mean_bp=lambda x:x.mean()*1e4,t=tt,n="count")
    # 21:00 by 72h return tercile
    s=s.dropna(subset=["r72"]).copy()
    s["q"]=s.groupby("coin")["r72"].transform(lambda x: pd.qcut(x,3,labels=False))
    out["ex2_21_by_r72_tercile"]=s.groupby("q")["ex2"].agg(mean_bp=lambda x:x.mean()*1e4,t=tt,n="count")
    # 21:00 by past 1h z tercile (does the clock effect add to reversal?)
    s=s.dropna(subset=["z"])
    s["zq"]=pd.qcut(s["z"],3,labels=False)
    out["ex2_21_by_zq"]=s.groupby("zq")["ex2"].agg(mean_bp=lambda x:x.mean()*1e4,t=tt,n="count")
    # hours 1-3 UTC weakness by year
    s=A[A["hr"].isin([1,2,3])].dropna(subset=["ex1"])
    out["ex1_h1to3_by_year"]=s.groupby("yr")["ex1"].agg(mean_bp=lambda x:x.mean()*1e4,t=tt,n="count")
    return out
