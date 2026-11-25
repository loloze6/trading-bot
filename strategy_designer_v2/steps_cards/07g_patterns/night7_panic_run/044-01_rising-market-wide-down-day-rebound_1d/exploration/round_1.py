def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            rng=(b["high"]-b["low"])/c
            b["r1"]=r; b["rs"]=rng/sd
            b["f3"]=c.shift(-3)/c-1
            b["f1"]=c.shift(-1)/c-1
            b["pos"]=np.arange(len(b))
            b["coin"]=coin; b["w"]=w
            b["rising"]=b["regime"]!="chop"
            b["r5"]=c/c.shift(5)-1
            b["absz"]=r.abs()/sd
            b["z1"]=r/sd
            b["wd"]=pd.to_datetime(b["timestamp"]).dt.dayofweek
            b["year"]=pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b[["coin","w","pos","r1","rs","f3","f1","rising","r5","absz","z1","wd","year","timestamp","regime"]])
    d=pd.concat(rows)
    g=d[(d.pos%3==0)&d.f3.notna()&d.rs.notna()].copy()
    drift=g.groupby("coin").f3.mean()
    usd=g.groupby("coin").f3.std()
    g["ex"]=g.f3-g.coin.map(drift)
    def tcl(x):
        if len(x)<5: return pd.Series({"n":len(x),"mean":np.nan,"t":np.nan})
        s=x.groupby(g.loc[x.index,"timestamp"] if False else None) if False else None
        return None
    def summ(sub):
        sub=sub.dropna(subset=["ex"])
        n=len(sub)
        if n<5: return pd.Series({"n":n,"mean_ex%":np.nan,"t_day":np.nan})
        dev=sub.ex-0
        s=dev.groupby(sub.timestamp.values).sum()
        G=len(s); m=dev.mean()
        se=np.sqrt((s**2).sum()*G/(G-1))/n
        return pd.Series({"n":n,"mean_ex%":100*m,"t_day":m/se})
    g["down"]=g.r1<0
    g["rsq"]=g.groupby(["rising","down"]).rs.transform(lambda x: pd.qcut(x,4,labels=False,duplicates="drop"))
    out={}
    out["rising_down_rsq"]=g.groupby(["rising","down","rsq"]).apply(summ)
    g["zq"]=pd.qcut(g.z1,5,labels=False)
    out["z1_quint_by_rising"]=g.groupby(["rising","zq"]).apply(summ)
    g["r5q"]=pd.qcut(g.r5,5,labels=False)
    out["r5_quint_by_rising"]=g.groupby(["rising","r5q"]).apply(summ)
    g["rsall"]=pd.qcut(g.rs,5,labels=False)
    out["rs_quint_all"]=g.groupby(["rsall"]).apply(summ)
    # weekday next-day
    d1=d[d.f1.notna()].copy()
    d1["ex1"]=d1.f1-d1.coin.map(d1.groupby("coin").f1.mean())
    out["weekday_next1"]=d1.groupby("wd").ex1.agg(["count","mean",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))])
    # book days
    dl=[]
    for coin,ws in data["days"].items():
        for w,t in ws.items():
            t=t.copy(); t["coin"]=coin; t["w"]=w; dl.append(t)
    D=pd.concat(dl)
    D["yr"]=pd.to_datetime(D["day"]).dt.year
    out["book_by_year"]=D.groupby("yr")[["book_return","coin_return"]].agg(["mean","count"])
    out["book_by_coin"]=D.groupby("coin")[["book_return","coin_return"]].mean()
    return out
