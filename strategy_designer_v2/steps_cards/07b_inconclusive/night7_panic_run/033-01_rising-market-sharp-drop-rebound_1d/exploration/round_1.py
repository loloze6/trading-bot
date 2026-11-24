def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=20).std()
            z = r1 / sd
            tr60 = c / c.shift(60) - 1
            sd365med = sd.rolling(365, min_periods=120).median()
            agit = (sd > sd365med).astype(float).where(sd365med.notna())
            n = len(df)
            for h in (1, 3, 5, 10):
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, n, h)
                sub = pd.DataFrame({
                    "coin": coin, "win": w, "h": h,
                    "fwd": fwd.iloc[idx].values,
                    "z": z.iloc[idx].values,
                    "fc": df["forecast"].iloc[idx].values,
                    "reg": df["regime"].iloc[idx].values,
                    "tr": tr60.iloc[idx].values,
                    "agit": agit.iloc[idx].values,
                })
                rows.append(sub)
    d = pd.concat(rows, ignore_index=True)
    d = d[d["fwd"].notna()]
    drift = d.groupby(["coin", "h"])["fwd"].mean().rename("drift")
    d = d.join(drift, on=["coin", "h"])
    d["ex"] = d["fwd"] - d["drift"]
    d["inprof"] = d["reg"] == "unknown"
    d["trend"] = np.where(d["tr"] > 0.10, "rising", np.where(d["tr"] < -0.10, "falling", "choppy"))
    d.loc[d["tr"].isna(), "trend"] = "na"
    d["fall"] = (-d["z"]).clip(lower=0)
    d["down"] = d["z"] < 0

    def slope(g, x="fc"):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 10 or g[x].std() == 0:
            return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan})
        res = stats.linregress(g[x], g["ex"])
        return pd.Series({"n": len(g), "slope": res.slope, "t": res.slope / res.stderr})

    out = {}
    ip = d[d["inprof"]]
    out["inprof slope by horizon (forecast)"] = ip.groupby("h").apply(slope)
    out["slope on fall(z) by horizon and trend"] = d.groupby(["h", "trend"]).apply(lambda g: slope(g, "fall"))
    ip3 = ip[ip["h"] == 3]
    out["inprof h3 slope by coin"] = ip3.groupby("coin").apply(slope)
    out["inprof h3 slope by window"] = ip3.groupby("win").apply(slope)
    out["inprof h3 slope by agitation"] = ip3.groupby("agit").apply(slope)
    ip3 = ip3.copy()
    ip3["zbin"] = pd.cut(ip3["z"], [-np.inf, -2, -1.5, -1, -0.5, 0, 0.5, 1, np.inf])
    out["inprof h3 excess by z bin"] = ip3.groupby("zbin")["ex"].agg(["count", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    d3 = d[d["h"] == 3].copy()
    d3["zbin"] = pd.cut(d3["z"], [-np.inf, -2, -1, 0, np.inf])
    out["h3 excess by trend x zbin"] = d3.groupby(["trend", "zbin"])["ex"].agg(["count", "mean"]).unstack()
    out["inprof h3 down-up diff"] = ip3.groupby("down")["ex"].agg(["count", "mean", "std"])
    return out
