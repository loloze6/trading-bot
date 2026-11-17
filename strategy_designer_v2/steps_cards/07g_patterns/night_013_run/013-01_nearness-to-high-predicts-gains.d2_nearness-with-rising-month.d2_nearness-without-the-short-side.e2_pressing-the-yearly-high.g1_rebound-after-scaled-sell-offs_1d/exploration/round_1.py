def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            z = r1 / vol30
            fwd3 = c.shift(-3) / c - 1
            fwd1 = c.shift(-1) / c - 1
            hi30 = c.rolling(30, min_periods=20).max()
            near = c / hi30 - 1
            r7 = c / c.shift(7) - 1
            vrel = df["volume"] / df["volume"].rolling(30, min_periods=20).mean()
            volrank = vol30 / vol30.rolling(90, min_periods=30).mean()
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(df)),
                              "fc": df["forecast"], "alloc": df["postRebalance_current_allocation"],
                              "z": z, "fwd3": fwd3, "fwd1": fwd1, "near": near, "r7": r7,
                              "vrel": vrel, "volrel": volrank,
                              "wd": pd.to_datetime(df["timestamp"]).dt.weekday,
                              "yr": pd.to_datetime(df["timestamp"]).dt.year})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A["ex3"] = A["fwd3"] - A.groupby("coin")["fwd3"].transform("mean")
    G = A[(A["pos"] % 3 == 0)].dropna(subset=["ex3", "z"])
    out = {}
    def tab(col, q=5):
        g = G.dropna(subset=[col]).copy()
        g["b"] = pd.qcut(g[col], q, labels=False, duplicates="drop")
        t = g.groupby("b").agg(lo=(col, "min"), hi=(col, "max"), n=("ex3", "size"),
                              mean=("ex3", "mean"), sd=("ex3", "std"))
        t["t"] = t["mean"] / (t["sd"] / np.sqrt(t["n"]))
        return t.drop(columns="sd")
    out["z_quint"] = tab("z", 7)
    out["near30_quint"] = tab("near")
    out["r7_quint"] = tab("r7")
    out["vol_quint"] = tab("volrel")
    out["volume_quint"] = tab("vrel")
    # by coin: up-day z slope
    res = []
    for coin, g in G.groupby("coin"):
        s = stats.linregress(g["z"], g["ex3"])
        up = g[g["z"] > 0]; su = stats.linregress(up["z"], up["ex3"])
        dn = g[g["z"] < 0]; sd = stats.linregress(dn["z"], dn["ex3"])
        res.append([coin, len(g), s.slope / s.stderr, su.slope / su.stderr, sd.slope / sd.stderr])
    out["coin_z_slope_t_all_up_down"] = pd.DataFrame(res, columns=["coin", "n", "t_all", "t_up", "t_down"])
    # weekday 1-day non-overlap is every bar
    A["ex1"] = A["fwd1"] - A.groupby("coin")["fwd1"].transform("mean")
    wd = A.dropna(subset=["ex1"]).groupby("wd")["ex1"].agg(["size", "mean", "std"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["size"]))
    out["weekday_1d"] = wd.drop(columns="std")
    yr = G.groupby("yr")["fwd3"].agg(["size", "mean"])
    out["year_fwd3"] = yr
    # book
    D = []
    for coin in days:
        for w, d in days[coin].items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; D.append(d)
    D = pd.concat(D, ignore_index=True)
    bk = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book_by_window"] = bk.groupby(level=0).agg(["mean", "count"]).iloc[:, [0, 2, 3]]
    br = bk["book_return"]
    top = br.nlargest(20).mean(); bot = br.nsmallest(20).mean()
    out["book_tail"] = pd.Series({"top20_mean": top, "bot20_mean": bot, "mean": br.mean(),
                                  "sharpe": br.mean() / br.std() * np.sqrt(365),
                                  "corr_coin": br.corr(bk["coin_return"])})
    # alloc vs forecast
    out["alloc_by_fc"] = A.assign(fb=pd.cut(A["fc"], [-0.1, 0.001, 2, 5, 10, 20.1])).groupby("fb")["alloc"].agg(["size", "mean"])
    return out
