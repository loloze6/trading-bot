def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # Weekday robustness: per coin, per year, cross-coin averaged per day
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            dt = pd.to_datetime(d["day"]); d["wd"] = dt.dt.weekday; d["yr"] = dt.dt.year
            d["past7"] = d["close"] / d["close"].shift(7) - 1
            d["vol20"] = d["coin_return"].rolling(20).std()
            dl.append(d)
    D = pd.concat(dl, ignore_index=True).dropna(subset=["coin_return"])
    D["sat"] = (D["wd"] == 5)
    def tt(s):
        return pd.Series({"mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))), "n": len(s)})
    sat = D[D["sat"]]; oth = D[~D["sat"]]
    out["sat daily return per coin"] = sat.groupby("coin")["coin_return"].apply(tt).unstack()
    out["sat daily return per year"] = sat.groupby("yr")["coin_return"].apply(tt).unstack()
    # cross-coin mean per day (removes inflation from correlated coins)
    X = D.groupby(["win", "day"]).agg(r=("coin_return", "mean"), wd=("wd", "first")).reset_index()
    wt = X.groupby("wd")["r"].apply(tt).unstack()
    out["weekday, coin-averaged day return"] = wt
    # Saturday excess graded by vol20 and by past7
    s = sat.dropna(subset=["vol20", "past7"]).copy()
    s["vq"] = s.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x.rank(method="first"), 4, labels=False))
    out["sat by vol20 quartile"] = s.groupby("vq")["coin_return"].apply(tt).unstack()
    s["pq"] = s.groupby("coin")["past7"].transform(lambda x: pd.qcut(x.rank(method="first"), 4, labels=False))
    out["sat by past7 quartile"] = s.groupby("pq")["coin_return"].apply(tt).unstack()
    out["sat minus other days welch"] = str(stats.ttest_ind(sat["coin_return"], oth["coin_return"], equal_var=False))
    # Trend-regime top-of-range continuation: per coin and per year, 5-day grid
    H = 5; rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); mx = b["high"].rolling(30).max(); mn = b["low"].rolling(30).min()
            rng = mx - mn; ratio = (c - c.shift(29)).abs() / rng; rp = (c - mn) / rng
            fwd = c.shift(-H) / c - 1; idx = np.arange(0, len(b), H)
            rows.append(pd.DataFrame({"coin": coin, "yr": pd.to_datetime(b["timestamp"]).dt.year.values[idx],
                                      "ratio": ratio.values[idx], "rp": rp.values[idx], "fwd": fwd.values[idx]}))
    g = pd.concat(rows, ignore_index=True).dropna()
    cm = g.groupby("coin")["fwd"].agg(["mean", "std"])
    g["ex"] = (g["fwd"] - g["coin"].map(cm["mean"])) / g["coin"].map(cm["std"])
    tr = g[g["ratio"] > 0.33].copy()
    tr["cent"] = tr["rp"] - 0.5
    pc = {}
    for k, d in tr.groupby("coin"):
        r, p = stats.spearmanr(d["cent"], d["ex"]); pc[k] = f"rho={r:.3f} p={p:.3f} n={len(d)}"
    out["trend rp->ex per coin"] = pd.Series(pc)
    py = {}
    for k, d in tr.groupby("yr"):
        r, p = stats.spearmanr(d["cent"], d["ex"]); py[k] = f"rho={r:.3f} p={p:.3f} n={len(d)}"
    out["trend rp->ex per year"] = pd.Series(py)
    return out
