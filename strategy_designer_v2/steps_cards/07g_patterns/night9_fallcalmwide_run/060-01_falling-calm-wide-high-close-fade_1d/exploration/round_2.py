def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            rng = (b["high"] - b["low"]) / c
            width = rng / sd
            loc = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            nxt = c.shift(-1) / c - 1
            nxt2 = c.shift(-2) / c - 1
            ret60 = c / c.shift(60) - 1
            pos = np.arange(len(b))
            df = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                               "r": r, "z": r / sd, "width": width, "loc": loc, "nxt": nxt, "nxt2": nxt2,
                               "ret60": ret60, "sd_rank": sd.rolling(180, min_periods=60).rank(pct=True),
                               "g2": (pos % 2 == 0)})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["day"] = d["ts"].dt.floor("D")
    d["unx"] = d["nxt"] - d["coin"].map(d.groupby("coin")["nxt"].mean())
    g2 = d[d["g2"]]
    d["unx2"] = d["nxt2"] - d["coin"].map(g2.groupby("coin")["nxt2"].mean())
    d = d.dropna(subset=["unx", "z", "width", "loc", "sd_rank", "ret60"])
    d["ag"] = np.where(d["sd_rank"] > 0.5, "agit", "calm")
    d["tr"] = pd.cut(d["ret60"], [-10, -0.1, 0.1, 100], labels=["falling", "choppy", "rising"])

    def stat(g, col="unx"):
        g = g.dropna(subset=[col])
        if len(g) < 3: return pd.Series({"n": len(g), "days": np.nan, "mean%": np.nan, "t": np.nan})
        dev = g[col] - g[col].mean()
        sdv = dev.groupby(g["day"]).sum()
        se = np.sqrt((sdv ** 2).sum()) / len(g)
        return pd.Series({"n": len(g), "days": len(sdv), "mean%": 100 * g[col].mean(), "t": g[col].mean() / se})

    def slope(g, x, col="unx"):
        g = g.dropna(subset=[col, x])
        X = g[x] - g[x].mean(); y = g[col]
        b = (X * y).sum() / (X ** 2).sum()
        e = y - y.mean() - b * X
        s = (X * e).groupby(g["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / (X ** 2).sum()
        return pd.Series({"n": len(g), "slope%": 100 * b, "t": b / se})

    out = {}
    up = d[d["z"] > 0].copy()
    up["zq"] = pd.qcut(up["z"], 4, labels=["q1", "q2", "q3", "q4"])
    out["up days: agit x trend x size"] = up.groupby(["ag", "tr", "zq"], observed=True).apply(stat).round(3)
    out["up days agit: slope unx on z, by trend"] = up[up["ag"] == "agit"].groupby("tr", observed=True).apply(slope, x="z").round(3)
    out["up days agit: by window"] = up[up["ag"] == "agit"].groupby("win").apply(stat).round(3)
    out["up days agit: 2-day, grid"] = up[(up["ag"] == "agit") & up["g2"]].groupby("tr", observed=True).apply(stat, col="unx2").round(3)
    hc = d[d["loc"] >= 0.75].copy()
    hc["wq"] = pd.qcut(hc["width"], 4, labels=["q1", "q2", "q3", "q4"])
    out["high close: agit x trend x width"] = hc.groupby(["ag", "tr", "wq"], observed=True).apply(stat).round(3)
    out["high close: slope unx on width, by ag"] = hc.groupby("ag").apply(slope, x="width").round(3)
    lc = d[d["loc"] <= 0.25].copy()
    out["low close: slope unx on width, by ag x trend"] = lc.groupby(["ag", "tr"], observed=True).apply(slope, x="width").round(3)
    return out
