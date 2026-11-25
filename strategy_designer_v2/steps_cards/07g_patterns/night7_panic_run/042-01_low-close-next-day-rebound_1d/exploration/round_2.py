def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            rng = (h - l)
            lr = np.log(c / c.shift(1))
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]),
                "clv": np.where(rng > 0, (h - c) / rng, np.nan),
                "ret0": c / c.shift(1) - 1,
                "rngpct": rng / c,
                "r1": c.shift(-1) / c - 1,
                "r2": c.shift(-2) / c - 1,
                "tr60": c / c.shift(60) - 1,
                "vol": b["volume"].astype(float),
                "sd30": lr.rolling(30, min_periods=20).std(),
            })
            d["rng20"] = d["rngpct"] / d["rngpct"].rolling(20, min_periods=10).mean().shift(1)
            d["vol20"] = d["vol"] / d["vol"].rolling(20, min_periods=10).mean().shift(1)
            d["agit"] = d["sd30"] / d["sd30"].rolling(120, min_periods=60).median()
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["r1x"] = D["r1"] - D.groupby("coin")["r1"].transform("mean")
    D["z1"] = D["r1x"] / D.groupby("coin")["r1"].transform("std")
    D["ret0z"] = D["ret0"] / D.groupby("coin")["ret0"].transform("std")
    D["day"] = D["ts"].dt.floor("D")
    def clus(df, ycol, xcols):
        df = df.dropna(subset=[ycol] + xcols)
        X = np.column_stack([np.ones(len(df))] + [df[c].values for c in xcols])
        y = df[ycol].values
        XtX = np.linalg.inv(X.T @ X); b = XtX @ X.T @ y; e = y - X @ b
        g = pd.DataFrame(X * e[:, None]).groupby(df["day"].values).sum().values
        G = len(g); n, k = X.shape
        V = XtX @ (g.T @ g) @ XtX * G / (G - 1) * (n - 1) / (n - k)
        return pd.DataFrame({"beta": b, "t_day": b / np.sqrt(np.diag(V))}, index=["c"] + xcols).assign(n=n, days=G)
    out = {}
    D["clvc"] = D["clv"] - 0.5
    out["clustered z1 ~ clv"] = clus(D, "z1", ["clvc"])
    out["clustered z1 ~ ret0z"] = clus(D, "z1", ["ret0z"])
    out["clustered z1 ~ clv + ret0z"] = clus(D, "z1", ["clvc", "ret0z"])
    D["lrr"] = np.log(D["rng20"])
    D["clv_x_rng"] = D["clvc"] * D["lrr"]
    out["clustered z1 ~ clv + logrelrange + clv*logrelrange"] = clus(D, "z1", ["clvc", "lrr", "clv_x_rng"])
    D["clvrw"] = D["clvc"] * D["rng20"]
    out["clustered z1 ~ clv*relrange (graded weighting)"] = clus(D, "z1", ["clvrw", "ret0z"])
    for tr in ["falling", "choppy", "rising"]:
        m = np.where(D["tr60"] > 0.1, "rising", np.where(D["tr60"] < -0.1, "falling", "choppy"))
        out["clustered clv*relrange in " + tr] = clus(D[(m == tr) & D["tr60"].notna()], "z1", ["clvrw"])
    D["ag"] = np.where(D["agit"] > 1, "agitated", "calm")
    for a in ["agitated", "calm"]:
        out["clustered clv*relrange " + a] = clus(D[(D["ag"] == a) & D["agit"].notna()], "z1", ["clvrw"])
    # relative range quintile x clv tercile mean z1
    X = D.dropna(subset=["rng20", "clv", "z1"]).copy()
    X["rq"] = pd.qcut(X["rng20"], 5, labels=False); X["cq"] = pd.qcut(X["clv"], 3, labels=False)
    out["relrange quintile x clv tercile mean z1"] = X.pivot_table(index="rq", columns="cq", values="z1", aggfunc="mean")
    # size in % of wide-day low-close vs high-close
    top = X[X["rq"] == 4]
    out["widest-range quintile: next-day drift-removed %, by clv tercile"] = top.groupby("cq")["r1x"].agg(["mean", "count"]).assign(mean_pct=lambda s: s["mean"] * 100)
    # 2-day horizon nonoverlap
    Y = D[D["pos"] % 2 == 0].copy()
    Y["r2x"] = Y["r2"] - D.groupby("coin")["r2"].transform("mean").loc[Y.index]
    Y["z2"] = Y["r2x"] / Y.groupby("coin")["r2"].transform("std")
    out["2-day nonoverlap z2 ~ clv*relrange"] = clus(Y, "z2", ["clvrw"])
    # volume version
    D["clvvw"] = D["clvc"] * D["vol20"].clip(upper=5)
    out["clustered z1 ~ clv*relvolume + clv*relrange"] = clus(D, "z1", ["clvvw", "clvrw"])
    # by coin for clv*relrange
    out["by coin clv*relrange"] = pd.concat({c: clus(x, "z1", ["clvrw"]).loc["clvrw"] for c, x in D.groupby("coin")}, axis=1).T
    return out
