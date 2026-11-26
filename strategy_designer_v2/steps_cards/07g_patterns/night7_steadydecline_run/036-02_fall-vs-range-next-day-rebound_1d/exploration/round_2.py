def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            rng = (h - l).shift(1).rolling(30).mean()
            d = pd.DataFrame(index=b.index)
            d["coin"] = coin; d["win"] = w
            d["s"] = (c - c.shift(1)) / rng
            d["sv"] = c.pct_change() / c.pct_change().shift(1).rolling(30).std()
            for k in [1, 2, 3, 5]:
                d["f%d" % k] = c.shift(-k) / c - 1
            d["clv"] = (c - l) / (h - l)
            d["tr60"] = c / c.shift(60) - 1
            d["r5"] = c / c.shift(5) - 1
            d["vol30"] = c.pct_change().rolling(30).std()
            ts = pd.to_datetime(b["timestamp"])
            d["wd"] = ts.dt.weekday.values
            d["year"] = ts.dt.year.values
            d["day"] = ts.dt.floor("D").values
            d["pos"] = np.arange(len(b))
            d["alloc"] = b["postRebalance_current_allocation"].values
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for k in [1, 2, 3, 5]:
        D["x%d" % k] = D["f%d" % k] - D["coin"].map(D.groupby("coin")["f%d" % k].mean())

    def summ(g, col="x1"):
        gg = g.dropna(subset=[col])
        v = gg[col]
        out = {"n": len(v), "days": np.nan, "mean%": np.nan, "t_day": np.nan, "hit": np.nan}
        if len(v) >= 3:
            ds = gg.groupby("day")[col].sum()
            out["days"] = len(ds)
            out["mean%"] = 100 * v.mean()
            out["t_day"] = ds.mean() / (ds.std() / np.sqrt(len(ds))) if len(ds) > 2 and ds.std() > 0 else np.nan
            out["hit"] = (v > 0).mean()
        return pd.Series(out)

    bins = [-np.inf, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, np.inf]
    D["sb"] = pd.cut(D["s"], bins).astype(str)
    out = {}
    out["next1 by move/range bucket"] = D.groupby("sb").apply(summ)
    D["svb"] = pd.cut(D["sv"], [-np.inf, -3, -2, -1, 0, 1, 2, 3, np.inf]).astype(str)
    out["next1 by move/std30 bucket"] = D.groupby("svb").apply(summ)
    res = {}
    for k in [2, 3, 5]:
        g = D[D["pos"] % k == 0]
        tmp = g.groupby("sb").apply(lambda x: summ(x, "x%d" % k))
        res["mean%%_%d" % k] = tmp["mean%"]; res["t_%d" % k] = tmp["t_day"]
    out["fwd k days by bucket (grid)"] = pd.DataFrame(res)
    F = D[D["s"] <= -1].copy()
    F["trend"] = np.where(F["tr60"].isna(), "na", np.where(F["tr60"] > 0.1, "rising", np.where(F["tr60"] < -0.1, "falling", "choppy")))
    out["fall>=1 by trend60"] = F.groupby("trend").apply(summ)
    out["fall>=1 by clv tercile"] = F.groupby(pd.qcut(F["clv"], 3, labels=["low", "mid", "high"])).apply(summ)
    out["fall>=1 by prior5d tercile"] = F.groupby(pd.qcut(F["r5"], 3, labels=["low", "mid", "high"])).apply(summ)
    out["fall>=1 by weekday"] = F.groupby("wd").apply(summ)
    out["fall>=1 by year"] = F.groupby("year").apply(summ)
    out["fall>=1 by coin"] = F.groupby("coin").apply(summ)
    D["vq"] = D.groupby("coin")["vol30"].transform(lambda v: pd.qcut(v, 3, labels=False, duplicates="drop"))
    out["fall>=1 by vol30 tercile"] = D[D["s"] <= -1].groupby("vq").apply(summ)
    out["all days by weekday"] = D.groupby("wd").apply(summ)
    out["all days by clv quintile"] = D.groupby(pd.qcut(D["clv"], 5, labels=False)).apply(summ)
    U = D[D["s"] >= 1]
    out["rise>=1 by clv tercile"] = U.groupby(pd.qcut(U["clv"], 3, labels=["low", "mid", "high"])).apply(summ)
    # book
    bd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["win"] = w; bd.append(t)
    B = pd.concat(bd, ignore_index=True)
    B["wd"] = pd.to_datetime(B["day"]).dt.weekday
    out["book daily by weekday (mean% , n)"] = B.groupby("wd")["book_return"].agg(lambda v: 100 * v.mean()).to_frame("mean%").assign(n=B.groupby("wd")["book_return"].count())
    out["book by window mean%"] = B.groupby("win")[["book_return", "coin_return"]].mean() * 100
    return out
