def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            er = (c - c.shift(30)).abs() / c.diff().abs().rolling(30).sum()
            r7 = c / c.shift(7) - 1
            r30 = c / c.shift(30) - 1
            vol = r1.rolling(30).std()
            s7 = r7 / (vol * np.sqrt(7))
            s30 = r30 / (vol * np.sqrt(30))
            f7 = c.shift(-7) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "er": er, "r7": r7, "r30": r30,
                               "s7": s7, "s30": s30, "vol": vol, "f7": f7, "fc": b["forecast"].astype(float),
                               "r1": r1, "f1": r1.shift(-1), "wd": ts.dt.weekday, "yr": ts.dt.year,
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    g = A[A["pos"] % 7 == 0].copy()
    drift = g.groupby("coin")["f7"].mean()
    g["adj"] = g["f7"] - g["coin"].map(drift)
    g = g.dropna(subset=["adj", "s7", "er", "r30"])
    g["volq"] = g.groupby("coin")["vol"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))

    def slope(d, x):
        d = d.dropna(subset=[x, "adj"])
        if len(d) < 20: return pd.Series({"n": len(d)})
        r = stats.linregress(d[x], d["adj"])
        return pd.Series({"n": len(d), "slope": r.slope, "t": r.slope / r.stderr})

    g["chop"] = g["er"] <= 0.3
    g["aligned"] = np.sign(g["r7"]) == np.sign(g["r30"])
    g["grp"] = np.where(g["chop"], "chop_", "trend_") + np.where(g["aligned"], "aligned", "against")
    out["s7 slope by group"] = g.groupby("grp").apply(lambda d: slope(d, "s7"))
    g["erq"] = pd.cut(g["er"], [0, .15, .3, .45, .6, 1.01])
    out["s7 slope by ER bin"] = g.groupby("erq").apply(lambda d: slope(d, "s7"))
    out["s30 slope by ER bin"] = g.groupby("erq").apply(lambda d: slope(d, "s30"))
    out["s7 slope by vol tercile"] = g.groupby("volq").apply(lambda d: slope(d, "s7"))
    out["s30 slope by vol tercile"] = g.groupby("volq").apply(lambda d: slope(d, "s30"))
    out["s7 slope by coin"] = g.groupby("coin").apply(lambda d: slope(d, "s7"))
    out["s30 slope by coin"] = g.groupby("coin").apply(lambda d: slope(d, "s30"))
    act = g[g["fc"] != 0].copy()
    act["sgn"] = np.sign(act["fc"]) * act["adj"]
    act["fq"] = pd.qcut(act["fc"].abs().rank(method="first"), 4, labels=False)
    out["active: signed adj by |fc| quartile"] = act.groupby("fq")["sgn"].agg(["count", "mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    act["side"] = np.where(act["fc"] > 0, "long", "short")
    out["active: signed adj by side"] = act.groupby("side")["sgn"].agg(["count", "mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    # weekday daily
    d1 = A.dropna(subset=["r1"])
    out["weekday daily return"] = d1.groupby("wd")["r1"].agg(["count", "mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    # after large daily moves: next day return by scaled 1d move
    d1 = d1.dropna(subset=["vol", "f1"]).copy()
    d1["z1"] = d1["r1"] / d1["vol"]
    d1["zb"] = pd.cut(d1["z1"], [-99, -2, -1, 0, 1, 2, 99])
    out["next day by z1 bin"] = d1.groupby("zb")["f1"].agg(["count", "mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    if tr:
        T = pd.concat(tr, ignore_index=True)
        T["days"] = T["duration_minutes"] / 1440
        T["db"] = pd.cut(T["days"], [0, 7, 14, 28, 1e9])
        out["trades by duration"] = T.groupby("db")["net_profit_loss_percent"].agg(["count", "mean", "sum"])
        out["trades by side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "sum"])
    # book worst/best days
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, w=w))
    D = pd.concat(dd, ignore_index=True)
    bk = D.groupby(["w", "day"])["book_return"].mean().dropna()
    cr = D.groupby(["w", "day"])["coin_return"].mean().dropna()
    j = pd.DataFrame({"bk": bk, "cr": cr}).dropna()
    j["q"] = pd.qcut(j["bk"].rank(method="first"), 10, labels=False)
    out["book decile vs coin day ret"] = j.groupby("q")[["bk", "cr"]].mean()
    out["book by window"] = j.groupby(level=0)["bk"].agg(["count", "mean", lambda x: x.mean()/x.std()*np.sqrt(365)])
    return out
