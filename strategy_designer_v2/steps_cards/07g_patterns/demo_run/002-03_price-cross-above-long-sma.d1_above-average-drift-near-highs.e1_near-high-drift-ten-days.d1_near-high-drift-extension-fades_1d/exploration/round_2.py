def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            d = pd.DataFrame(index=b.index)
            d["coin"] = coin; d["win"] = w
            d["i"] = np.arange(len(b))
            d["ret1"] = c.pct_change()
            d["ret5p"] = c / c.shift(5) - 1
            d["ret30"] = c / c.shift(30) - 1
            hi = c.rolling(20).max(); lo = c.rolling(20).min()
            d["rpos"] = (c - lo) / (hi - lo)
            d["vol20"] = d["ret1"].rolling(20).std()
            d["f10"] = c.shift(-10) / c - 1
            d["f5"] = c.shift(-5) / c - 1
            d["f1"] = c.shift(-1) / c - 1
            d["trend"] = (b["regime"] == "trending").astype(int)
            d["fc"] = b["forecast"].astype(float)
            d["pos"] = b["postRebalance_current_allocation"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            d["wd"] = ts.dt.weekday.values
            d["year"] = ts.dt.year.values
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    out = {}
    def tab(df, key, val):
        r = df.dropna(subset=[key, val]).groupby(key)[val].agg(["mean", "count", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r.drop(columns="std")
    try:
        g10 = D[D["i"] % 10 == 0].dropna(subset=["f10"]).copy()
        g10["ex10"] = g10["f10"] - g10.groupby("coin")["f10"].transform("mean")
        g10["q30"] = g10.groupby("coin")["ret30"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
        g10["qr"] = pd.cut(g10["rpos"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.0], labels=False)
        g10["qv"] = g10.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
        out["ret30 q -> ex10, all"] = tab(g10, "q30", "ex10")
        out["ret30 q -> ex10, trending"] = tab(g10[g10.trend == 1], "q30", "ex10")
        out["ret30 q -> ex10, below200"] = tab(g10[g10.trend == 0], "q30", "ex10")
        out["range pos -> ex10, trending"] = tab(g10[g10.trend == 1], "qr", "ex10")
        out["range pos -> ex10, below200"] = tab(g10[g10.trend == 0], "qr", "ex10")
        out["vol20 q -> ex10"] = tab(g10, "qv", "ex10")
        out["regime -> ex10"] = tab(g10, "trend", "ex10")
        gt = g10[g10.trend == 1].copy()
        gt["qf"] = pd.qcut(gt["fc"].rank(method="first"), 5, labels=False)
        out["forecast q -> ex10, trending"] = tab(gt, "qf", "ex10")
    except Exception as e:
        out["err10"] = str(e)[:200]
    try:
        g5 = D[D["i"] % 5 == 0].dropna(subset=["f5"]).copy()
        g5["ex5"] = g5["f5"] - g5.groupby("coin")["f5"].transform("mean")
        g5["q5"] = g5.groupby("coin")["ret5p"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
        out["5d past ret q -> ex5"] = tab(g5, "q5", "ex5")
    except Exception as e:
        out["err5"] = str(e)[:200]
    try:
        D1 = D.dropna(subset=["f1"]).copy()
        D1["ex1"] = D1["f1"] - D1.groupby("coin")["f1"].transform("mean")
        out["weekday -> ex1"] = tab(D1, "wd", "ex1")
        D1["pg"] = D1["pos"] * D1["f1"]
        D1["posbin"] = pd.cut(D1["pos"], [-10, -0.001, 0.001, 0.5, 1.0, 10], labels=False)
        out["position bin -> ex1"] = tab(D1, "posbin", "ex1")
        out["book gain by year"] = tab(D1, "year", "pg")
        out["book gain by coin"] = tab(D1, "coin", "pg")
    except Exception as e:
        out["err1"] = str(e)[:200]
    try:
        dd = []
        for coin, wins in data["days"].items():
            for w, t in wins.items():
                t = t.copy(); t["coin"] = coin; t["win"] = w
                t["prev3"] = t["coin_return"].rolling(3).sum().shift(1)
                t["next3"] = t["coin_return"].shift(-1).rolling(3).sum().shift(-2)
                dd.append(t)
        DD = pd.concat(dd, ignore_index=True).dropna(subset=["book_return"])
        thr_lo = DD["book_return"].quantile(0.02); thr_hi = DD["book_return"].quantile(0.98)
        lo = DD[DD["book_return"] <= thr_lo]; hi = DD[DD["book_return"] >= thr_hi]
        out["worst 2% book days"] = pd.Series({"n": len(lo), "book": lo["book_return"].mean(), "coin": lo["coin_return"].mean(), "coin prev3": lo["prev3"].mean(), "coin next3": lo["next3"].mean()})
        out["best 2% book days"] = pd.Series({"n": len(hi), "book": hi["book_return"].mean(), "coin": hi["coin_return"].mean(), "coin prev3": hi["prev3"].mean(), "coin next3": hi["next3"].mean()})
    except Exception as e:
        out["errdays"] = str(e)[:200]
    try:
        tr = []
        for coin, wins in data["trades"].items():
            for w, t in wins.items():
                if len(t): tr.append(t.assign(coin=coin))
        T = pd.concat(tr, ignore_index=True)
        T["dur"] = pd.cut(T["duration_minutes"] / 1440, [-1, 1, 3, 10, 30, 1e9], labels=False)
        out["trades by duration"] = T.groupby("dur")["net_profit_loss_percent"].agg(["mean", "count", "sum"])
    except Exception as e:
        out["errtr"] = str(e)[:200]
    return out
