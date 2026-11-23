def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        grid3 = []
        per = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            idx = np.arange(0, n - 3, 3)
            grid3.extend(list(c[idx + 3] / c[idx] - 1))
            r = pd.Series(c).pct_change()
            vol = r.rolling(20, min_periods=20).std()
            vol60 = r.rolling(60, min_periods=60).std()
            ts = pd.to_datetime(df["timestamp"])
            for t in range(n):
                per.append({"coin": coin, "win": w, "year": ts.iloc[t].year, "wd": ts.iloc[t].weekday(),
                            "r": r.iloc[t], "vol": vol.iloc[t], "vol60": vol60.iloc[t],
                            "fc": float(df["forecast"].iloc[t]),
                            "r3": c[t + 3] / c[t] - 1 if t + 3 < n else np.nan})
        p = pd.DataFrame(per)
        p["x3"] = p["r3"] - np.nanmean(grid3)
        p["usual3"] = np.nanstd(grid3)
        rows.append(p)
    a = pd.concat(rows, ignore_index=True)
    a["z"] = a.r / a.vol
    a["volrel"] = a.vol / a.groupby("coin").vol.transform("median")
    a = a.dropna(subset=["z", "x3", "volrel"])
    out = {}
    def slope(g, xcol="z"):
        if len(g) < 20:
            return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan})
        res = stats.linregress(g[xcol], g["x3"])
        return pd.Series({"n": len(g), "slope": res.slope, "t": res.slope / res.stderr})
    out["slope_x3_on_z_by_weekday"] = a.groupby("wd").apply(slope)
    out["slope_x3_on_r_by_weekday"] = a.groupby("wd").apply(lambda g: slope(g, "r"))
    sun = a[a.wd == 6].copy()
    sun["vt"] = pd.qcut(sun.volrel, 3, labels=["lowvol", "midvol", "highvol"])
    out["sunday_slope_z_by_vol"] = sun.groupby("vt").apply(slope)
    out["sunday_slope_r_by_vol"] = sun.groupby("vt").apply(lambda g: slope(g, "r"))
    def summ(g):
        x = g["x3"]
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    sun["rb"] = pd.cut(sun.r, [-np.inf, -0.08, -0.05, -0.03, -0.015, 0, 0.015, 0.03, 0.05, 0.08, np.inf])
    out["sunday_by_raw_return_bin"] = sun.groupby("rb").apply(summ)
    falls = sun[sun.r < 0].copy()
    falls["zt"] = pd.qcut(falls.z, 3, labels=["deep", "mid", "shallow"])
    out["sunday_falls_vol_x_depth"] = falls.groupby(["vt", "zt"]).apply(summ)
    rises = sun[sun.r > 0].copy()
    out["sunday_rises_by_vol"] = rises.groupby("vt").apply(summ)
    # graded by vol level among Sunday falls
    falls["vq"] = pd.qcut(falls.volrel, 5, labels=False)
    out["sunday_falls_by_vol_quintile"] = falls.groupby("vq").apply(lambda g: pd.concat([summ(g), pd.Series({"volrel": g.volrel.mean()})]))
    # same on other weekdays' falls (comparison)
    of = a[(a.wd != 6) & (a.r < 0)].copy()
    of["vq"] = pd.qcut(of.volrel, 5, labels=False)
    out["otherday_falls_by_vol_quintile"] = of.groupby("vq").apply(summ)
    # Sunday fall magnitude (-r) x x3 slope in high vol
    out["sunday_falls_slope_negr_by_vol"] = falls.assign(nr=-falls.r).groupby("vt").apply(lambda g: slope(g, "nr"))
    out["sunday_falls_by_year_highvol"] = falls[falls.vt == "highvol"].groupby("year").apply(summ)
    out["sunday_falls_by_year_lowvol"] = falls[falls.vt == "lowvol"].groupby("year").apply(summ)
    return out
