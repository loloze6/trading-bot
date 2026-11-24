def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; o = b["open"].values; h = b["high"].values; l = b["low"].values
            n = len(b)
            rng = pd.Series(h - l)
            ratio = (rng / rng.rolling(20, min_periods=20).mean()).values
            r5 = pd.Series(c).pct_change(5).values
            ts = pd.to_datetime(b["timestamp"])
            H = 3
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, win=w, day=ts.iloc[i].normalize(), year=ts.iloc[i].year,
                                 fwd=c[i + H] / c[i] - 1, ratio=ratio[i], r5=r5[i],
                                 up=c[i] > o[i], reg=b["regime"].iloc[i]))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby("coin")["fwd"].transform("mean")
    d["ex"] = d["fwd"] - d["drift"]
    d = d.dropna(subset=["ratio", "r5"])

    def mean_t(g):
        s = g.groupby("day")["ex"].agg(["sum", "size"])
        m = g["ex"].mean()
        dev = g.assign(dv=g["ex"] - m).groupby("day")["dv"].sum()
        se = np.sqrt((dev ** 2).sum()) / len(g)
        return pd.Series(dict(n=len(g), days=len(s), mean=m, t=m / se))

    def slope_t(g, x="ratio"):
        if len(g) < 30: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        X = g[x].values - g[x].mean(); y = g["ex"].values
        bta = (X * y).sum() / (X ** 2).sum()
        res = y - y.mean() - bta * X
        s = pd.DataFrame(dict(day=g["day"].values, sc=X * res)).groupby("day")["sc"].sum()
        se = np.sqrt((s ** 2).sum()) / (X ** 2).sum()
        return pd.Series(dict(n=len(g), slope=bta, t=bta / se))

    out = {}
    up = d[d.r5 > 0].copy()
    up["rq"] = pd.qcut(up["ratio"], 5, labels=False)
    out["up: mean ex by ratio quintile, day-clustered t"] = up.groupby("rq").apply(mean_t)
    up["top"] = up["rq"] == 4
    out["up: top quintile by close>open"] = up[up.top].groupby("up").apply(mean_t)
    up["r5q"] = pd.qcut(up["r5"], 3, labels=["weak", "mid", "strong"])
    out["up: top quintile by run strength"] = up[up.top].groupby("r5q").apply(mean_t)
    out["up: top quintile by year"] = up[up.top].groupby("year").apply(mean_t)
    out["up: top quintile by coin"] = up[up.top].groupby("coin").apply(mean_t)
    up["lr"] = np.log(up["ratio"])
    out["up: slope on log ratio"] = slope_t(up, "lr").to_frame().T
    out["up strong runs: slope on ratio"] = slope_t(up[up.r5q == "strong"]).to_frame().T
    dn = d[d.r5 <= 0].copy()
    dn["rq"] = pd.qcut(dn["ratio"], 5, labels=False)
    out["down: mean ex by ratio quintile"] = dn.groupby("rq").apply(mean_t)
    return out
