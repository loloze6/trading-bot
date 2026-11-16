def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            d = pd.DataFrame({"coin": coin, "win": w})
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
            d["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            d["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    # coin mean 10d return on grid
    g10 = D[D["i"] % 10 == 0].dropna(subset=["f10"]).copy()
    g10["ex10"] = g10["f10"] - g10.groupby("coin")["f10"].transform("mean")
    g5 = D[D["i"] % 5 == 0].dropna(subset=["f5"]).copy()
    g5["ex5"] = g5["f5"] - g5.groupby("coin")["f5"].transform("mean")
    out = {}
    def tab(df, key, val):
        r = df.dropna(subset=[key, val]).groupby(key)[val].agg(["mean", "count", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r.drop(columns="std")
    # past 30-day return quintile -> next 10d, by regime
    g10["q30"] = g10.groupby("coin")["ret30"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    g10["qr"] = pd.cut(g10["rpos"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.0], labels=False)
    out["ret30 quintile -> ex10, all"] = tab(g10, "q30", "ex10")
    out["ret30 quintile -> ex10, trending"] = tab(g10[g10.trend == 1], "q30", "ex10")
    out["ret30 quintile -> ex10, below200"] = tab(g10[g10.trend == 0], "q30", "ex10")
    out["range pos -> ex10, trending"] = tab(g10[g10.trend == 1], "qr", "ex10")
    out["range pos -> ex10, below200"] = tab(g10[g10.trend == 0], "qr", "ex10")
    g5["q5"] = g5.groupby("coin")["ret5p"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["5d past ret quintile -> ex5"] = tab(g5, "q5", "ex5")
    g5["qv"] = g5.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["vol20 quintile -> ex5"] = tab(g5, "qv", "ex5")
    out["regime -> ex10"] = tab(g10, "trend", "ex10")
    # weekday next day
    D1 = D.dropna(subset=["f1"]).copy()
    D1["ex1"] = D1["f1"] - D1.groupby("coin")["f1"].transform("mean")
    out["weekday -> ex1"] = tab(D1, "wd", "ex1")
    # book: position side/size vs next day
    D1["pg"] = D1["pos"] * D1["f1"]
    D1["posbin"] = pd.cut(D1["pos"], [-10, -0.001, 0.001, 0.5, 1.0, 10], labels=False)
    out["position bin -> f1"] = D1.groupby("posbin")["f1"].agg(["mean", "count"])
    out["book gain by year"] = D1.groupby("year")["pg"].agg(["mean", "count"])
    out["book gain by coin"] = D1.groupby("coin")["pg"].agg(["mean", "count"])
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    T = pd.concat(tr)
    T["dd"] = T["duration_minutes"] / 1440
    T["dur"] = pd.cut(T["dd"], [-1, 1, 3, 10, 30, 1e9], labels=False)
    out["trades by duration"] = T.groupby("dur")["net_profit_loss_percent"].agg(["mean", "count", "sum"])
    return out
