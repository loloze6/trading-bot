def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            d = pd.DataFrame()
            d["ts"] = pd.to_datetime(b["timestamp"])
            d["coin"] = coin; d["w"] = w
            h, l, c, o = b["high"], b["low"], b["close"], b["open"]
            rng = (h - l)
            d["clv"] = ((c - l) / rng.replace(0, np.nan))
            d["width"] = rng / rng.rolling(20, min_periods=10).mean()
            d["body"] = (c - o) / rng.replace(0, np.nan)
            d["r0"] = c.pct_change()
            d["r1"] = c.shift(-1) / c - 1
            d["r2"] = c.shift(-2) / c.shift(-1) - 1
            d["r3"] = c.shift(-3) / c.shift(-2) - 1
            d["ret5"] = c / c.shift(5) - 1
            d["ret60"] = c / c.shift(60) - 1
            d["vol30"] = d["r0"].rolling(30, min_periods=20).std()
            d["fc"] = b["forecast"]
            d["alloc"] = b["postRebalance_current_allocation"]
            d["pos_gain"] = d["alloc"] * d["r1"]
            d["pos"] = np.arange(len(d))
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["r0"].mean()
    for k in ["r1", "r2", "r3"]:
        D["x" + k[1]] = D[k] - D["coin"].map(drift)
    D["vrank"] = D.groupby("coin")["vol30"].rank(pct=True)
    D["day"] = D["ts"].dt.floor("D")
    D["wd"] = D["ts"].dt.dayofweek
    D["year"] = D["ts"].dt.year

    def summ(g, col="x1"):
        s = g[col].dropna()
        n = len(s)
        return pd.Series({"n": n, "mean%": 100 * s.mean(),
                          "t": s.mean() / (s.std() / np.sqrt(n)) if n > 2 else np.nan})

    def ct(df, col, xcol):
        # day-clustered slope t of col on xcol
        z = df[[col, xcol, "day"]].dropna()
        x = z[xcol] - z[xcol].mean(); y = z[col]
        beta = (x * (y - y.mean())).sum() / (x ** 2).sum()
        e = y - y.mean() - beta * x
        s = (x * e).groupby(z["day"]).sum()
        G = len(s)
        se = np.sqrt((s ** 2).sum() * G / (G - 1)) / (x ** 2).sum()
        return pd.Series({"n": len(z), "days": G, "slope": beta, "t": beta / se})

    out = {}
    D["clvq"] = pd.qcut(D["clv"], 5, labels=False)
    D["widq"] = pd.qcut(D["width"], 3, labels=False)
    out["clv quintile -> next day x1"] = D.groupby("clvq").apply(summ)
    out["clv quintile -> day2 x2"] = D.groupby("clvq").apply(lambda g: summ(g, "x2"))
    out["clv quintile -> day3 x3"] = D.groupby("clvq").apply(lambda g: summ(g, "x3"))
    out["width tercile x clv low/high"] = D.assign(lowc=(D["clv"] < 0.5).astype(int)).groupby(["widq", "lowc"]).apply(summ)
    D["r0q"] = pd.qcut(D["r0"], 5, labels=False)
    out["own-day return quintile -> x1"] = D.groupby("r0q").apply(summ)
    D["r5q"] = pd.qcut(D["ret5"], 5, labels=False)
    out["5d return quintile -> x1"] = D.groupby("r5q").apply(summ)
    D["bodyq"] = pd.qcut(D["body"], 5, labels=False)
    out["body quintile -> x1"] = D.groupby("bodyq").apply(summ)
    D["sig"] = 0.5 - D["clv"]
    D["trend"] = pd.cut(D["ret60"], [-np.inf, -0.1, 0.1, np.inf], labels=["fall", "chop", "rise"])
    D["agit"] = np.where(D["vrank"] > 0.5, "agit", "calm")
    D.loc[D["vrank"].isna(), "agit"] = np.nan
    out["clv-signal slope by trend"] = D.groupby("trend").apply(lambda g: ct(g, "x1", "sig"))
    out["clv-signal slope by agitation"] = D.groupby("agit").apply(lambda g: ct(g, "x1", "sig"))
    out["clv-signal slope by width tercile"] = D.groupby("widq").apply(lambda g: ct(g, "x1", "sig"))
    out["clv-signal slope by coin"] = D.groupby("coin").apply(lambda g: ct(g, "x1", "sig"))
    out["clv-signal slope by year"] = D.groupby("year").apply(lambda g: ct(g, "x1", "sig"))
    out["forecast slope all"] = ct(D, "x1", "fc")
    out["mean x1 by weekday"] = D.groupby("wd").apply(summ)
    out["clv-signal slope by weekday"] = D.groupby("wd").apply(lambda g: ct(g, "x1", "sig"))
    # book
    bk = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["coin"] = coin; x["w"] = w; bk.append(x)
    B = pd.concat(bk)
    B["day"] = pd.to_datetime(B["day"])
    bd = B.groupby("day")[["book_return", "coin_return"]].mean().dropna()
    bd["wd"] = bd.index.dayofweek
    out["book by weekday"] = bd.groupby("wd")["book_return"].agg(["count", "mean", "std"]).assign(t=lambda z: z["mean"] / (z["std"] / np.sqrt(z["count"])))
    q = bd["book_return"].quantile([0.05, 0.95])
    out["coin ret on book worst5%/best5% days"] = pd.Series({
        "coin mean worst": bd.loc[bd["book_return"] <= q.iloc[0], "coin_return"].mean(),
        "coin mean best": bd.loc[bd["book_return"] >= q.iloc[1], "coin_return"].mean(),
        "coin mean all": bd["coin_return"].mean(),
        "corr book-coin": bd["book_return"].corr(bd["coin_return"])})
    D["longside"] = np.sign(D["alloc"])
    out["position gain by side"] = D.groupby("longside")["pos_gain"].agg(["count", "mean", "sum"])
    return out
