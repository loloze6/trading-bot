def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            s24 = r.rolling(24).std()
            s720 = r.rolling(720).std()
            z = r / s24
            ratio = s24 / s720
            n = len(b)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            fc = b["forecast"].astype(float)
            for h in (24,):
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, n, h)
                df = pd.DataFrame({"coin": coin, "win": w, "z": z.values[idx],
                                   "ratio": ratio.values[idx], "fwd": fwd.values[idx],
                                   "fc": fc.values[idx], "r1": r.values[idx], "s24": s24.values[idx],
                                   "year": ts.dt.year.values[idx], "hour": ts.dt.hour.values[idx]})
                rows.append(df)
    d = pd.concat(rows).dropna(subset=["z", "fwd", "ratio"])
    d["drift"] = d.groupby("coin")["fwd"].transform("mean")
    d["un"] = d["fwd"] - d["drift"]
    d["sz"] = np.sign(d["z"]) * d["un"]
    d["tot"] = np.sign(d["z"]) * d["fwd"]
    def tstat(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x)))})
    def slope(g, col="z"):
        g = g.dropna(subset=[col,"un"])
        res = stats.linregress(g[col].clip(-6,6), g["un"])
        return pd.Series({"n": len(g), "slope_bp": 1e4*res.slope, "t": res.slope/res.stderr})
    out = {}
    hv = d[d.ratio >= 1].copy()
    out["hv signed move by coin"] = hv.groupby("coin")["sz"].apply(tstat).unstack()
    out["hv slope by year"] = hv.groupby("year").apply(slope)
    out["hv signed move by side"] = hv[hv.z != 0].groupby(np.sign(hv.loc[hv.z!=0,"z"]))["sz"].apply(tstat).unstack()
    out["hv total signed move by side"] = hv[hv.z != 0].groupby(np.sign(hv.loc[hv.z!=0,"z"]))["tot"].apply(tstat).unstack()
    hv["half"] = hv["win"].str[1:].astype(int) <= 12
    out["hv slope by first/second half windows"] = hv.groupby("half").apply(slope)
    # graded by ratio: z * ratio
    d["zr"] = d["z"] * d["ratio"]
    out["slope on z*ratio all"] = slope(d, "zr").to_frame().T
    # raw 1h return scaled by 30d vol (s720) instead
    d["z720"] = d["z"] * d["ratio"]
    # quiet case with the strategy's forecast
    q = d[(d.fc != 0)]
    out["quiet slope on forecast"] = slope(q, "fc").to_frame().T
    out["quiet signed by fc |size|"] = q.groupby(pd.cut(q.fc.abs(), [0,5,10,15,20.01]))["sz"].apply(tstat).unstack()
    out["hv by ratio bucket signed"] = hv.groupby(pd.cut(hv.ratio, [1,1.2,1.5,2,10]))["sz"].apply(tstat).unstack()
    out["hv total move abs z>1 by ratio>1.2"] = hv[(hv.z.abs()>1)].groupby(hv.ratio>1.2)["tot"].apply(tstat).unstack()
    d["settle"] = d["hour"].isin([0, 8, 16])
    out["hv slope settle vs not"] = hv.assign(settle=hv.hour.isin([0,8,16])).groupby("settle").apply(slope)
    return out
