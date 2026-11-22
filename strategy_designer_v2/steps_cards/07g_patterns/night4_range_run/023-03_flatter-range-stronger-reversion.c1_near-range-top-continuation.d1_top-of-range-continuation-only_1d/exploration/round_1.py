def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            hi = c.rolling(30).max(); lo = c.rolling(30).min()
            pos = (c - lo) / (hi - lo)
            r30 = c / c.shift(30) - 1
            lr = np.log(c).diff()
            vol30 = lr.rolling(30).std()
            trend = (np.log(c / c.shift(30))) / (vol30 * np.sqrt(30))
            r1 = c.pct_change()
            r5 = c / c.shift(5) - 1
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            for i in range(0, n, H):
                if i + H < n:
                    rows.append(dict(coin=coin, w=w, pos=pos[i], trend=trend[i], r30=r30[i],
                                     vol=vol30[i], r1=r1[i], r5=r5[i], fwd=fwd[i],
                                     fc=b["forecast"].iloc[i], dow=ts[i].dayofweek))
            d = pd.DataFrame(dict(coin=coin, w=w, r1=r1, fwd1=fwd1, vol=vol30, pos=pos,
                                  trend=trend, dow=ts.dt.dayofweek, yr=ts.dt.year,
                                  alloc=b["postRebalance_current_allocation"]))
            daily.append(d)
    g = pd.DataFrame(rows)
    g["drift"] = g.groupby("coin")["fwd"].transform("mean")
    g["ex"] = g["fwd"] - g["drift"]
    g = g.dropna(subset=["pos", "ex"])
    out = {}
    def summ(df, key):
        a = df.groupby(key)["ex"].agg(["count", "mean", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        return a.round(4)
    g["posq"] = pd.cut(g["pos"], [-0.01, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.01])
    out["ex10 by range pos"] = summ(g, "posq")
    g["trq"] = pd.qcut(g["trend"], 3, labels=["down", "flat", "up"])
    g["posh"] = pd.cut(g["pos"], [-0.01, .2, .8, 1.01], labels=["bottom", "mid", "top"])
    out["ex10 by trend x pos"] = summ(g, ["trq", "posh"])
    g["volq"] = g.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["ex10 by vol tercile"] = summ(g, "volq")
    out["ex10 by vol x pos"] = summ(g, ["volq", "posh"])
    g["r30q"] = g.groupby("coin")["r30"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["ex10 by 30d ret quintile"] = summ(g, "r30q")
    g["r5q"] = g.groupby("coin")["r5"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["ex10 by 5d ret quintile"] = summ(g, "r5q")
    out["ex10 by coin x pos"] = summ(g, ["coin", "posh"])
    D = pd.concat(daily, ignore_index=True).dropna(subset=["r1", "fwd1"])
    D["z"] = D["r1"] / D["vol"].shift(0)
    D["zq"] = pd.cut(D["z"], [-99, -2, -1, 0, 1, 2, 99])
    a = D.groupby("zq")["fwd1"].agg(["count", "mean", "std"]); a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["next day ret by today z-move"] = a.round(4)
    a = D.groupby("dow")["fwd1"].agg(["count", "mean", "std"]); a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["next day ret by dow of decision bar"] = a.round(4)
    # book
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; bk.append(d)
    B = pd.concat(bk, ignore_index=True).dropna(subset=["book_return"])
    B["day"] = pd.to_datetime(B["day"])
    B["yr"] = B["day"].dt.year
    by = B.groupby("yr")[["book_return", "coin_return"]].mean()
    by["n"] = B.groupby("yr").size()
    out["book vs coin by year (mean daily)"] = by.round(5)
    pc = B.groupby("coin")[["book_return", "coin_return"]].agg(["mean", "std"])
    out["book by coin"] = pc.round(5)
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): t = t.copy(); t["coin"] = coin; tr.append(t)
    T = pd.concat(tr, ignore_index=True)
    T["fq"] = pd.qcut(T["entry_forecast"], 4, duplicates="drop")
    a = T.groupby("fq")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades by entry forecast"] = a.round(3)
    T["dur_d"] = T["duration_minutes"] / 1440
    T["durq"] = pd.cut(T["dur_d"], [0, 10.5, 20.5, 40.5, 1000])
    out["trades by duration"] = T.groupby("durq")["net_profit_loss_percent"].agg(["count", "mean", "median"]).round(3)
    return out
