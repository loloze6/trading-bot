def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            r = c.pct_change(); vol20 = r.rolling(20).std()
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                               "ts": pd.to_datetime(b["timestamp"])})
            df["z1"] = r / vol20.shift(1)
            df["z20"] = (c / c.shift(20) - 1) / (vol20 * np.sqrt(20))
            df["z10"] = (c / c.shift(10) - 1) / (vol20 * np.sqrt(10))
            df["z40"] = (c / c.shift(40) - 1) / (vol20 * np.sqrt(40))
            df["clv"] = (c - l) / (h - l).replace(0, np.nan)
            rng = (h - l) / c
            df["rngratio"] = rng.rolling(5).mean() / rng.rolling(60, min_periods=30).mean()
            for hz in (1, 2, 5, 10):
                df[f"f{hz}"] = c.shift(-hz) / c - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D"); D["year"] = D["ts"].dt.year
    def grid(hz):
        g = D[D["pos"] % hz == 0].dropna(subset=[f"f{hz}"]).copy()
        g["exs"] = (g[f"f{hz}"] - g.groupby("coin")[f"f{hz}"].transform("mean")) / g.groupby("coin")[f"f{hz}"].transform("std")
        return g
    def cl_slope(g, col, y="exs"):
        gg = g.dropna(subset=[col, y]).copy()
        x = gg.groupby("coin")[col].rank(pct=True) - 0.5
        gg["x"] = x
        X = np.c_[np.ones(len(gg)), gg["x"].values]; Y = gg[y].values
        beta = np.linalg.lstsq(X, Y, rcond=None)[0]; e = Y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        S = np.zeros((2, 2))
        for _, idx in gg.groupby("day").indices.items():
            s = X[idx].T @ e[idx]; S += np.outer(s, s)
        nd = gg["day"].nunique(); V = XtXi @ S @ XtXi * nd / (nd - 1)
        return beta[1], beta[1] / np.sqrt(V[1, 1]), len(gg), nd
    out = {}
    res = {}
    for hz in (1, 2, 5, 10):
        g = grid(hz)
        for col in ["z10", "z20", "z40", "clv", "z1"]:
            s = cl_slope(g, col); res[f"h{hz}_{col}"] = s
    out["clustered_slopes"] = pd.DataFrame(res, index=["slope", "t", "n", "days"]).T.round(4)
    for hz, col in [(5, "z20"), (1, "clv"), (10, "z20")]:
        g = grid(hz)
        for key in ["win", "coin", "year"]:
            r2 = {}
            for k, x in g.groupby(key):
                xx = x.dropna(subset=[col])
                if len(xx) < 20: continue
                s = stats.linregress(xx.groupby("coin")[col].rank(pct=True), xx["exs"])
                r2[k] = (s.slope, s.slope / s.stderr, len(xx))
            out[f"h{hz}_{col}_by_{key}"] = pd.DataFrame(r2, index=["slope", "t", "n"]).T.round(3)
    # z20 slope within calm vs not calm (h5)
    g = grid(5).dropna(subset=["z20", "rngratio"])
    g["calm"] = g["rngratio"] < g.groupby("coin")["rngratio"].transform("median")
    r3 = {}
    for k, x in g.groupby("calm"):
        r3[str(k)] = cl_slope(x, "z20")
    out["h5_z20_calm_split"] = pd.DataFrame(r3, index=["slope", "t", "n", "days"]).T.round(4)
    # clv controlling z1: two-way at h1
    g = grid(1).dropna(subset=["clv", "z1"])
    g["zq"] = pd.qcut(g["z1"].rank(method="first"), 3, labels=False)
    r4 = {}
    for k, x in g.groupby("zq"):
        r4[k] = cl_slope(x, "clv")
    out["h1_clv_within_z1_tercile"] = pd.DataFrame(r4, index=["slope", "t", "n", "days"]).T.round(4)
    # raw pct effect sizes: top minus bottom quintile z20 at h5, clv at h1
    for hz, col in [(5, "z20"), (1, "clv")]:
        g = grid(hz).dropna(subset=[col])
        g["q"] = g.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
        out[f"raw_h{hz}_{col}"] = g.groupby("q")[f"f{hz}"].agg(["mean", "count"]).round(5)
    return out
