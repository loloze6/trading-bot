def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); v = b["volume"].astype(float)
            lr = np.log(c).diff()
            f = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"])})
            f["ret28"] = c / c.shift(28) - 1
            f["ret7"] = c / c.shift(7) - 1
            f["ret1"] = c / c.shift(1) - 1
            f["rng5_28"] = np.log(((h - l) / c).rolling(5).mean() / ((h - l) / c).rolling(28).mean())
            f["vol5_28"] = np.log(v.rolling(5).mean() / v.rolling(28).mean())
            f["rv20"] = lr.rolling(20).std()
            f["pos28"] = (c - c.rolling(28).min()) / (c.rolling(28).max() - c.rolling(28).min())
            f["fc"] = b["forecast"].astype(float)
            f["fwd5"] = c.shift(-5) / c - 1
            f["fwd1"] = c.shift(-1) / c - 1
            f["grid"] = (np.arange(len(b)) % 5 == 0)
            f["wd"] = f["ts"].dt.weekday
            rows.append(f)
    A = pd.concat(rows, ignore_index=True)
    A["rv20n"] = np.log(A["rv20"] / A.groupby("coin")["rv20"].transform("median"))
    G = A[A["grid"] & A["fwd5"].notna()].copy()
    G["ex"] = G["fwd5"] - G.groupby("coin")["fwd5"].transform("mean")
    A["ex1"] = A["fwd1"] - A.groupby("coin")["fwd1"].transform("mean")
    out = {}
    def tday(df, col="ex"):
        d = df.groupby("ts")[col].sum() / df.groupby("ts")[col].count()
        d = df.groupby("ts")[col].mean()
        n = len(d)
        return d.mean(), (d.mean() / (d.std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan), n
    def slope(df, x, col="ex"):
        d = df[[x, col, "ts"]].dropna()
        z = (d[x] - d[x].mean()) / d[x].std()
        X = np.column_stack([np.ones(len(d)), z]); y = d[col].values
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((2, 2))
        for _, idx in d.groupby("ts").indices.items():
            s = X[idx].T @ e[idx]; meat += np.outer(s, s)
        se = np.sqrt(np.diag(XtXi @ meat @ XtXi))
        return beta[1], beta[1] / se[1], len(d)
    feats = ["ret28", "ret7", "ret1", "rng5_28", "vol5_28", "rv20n", "pos28", "fc"]
    sl = []
    for x in feats:
        b_, t_, n_ = slope(G, x); sl.append((x, b_, t_, n_))
        sub = G[G["ret28"] < 0]
        b2, t2, n2 = slope(sub, x); sl[-1] = sl[-1] + (b2, t2, n2)
    out["slopes_5d_excess_per_1sd (all | ret28<0)"] = pd.DataFrame(sl, columns=["feat", "b_all", "t_all", "n_all", "b_dec", "t_dec", "n_dec"]).round(5)
    for x in ["ret28", "ret7", "ret1", "rng5_28", "vol5_28", "rv20n", "pos28"]:
        d = G[[x, "ex", "ts"]].dropna().copy()
        d["q"] = pd.qcut(d[x], 5, labels=False)
        r = []
        for q, g in d.groupby("q"):
            m, t, n = tday(g); r.append((q, g[x].mean(), m, t, n))
        out["quint_" + x] = pd.DataFrame(r, columns=["q", "featmean", "ex5", "t", "days"]).round(4)
    r = []
    for wd, g in A.dropna(subset=["ex1"]).groupby("wd"):
        m, t, n = tday(g, "ex1"); r.append((wd, m, t, n))
    out["weekday_next1d_excess"] = pd.DataFrame(r, columns=["wd", "ex1", "t", "days"]).round(5)
    # book
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D)
    bk = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book_by_window"] = bk.groupby(level=0).agg(["mean", "count"]).round(5)
    return out
