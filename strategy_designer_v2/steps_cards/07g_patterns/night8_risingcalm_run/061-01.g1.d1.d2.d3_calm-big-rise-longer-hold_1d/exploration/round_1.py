def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=30).std()
            z = r1 / sd
            hi20 = c.rolling(20, min_periods=20).max()
            prox = c / hi20
            r5p = c / c.shift(5) - 1
            inprof = (df["regime"] != "chop").astype(int)
            ts = pd.to_datetime(df["timestamp"])
            for h in (1, 3, 5, 10):
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, len(df), h)
                sub = pd.DataFrame({"coin": coin, "w": w, "h": h, "z": z.values[idx], "prox": prox.values[idx],
                                    "r5p": (r5p / sd).values[idx],
                                    "fwd": fwd.values[idx], "inprof": inprof.values[idx],
                                    "wd": ts.dt.weekday.values[idx], "day": ts.dt.floor("D").values[idx]})
                rows.append(sub)
    g = pd.concat(rows).dropna(subset=["fwd"])
    drift = g.groupby(["coin", "h"])["fwd"].mean().rename("drift")
    g = g.join(drift, on=["coin", "h"])
    g["unu"] = g["fwd"] - g["drift"]
    def summ(x):
        n = len(x); m = x.mean(); s = x.std()
        return pd.Series({"n": n, "mean%": 100 * m, "t": m / (s / np.sqrt(n)) if n > 2 else np.nan})
    gz = g.dropna(subset=["z"]).copy()
    gz["zbin"] = pd.cut(gz["z"], [-99, -2, -1, 0, 1, 2, 99])
    for h in (1, 5, 10):
        s = gz[gz.h == h]
        out[f"z bins x inprof, h{h}"] = s.groupby(["inprof", "zbin"], observed=True)["unu"].apply(summ).unstack()
    # signed continuation: unu * sign(z), graded by |z|
    gz["cont"] = gz["unu"] * np.sign(gz["z"])
    gz["absz"] = pd.cut(gz["z"].abs(), [0, 1, 2, 99])
    out["continuation by |z| x inprof (all h)"] = gz.groupby(["h", "inprof", "absz"], observed=True)["cont"].apply(summ).unstack()
    # 5-day scaled move
    gz["r5bin"] = pd.cut(gz["r5p"], [-99, -3, -1, 1, 3, 99])
    out["5d scaled past move bins, h5/h10"] = gz[gz.h.isin([5, 10])].groupby(["h", "r5bin"], observed=True)["unu"].apply(summ).unstack()
    out["proximity quartile, h10"] = gz[gz.h == 10].assign(pq=lambda d: pd.qcut(d["prox"], 4, labels=False, duplicates="drop")).groupby("pq")["unu"].apply(summ).unstack()
    out["weekday h1"] = g[g.h == 1].groupby("wd")["unu"].apply(summ).unstack()
    # correlations
    cr = []
    for h in (1, 3, 5, 10):
        s = gz[gz.h == h]
        rho, p = stats.spearmanr(s["z"], s["unu"])
        cr.append({"h": h, "rho": rho, "p": p, "n": len(s)})
    out["spearman z vs fwd"] = pd.DataFrame(cr)
    # book days
    d = []
    for coin in data["days"]:
        for w, df in data["days"][coin].items():
            d.append(df.assign(coin=coin, w=w))
    D = pd.concat(d)
    out["book by window"] = D.groupby("w").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "count"))
    # trades
    T = []
    for coin in data["trades"]:
        for w, df in data["trades"][coin].items():
            T.append(df.assign(coin=coin))
    T = pd.concat(T)
    T["fq"] = pd.qcut(T["entry_forecast"], 4, labels=False, duplicates="drop")
    out["trades by entry forecast quartile"] = T.groupby("fq")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"])
    return out
