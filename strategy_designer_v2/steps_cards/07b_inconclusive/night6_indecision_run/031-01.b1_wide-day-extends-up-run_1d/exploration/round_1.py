def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; o = b["open"].values; h = b["high"].values; l = b["low"].values
            n = len(b)
            rng = pd.Series(h - l)
            ratio = (rng / rng.rolling(20, min_periods=20).mean()).values
            r5 = pd.Series(c).pct_change(5).values
            flat = np.abs(c - o) / np.where(h - l > 0, h - l, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            for H in (1, 3, 5, 10):
                for i in range(0, n - H, H):
                    rows.append(dict(coin=coin, win=w, H=H, i=i, day=ts.iloc[i].normalize(),
                                     year=ts.iloc[i].year, fwd=c[i + H] / c[i] - 1, ratio=ratio[i],
                                     r5=r5[i], flat=flat[i], fc=b["forecast"].iloc[i],
                                     reg=b["regime"].iloc[i], up=c[i] > o[i]))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "H"])["fwd"].transform("mean")
    d["ex"] = d["fwd"] - d["drift"]
    d = d.dropna(subset=["ratio", "r5", "flat"])

    def slope_t(g, x="ratio"):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 30: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        X = g[x].values - g[x].mean(); y = g["ex"].values
        bta = (X * y).sum() / (X ** 2).sum()
        res = y - y.mean() - bta * X
        s = pd.DataFrame(dict(day=g["day"].values, sc=X * res)).groupby("day")["sc"].sum()
        se = np.sqrt((s ** 2).sum()) / (X ** 2).sum()
        return pd.Series(dict(n=len(g), slope=bta, t=bta / se))

    up = d[d.r5 > 0]; dn = d[d.r5 <= 0]
    out = {}
    out["slope by H, up-run"] = up.groupby("H").apply(slope_t)
    out["slope by H, down-run"] = dn.groupby("H").apply(slope_t)
    out["slope by H, all days"] = d.groupby("H").apply(slope_t)
    u3 = up[up.H == 3]
    out["up H3 by coin"] = u3.groupby("coin").apply(slope_t)
    out["up H3 by year"] = u3.groupby("year").apply(slope_t)
    u3 = u3.copy()
    u3["rq"] = pd.qcut(u3["ratio"], 5, labels=False)
    out["up H3 by ratio quintile"] = u3.groupby("rq").agg(n=("ex", "size"), ratio=("ratio", "mean"), ex=("ex", "mean"),
                                                         sd=("ex", "std"))
    u3["fq"] = pd.qcut(u3["flat"], 3, labels=["flat", "mid", "directional"])
    u3["wide"] = u3["ratio"] > u3["ratio"].median()
    out["up H3 mean ex by flatness x wide"] = u3.groupby(["fq", "wide"])["ex"].agg(["size", "mean", "std"])
    out["up H3 slope by flatness"] = u3.groupby("fq").apply(slope_t)
    out["up H3 slope by close>open"] = u3.groupby("up").apply(slope_t)
    u3["r5q"] = pd.qcut(u3["r5"], 3, labels=["weak", "mid", "strong"])
    out["up H3 slope by run strength"] = u3.groupby("r5q").apply(slope_t)
    d3 = dn[dn.H == 3].copy()
    d3["fq"] = pd.qcut(d3["flat"], 3, labels=["flat", "mid", "directional"])
    out["down H3 slope by flatness"] = d3.groupby("fq").apply(slope_t)
    return out
