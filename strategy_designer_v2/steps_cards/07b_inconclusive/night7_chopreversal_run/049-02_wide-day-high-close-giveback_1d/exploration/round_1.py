def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            h, l, c = b["high"], b["low"], b["close"]
            rng = (h - l)
            base = rng.rolling(30, min_periods=20).mean()
            width = rng / base
            loc = ((c - l) / rng.replace(0, np.nan))
            nxt = c.shift(-1) / c - 1
            r1 = c.pct_change()
            tr60 = c / c.shift(60) - 1
            vol30 = r1.rolling(30, min_periods=20).std()
            volmed = vol30.expanding(min_periods=30).median()
            year = pd.to_datetime(b["timestamp"]).dt.year
            d = pd.DataFrame({"coin": coin, "w": w, "year": year, "fc": b["forecast"],
                              "width": width, "loc": loc, "nxt": nxt, "r1": r1,
                              "tr60": tr60, "agit": vol30 > volmed,
                              "day": pd.to_datetime(b["timestamp"]).dt.floor("D")})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["nxt"].transform("mean")
    D["ex"] = D["nxt"] - mu
    D = D.dropna(subset=["ex", "width", "loc", "fc"])
    D["sig"] = np.sign(D["fc"])
    D["lean"] = D["sig"] * D["ex"]
    # reversal score: -(loc-0.5)*width ; positive => expect rise
    D["score"] = (0.5 - D["loc"]) * D["width"]

    def tstat(x):
        x = x.dropna(); n = len(x)
        return pd.Series({"n": n, "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})

    def slope_t(g, xcol="fc"):
        x = g[xcol]; y = g["ex"]
        if len(g) < 30: return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan})
        xm = x - x.mean(); b_ = (xm * y).sum() / (xm ** 2).sum()
        res = y - y.mean() - b_ * xm
        # day clustered
        s = (xm * res).groupby(g["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / (xm ** 2).sum()
        return pd.Series({"n": len(g), "slope": b_, "t": b_ / se})

    out = {}
    out["all slope"] = slope_t(D)
    out["by coin"] = D.groupby("coin").apply(slope_t)
    out["by year"] = D.groupby("year").apply(slope_t)
    D["wq"] = pd.qcut(D["width"], 5, labels=False)
    D["lq"] = pd.qcut(D["loc"], 5, labels=False)
    # mean next-day excess (%) by width quintile x loc quintile
    out["ex% width x loc"] = (D.pivot_table(index="wq", columns="lq", values="ex", aggfunc="mean") * 100).round(3)
    out["t width x loc"] = D.pivot_table(index="wq", columns="lq", values="ex",
        aggfunc=lambda x: x.mean() / (x.std() / np.sqrt(len(x)))).round(2)
    out["lean by side"] = D.groupby("sig").apply(lambda g: tstat(g["lean"]))
    D["trend"] = np.where(D["tr60"] > 0.1, "rising", np.where(D["tr60"] < -0.1, "falling", np.where(D["tr60"].notna(), "choppy", "na")))
    out["slope by trend"] = D.groupby("trend").apply(slope_t)
    out["slope by agit"] = D.groupby("agit").apply(slope_t)
    out["slope by trend x agit"] = D.groupby(["trend", "agit"]).apply(slope_t)
    # day's own return direction vs close loc: is it really the day's return?
    out["slope on day return"] = D.assign(r1n=-D["r1"]).pipe(lambda g: slope_t(g, "r1n"))
    out["slope on score"] = slope_t(D, "score")
    # top width only
    out["wide days (top fifth) slope on loc-score"] = slope_t(D[D["wq"] == 4], "score")
    return out
