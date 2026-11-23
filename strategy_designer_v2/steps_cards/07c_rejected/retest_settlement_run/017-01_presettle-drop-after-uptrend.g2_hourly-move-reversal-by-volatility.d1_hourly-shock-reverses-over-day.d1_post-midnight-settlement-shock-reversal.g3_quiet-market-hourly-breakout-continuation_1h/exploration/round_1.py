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
            for h in (1, 4, 12, 24, 48):
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, n, h)
                df = pd.DataFrame({"coin": coin, "win": w, "h": h, "z": z.values[idx],
                                   "ratio": ratio.values[idx], "fwd": fwd.values[idx],
                                   "fc": b["forecast"].values[idx],
                                   "year": ts.dt.year.values[idx], "hour": ts.dt.hour.values[idx],
                                   "r24": (c / c.shift(24) - 1).values[idx]})
                rows.append(df)
    d = pd.concat(rows).dropna(subset=["z", "fwd"])
    d["drift"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["un"] = d["fwd"] - d["drift"]
    d["sz"] = np.sign(d["z"]) * d["un"]
    d["quiet"] = d["ratio"] < 1
    def tstat(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    def slope(g):
        g = g.dropna(subset=["z","un"])
        res = stats.linregress(g["z"].clip(-6,6), g["un"])
        return pd.Series({"n": len(g), "slope_bp": 1e4*res.slope, "t": res.slope/res.stderr})
    out = {}
    out["slope by h x quiet"] = d.groupby(["h","quiet"]).apply(slope)
    out["signed move by h x quiet"] = d.groupby(["h","quiet"])["sz"].apply(tstat).unstack()
    d24 = d[d.h==24].copy()
    d24["zb"] = pd.cut(d24["z"].abs(), [0,0.5,1,1.5,2,3,100])
    out["24h quiet by |z| bucket"] = d24[d24.quiet].groupby("zb")["sz"].apply(tstat).unstack()
    out["24h nonquiet by |z| bucket"] = d24[~d24.quiet].groupby("zb")["sz"].apply(tstat).unstack()
    out["24h quiet by coin"] = d24[d24.quiet].groupby("coin").apply(slope)
    out["24h quiet by side"] = d24[d24.quiet].groupby(np.sign(d24.loc[d24.quiet,"z"]))["sz"].apply(tstat).unstack()
    out["24h quiet by year"] = d24[d24.quiet].groupby("year").apply(slope)
    d24["rb"] = pd.qcut(d24["ratio"], 5)
    out["24h slope by ratio quintile"] = d24.groupby("rb").apply(slope)
    d4 = d[d.h==4].copy()
    out["4h slope by ratio"] = d4.groupby(pd.qcut(d4["ratio"],5)).apply(slope)
    out["24h slope all, by coin"] = d24.groupby("coin").apply(slope)
    return out
