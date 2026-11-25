def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            hi28 = c.rolling(28, min_periods=28).max()
            df = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "near": c / hi28 - 1,
                "ret28": c / c.shift(27) - 1,
                "ret5p": c / c.shift(5) - 1,
                "ret1": r1,
                "vol20": r1.rolling(20).std(),
                "volrel": r1.rolling(10).std() / r1.rolling(60, min_periods=30).std(),
                "rng": ((b["high"] - b["low"]) / c).rolling(5).mean() / ((b["high"] - b["low"]) / c).rolling(60, min_periods=30).mean(),
                "vrel": b["volume"].rolling(5).mean() / b["volume"].rolling(60, min_periods=30).mean(),
                "fc": b["forecast"],
                "fwd": c.shift(-H) / c - 1,
                "pos": np.arange(len(b)),
            })
            rows.append(df[df["pos"] % H == 0])
    g = pd.concat(rows).dropna(subset=["fwd"])
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g["day"] = g["ts"].dt.floor("D")
    out = {}
    def clus_t(x, y):
        d = pd.DataFrame({"x": x, "y": y, "day": g.loc[x.index, "day"]}).dropna()
        X = np.c_[np.ones(len(d)), d["x"].values]
        beta = np.linalg.lstsq(X, d["y"].values, rcond=None)[0]
        e = d["y"].values - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        s = pd.DataFrame(X * e[:, None]).groupby(d["day"].values).sum().values
        G = len(s)
        V = XtXi @ (s.T @ s) @ XtXi * G / (G - 1)
        return beta[1], beta[1] / np.sqrt(V[1, 1]), len(d), G
    sl = {}
    for f in ["near", "ret28", "ret5p", "ret1", "vol20", "volrel", "rng", "vrel", "fc"]:
        x = (g[f] - g.groupby("coin")[f].transform("mean")) / g.groupby("coin")[f].transform("std")
        b_, t_, n_, G_ = clus_t(x, g["ex"])
        sl[f] = {"slope_per_sd": b_, "t_day": t_, "n": n_, "days": G_}
    out["slopes"] = pd.DataFrame(sl).T
    def qtab(f, q=5):
        d = g.dropna(subset=[f]).copy()
        d["q"] = d.groupby("coin")[f].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        return d.groupby("q")["ex"].agg(["mean", "count", lambda s: s.mean() / s.std() * np.sqrt(len(s))]).rename(columns={"<lambda_0>": "t"})
    for f in ["near", "ret28", "ret5p", "vol20", "volrel", "rng", "vrel"]:
        out["q_" + f] = qtab(f)
    d = g.dropna(subset=["near", "ret28", "rng"]).copy()
    d["near_t"] = d.groupby("coin")["near"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    d["calm"] = d.groupby("coin")["rng"].transform(lambda s: pd.qcut(s.rank(method="first"), 2, labels=False))
    d["up28"] = (d["ret28"] > 0).astype(int)
    out["near_x_up28"] = d.groupby(["up28", "near_t"])["ex"].agg(["mean", "count"])
    out["near_x_calm"] = d.groupby(["calm", "near_t"])["ex"].agg(["mean", "count"])
    out["by_win"] = g.groupby("win")["ex"].agg(["mean", "count"])
    out["by_wd"] = g.assign(wd=g["ts"].dt.weekday).groupby("wd")["ex"].agg(["mean", "count"])
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            dd.append(x.assign(coin=coin, win=w))
    dd = pd.concat(dd)
    bk = dd.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    bk["wd"] = pd.to_datetime(bk.index.get_level_values("day")).weekday
    out["book_by_wd"] = bk.groupby("wd")[["book_return", "coin_return"]].mean()
    out["book_by_win"] = bk.groupby("win")[["book_return", "coin_return"]].agg(["mean"])
    q = bk["book_return"].quantile([0.05, 0.95])
    out["book_tails"] = pd.DataFrame({"low5_mean": [bk.loc[bk.book_return <= q.iloc[0], "book_return"].mean()],
                                      "high5_mean": [bk.loc[bk.book_return >= q.iloc[1], "book_return"].mean()],
                                      "corr_book_coin": [bk["book_return"].corr(bk["coin_return"])],
                                      "beta": [np.polyfit(bk["coin_return"], bk["book_return"], 1)[0]]})
    return out
