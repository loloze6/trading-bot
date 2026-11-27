def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            d = pd.DataFrame(index=b.index)
            d["coin"] = coin; d["win"] = w
            d["pos"] = np.arange(len(b))
            d["r1"] = c.pct_change()
            d["r3"] = c / c.shift(3) - 1
            d["r20"] = c / c.shift(20) - 1
            d["r60"] = c / c.shift(60) - 1
            rng = (b["high"] - b["low"]).astype(float)
            d["clv"] = (c - b["low"].astype(float)) / rng.replace(0, np.nan)
            d["rngs"] = rng / c
            d["vol30"] = d["r1"].rolling(30).std()
            d["f5"] = c.shift(-5) / c - 1
            d["f2"] = c.shift(-2) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            d["wd"] = ts.dt.weekday.values
            d["day"] = ts.dt.floor("D").values
            d["alloc"] = b["postRebalance_current_allocation"].astype(float).values
            rows.append(d)
    df = pd.concat(rows, ignore_index=True)
    grid = df[df.pos % 5 == 0]
    drift5 = grid.groupby("coin")["f5"].mean()
    sd5 = grid.groupby("coin")["f5"].std()
    df["u5"] = df["f5"] - df["coin"].map(drift5)
    df["s5"] = df["u5"] / df["coin"].map(sd5)
    vmed = df.groupby("coin")["vol30"].median()
    df["agit"] = df["vol30"] > df["coin"].map(vmed)
    df["trend"] = np.where(df.r60 > .1, "rising", np.where(df.r60 < -.1, "falling", "choppy"))
    df.loc[df.r60.isna(), "trend"] = "na"
    g = df[(df.pos % 5 == 0) & df.u5.notna()].copy()

    def summ(x, col="u5"):
        x = x.dropna(subset=[col])
        if len(x) < 5:
            return pd.Series({"n": float(len(x)), "days": np.nan, "mean_u5": np.nan, "strength": np.nan, "t_day": np.nan})
        dd = x.groupby("day")[col].sum()
        nd = len(dd)
        t = dd.mean() / (dd.std() / np.sqrt(nd)) if nd > 2 and dd.std() > 0 else np.nan
        return pd.Series({"n": float(len(x)), "days": float(nd), "mean_u5": x[col].mean(),
                          "strength": x["s5"].mean(), "t_day": t})

    out = {}
    def safe(name, f):
        try:
            out[name] = f()
        except Exception as e:
            out[name] = "err: " + str(e)[:80]
    g["r20b"] = pd.cut(g.r20, [-1, -.3, -.2, -.15, -.1, -.05, 0, .05, .1, .2, .3, 10])
    safe("choppy by r20 bin (u5 long side)", lambda: g[g.trend == "choppy"].groupby("r20b", observed=True).apply(summ))
    safe("falling by r20 bin", lambda: g[g.trend == "falling"].groupby("r20b", observed=True).apply(summ))
    safe("rising by r20 bin", lambda: g[g.trend == "rising"].groupby("r20b", observed=True).apply(summ))
    safe("deep fall r20<=-10 by trend x agit", lambda: g[g.r20 <= -.1].groupby(["trend", "agit"]).apply(summ))
    g["clvb"] = pd.cut(g.clv, [0, .2, .4, .6, .8, 1.0001], include_lowest=True)
    safe("choppy x agit x clv", lambda: g[g.trend == "choppy"].groupby(["agit", "clvb"], observed=True).apply(summ))
    g["z1"] = g.r1 / g.vol30
    g["z1b"] = pd.qcut(g.z1, 5)
    safe("trend x scaled 1d move quintile", lambda: g.groupby(["trend", "z1b"], observed=True).apply(summ))
    g["rgb"] = g.groupby("coin")["rngs"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=["narrow", "mid", "wide"]))
    safe("trend x range tercile", lambda: g.groupby(["trend", "rgb"], observed=True).apply(summ))
    safe("by weekday", lambda: g.groupby("wd").apply(summ))
    safe("by window", lambda: g.groupby("win").apply(summ))
    dl = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["coin"] = coin; x["win"] = w; dl.append(x)
    D = pd.concat(dl, ignore_index=True)
    act = D[D.book_return.abs() > 1e-9]
    safe("book active coin-days", lambda: pd.Series({"n": float(len(act)), "mean_book": act.book_return.mean(),
                                              "mean_coin": act.coin_return.mean(),
                                              "corr": act.book_return.corr(act.coin_return)}))
    safe("book by coin", lambda: act.groupby("coin")["book_return"].agg(["count", "mean", "sum"]))
    safe("book by window", lambda: act.groupby("win")["book_return"].agg(["count", "mean", "sum"]))
    return out
