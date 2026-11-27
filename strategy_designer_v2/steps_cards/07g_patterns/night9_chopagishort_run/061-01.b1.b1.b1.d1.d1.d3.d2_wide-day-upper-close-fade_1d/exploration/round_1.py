def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            if len(b) < 30: continue
            rng = (b.high - b.low)
            loc = (b.close - b.low) / rng.replace(0, np.nan)
            ret5 = b.close / b.close.shift(5) - 1
            ret1 = b.close / b.close.shift(1) - 1
            rm = rng / rng.rolling(20, min_periods=20).mean()
            fwd = b.close.shift(-H) / b.close - 1
            fwd2 = b.close.shift(-2) / b.close - 1
            ts = pd.to_datetime(b.timestamp)
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                              "loc": loc, "ret5": ret5, "ret1": ret1, "rm": rm,
                              "fwd": fwd, "fwd2": fwd2, "regime": b.regime.astype(str),
                              "alloc": b.postRebalance_current_allocation,
                              "wd": ts.dt.weekday, "day": ts.dt.floor("D"),
                              "year": ts.dt.year})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A.pos % H == 0) & A.fwd.notna()].copy()
    drift = G.groupby("coin").fwd.mean()
    G["unu"] = G.fwd - G.coin.map(drift)
    G["inprof"] = G.regime != "chop"

    def ct(s, days):
        df = pd.DataFrame({"v": s.values, "d": days.values}).dropna()
        n = len(df)
        if n < 5: return (n, np.nan, np.nan)
        m = df.v.mean()
        g = (df.v - m).groupby(df.d).sum()
        k = len(g)
        se = np.sqrt((g ** 2).sum() * k / max(k - 1, 1)) / n
        return (n, m, m / se if se > 0 else np.nan)

    def tab(df, by):
        out = []
        for key, g in df.groupby(by, observed=True):
            n, m, t = ct(g.unu, g.day)
            out.append({"key": str(key), "n": n, "days": g.day.nunique(), "mean_unu": m, "t": t})
        return pd.DataFrame(out)

    G["locq"] = pd.cut(G["loc"], [0, .2, .4, .6, .8, 1.0001], include_lowest=True)
    G["r5s"] = np.sign(G.ret5)
    G["rmq"] = pd.qcut(G.rm, 4, duplicates="drop")
    res = {}
    res["regime counts"] = A.regime.value_counts()
    res["in profile: loc bins"] = tab(G[G.inprof], "locq")
    res["out profile: loc bins"] = tab(G[~G.inprof], "locq")
    res["in profile: loc x ret5 sign"] = tab(G[G.inprof], ["locq", "r5s"])
    res["in profile: rm quartile"] = tab(G[G.inprof], "rmq")
    res["out profile: rm quartile"] = tab(G[~G.inprof], "rmq")
    G["r1q"] = pd.qcut(G.ret1, 5, duplicates="drop")
    res["in profile: ret1 quintile"] = tab(G[G.inprof], "r1q")
    res["out profile: ret1 quintile"] = tab(G[~G.inprof], "r1q")
    G["r5q"] = pd.qcut(G.ret5, 5, duplicates="drop")
    res["in profile: ret5 quintile"] = tab(G[G.inprof], "r5q")
    res["out profile: ret5 quintile"] = tab(G[~G.inprof], "r5q")
    res["all: weekday"] = tab(G, "wd")
    # book daily
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D)
    D["wd"] = pd.to_datetime(D.day).dt.weekday
    bk = D.groupby("day").agg(br=("book_return", "mean"), cr=("coin_return", "mean"))
    res["book by window"] = D.groupby("win").agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    res["book by coin"] = D.groupby("coin").agg(book=("book_return", "mean"), n=("book_return", "count"))
    return res
