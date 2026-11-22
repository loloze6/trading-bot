def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days=data["days"]
    out = {}
    H=[]; C=[]
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df[["timestamp","close","volume"]].copy()
            df["ts"]=pd.to_datetime(df["timestamp"],utc=True)
            df=df.sort_values("ts").reset_index(drop=True)
            c=pd.Series(df["close"].values)
            r1=c.pct_change()
            vol=r1.rolling(720,min_periods=200).std()
            z=r1/vol.shift(1)
            n=len(c)
            f={}
            for k in [1,6,24]:
                f[k]=(c.shift(-k)/c-1)
            h=pd.DataFrame({"coin":coin,"w":w,"year":df["ts"].dt.year,"hour":df["ts"].dt.hour,
                            "wd":df["ts"].dt.weekday,"r":r1,"z":z,"f1":f[1],"f6":f[6],"f24":f[24],"pos":np.arange(n)})
            H.append(h)
            # 24h past move z vs next 24h, non-overlapping grid of 24
            r24=c.pct_change(24); s24=r24.abs().rolling(720,min_periods=200).mean()
            g=pd.DataFrame({"coin":coin,"w":w,"z24":r24/s24,"f24":f[24],"s24":s24,"pos":np.arange(n)})
            C.append(g[g.pos%24==0])
    H=pd.concat(H); C=pd.concat(C).dropna()
    def tt(x):
        x=x.dropna(); return pd.Series({"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))),"n":len(x)})
    # hour 21-22 effect by coin and by year (1h returns of bars starting 21 and 22)
    e=H[H.hour.isin([21,22])]
    out["h21_22_by_coin"]=e.groupby("coin")["r"].apply(tt).unstack()
    out["h21_22_by_year"]=e.groupby("year")["r"].apply(tt).unstack()
    out["h21_22_by_wd"]=e.groupby("wd")["r"].apply(tt).unstack()
    # 2-hour block 21-22 summed per day, per coin day (one case per coin-day)
    blk=e.groupby(["coin","w","year","pos"]).r.sum()
    # reversal after 1h extreme z, grid cells of horizon k
    for k in [1,6,24]:
        a=H[(H.pos%k==0)].dropna(subset=["z",f"f{k}"]).copy()
        a["u"]=a[f"f{k}"]-a.groupby("coin")[f"f{k}"].transform("mean")
        a["q"]=pd.qcut(a["z"],10,labels=False)
        out[f"next{k}h_u_by_prev1h_z_decile"]=a.groupby("q")["u"].apply(tt).unstack()
        if k==6:
            lo=a[a.q==0]
            out["drop_rev6_by_coin"]=lo.groupby("coin")["u"].apply(tt).unstack()
            out["drop_rev6_by_year"]=lo.groupby("year")["u"].apply(tt).unstack()
            s=stats.linregress(a["z"].clip(-6,6),a["u"]); out["slope6"]=f"{s.slope:.5f} t={s.slope/s.stderr:.2f} n={len(a)}"
    C["u"]=C["f24"]-C.groupby("coin")["f24"].transform("mean")
    C["q"]=pd.qcut(C["z24"],10,labels=False)
    out["next24_u_by_past24_z_decile"]=C.groupby("q")["u"].apply(tt).unstack()
    # saturday by year
    D=[]
    for coin,ws in days.items():
        for w,dd in ws.items():
            dd=dd.copy(); d=pd.to_datetime(dd["day"]); dd["wd"]=d.dt.weekday; dd["year"]=d.dt.year; dd["coin"]=coin; D.append(dd)
    D=pd.concat(D)
    out["sat_by_year"]=D[D.wd==5].groupby("year")["coin_return"].apply(tt).unstack()
    out["fri_sat_minus_rest_t"]=str(stats.ttest_ind(D[D.wd.isin([4,5])].coin_return.dropna(),D[~D.wd.isin([4,5])].coin_return.dropna(),equal_var=False))
    return out
