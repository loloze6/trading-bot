def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            rng = (h - l).shift(1).rolling(30).mean()
            d = pd.DataFrame({"coin": coin, "win": w})
            d["s"] = (c - c.shift(1)) / rng
            d["r1"] = c.pct_change()
            for k in [1, 2, 3, 5]:
                d["f%d" % k] = c.shift(-k) / c - 1
            d["clv"] = (c - l) / (h - l)
            d["tr60"] = c / c.shift(60) - 1
            d["r5"] = c / c.shift(5) - 1
            d["vol30"] = c.pct_change().rolling(30).std()
            d["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            d["year"] = pd.to_datetime(b["timestamp"]).dt.year
            d["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            d["pos"] = np.arange(len(b))
            d["alloc"] = b["postRebalance_current_allocation"]
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["f1"].mean()
    for k in [1, 2, 3, 5]:
        D["x%d" % k] = D["f%d" % k] - D["coin"].map(D.groupby("coin")["f%d" % k].mean())

    def summ(g, col="x1"):
        v = g[col].dropna()
        if len(v) < 3:
            return pd.Series({"n": len(v)})
        ds = g.dropna(subset=[col]).groupby("day")[col].sum()
        t_day = ds.mean() / (ds.std() / np.sqrt(len(ds))) if len(ds) > 2 else np.nan
        return pd.Series({"n": len(v), "days": len(ds), "mean%": 100 * v.mean(), "t_day": t_day,
                          "hit": (v > 0).mean()})

    bins = [-np.inf, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, np.inf]
    D["sb"] = pd.cut(D["s"], bins).astype(str)
    out = {}
    out["next1 by signed move/range"] = D.groupby("sb").apply(summ)
    # multi-horizon after falls, non-overlapping grid positions
    res = {}
    for k in [2, 3, 5]:
        g = D[D["pos"] % k == 0]
        res[k] = g.groupby("sb").apply(lambda x: summ(x, "x%d" % k))["mean%"]
    out["fwd k days by move bucket (grid), mean%"] = pd.DataFrame(res)
    F = D[D["s"] <= -1].copy()
    out["fall>=1 by clv tercile"] = F.groupby(pd.qcut(F["clv"], 3, labels=["lowclose", "mid", "highclose"])).apply(summ)
    F["trend"] = np.where(F["tr60"] > 0.1, "rising", np.where(F["tr60"] < -0.1, "falling", np.where(F["tr60"].isna(), "na", "choppy")))
    out["fall>=1 by trend60"] = F.groupby("trend").apply(summ)
    out["fall>=1 by prior 5d return tercile"] = F.groupby(pd.qcut(F["r5"], 3, labels=["low", "mid", "high"])).apply(summ)
    out["fall>=1 by weekday"] = F.groupby("wd").apply(summ)
    out["fall>=1 by year"] = F.groupby("year").apply(summ)
    out["fall>=1 by coin"] = F.groupby("coin").apply(summ)
    out["fall>=1 by window"] = F.groupby("win").apply(summ)
    D["vq"] = D.groupby("coin")["vol30"].transform(lambda v: pd.qcut(v, 3, labels=False, duplicates="drop"))
    out["fall>=1 by vol30 tercile(coin)"] = D[D["s"] <= -1].groupby("vq").apply(summ)
    out["all days by weekday"] = D.groupby("wd").apply(summ)
    U = D[D["s"] >= 1]
    out["rise>=1 by clv tercile"] = U.groupby(pd.qcut(U["clv"], 3, labels=["low", "mid", "high"])).apply(summ)
    out["all days clv tercile"] = D.groupby(pd.qcut(D["clv"], 5, labels=False)).apply(summ)
    return out
