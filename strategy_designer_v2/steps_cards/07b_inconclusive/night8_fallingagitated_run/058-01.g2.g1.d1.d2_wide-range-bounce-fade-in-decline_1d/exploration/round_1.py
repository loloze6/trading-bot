def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    allret = {}
    for coin, wins in data["bars"].items():
        rs = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            rs.append((c.shift(-1) / c - 1).dropna())
        allret[coin] = pd.concat(rs).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float)
            r1 = c / c.shift(1) - 1
            r3 = c / c.shift(3) - 1
            sd30 = r1.rolling(30, min_periods=20).std()
            rr = ((h - l) / c) / sd30
            n1 = c.shift(-1) / c - 1
            n2 = c.shift(-2) / c - 1
            n3 = c.shift(-3) / c - 1
            f = b["forecast"].astype(float)
            d = pd.DataFrame({"coin": coin, "win": w, "year": pd.to_datetime(b["timestamp"]).dt.year,
                              "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                              "f": f, "r1": r1 / sd30, "r3": r3 / sd30, "rr": rr,
                              "u1": -(n1 - allret[coin]), "u2": -(n2 - 2 * allret[coin]),
                              "u3": -(n3 - 3 * allret[coin]), "sd": sd30})
            rows.append(d[(f != 0) & f.notna()])
    X = pd.concat(rows)
    X = X.dropna(subset=["u1"])

    def pooled_t(df, col):
        g = df.dropna(subset=[col]).groupby("day")[col].sum()
        n = df[col].notna().sum()
        m = df[col].mean()
        dev = df.dropna(subset=[col]).assign(dv=lambda z: z[col] - m).groupby("day")["dv"].sum()
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / n if G > 1 else np.nan
        return m, m / se if se else np.nan, n, G

    def summ(groups):
        out = {}
        for k, df in groups:
            m1, t1, n, G = pooled_t(df, "u1")
            m2, t2, _, _ = pooled_t(df, "u2")
            m3, t3, _, _ = pooled_t(df, "u3")
            out[k] = {"n": n, "days": G, "u1": m1, "t1": t1, "u2": m2, "t2": t2, "u3": m3, "t3": t3}
        return pd.DataFrame(out).T

    X["fq"] = pd.qcut(X["f"].abs().rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    X["rrq"] = pd.qcut(X["rr"].rank(method="first"), 4, labels=["r1", "r2", "r3", "r4"])
    X["r1q"] = pd.qcut(X["r1"].rank(method="first"), 4, labels=["a1", "a2", "a3", "a4"])
    X["r3q"] = pd.qcut(X["r3"].rank(method="first"), 3, labels=["deep", "mid", "shallow"])
    res = {
        "all": summ([("all", X)]),
        "by_coin": summ(X.groupby("coin")),
        "by_year": summ(X.groupby("year")),
        "by_window": summ(X.groupby("win")),
        "by_absforecast_q": summ(X.groupby("fq", observed=True)),
        "by_rangeratio_q": summ(X.groupby("rrq", observed=True)),
        "by_upday_size_q": summ(X.groupby("r1q", observed=True)),
        "by_ret3_depth": summ(X.groupby("r3q", observed=True)),
        "spearman_absf_u1": float(stats.spearmanr(X["f"].abs(), X["u1"]).correlation),
        "spearman_r1_u1": float(stats.spearmanr(X["r1"], X["u1"]).correlation),
    }
    return res
