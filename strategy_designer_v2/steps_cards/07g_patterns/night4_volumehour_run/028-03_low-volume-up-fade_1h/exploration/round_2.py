def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            ts=pd.to_datetime(b["timestamp"])
            r1=c/c.shift(1)-1
            mabs=r1.abs().rolling(720,min_periods=240).mean().shift(1)
            vr=v/v.rolling(720,min_periods=240).mean().shift(1)
            d=pd.DataFrame({"coin":coin,"w":w,"yr":ts.dt.year,"hour":ts.dt.hour,"wd":ts.dt.weekday,
                            "r1":r1,"mabs":mabs,"vr":vr,"c":c,
                            "alloc":b["postRebalance_current_allocation"].astype(float)})
            # return over 20:00 and 21:00 bars: close of 21:00 bar / close of 19:00 bar
            d["ev2"]=c.shift(-2)/c-1      # from close of this bar over next 2 bars
            d["prior7"]=c/c.shift(7)-1    # past 7 hours
            d["prior24"]=c/c.shift(24)-1
            d["f1"]=c.shift(-1)/c-1
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    out={}
    mu1=D.groupby("coin")["f1"].mean()
    D["ex1"]=D["f1"]-D["coin"].map(mu1)
    def agg(x):
        x=x.dropna(); n=len(x)
        return pd.Series({"n":n,"mean_bp":x.mean()*1e4,"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    # evening window: decision at close of 19:00 bar, return over the 20:00 and 21:00 bars
    E=D[D.hour==19].copy()
    mu2=D.groupby("coin")["ev2"].mean()  # rough normal 2h drift
    E["ex2"]=E["ev2"]-E["coin"].map(mu2)
    out["eve_by_coin"]=E.groupby("coin")["ex2"].apply(agg).unstack().round(2)
    out["eve_by_year"]=E.groupby("yr")["ex2"].apply(agg).unstack().round(2)
    out["eve_by_weekday"]=E.groupby("wd")["ex2"].apply(agg).unstack().round(2)
    wm=E.groupby(["coin","w"])["ex2"].mean()
    out["eve_share_windows_positive"]=pd.Series({"share":(wm>0).mean(),"n":len(wm)})
    E["p7"]=E["prior7"]/(E["mabs"]*np.sqrt(7))
    E["p7q"]=pd.qcut(E["p7"],5,labels=False)
    out["eve_by_prior7_quintile"]=E.groupby("p7q")["ex2"].apply(agg).unstack().round(2)
    E["p24q"]=pd.qcut(E["prior24"]/(E["mabs"]*np.sqrt(24)),5,labels=False)
    out["eve_by_prior24_quintile"]=E.groupby("p24q")["ex2"].apply(agg).unstack().round(2)
    E["vq"]=pd.qcut(E["vr"],4,labels=False)
    out["eve_by_vol_ratio_q"]=E.groupby("vq")["ex2"].apply(agg).unstack().round(2)
    # early-hours weakness: decision at 23:00 close, over 00-02 bars (3 bars)
    D["ev3"]=D.groupby(["coin","w"])["c"].transform(lambda s:s.shift(-3)/s-1)
    N=D[D.hour==23].copy()
    mu3=D.groupby("coin")["ev3"].mean()
    N["ex3"]=N["ev3"]-N["coin"].map(mu3)
    out["night_by_coin"]=N.groupby("coin")["ex3"].apply(agg).unstack().round(2)
    out["night_by_year"]=N.groupby("yr")["ex3"].apply(agg).unstack().round(2)
    # book decomposition
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    DD=pd.concat(dd).dropna(subset=["book_return","coin_return"])
    out["mean_alloc_all_bars"]=float(D["alloc"].mean())
    out["coin_mean_daily_bp"]=DD.groupby("coin")["coin_return"].mean().mul(1e4).round(2)
    out["book_mean_daily_bp"]=DD.groupby("coin")["book_return"].mean().mul(1e4).round(2)
    # share of time short, gain from market rise
    ma=D.groupby("coin")["alloc"].mean()
    out["market_part_daily_bp"]=(ma*DD.groupby("coin")["coin_return"].mean()*1e4).round(2)
    return out
