def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; hr=[]
    for coin,ws in data["bars"].items():
        g=[];sds=[]
        for w,b in ws.items():
            c=b["close"].values.astype(float)
            idx=np.arange(0,len(c)-24,24)
            g.append(c[idx+24]/c[idx]-1)
        g=np.concatenate(g); drift=g.mean(); sd=g.std()
        for w,b in ws.items():
            ts=pd.to_datetime(b["timestamp"]); c=b["close"].astype(float).reset_index(drop=True)
            v=b["volume"].astype(float).reset_index(drop=True)
            d=pd.DataFrame({"hour":ts.dt.hour.values,"wd":ts.dt.weekday.values,"year":ts.dt.year.values})
            r1=c.pct_change()
            d["r1"]=r1; d["r24"]=c/c.shift(24)-1; d["f24"]=c.shift(-24)/c-1-drift
            d["f6"]=c.shift(-6)/c-1; d["h1"]=r1.shift(24)
            d["vol24"]=r1.rolling(24).std(); d["z"]=d["r24"]/sd; d["coin"]=coin; d["win"]=w
            d["lv"]=np.log(v+1); d["lvn"]=d["lv"]-d["lv"].rolling(168,min_periods=48).mean()
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["vt"]=D.groupby("coin")["vol24"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    def slope(x):
        x=x.dropna(subset=["z","f24"])
        if len(x)<50: return pd.Series({"n":len(x),"slope":np.nan,"t":np.nan})
        r=stats.linregress(-x["z"],x["f24"]); return pd.Series({"n":len(x),"slope":r.slope,"t":r.slope/r.stderr})
    # reversal slope by hour, all days (one bar per day per hour)
    by_hour=D.groupby("hour").apply(slope)
    cond=D[np.sign(D["h1"])==-np.sign(D["r24"])]
    by_hour_cond=D[np.sign(D["h1"])==-np.sign(D["r24"])].groupby("hour").apply(slope)
    h0=D[D.hour==0]
    out={}
    out["rev slope by hour, all days"]=by_hour
    out["rev slope by hour, disagree cond"]=by_hour_cond
    out["h0 by vol tercile"]=h0.groupby("vt").apply(slope)
    out["all hours by vol tercile (hour 0,8,16 grid)"]=D[D.hour.isin([0,8,16])].groupby("vt").apply(slope)
    out["h0 by weekday"]=h0.groupby("wd").apply(slope)
    out["h0 by coin"]=h0.groupby("coin").apply(slope)
    out["h0 by year"]=h0.groupby("year").apply(slope)
    hh=D.groupby("hour")["r1"].agg(["mean","std","count"]); hh["t"]=hh["mean"]/(hh["std"]/np.sqrt(hh["count"]))
    hh["vol_norm"]=D.groupby("hour")["lvn"].mean()
    out["hourly ret and vol by hour"]=hh[["mean","t","vol_norm"]]
    # z quintiles at hour 0
    h0q=h0.dropna(subset=["z","f24"]).copy(); h0q["q"]=pd.qcut(h0q["z"],5,labels=False)
    out["h0 f24 by r24 quintile"]=h0q.groupby("q")["f24"].agg(["mean","count"])
    # book days
    dd=pd.concat([x.assign(coin=c) for c,ws in data["days"].items() for x in ws.values()])
    dd["wd"]=pd.to_datetime(dd["day"]).dt.weekday; dd["yr"]=pd.to_datetime(dd["day"]).dt.year
    out["book by weekday"]=dd.groupby("wd")["book_return"].agg(["mean","count"])
    out["book by year"]=dd.groupby("yr")[["book_return","coin_return"]].mean()
    return out
