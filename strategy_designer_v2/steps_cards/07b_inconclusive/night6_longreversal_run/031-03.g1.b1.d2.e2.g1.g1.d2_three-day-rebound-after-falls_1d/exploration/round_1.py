def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    coin = list(data["bars"].keys())[0]
    wins = data["bars"][coin]
    H = [1,2,3,5,7,10,14]
    rows = []
    for w, df in wins.items():
        df = df.reset_index(drop=True)
        c = df["close"].values
        f = df["forecast"].values
        raw = df.get("debug_info.components.scaled_fall.last_history_value")
        r1 = pd.Series(c).pct_change().values
        vol = pd.Series(r1).rolling(30, min_periods=20).std().values
        yr = pd.to_datetime(df["timestamp"]).dt.year.values
        n = len(df)
        for i in range(n):
            d = {"w": w, "pos": i, "f": f[i], "yr": yr[i], "r1": r1[i], "vol": vol[i],
                 "raw": raw.values[i] if raw is not None else np.nan}
            for h in H:
                d[f"fr{h}"] = c[i+h]/c[i]-1 if i+h < n else np.nan
            rows.append(d)
    a = pd.DataFrame(rows)
    a["z1"] = a["r1"]/a["vol"]
    out = {}
    # per horizon on own grid
    hz = []
    for h in H:
        g = a[(a["pos"] % h == 0)].dropna(subset=[f"fr{h}"]).copy()
        ex = g[f"fr{h}"] - g[f"fr{h}"].mean()
        r, p = stats.pearsonr(g["f"], ex)
        n = len(g); t = r*np.sqrt((n-2)/(1-r**2))
        gz = g.dropna(subset=["z1"])
        exz = gz[f"fr{h}"] - g[f"fr{h}"].mean()
        r2 = stats.pearsonr(-gz["z1"], exz)[0]; n2 = len(gz)
        t2 = r2*np.sqrt((n2-2)/(1-r2**2))
        pos = g[g["f"] > 0]; exp = pos[f"fr{h}"] - g[f"fr{h}"].mean()
        zer = g[g["f"] == 0]; exzz = zer[f"fr{h}"] - g[f"fr{h}"].mean()
        hz.append({"h": h, "n": n, "corr_f": r, "t_f": t, "corr_negz1_both_sides": r2, "t_negz1": t2,
                   "n_pos": len(pos), "mean_ex_pos": exp.mean(), "t_pos": stats.ttest_1samp(exp, 0)[1] and exp.mean()/(exp.std()/np.sqrt(len(exp))),
                   "mean_ex_zero": exzz.mean()})
    out["by_horizon"] = pd.DataFrame(hz)
    g = a[(a["pos"] % 3 == 0)].dropna(subset=["fr3"]).copy()
    g["ex"] = g["fr3"] - g["fr3"].mean()
    pos = g[g["f"] > 0].copy()
    pos["q"] = pd.qcut(pos["f"].rank(method="first"), 5, labels=False)
    out["pos_by_forecast_quintile"] = pos.groupby("q").agg(n=("ex", "size"), fmean=("f", "mean"), ex=("ex", "mean"), sd=("ex", "std"))
    def yt(x):
        if len(x) < 5: return pd.Series({"n": len(x)})
        r = np.corrcoef(x["f"], x["ex"])[0, 1]; n = len(x)
        return pd.Series({"n": n, "corr": r, "t": r*np.sqrt((n-2)/(1-r**2)), "ex_pos": x.loc[x.f > 0, "ex"].mean(), "n_pos": (x.f > 0).sum()})
    out["by_year"] = g.groupby("yr").apply(yt)
    # up-day side: large up days scaled -> subsequent
    gz = g.dropna(subset=["z1"]).copy()
    gz["zb"] = pd.cut(gz["z1"], [-99, -2, -1, -0.5, 0, 0.5, 1, 2, 99])
    out["ex3_by_z1_bin"] = gz.groupby("zb").agg(n=("ex", "size"), ex=("ex", "mean"), sd=("ex", "std"))
    # vol ratio effect: within falls, does ex depend on vol level
    gz["vq"] = pd.qcut(gz["vol"], 3, labels=["lowvol", "midvol", "hivol"])
    fall = gz[gz["z1"] < 0]
    def ct(x):
        r = np.corrcoef(-x["z1"], x["ex"])[0, 1]; n = len(x)
        return pd.Series({"n": n, "corr": r, "t": r*np.sqrt((n-2)/(1-r**2)), "ex": x["ex"].mean()})
    out["falls_by_vol_tercile"] = fall.groupby("vq").apply(ct)
    return out
