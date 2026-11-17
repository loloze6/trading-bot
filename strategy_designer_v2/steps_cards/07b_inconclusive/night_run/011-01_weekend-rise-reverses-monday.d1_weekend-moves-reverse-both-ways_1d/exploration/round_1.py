def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    # coin mean h-bar returns on non-overlapping grid
    means = {}
    for coin, wins in bars.items():
        for h in [1,2,3,5]:
            vals = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c)-h, h)
                vals.extend(list(c[idx+h]/c[idx]-1))
            means[(coin,h)] = np.mean(vals)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"])
            c = df["close"].values
            r1 = pd.Series(c).pct_change()
            vol = r1.rolling(20).std()
            z = (r1/vol).values
            vmean = df["volume"].rolling(30).mean().values
            n = len(df)
            for i in range(n):
                dow = ts.iloc[i].dayofweek
                rec = {"coin":coin,"win":w,"year":ts.iloc[i].year,"dow":dow,
                       "f":df["forecast"].iloc[i],"z":z[i],
                       "relvol":df["volume"].iloc[i]/vmean[i] if vmean[i]>0 else np.nan}
                for h in [1,2,3,5]:
                    rec[f"x{h}"] = (c[i+h]/c[i]-1-means[(coin,h)]) if i+h<n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    out = {}
    sun = d[(d.dow==6)&d.x2.notna()].copy()
    sun["v"] = sun.f/10*sun.x2
    sun["s"] = np.sign(sun.f)*sun.x2
    def tt(x):
        x = x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    out["by_coin"] = sun.groupby("coin")["v"].apply(tt).unstack()
    out["by_year"] = sun.groupby("year")["v"].apply(tt).unstack()
    sun["side"] = np.where(sun.f>0,"long_after_fall",np.where(sun.f<0,"short_after_rise","flat"))
    out["by_side"] = sun.groupby("side")["v"].apply(tt).unstack()
    sun["q"] = pd.qcut(sun.f.abs().rank(method="first"),5,labels=False)
    out["by_absf_quint_signx2"] = sun.groupby("q")["s"].apply(tt).unstack()
    # horizons, using sign(-z) x excess for all days by weekday: does reversal concentrate on Sunday?
    hz = {}
    for h in [1,2,3,5]:
        for dw in range(7):
            sub = d[(d.dow==dw)&d[f"x{h}"].notna()&d.z.notna()]
            val = -sub.z.clip(-3,3)*sub[f"x{h}"]
            hz[(h,dw)] = tt(val)
    out["neg_z_times_excess_by_h_dow"] = pd.DataFrame(hz).T
    # volume relation on Sunday
    sun["vq"] = pd.qcut(sun.relvol.rank(method="first"),3,labels=["lowvol","mid","highvol"])
    out["sun_by_relvol"] = sun.groupby("vq")["v"].apply(tt).unstack()
    return out
