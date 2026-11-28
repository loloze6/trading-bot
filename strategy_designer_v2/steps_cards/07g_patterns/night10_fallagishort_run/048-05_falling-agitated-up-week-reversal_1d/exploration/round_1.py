def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 3
    rows = []
    allret = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; o = b["open"]; hi = b["high"]; lo = b["low"]
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            b["fwd"] = c.shift(-H) / c - 1
            b["sw"] = (c / c.shift(7) - 1) / (sd30 * np.sqrt(7))
            b["s1"] = r1 / sd30
            b["s3"] = (c / c.shift(3) - 1) / (sd30 * np.sqrt(3))
            rng = (hi - lo)
            b["clv"] = (c - lo) / rng.replace(0, np.nan)
            b["rngs"] = (rng / c.shift(1)) / sd30
            b["dhi20"] = (c / hi.rolling(20, min_periods=10).max() - 1) / sd30
            b["dlo20"] = (c / lo.rolling(20, min_periods=10).min() - 1) / sd30
            b["vrel"] = np.log(b["volume"] / b["volume"].rolling(20, min_periods=10).mean())
            b["r60"] = c / c.shift(60) - 1
            b["inprof"] = b["regime"].isin(["mean_reversion", "unknown"])
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["pos"] = b["postRebalance_current_allocation"]
            g = b.iloc[::H].copy()
            g["coin"] = coin; g["win"] = w
            allret.append(g[["coin", "fwd"]].dropna())
            rows.append(g)
    G = pd.concat(rows)
    A = pd.concat(allret)
    cm = A.groupby("coin")["fwd"].mean()
    G["y"] = G["fwd"] - G["coin"].map(cm)
    P = G[G["inprof"]].dropna(subset=["y"])
    out = {}
    out["coin mean 3d"] = cm
    out["n in profile grid, by coin"] = P.groupby("coin").size()
    out["profile mean y"] = pd.Series({"mean": P["y"].mean(), "t": stats.ttest_1samp(P["y"], 0).statistic, "n": len(P), "mean fwd": P["fwd"].mean()})
    def qtab(col, q=5):
        d = P.dropna(subset=[col]).copy()
        d["q"] = pd.qcut(d[col], q, labels=False, duplicates="drop")
        t = d.groupby("q").agg(lo=(col, "min"), hi=(col, "max"), n=("y", "size"), mean_y=("y", "mean"), mean_fwd=("fwd", "mean"))
        t["t"] = d.groupby("q")["y"].apply(lambda s: stats.ttest_1samp(s, 0).statistic if len(s) > 2 else np.nan)
        rho = stats.spearmanr(d[col], d["y"])
        sl = stats.linregress(d[col], d["y"])
        t.loc["slope_t", "mean_y"] = sl.slope / sl.stderr
        t.loc["spearman", "mean_y"] = rho.correlation
        return t
    for col in ["sw", "s1", "s3", "clv", "rngs", "dhi20", "dlo20", "vrel", "r60"]:
        out["q " + col] = qtab(col)
    out["weekday"] = P.groupby("wd")["y"].agg(["size", "mean"])
    out["by window"] = P.groupby("win")["y"].agg(["size", "mean"])
    return out
