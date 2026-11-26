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
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "z": z, "r": r,
                "agit": (b["regime"] != "chop").astype(int),
                "fc": b["forecast"].astype(float),
                "n1": c.shift(-1) / c - 1,
                "n2": c.shift(-2) / c - 1,
                "n3": c.shift(-3) / c - 1,
                "ret60": c / c.shift(60) - 1,
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["r"].mean()
    D["mu"] = D["coin"].map(mu)
    D["x1"] = D["n1"] - D["mu"]
    D["x2"] = D["n2"] - 2 * D["mu"]
    D["x3"] = D["n3"] - 3 * D["mu"]

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
    fall = D[D["z"] < 0]
    rise = D[D["z"] > 0].copy()
    rise["s"] = D["z"]
    out = {}
    tab = {}
    tab["agit_fall_x1"] = slope(fall[fall.agit == 1])
    tab["calm_fall_x1"] = slope(fall[fall.agit == 0])
    tab["agit_rise_x1(z)"] = slope(rise[rise.agit == 1])
    tab["agit_fall_x2"] = slope(fall[fall.agit == 1], ycol="x2")
    tab["agit_fall_x3"] = slope(fall[fall.agit == 1], ycol="x3")
    tab["agit_fall_fc_x1"] = slope(fall[(fall.agit == 1) & (fall.fc > 0)].assign(s=lambda d: d.fc))
    out["slopes"] = pd.DataFrame(tab).T
    A = fall[fall.agit == 1].copy()
    out["by_coin"] = A.groupby("coin").apply(slope)
    out["by_win"] = A.groupby("win").apply(slope)
    A["trend"] = np.where(A.ret60 > .1, "rising", np.where(A.ret60 < -.1, "falling", "choppy"))
    out["by_trend"] = A.groupby("trend").apply(slope)
    A["q"] = pd.qcut(A["s"], 5, labels=False)
    out["quint_agit"] = A.groupby("q").agg(n=("x1", "size"), s=("s", "mean"), x1=("x1", "mean"), x2=("x2", "mean"), x3=("x3", "mean"))
    C = fall[fall.agit == 0].copy()
    C["q"] = pd.qcut(C["s"], 5, labels=False)
    out["quint_calm"] = C.groupby("q").agg(n=("x1", "size"), s=("s", "mean"), x1=("x1", "mean"))
    return out
