def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); h = df["high"].astype(float); l = df["low"].astype(float)
            r6 = c / c.shift(6) - 1
            mabs = r6.abs().rolling(180, min_periods=60).mean()
            z6 = r6 / mabs
            rng = (h.rolling(6).max() - l.rolling(6).min()) / c
            rngz = rng / rng.rolling(180, min_periods=60).mean()
            r1 = np.log(c).diff()
            vol = r1.rolling(180, min_periods=60).std()
            volz = vol / vol.rolling(540, min_periods=180).mean()
            tr180 = c / c.shift(180) - 1
            ts = pd.to_datetime(df["timestamp"])
            out = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(df)), "z6": z6, "rngz": rngz,
                                "volz": volz, "tr180": tr180, "fc": df["forecast"],
                                "hour": ts.dt.hour, "wd": ts.dt.weekday, "year": ts.dt.year})
            for H in [1, 6, 18, 42, 84]:
                out[f"f{H}"] = c.shift(-H) / c - 1
            rows.append(out)
    A = pd.concat(rows, ignore_index=True)
    res = {}
    def grid(H):
        g = A[A["pos"] % H == 0].dropna(subset=[f"f{H}"]).copy()
        g["ex"] = g[f"f{H}"] - g.groupby("coin")[f"f{H}"].transform("mean")
        return g
    def tab(g, col, q=5):
        g = g.dropna(subset=[col]).copy()
        g["b"] = pd.qcut(g[col].rank(method="first"), q, labels=False)
        t = g.groupby("b").agg(lo=(col, "min"), hi=(col, "max"), n=("ex", "size"), mean_ex=("ex", "mean"), sd=("ex", "std"))
        t["t"] = t["mean_ex"] / (t["sd"] / np.sqrt(t["n"]))
        return t.drop(columns="sd")
    for H in [6, 18, 42, 84]:
        res[f"z6 quintiles -> ex {H}bars"] = tab(grid(H), "z6")
    g84 = grid(84); g42 = grid(42)
    res["range quintiles -> ex 84"] = tab(g84, "rngz")
    res["range quintiles -> ex 42"] = tab(g42, "rngz")
    res["vol level quintiles -> ex 84"] = tab(g84, "volz")
    res["180bar trend quintiles -> ex 84"] = tab(g84, "tr180")
    res["180bar trend quintiles -> ex 42"] = tab(g42, "tr180")
    # panic: big range and fall
    for H, g in [(42, g42), (84, g84)]:
        p = g[(g.rngz > g.rngz.quantile(0.8)) & (g.z6 < 0)]
        res[f"panic (top range, fall) ex {H}"] = pd.Series({"n": len(p), "mean": p.ex.mean(), "t": p.ex.mean() / (p.ex.std() / np.sqrt(len(p)))})
    g1 = grid(1)
    hr = g1.groupby("hour")["ex"].agg(["size", "mean", "std"]); hr["t"] = hr["mean"] / (hr["std"] / np.sqrt(hr["size"]))
    res["hour -> next bar ex"] = hr.drop(columns="std")
    g6 = grid(6)
    wd = g6.groupby("wd")["ex"].agg(["size", "mean", "std"]); wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["size"]))
    res["weekday -> next day ex"] = wd.drop(columns="std")
    # by coin z6 slope 84
    sl = {}
    for coin, g in g84.dropna(subset=["z6"]).groupby("coin"):
        s = stats.linregress(g.z6, g.ex); sl[coin] = {"slope": s.slope, "t": s.slope / s.stderr, "n": len(g)}
    res["per coin slope ex84 on z6"] = pd.DataFrame(sl).T
    # book
    D = []
    for coin, wins in days.items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D)
    yr = pd.to_datetime(D["day"]).dt.year
    by = D.groupby(yr).agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "size"))
    res["book vs coin daily by year"] = by
    bw = D.groupby("win").agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    res["book vs coin by window"] = bw
    return res
