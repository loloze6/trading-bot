def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "pos": np.arange(len(b)),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "z": z, "r": r,
                "agit": (b["regime"] != "chop").astype(int),
                "fc": b["forecast"].astype(float),
                "n1": c.shift(-1) / c - 1,
                "n3": c.shift(-3) / c - 1,
                "ret60": c / c.shift(60) - 1,
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["r"].mean()
    D["mu"] = D["coin"].map(mu)
    D["x1"] = D["n1"] - D["mu"]
    D["x3"] = D["n3"] - 3 * D["mu"]
    D["trend"] = np.where(D.ret60 > .1, "rising", np.where(D.ret60 < -.1, "falling", "choppy"))

    def slope(df, xcol="s", ycol="x1"):
        df = df[[xcol, ycol, "day"]].dropna()
        n = len(df)
        if n < 30:
            return pd.Series({"n": n, "slope": np.nan, "t": np.nan, "days": np.nan})
        x = df[xcol].values; y = df[ycol].values
        X = np.column_stack([np.ones(n), x])
        XtX = np.linalg.inv(X.T @ X)
        b = XtX @ X.T @ y
        e = y - X @ b
        g = pd.DataFrame(X * e[:, None]).groupby(df["day"].values).sum().values
        G = len(g)
        V = XtX @ (g.T @ g) @ XtX * G / (G - 1)
        return pd.Series({"n": n, "slope": b[1], "t": b[1] / np.sqrt(V[1, 1]), "days": G})

    D["s"] = -D["z"]
    F = D[D.z < 0]
    out = {}
    tab = {}
    for ag in [1, 0]:
        for tr in ["falling", "choppy", "rising"]:
            sub = F[(F.agit == ag) & (F.trend == tr)]
            tab[f"{'agit' if ag else 'calm'}_{tr}_x1"] = slope(sub)
    fa = F[(F.agit == 1) & (F.trend == "falling")]
    tab["agit_falling_x3_grid3"] = slope(fa[fa.pos % 3 == 0], ycol="x3")
    tab["agit_all_x3_grid3"] = slope(F[(F.agit == 1) & (F.pos % 3 == 0)], ycol="x3")
    tab["agit_falling_fc_x1"] = slope(fa[fa.fc > 0].assign(s=lambda d: d.fc))
    R = D[(D.z > 0) & (D.agit == 1) & (D.trend == "falling")].copy()
    R["s"] = R["z"]
    tab["agit_falling_RISE_x1(z)"] = slope(R)
    out["slopes"] = pd.DataFrame(tab).T
    out["agit_falling_by_coin"] = fa.groupby("coin").apply(slope)
    out["agit_falling_by_win"] = fa.groupby("win").apply(slope)
    fa = fa.copy()
    fa["q"] = pd.qcut(fa["s"], 3, labels=False)
    out["agit_falling_terciles"] = fa.groupby("q").agg(n=("x1", "size"), s=("s", "mean"), x1=("x1", "mean"))
    return out
