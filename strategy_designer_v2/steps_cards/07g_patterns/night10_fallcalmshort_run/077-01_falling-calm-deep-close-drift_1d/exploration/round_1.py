def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True).copy()
            c = df["close"]; h = df["high"]; l = df["low"]; o = df["open"]; v = df["volume"]
            r1 = c.pct_change()
            feat = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(df["timestamp"]),
                "inprof": (df["regime"] == "unknown").astype(int),
                "ret1": r1,
                "ret3p": c / c.shift(3) - 1,
                "ret5p": c / c.shift(5) - 1,
                "ret10p": c / c.shift(10) - 1,
                "clv": ((c - l) / (h - l)).where(h > l),
                "rng_vol": ((h - l) / c) / r1.rolling(20).std(),
                "body_vol": ((c - o) / o) / r1.rolling(20).std(),
                "volratio": v / v.rolling(20).mean(),
                "depth": ((c - h.rolling(20).max()) / h.rolling(20).max()) / r1.rolling(20).std(),
                "uplow": ((c - l.rolling(20).min()) / l.rolling(20).min()) / r1.rolling(20).std(),
                "vol20": r1.rolling(20).std(),
                "fc": df["forecast"],
            })
            for hz in (1, 3, 5, 10):
                feat[f"f{hz}"] = c.shift(-hz) / c - 1
            feat["pos"] = np.arange(len(df))
            rows.append(feat)
    A = pd.concat(rows, ignore_index=True)
    A["day"] = A["ts"].dt.floor("D")
    A["wd"] = A["ts"].dt.weekday
    A["year"] = A["ts"].dt.year
    out = {}
    def grid(hz):
        G = A[A["pos"] % hz == 0].copy()
        mu = G.groupby("coin")[f"f{hz}"].mean()
        G["ex"] = G[f"f{hz}"] - G["coin"].map(mu)
        return G
    def clust_t(G, x, y="ex"):
        d = G[[x, y, "day"]].dropna()
        if len(d) < 30: return np.nan, np.nan, len(d)
        X = d[x] - d[x].mean(); b = (X * d[y]).sum() / (X**2).sum()
        e = d[y] - d[y].mean() - b * X
        s = (X * e).groupby(d["day"]).sum()
        g = len(s); se = np.sqrt((s**2).sum() * g / (g - 1)) / (X**2).sum()
        return b, b / se, len(d)
    feats = ["ret1", "ret3p", "ret5p", "ret10p", "clv", "rng_vol", "body_vol", "volratio", "depth", "uplow", "vol20"]
    res = []
    for hz in (1, 3, 5, 10):
        G = grid(hz); P = G[G["inprof"] == 1]
        for f in feats:
            b, t, n = clust_t(P, f)
            res.append({"hz": hz, "feat": f, "slope": b, "t": t, "n": n})
    out["slopes_in_profile"] = pd.DataFrame(res).pivot(index="feat", columns="hz", values="t").round(2)
    G3 = grid(3); P3 = G3[G3["inprof"] == 1].copy()
    out["n_inprof_grid3"] = len(P3)
    out["inprof_mean_ex3"] = float(P3["ex"].mean())
    out["inprof_mean_f3"] = float(P3["f3"].mean())
    tab = {}
    for f in ["ret1", "ret5p", "ret10p", "clv", "rng_vol", "volratio", "depth", "uplow"]:
        q = pd.qcut(P3[f], 5, labels=False, duplicates="drop")
        tab[f] = P3.groupby(q)["ex"].mean() * 100
    out["quintile_ex3_pct"] = pd.DataFrame(tab).round(3)
    out["wd_ex3"] = P3.groupby("wd")["ex"].agg(["mean", "count"]).round(4)
    out["year_inprof_ex3"] = P3.groupby("year")["ex"].agg(["mean", "count"]).round(4)
    out["coin_inprof_ex3"] = P3.groupby("coin")["ex"].agg(["mean", "count"]).round(4)
    # in-profile vs out comparison of f3
    out["prof_vs_out_f3"] = G3.groupby("inprof")["f3"].agg(["mean", "std", "count"]).round(4)
    # book: daily returns
    dd = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            x = df.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    D = pd.concat(dd, ignore_index=True)
    out["book_by_window"] = D.groupby("win")["book_return"].agg(["mean", "count"]).round(5)
    return out
