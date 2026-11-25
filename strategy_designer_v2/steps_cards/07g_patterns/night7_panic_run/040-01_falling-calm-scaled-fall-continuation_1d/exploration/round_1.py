def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]),
                "r1": r1, "sd30": sd30,
                "s1": r1 / sd30,
                "s3": (c / c.shift(3) - 1) / sd30,
                "s10": (c / c.shift(10) - 1) / sd30,
                "f1": c.shift(-1) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "inprof": (b["regime"] == "unknown").astype(int),
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "rng": (b["high"] - b["low"]) / c / sd30,
                "clpos": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["wd"] = A["ts"].dt.weekday
    A["year"] = A["ts"].dt.year
    g3 = A[A["pos"] % 3 == 0].copy()
    drift3 = g3.groupby("coin")["f3"].mean()
    g3["u3"] = g3["f3"] - g3["coin"].map(drift3)
    drift1 = A.groupby("coin")["f1"].mean()
    A["u1"] = A["f1"] - A["coin"].map(drift1)

    def summ(x):
        x = x.dropna()
        n = len(x)
        m = x.mean() if n else np.nan
        t = m / (x.std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series({"n": n, "mean%": 100 * m, "t": t})

    out = {}
    g = g3.dropna(subset=["s3", "u3"]).copy()
    g["q"] = pd.qcut(g["s3"], 5, labels=False)
    out["s3 quintile -> u3, all bars"] = g.groupby("q")["u3"].apply(summ).unstack()
    out["s3 quintile -> u3, by in-profile"] = g.groupby(["inprof", "q"])["u3"].apply(summ).unstack()
    g["q10"] = pd.qcut(g["s10"], 5, labels=False)
    out["s10 quintile -> u3"] = g.dropna(subset=["s10"]).groupby("q10")["u3"].apply(summ).unstack()
    a1 = A.dropna(subset=["s1", "u1"]).copy()
    a1["q"] = pd.qcut(a1["s1"], 10, labels=False)
    out["s1 decile -> next day u1"] = a1.groupby("q")["u1"].apply(summ).unstack()
    a1["rq"] = pd.qcut(a1["rng"], 5, labels=False)
    out["range/sd quintile -> u1 signed by day dir"] = a1.assign(
        su=a1["u1"] * np.sign(a1["r1"])).groupby("rq")["su"].apply(summ).unstack()
    a1["cq"] = pd.qcut(a1["clpos"], 5, labels=False)
    out["close-in-range quintile -> u1"] = a1.dropna(subset=["cq"]).groupby("cq")["u1"].apply(summ).unstack()
    out["weekday -> r1"] = A.groupby("wd")["r1"].apply(summ).unstack()
    out["year -> r1"] = A.groupby("year")["r1"].apply(summ).unstack()
    # book
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin, win=w))
    D = pd.concat(D, ignore_index=True)
    bk = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book by window"] = bk.groupby("win")["book_return"].apply(summ).unstack()
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            T.append(t.assign(coin=coin, win=w))
    T = pd.concat(T, ignore_index=True)
    T["fq"] = pd.qcut(T["entry_forecast"].astype(float), 4, labels=False, duplicates="drop")
    out["trades by entry forecast quartile"] = T.groupby("fq")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"])
    T["dd"] = T["duration_minutes"] / 1440
    out["trade duration days"] = T["dd"].describe()
    # in-profile, forecast<0 grid cases: u3 by forecast tercile
    ip = g[(g["fc"] < 0)].copy()
    ip["fq"] = pd.qcut(ip["fc"], 3, labels=False, duplicates="drop")
    out["in-prof short cases: fc tercile -> u3"] = ip.groupby("fq")["u3"].apply(summ).unstack()
    return out
