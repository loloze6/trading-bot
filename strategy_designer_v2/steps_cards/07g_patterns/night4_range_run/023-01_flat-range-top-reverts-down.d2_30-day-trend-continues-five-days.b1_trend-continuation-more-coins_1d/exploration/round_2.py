def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        for w,df in wins.items():
            d=df.reset_index(drop=True).copy()
            c=d["close"]; h=d["high"]; l=d["low"]
            d["ret30"]=c/c.shift(30)-1
            hh=h.rolling(30).max(); ll=l.rolling(30).min()
            d["nmr"]=(c-c.shift(30)).abs()/(hh-ll)
            d["rpos"]=(c-(hh+ll)/2)/(hh-ll)
            d["fwd5"]=c.shift(-5)/c-1
            d["fwd10"]=c.shift(-10)/c-1
            d["yr"]=pd.to_datetime(d["timestamp"]).dt.year
            d["vol20"]=(c/c.shift(1)-1).rolling(20).std()
            g5=d.iloc[::5].copy(); g5["coin"]=coin; g5["win"]=w; g5["grid"]=5
            g10=d.iloc[::10].copy(); g10["coin"]=coin; g10["win"]=w; g10["grid"]=10
            rows+= [g5,g10]
    G=pd.concat(rows,ignore_index=True)
    out={}
    def summ(gb,col="y"):
        r=gb[col].agg(["count","mean","std"])
        r["t"]=r["mean"]/(r["std"]/np.sqrt(r["count"]))
        return r.round(4)
    G5=G[G.grid==5].dropna(subset=["fwd5","rpos","nmr"]).copy()
    G5["drift"]=G5.groupby("coin")["fwd5"].transform("mean")
    G5["un"]=G5["fwd5"]-G5["drift"]
    G10=G[G.grid==10].dropna(subset=["fwd10","rpos","nmr"]).copy()
    G10["drift"]=G10.groupby("coin")["fwd10"].transform("mean")
    G10["un"]=G10["fwd10"]-G10["drift"]
    for nm,X in [("5d",G5),("10d",G10)]:
        N=X[X.regime!="trending"].copy()
        N["y"]=N["un"]
        N["rq"]=pd.qcut(N["rpos"],5,labels=False)
        out[f"nontrend {nm}: by rpos quintile"]=summ(N.groupby("rq"))
        sl=stats.linregress(N["rpos"],N["un"])
        out[f"nontrend {nm}: slope on rpos, t, n"]=f"{sl.slope:.4f}, t={sl.slope/sl.stderr:.2f}, n={len(N)}"
        T=X[X.regime=="trending"].copy()
        sl=stats.linregress(T["rpos"],T["un"])
        out[f"trend {nm}: slope on rpos, t, n"]=f"{sl.slope:.4f}, t={sl.slope/sl.stderr:.2f}, n={len(T)}"
        A=X.copy()
        sl=stats.linregress(A["rpos"],A["un"])
        out[f"all {nm}: slope on rpos, t, n"]=f"{sl.slope:.4f}, t={sl.slope/sl.stderr:.2f}, n={len(A)}"
    N=G5[G5.regime!="trending"].copy()
    N["y"]=N["un"]*np.sign(N["rpos"])
    out["nontrend 5d: dir(rpos) unusual by year"]=summ(N.groupby("yr"))
    out["nontrend 5d: dir(rpos) unusual by coin"]=summ(N.groupby("coin"))
    N["y"]=N["un"]; N["s30"]=np.sign(N["ret30"])
    N["rh"]=np.where(N.rpos>0,"upper","lower")
    out["nontrend 5d: unusual by rpos half x ret30 sign"]=summ(N.groupby(["rh","s30"]))
    # all bars, rpos within vol terciles
    A=G5.dropna(subset=["vol20"]).copy()
    A["vq"]=A.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    res={}
    for v,x in A.groupby("vq"):
        sl=stats.linregress(x["rpos"],x["un"]); res[v]=(round(sl.slope,4),round(sl.slope/sl.stderr,2),len(x))
    out["all 5d: rpos slope by vol tercile (slope,t,n)"]=pd.DataFrame(res,index=["slope","t","n"]).T
    # weekday on cross-coin daily mean
    dd=[]
    for coin,wins in data["days"].items():
        for w,df in wins.items():
            x=df.copy(); x["coin"]=coin; dd.append(x)
    D=pd.concat(dd,ignore_index=True)
    M=D.groupby("day")[["coin_return","book_return"]].mean().reset_index()
    M["wd"]=pd.to_datetime(M["day"]).dt.dayofweek
    M["y"]=M["coin_return"]; out["day-mean coin ret by weekday"]=summ(M.dropna(subset=["y"]).groupby("wd"))
    M["y"]=M["book_return"]; out["day-mean book ret by weekday"]=summ(M.dropna(subset=["y"]).groupby("wd"))
    return out
