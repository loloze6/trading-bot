def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr += list(c[idx + H] / c[idx] - 1)
        mu = np.mean(allr)
        allr1 = []
        for w, b in wins.items():
            allr1 += list(b["close"].pct_change().dropna().values)
        mu1 = np.mean(allr1)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            daily.append(pd.DataFrame({"coin": coin, "wd": ts.dt.weekday, "year": ts.dt.year,
                                       "r1x": r1 - mu1, "nxt": r1.shift(-1) - mu1}))
            vol = r1.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "year": ts.dt.year,
                "fc": b["forecast"],
                "r1": r1,
                "absr1v": r1.abs() / vol.shift(1),
                "r1v": r1 / vol.shift(1),
                "rangev": ((b["high"] - b["low"]) / c) / ((b["high"] - b["low"]) / c).rolling(30, min_periods=20).mean().shift(1),
                "volz": b["volume"] / b["volume"].rolling(20, min_periods=15).mean().shift(1),
                "fwd": c.shift(-H) / c - 1 - mu,
                "fwdv": (c.shift(-H) / c - 1 - mu) / (vol * np.sqrt(H)),
            })
            rows.append(df.iloc[np.arange(0, len(df), H)])
    g = pd.concat(rows).dropna(subset=["fwd"])
    D = pd.concat(daily).dropna(subset=["r1x"])
    out = {}
    def qt(d, col, y="fwd", n=5):
        d = d.dropna(subset=[col, y]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), n, labels=False))
        t = d.groupby("q")[y].agg(["mean", "count", "std"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t.round(4)
    def percoin(col, y="fwd"):
        d = g.dropna(subset=[col, y])
        r = d.groupby("coin").apply(lambda x: pd.Series({"n": len(x), "rho": stats.spearmanr(x[col], x[y])[0]}))
        r2 = d.groupby("year").apply(lambda x: stats.spearmanr(x[col], x[y])[0])
        return r.round(3), r2.round(3)
    for col in ["absr1v", "rangev", "volz"]:
        out["fwd5 by quintile " + col] = qt(g, col)
        out["fwdv by quintile " + col] = qt(g, col, "fwdv")
        a, b2 = percoin(col)
        out["rho per coin " + col] = a
        out["rho per year " + col] = b2
    # partial: range effect residual on forecast
    d = g.dropna(subset=["rangev", "fc", "fwd"]).copy()
    X = np.column_stack([np.ones(len(d)), d["fc"] / 10, d.groupby("coin")["rangev"].transform(lambda s: (s - s.mean()) / s.std()),
                         d.groupby("coin")["absr1v"].transform(lambda s: (s - s.mean()) / s.std()).fillna(0)])
    beta, res, *_ = np.linalg.lstsq(X, d["fwd"].values, rcond=None)
    e = d["fwd"].values - X @ beta
    s2 = e.var(ddof=4); cov = s2 * np.linalg.inv(X.T @ X)
    out["ols fwd ~ fc + rangez + absr1z"] = pd.DataFrame({"beta": beta, "t": beta / np.sqrt(np.diag(cov))}, index=["c", "fc10", "rangez", "absr1z"]).round(5)
    # daily coin return by weekday (excess of coin mean)
    t = D.groupby("wd")["r1x"].agg(["mean", "count", "std"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    out["daily excess return by weekday"] = t.round(5)
    out["daily weekday mean per coin (bp)"] = D.pivot_table(index="coin", columns="wd", values="r1x", aggfunc="mean").mul(1e4).round(1)
    out["daily weekday mean per year (bp)"] = D.pivot_table(index="year", columns="wd", values="r1x", aggfunc="mean").mul(1e4).round(1)
    # next-day after large signed day (vol-scaled)
    g2 = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].reset_index(drop=True); r1 = c.pct_change(); v = r1.rolling(30, min_periods=20).std().shift(1)
            g2.append(pd.DataFrame({"coin": coin, "z": r1 / v, "fwd": c.shift(-H) / c - 1}).iloc[np.arange(0, len(c), H)])
    g2 = pd.concat(g2).dropna()
    g2["fwd"] = g2["fwd"] - g2.groupby("coin")["fwd"].transform("mean")
    g2["b"] = pd.cut(g2["z"], [-np.inf, -2, -1, 0, 1, 2, np.inf])
    t = g2.groupby("b")["fwd"].agg(["mean", "count", "std"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    out["fwd5 by signed day z bucket"] = t.round(4)
    return out
