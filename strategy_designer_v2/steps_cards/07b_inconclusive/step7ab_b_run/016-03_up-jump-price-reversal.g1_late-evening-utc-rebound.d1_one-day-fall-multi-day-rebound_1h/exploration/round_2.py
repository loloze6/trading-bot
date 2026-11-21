def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values
            f = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"]).values
            n = len(c)
            r24p = np.full(n, np.nan); r24p[24:] = c[24:]/c[:-24]-1
            r720 = np.full(n, np.nan); r720[720:] = c[720:]/c[:-720]-1
            lr = np.diff(np.log(c), prepend=np.nan)
            vol720 = pd.Series(lr).rolling(720, min_periods=240).std().values
            for i in range(0, n, 72):
                rec = {"coin": coin, "w": w, "f": f[i], "r24p": r24p[i], "r720": r720[i],
                       "z": r24p[i]/(vol720[i]*np.sqrt(24)) if vol720[i] > 0 else np.nan,
                       "year": pd.Timestamp(ts[i]).year}
                for h in (24, 72, 168):
                    rec[f"y{h}"] = c[i+h]/c[i]-1 if i+h < n else np.nan
                rows.append(rec)
    g = pd.DataFrame(rows)
    for h in (24, 72, 168):
        g[f"x{h}"] = g[f"y{h}"] - g.groupby("coin")[f"y{h}"].transform("mean")
    def tmean(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s) > 2 else np.nan})
    out = {}
    out["forecast_quantiles_pos"] = g.loc[g["f"] > 0, "f"].describe()
    out["share_at_cap"] = float((g["f"] >= 19.99).mean())
    # vol-scaled depth
    fall = g[g["z"] < 0].copy()
    fall["zbin"] = pd.qcut(fall["z"], 5)
    out["zquint"] = fall.groupby("zbin").agg(n=("x72", "count"), x24=("x24", "mean"), x72=("x72", "mean"), x168=("x168", "mean"))
    deep = g[g["r24p"] <= g["r24p"].quantile(0.1)]
    out["deep10_t"] = pd.DataFrame({h: tmean(deep[f"x{h}"]) for h in (24, 72, 168)}).T
    out["deep10_by_coin"] = deep.groupby("coin")["x72"].apply(tmean).unstack()
    out["deep10_by_year"] = deep.groupby("year")["x72"].apply(tmean).unstack()
    g["trend"] = np.where(g["r720"] > 0, "up30d", np.where(g["r720"] <= 0, "down30d", "na"))
    deep = g[g["r24p"] <= g["r24p"].quantile(0.1)]
    out["deep10_by_trend"] = deep.groupby("trend")["x72"].apply(tmean).unstack()
    # slope of x72 on raw fall depth (positive = deeper fall, more rise) among falls
    ff = g[(g["r24p"] < 0)].dropna(subset=["x72"])
    r = stats.linregress(-ff["r24p"], ff["x72"])
    out["slope_raw_fall"] = pd.Series({"slope": r.slope, "t": r.slope/r.stderr, "n": len(ff)})
    ffz = g[(g["z"] < 0)].dropna(subset=["x72", "z"])
    r = stats.linregress(-ffz["z"], ffz["x72"])
    out["slope_z_fall"] = pd.Series({"slope": r.slope, "t": r.slope/r.stderr, "n": len(ffz)})
    up = ff[ff["r720"] > 0]
    r = stats.linregress(-up["r24p"], up["x72"])
    out["slope_raw_fall_up30d"] = pd.Series({"slope": r.slope, "t": r.slope/r.stderr, "n": len(up)})
    return out
