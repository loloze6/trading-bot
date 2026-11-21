def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        allr=[]
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            d=pd.DataFrame({"coin":coin,"win":w})
            d["r1"]=c.shift(-1)/c-1
            d["r2"]=c.shift(-2)/c-1
            d["past1"]=c/c.shift(1)-1
            d["mom7"]=c/c.shift(7)-1
            d["mom28"]=c/c.shift(28)-1
            lr=np.log(c).diff()
            d["vol20"]=lr.rolling(20).std()
            d["nextwd"]=(ts+pd.Timedelta(days=1)).dt.weekday
            d["pos"]=b["postRebalance_current_allocation"].astype(float)
            d["fc"]=b["forecast"].astype(float)
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["drift"]=D.groupby("coin")["r1"].transform("mean")
    D["x1"]=D["r1"]-D["drift"]
    D["z7"]=D["mom7"]/(D["vol20"]*np.sqrt(7))
    D["z28"]=D["mom28"]/(D["vol20"]*np.sqrt(28))
    D["zp1"]=D["past1"]/D["vol20"]
    D["xs"]=D["x1"]/D["vol20"]
    out={}
    def tcorr(g,col):
        g=g[[col,"xs"]].dropna()
        if len(g)<30: return pd.Series({"n":len(g),"corr":np.nan,"t":np.nan})
        r=g[col].corr(g["xs"]); n=len(g)
        return pd.Series({"n":n,"corr":r,"t":r*np.sqrt((n-2)/(1-r*r))})
    out["wd_mean_excess"]=D.groupby("nextwd").apply(lambda g: pd.Series({"n":g["x1"].notna().sum(),"mean_x":g["x1"].mean(),"t":stats.ttest_1samp(g["x1"].dropna(),0)[1] and g["x1"].mean()/(g["x1"].std()/np.sqrt(g["x1"].notna().sum()))}))
    out["z7_by_nextwd"]=D.groupby("nextwd").apply(lambda g: tcorr(g,"z7"))
    out["z28_by_nextwd"]=D.groupby("nextwd").apply(lambda g: tcorr(g,"z28"))
    out["zp1_by_nextwd"]=D.groupby("nextwd").apply(lambda g: tcorr(g,"zp1"))
    sat=D[D["nextwd"]==5]
    out["z7_sat_by_coin"]=sat.groupby("coin").apply(lambda g: tcorr(g,"z7"))
    sat2=sat.copy(); sat2["q"]=pd.qcut(sat2["z7"],5,labels=False)
    out["sat_z7_quintile"]=sat2.groupby("q").agg(n=("x1","count"),mean_x=("x1","mean"),mean_r2=("r2","mean"))
    D["vq"]=D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["volq_next"]=D.groupby("vq").agg(n=("x1","count"),mean_x=("x1","mean"),abs_r1=("r1",lambda s:s.abs().mean()))
    out["z7_sat_by_volq"]=sat.assign(vq=D.loc[sat.index,"vq"]).groupby("vq").apply(lambda g: tcorr(g,"z7"))
    D["year_w"]=D["win"]
    out["z7_sat_by_window"]=sat.groupby("win").apply(lambda g: tcorr(g,"z7"))
    out["sun_z7_sat_ret"]=D[D["nextwd"]==6].pipe(lambda g: tcorr(g,"z7"))
    # Saturday + Sunday horizon from Friday close
    s=sat[["z7","r2"]].dropna(); out["sat_z7_r2_corr"]=pd.Series({"n":len(s),"corr":s["z7"].corr(s["r2"])})
    # book days
    dd=[]
    for coin,wins in data["days"].items():
        for w,t in wins.items():
            t=t.copy(); t["coin"]=coin; t["wd"]=pd.to_datetime(t["day"]).dt.weekday; dd.append(t)
    Dy=pd.concat(dd)
    out["book_by_wd"]=Dy.groupby("wd").agg(book=("book_return","mean"),coin=("coin_return","mean"),n=("book_return","count"))
    out["book_by_coin"]=Dy.groupby("coin").agg(book=("book_return","mean"),sd=("book_return","std"))
    return out
