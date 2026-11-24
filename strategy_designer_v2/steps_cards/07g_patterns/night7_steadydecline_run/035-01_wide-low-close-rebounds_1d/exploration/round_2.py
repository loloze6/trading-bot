def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            d = pd.DataFrame()
            d["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            d["coin"] = coin; d["win"] = w
            c = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]
            rng = h - l
            d["width"] = rng / rng.shift(1).rolling(14).mean()
            d["clv"] = ((c - l) / rng.replace(0, np.nan))
            d["ret0"] = c / c.shift(1) - 1
            d["sd14"] = d["ret0"].shift(1).rolling(14).std()
            d["z0"] = d["ret0"] / d["sd14"]
            d["r3d"] = c / c.shift(3) - 1
            d["r1"] = c.shift(-1) / c - 1
            for k in [2, 3, 5]:
                d[f"r{k}"] = c.shift(-k) / c - 1
            d["tr60"] = c / c.shift(60) - 1
            v30 = d["ret0"].rolling(30).std()
            d["agit"] = v30.rolling(365, min_periods=120).apply(lambda s: (s <= s[-1]).mean(), raw=True)
            d["pos"] = b["postRebalance_current_allocation"]
            d["idx"] = np.arange(len(b))
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for k in [1, 2, 3, 5]:
        mu = D[D.idx % k == 0].groupby("coin")[f"r{k}"].mean()
        D[f"x{k}"] = D[f"r{k}"] - D["coin"].map(mu)

    def clus_ols(df, ys, xs):
        df = df.dropna(subset=[ys] + xs)
        X = np.column_stack([np.ones(len(df))] + [df[x].values for x in xs])
        y = df[ys].values
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        e = y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        S = pd.DataFrame(X * e[:, None]).groupby(df["day"].values).sum().values
        V = XtXi @ (S.T @ S) @ XtXi
        G = len(S)
        V *= G / (G - 1)
        return pd.DataFrame({"beta": beta, "t": beta / np.sqrt(np.diag(V))}, index=["const"] + xs).assign(n=len(df), days=G)

    def tab(df, keys, col="x1"):
        df = df.dropna(subset=[col] + keys)
        out = []
        for k, g in df.groupby(keys, observed=True):
            n = len(g); m = g[col].mean()
            dd = (g[col] - m).groupby(g["day"]).sum()
            se = np.sqrt((dd ** 2).sum()) / n if n > 1 else np.nan
            out.append({"key": str(k), "n": n, "days": g["day"].nunique(), "mean%": 100 * m, "t": m / se if se else np.nan})
        return pd.DataFrame(out)

    D["lowness"] = 1 - D["clv"]
    D["prod"] = D["width"] * D["lowness"]
    D["neg_z0"] = -D["z0"].clip(upper=0)
    D["wneg"] = D["width"] * D["neg_z0"]
    res = {}
    res["ols x1 ~ width, lowness, prod"] = clus_ols(D, "x1", ["width", "lowness", "prod"])
    res["ols x1 ~ prod + neg_z0"] = clus_ols(D, "x1", ["prod", "neg_z0"])
    res["ols x1 ~ neg_z0 only"] = clus_ols(D, "x1", ["neg_z0"])
    res["ols x1 ~ wneg"] = clus_ols(D, "x1", ["wneg"])
    for k in [2, 3, 5]:
        res[f"ols x{k} ~ prod (grid {k})"] = clus_ols(D[D.idx % k == 0], f"x{k}", ["prod"])
        res[f"ols x{k} ~ neg_z0 (grid {k})"] = clus_ols(D[D.idx % k == 0], f"x{k}", ["neg_z0"])
    D["agq"] = np.where(D.agit > 0.5, "agitated", np.where(D.agit.notna(), "calm", np.nan))
    D["trend"] = pd.cut(D["tr60"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"]).astype(str)
    for prof in ["agitated", "calm"]:
        res[f"ols x1 ~ prod in {prof}"] = clus_ols(D[D.agq == prof], "x1", ["prod"])
    for tr in ["falling", "choppy", "rising"]:
        res[f"ols x1 ~ prod in {tr}"] = clus_ols(D[D.trend == tr], "x1", ["prod"])
    D["zq"] = D.groupby("coin")["z0"].transform(lambda s: pd.qcut(s, 5, labels=False))
    D["cq"] = pd.cut(D["clv"], [-0.01, 0.2, 0.8, 1.01], labels=["nearlow", "middle", "nearhigh"])
    res["z0 quint x close-loc -> next"] = tab(D, ["zq", "cq"])
    res["coin: top prod quintile next"] = tab(D[D.groupby("coin")["prod"].transform(lambda s: s.rank(pct=True)) > 0.8], ["coin"])
    res["year x top prod quintile next"] = tab(D[D.groupby("coin")["prod"].transform(lambda s: s.rank(pct=True)) > 0.8].assign(yr=lambda x: x.day.dt.year), ["yr"])
    return res
