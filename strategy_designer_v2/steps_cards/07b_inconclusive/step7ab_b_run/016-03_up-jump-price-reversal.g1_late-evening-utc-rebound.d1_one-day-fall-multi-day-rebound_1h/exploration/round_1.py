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
            # trailing 30-day return as regime
            r720 = np.full(n, np.nan); r720[720:] = c[720:]/c[:-720]-1
            lr = np.diff(np.log(c), prepend=np.nan)
            vol24 = pd.Series(lr).rolling(24).std().values
            vol720 = pd.Series(lr).rolling(720).std().values
            for i in range(0, n, 72):
                rec = {"coin": coin, "w": w, "f": f[i], "r24p": r24p[i], "r720": r720[i],
                       "volratio": vol24[i]/vol720[i] if vol720[i] > 0 else np.nan,
                       "year": pd.Timestamp(ts[i]).year}
                for h in (24, 72, 168):
                    rec[f"y{h}"] = c[i+h]/c[i]-1 if i+h < n else np.nan
                rows.append(rec)
    g = pd.DataFrame(rows)
    for h in (24, 72, 168):
        g[f"x{h}"] = g[f"y{h}"] - g.groupby("coin")[f"y{h}"].transform("mean")
    def slope(d, y):
        d = d.dropna(subset=[y, "f"])
        if len(d) < 20 or d["f"].std() == 0: return pd.Series({"slope": np.nan, "t": np.nan, "n": len(d)})
        r = stats.linregress(d["f"], d[y])
        return pd.Series({"slope": r.slope, "t": r.slope/r.stderr, "n": len(d)})
    out = {}
    out["by_horizon"] = pd.DataFrame({h: slope(g, f"x{h}") for h in (24, 72, 168)}).T
    out["by_coin"] = g.groupby("coin").apply(lambda d: slope(d, "x72"))
    out["by_year"] = g.groupby("year").apply(lambda d: slope(d, "x72"))
    g["fbin"] = pd.cut(g["f"], [-0.1, 0, 0.5, 1.0, 1.5, 2.0, 20], labels=["0", "0-.5", ".5-1", "1-1.5", "1.5-2", ">2"])
    out["by_fbin"] = g.groupby("fbin").agg(n=("x72", "count"), mean_x72=("x72", "mean"), mean_x168=("x168", "mean"),
                                         mean_x24=("x24", "mean"), mean_r24p=("r24p", "mean"))
    # raw depth of fall
    pos = g[g["r24p"] < 0].copy()
    pos["dbin"] = pd.qcut(pos["r24p"], 5)
    out["raw_fall_quintile"] = pos.groupby("dbin").agg(n=("x72", "count"), x72=("x72", "mean"), x168=("x168", "mean"))
    g["trend"] = np.where(g["r720"] > 0, "up30d", "down30d")
    g.loc[g["r720"].isna(), "trend"] = "na"
    out["by_trend"] = g.groupby("trend").apply(lambda d: slope(d, "x72"))
    g["volreg"] = pd.qcut(g["volratio"], 3, labels=["calm", "mid", "hot"])
    out["by_volratio"] = g.groupby("volreg").apply(lambda d: slope(d, "x72"))
    out["pos_only"] = slope(g[g["f"] > 0], "x72")
    return out
