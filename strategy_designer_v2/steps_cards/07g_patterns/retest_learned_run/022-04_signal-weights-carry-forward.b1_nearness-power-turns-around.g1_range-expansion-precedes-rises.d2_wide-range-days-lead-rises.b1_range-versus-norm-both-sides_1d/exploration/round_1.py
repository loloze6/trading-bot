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
            r20=c/c.shift(20)-1
            vol=r1.rolling(30,min_periods=10).std()
            volrel=vol/vol.rolling(90,min_periods=30).mean()
            clv=(c-b["low"])/(rng.replace(0,np.nan))  # close location in range
            hi30=c/b["high"].rolling(30,min_periods=10).max()-1
            f3=c.shift(-3)/c-1
            idx=np.arange(0,len(b)-3,3)
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"fc":b["forecast"].values[idx],"ratio":ratio.values[idx],
                "r1":r1.values[idx],"r5":r5.values[idx],"r20":r20.values[idx],"volrel":volrel.values[idx],
                "clv":clv.values[idx],"hi30":hi30.values[idx],"f3":f3.values[idx],
                "wd":ts.dt.weekday.values[idx],"yr":ts.dt.year.values[idx],
                "alloc":b["postRebalance_current_allocation"].values[idx]})
            rows.append(d)
    g=pd.concat(rows)
    g["ex"]=g["f3"]-g.groupby("coin")["f3"].transform("mean")
    out={}
    def tab(col,q=5):
        x=g.dropna(subset=[col,"ex"]).copy()
        x["b"]=x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"),q,labels=False))
        t=x.groupby("b")["ex"].agg(["mean","count","std"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
        return t[["mean","count","t"]]
    for col in ["fc","ratio","r1","r5","r20","volrel","clv","hi30"]:
        out["q_"+col]=tab(col)
    # interaction: wide range split by direction of day
    x=g.dropna(subset=["ratio","r1","ex"]).copy()
    x["wide"]=x.groupby("coin")["ratio"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    x["up"]=(x["r1"]>0).astype(int)
    t=x.groupby(["wide","up"])["ex"].agg(["mean","count","std"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["wide_x_up"]=t[["mean","count","t"]]
    x["clvb"]=pd.cut(x["clv"],[-.01,.33,.67,1.01],labels=False)
    t=x.groupby(["wide","clvb"])["ex"].agg(["mean","count","std"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["wide_x_clv"]=t[["mean","count","t"]]
    t=g.groupby("wd")["ex"].agg(["mean","count","std"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"])); out["weekday"]=t[["mean","count","t"]]
    # slope of ex on fc by coin and year
    def sl(d):
        d=d.dropna(subset=["fc","ex"])
        r=stats.linregress(d["fc"],d["ex"]); return pd.Series({"slope":r.slope,"t":r.slope/r.stderr,"n":len(d)})
    out["slope_by_coin"]=g.groupby("coin").apply(sl)
    out["slope_by_year"]=g.groupby("yr").apply(sl)
    # book daily
    dd=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            d=d.copy(); d["coin"]=coin; d["w"]=w; dd.append(d)
    D=pd.concat(dd)
    D["yr"]=pd.to_datetime(D["day"]).dt.year
    out["book_by_year"]=D.groupby("yr")[["book_return","coin_return"]].mean()
    out["book_by_coin"]=D.groupby("coin")[["book_return","coin_return"]].agg(["mean","std"])
    # alloc distribution
    al=pd.concat([b["postRebalance_current_allocation"] for wins in data["bars"].values() for b in wins.values()])
    out["alloc_desc"]=al.describe()
    return out
