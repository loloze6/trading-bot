def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; hourrows=[]
    for coin, wins in data["bars"].items():
        grid=[]
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].values
            r2=c[2::2]/c[:-2:2]-1 if len(c)>2 else np.array([])
            grid.extend(list(r2))
        drift=np.nanmean(grid); usual=np.nanstd(grid)
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"]); c=b["close"]
            lr=np.log(c).diff()
            vol=lr.rolling(720,min_periods=300).std()
            vstd=(vol-vol.rolling(500,min_periods=120).mean())/vol.rolling(500,min_periods=120).std()
            fwd2=c.shift(-2)/c-1
            okts=(ts.shift(-2)-ts)==pd.Timedelta(hours=2)
            prev24=c/c.shift(24)-1
            prev3=c/c.shift(3)-1
            df=pd.DataFrame({"coin":coin,"w":w,"hour":ts.dt.hour,"wd":ts.dt.weekday,"year":ts.dt.year,
                             "ex":(fwd2-drift).where(okts),"z":(fwd2-drift).where(okts)/usual,
                             "vol":vol,"vstd":vstd,"pos":b["postRebalance_current_allocation"],
                             "p24":prev24,"p3":prev3,"wnum":int(w[1:])})
            hourrows.append(df[["coin","hour","ex"]].iloc[::2] if False else df[["coin","hour","ex","z"]])
            rows.append(df[df.hour==20])
    d=pd.concat(rows).dropna(subset=["ex"])
    def g(x):
        n=len(x); m=x["ex"].mean(); t=m/(x["ex"].std()/np.sqrt(n)) if n>2 else np.nan
        return pd.Series({"n":n,"mean_ex_pct":100*m,"t":t,"strength":x["z"].mean()})
    out={}
    out["by_coin"]=d.groupby("coin").apply(g)
    out["by_year"]=d.groupby("year").apply(g)
    out["by_weekday"]=d.groupby("wd").apply(g)
    d["volq"]=d.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["by_raw_vol_quintile_within_coin"]=d.groupby("volq").apply(g)
    d["vsq"]=pd.qcut(d["vstd"].rank(method="first"),5,labels=False)
    out["by_vol_standardised_quintile"]=d.groupby("vsq").apply(g)
    d["p24q"]=d.groupby("coin")["p24"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["by_prior24h_quintile"]=d.groupby("p24q").apply(g)
    d["p3q"]=d.groupby("coin")["p3"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["by_prior3h_quintile"]=d.groupby("p3q").apply(g)
    h=pd.concat(hourrows).dropna(subset=["ex"])
    out["2h_excess_by_start_hour_close"]=h.groupby("hour").apply(g)
    return out
