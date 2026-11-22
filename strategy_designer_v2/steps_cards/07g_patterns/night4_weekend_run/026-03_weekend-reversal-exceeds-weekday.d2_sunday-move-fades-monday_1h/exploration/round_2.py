def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []; hrows = []
    for coin in bars:
        for w, df in bars[coin].items():
            d = df[["timestamp","close"]].copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.reset_index(drop=True)
            c = d["close"].values; ts = d["timestamp"]; n = len(d)
            r1 = pd.Series(c).pct_change().shift(-1).values
            lr = np.diff(np.log(c))
            hrows.append(pd.DataFrame({"coin":coin,"w":w,"hour":ts.dt.hour,"yr":ts.dt.year,"wd":ts.dt.weekday,"r1":r1,
                                       "p24":pd.Series(c).pct_change(24).values}))
            # 24h grid from window start, all start hours
            for i in range(168, n-48, 24):
                if (ts[i+48]-ts[i-168]) != pd.Timedelta(hours=216): continue
                rows.append(dict(coin=coin,w=w,yr=ts[i].year,hc=(ts[i]+pd.Timedelta(hours=1)).hour,
                    wdc=(ts[i]+pd.Timedelta(hours=1)).weekday(),
                    p24=c[i]/c[i-24]-1,f24=c[i+24]/c[i]-1,f48=c[i+48]/c[i]-1,
                    vol=np.std(lr[i-168:i])))
    R = pd.DataFrame(rows)
    sd = R.groupby("coin")["f24"].transform("std")
    R["u24"]=(R.f24-R.groupby("coin")["f24"].transform("mean"))/sd
    R["u48"]=(R.f48-R.groupby("coin")["f48"].transform("mean"))/sd
    R["z"]=R.p24/sd
    R["vt"]=R.groupby("coin")["vol"].transform(lambda v: pd.qcut(v,3,labels=False))
    def reg(g,x,y):
        g=g[[x,y]].dropna()
        if len(g)<30: return pd.Series({"n":len(g)})
        s=stats.linregress(g[x],g[y]); return pd.Series({"n":len(g),"slope":s.slope,"t":s.slope/s.stderr})
    out={}
    out["all_grid_24h_rev"]=reg(R,"z","u24")
    out["grid_by_vol_tercile"]=R.groupby("vt").apply(lambda g: reg(g,"z","u24"))
    out["grid_by_year"]=R.groupby("yr").apply(lambda g: reg(g,"z","u24"))
    out["grid_by_coin"]=R.groupby("coin").apply(lambda g: reg(g,"z","u24"))
    R["wkend"]=R.wdc.isin([6,0]).astype(int)  # close Sun 00h-23h or Mon: situation covers weekend
    out["grid_weekend_vs_not"]=R.groupby("wkend").apply(lambda g: reg(g,"z","u24"))
    out["grid_hivol_by_wkend"]=R[R.vt==2].groupby("wkend").apply(lambda g: reg(g,"z","u24"))
    # hour 20-21 effect robustness
    H=pd.concat(hrows).dropna(subset=["r1"])
    H["zr"]=H.r1/H.groupby("coin")["r1"].transform("std")
    H["h2021"]=H.hour.isin([20,21])
    E=H[H.h2021]
    def tm(x): return pd.Series({"mean":x.mean(),"n":len(x),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    out["h20_21_by_coin"]=E.groupby("coin")["zr"].apply(tm).unstack()
    out["h20_21_by_year"]=E.groupby("yr")["zr"].apply(tm).unstack()
    out["h20_21_by_weekday"]=E.groupby("wd")["zr"].apply(tm).unstack()
    out["h20_21_minus_other_welch"]=pd.Series(dict(zip(["t","p"],stats.ttest_ind(E.zr,H[~H.h2021].zr,equal_var=False))))
    # windows positive for h20-21
    wm=E.groupby(["coin","w"])["zr"].mean()
    out["h20_21_share_coinwindows_pos"]=pd.Series({"pos":(wm>0).sum(),"n":len(wm)})
    # graded: h20-21 return by prior 24h return quintile
    E2=E.dropna(subset=["p24"]).copy()
    E2["q"]=E2.groupby("coin")["p24"].transform(lambda v: pd.qcut(v,5,labels=False))
    out["h20_21_by_prior24_quint"]=E2.groupby("q")["zr"].apply(tm).unstack()
    return out
