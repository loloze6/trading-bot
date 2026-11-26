def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); v = b["volume"].astype(float)
            r = c.pct_change()
            vol20 = r.rolling(20).std()
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                               "ts": pd.to_datetime(b["timestamp"])})
            df["r1"] = r
            df["z1"] = r / vol20.shift(1)
            df["z5"] = (c / c.shift(5) - 1) / (vol20 * np.sqrt(5))
            df["z20"] = (c / c.shift(20) - 1) / (vol20 * np.sqrt(20))
            rng = (h - l) / c
            df["rngratio"] = rng.rolling(5).mean() / rng.rolling(60, min_periods=30).mean()
            df["volratio"] = v.rolling(5).mean() / v.rolling(60, min_periods=30).mean()
            df["volreg"] = vol20 / vol20.rolling(60, min_periods=30).median()
            df["rngday"] = rng / rng.rolling(20).mean()
            df["clv"] = (c - l) / (h - l).replace(0, np.nan)
            for hz in (1, 2, 5):
                df[f"f{hz}"] = c.shift(-hz) / c - 1
            df["alloc"] = b["postRebalance_current_allocation"].astype(float)
            df["fwd1"] = c.shift(-1) / c - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["wd"] = D["ts"].dt.weekday
    out = {}
    def grid(hz):
        g = D[D["pos"] % hz == 0].copy()
        g = g.dropna(subset=[f"f{hz}"])
        g["ex"] = g[f"f{hz}"] - g.groupby("coin")[f"f{hz}"].transform("mean")
        g["exs"] = g["ex"] / g.groupby("coin")[f"f{hz}"].transform("std")
        return g
    def tab(g, col, q=5):
        gg = g.dropna(subset=[col]).copy()
        gg["b"] = gg.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        t = gg.groupby("b")["exs"].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        sl = stats.linregress(gg.groupby("coin")[col].rank(pct=True), gg["exs"])
        t.loc["slope", "mean"] = sl.slope; t.loc["slope", "t"] = sl.slope / sl.stderr
        return t[["mean", "count", "t"]].round(4)
    for hz in (1, 2, 5):
        g = grid(hz)
        for col in ["z1", "z5", "z20", "rngratio", "volratio", "volreg", "clv", "rngday"]:
            out[f"h{hz}_{col}"] = tab(g, col)
    g = grid(1)
    wd = g.groupby("wd")["exs"].agg(["mean", "count", "std"]); wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["h1_weekday"] = wd.round(4)
    # calm decline: z20 negative and rngratio low
    g5 = grid(5).dropna(subset=["z20", "rngratio"])
    g5["dec"] = pd.cut(g5["z20"], [-99, -1.5, -0.5, 0.5, 1.5, 99])
    g5["calm"] = g5["rngratio"] < g5.groupby("coin")["rngratio"].transform("median")
    t = g5.groupby(["dec", "calm"])["exs"].agg(["mean", "count", "std"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    out["h5_z20_by_calm"] = t.round(4)
    # by coin, z1 slope h2
    g2 = grid(2).dropna(subset=["z1"])
    res = {}
    for coin, x in g2.groupby("coin"):
        s = stats.linregress(x["z1"].clip(-5, 5), x["exs"]); res[coin] = (s.slope, s.slope / s.stderr, len(x))
    out["h2_z1_slope_by_coin"] = pd.DataFrame(res, index=["slope", "t", "n"]).T.round(4)
    return out
