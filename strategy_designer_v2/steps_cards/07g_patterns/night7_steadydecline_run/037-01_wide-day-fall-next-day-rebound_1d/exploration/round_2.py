def explore(data):
    import numpy as np, pandas as pd
    def q3(s, labels):
        r = s.rank(method="first", pct=True)
        return pd.cut(r, [0, 1/3, 2/3, 1.0], labels=labels, include_lowest=True)
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; r1 = c / c.shift(1) - 1
            rng = (b["high"] - b["low"]) / c
            rm = rng / rng.shift(1).rolling(14, min_periods=10).mean()
            cl = (b["close"] - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "win": w, "r1": r1, "rm": rm, "cl": cl,
                              "r5": c / c.shift(5) - 1, "tr60": c / c.shift(60) - 1,
                              "vol20": r1.rolling(20).std(),
                              "nx1": c.shift(-1) / c - 1, "nx3": c.shift(-3) / c - 1,
                              "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                              "wd": ts.dt.weekday, "yr": ts.dt.year, "pos": np.arange(len(b))})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["nx1"].mean(); D["ex1"] = D["nx1"] - D["coin"].map(mu)
    mu3 = D[D.pos % 3 == 0].groupby("coin")["nx3"].mean(); D["ex3"] = D["nx3"] - D["coin"].map(mu3)
    def summ(g, col="ex1"):
        x = g[col].dropna(); n = len(x)
        return pd.Series({"n": n, "mean%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    D["volQ"] = D.groupby("coin")["vol20"].transform(lambda s: q3(s, ["lowvol", "midvol", "highvol"]))
    D["trend"] = pd.cut(D["tr60"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    dn = D[D.r1 < 0].copy()
    dn["fallQ"] = dn.groupby("coin")["r1"].transform(lambda s: q3(-s, ["small", "mid", "large"]))
    dn["rmQ"] = dn.groupby("coin")["rm"].transform(lambda s: q3(s, ["narrow", "mid", "wide"]))
    dn["clQ"] = pd.cut(dn["cl"], [-0.01, 0.2, 0.5, 1.01], labels=["lowclose", "midclose", "highclose"])
    dn["r5Q"] = dn.groupby("coin")["r5"].transform(lambda s: q3(s, ["5d_down", "5d_mid", "5d_up"]))
    up = D[D.r1 > 0].copy()
    up["riseQ"] = up.groupby("coin")["r1"].transform(lambda s: q3(s, ["small", "mid", "large"]))
    up["rmQ"] = up.groupby("coin")["rm"].transform(lambda s: q3(s, ["narrow", "mid", "wide"]))
    out = {}
    def safe(name, f):
        try: out[name] = f()
        except Exception as e: out[name] = "err: " + str(e)[:80]
    safe("down fall x range", lambda: dn.groupby(["fallQ", "rmQ"]).apply(summ).round(3))
    safe("down fall x closeloc", lambda: dn.groupby(["fallQ", "clQ"]).apply(summ).round(3))
    safe("down 3d ex grid fall x range", lambda: dn[dn.pos % 3 == 0].groupby(["fallQ", "rmQ"]).apply(lambda g: summ(g, "ex3")).round(3))
    safe("up rise x range", lambda: up.groupby(["riseQ", "rmQ"]).apply(summ).round(3))
    safe("down fall x vol", lambda: dn.groupby(["fallQ", "volQ"]).apply(summ).round(3))
    safe("down large fall x trend", lambda: dn[dn.fallQ == "large"].groupby("trend").apply(summ).round(3))
    safe("down large fall x 5d", lambda: dn[dn.fallQ == "large"].groupby("r5Q").apply(summ).round(3))
    safe("all by weekday", lambda: D.groupby("wd").apply(summ).round(3))
    safe("fc>0 by weekday", lambda: D[D.fc > 0].groupby("wd").apply(summ).round(3))
    safe("fc>0 by year", lambda: D[D.fc > 0].groupby("yr").apply(summ).round(3))
    safe("fc>0 by coin", lambda: D[D.fc > 0].groupby("coin").apply(summ).round(3))
    def fcq():
        P = D[D.fc > 0].copy(); P["fcQ"] = q3(P["fc"], ["lowfc", "midfc", "highfc"])
        return P.groupby("fcQ").apply(summ).round(3)
    safe("fc terciles", fcq)
    safe("fc>0 by trend", lambda: D[D.fc > 0].groupby("trend").apply(summ).round(3))
    safe("fc>0 by volQ", lambda: D[D.fc > 0].groupby("volQ").apply(summ).round(3))
    safe("all by volQ", lambda: D.groupby("volQ").apply(summ).round(3))
    safe("all by trend", lambda: D.groupby("trend").apply(summ).round(3))
    # book: largest gains and losses days
    def book():
        R = []
        for coin, wins in data["days"].items():
            for w, d in wins.items():
                R.append(d[["book_return", "coin_return"]].assign(coin=coin, win=w))
        B = pd.concat(R).dropna()
        B["bq"] = B.groupby("coin")["book_return"].transform(lambda s: q3(s, ["worst", "mid", "best"]))
        top = B[B.book_return != 0]
        res = pd.DataFrame({
            "share_days_nonzero": [len(top) / len(B)],
            "mean_book%": [100 * B.book_return.mean()],
            "top5pct_book_sum_share": [top.book_return.nlargest(int(len(top) * 0.05)).sum() / B.book_return.sum()],
            "bot5pct_book_sum_share": [top.book_return.nsmallest(int(len(top) * 0.05)).sum() / B.book_return.sum()],
        })
        return res.round(3)
    safe("book tails", book)
    def bookwin():
        R = []
        for coin, wins in data["days"].items():
            for w, d in wins.items():
                R.append(pd.Series({"win": w, "coin": coin, "book%": 100 * d.book_return.mean(), "coin%": 100 * d.coin_return.mean()}))
        return pd.DataFrame(R).groupby("win")[["book%", "coin%"]].mean().round(3)
    safe("book by window", bookwin)
    return out
