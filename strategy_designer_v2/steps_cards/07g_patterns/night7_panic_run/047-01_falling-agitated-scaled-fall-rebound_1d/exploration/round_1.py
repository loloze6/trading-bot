def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            r5 = c / c.shift(5) - 1
            z5 = r5 / (sd * np.sqrt(5))
            for h in (1, 3, 7):
                b[f"f{h}"] = c.shift(-h) / c - 1
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "z": z, "z5": z5, "sd": sd,
                "f1": b["f1"], "f3": b["f3"], "f7": b["f7"],
                "inprof": (b["regime"] == "unknown").astype(int),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "fc": b["forecast"].astype(float),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift3 = A[A.pos % 3 == 0].groupby("coin")["f3"].mean()
    G3 = A[(A.pos % 3 == 0)].dropna(subset=["z", "f3"]).copy()
    G3["u3"] = G3["f3"] - G3["coin"].map(drift3)
    G3["zb"] = pd.cut(G3["z"], [-np.inf, -2, -1, -0.3, 0.3, 1, 2, np.inf])

    def summ(g, col="u3"):
        x = g[col].dropna()
        n = len(x)
        t = x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series({"n": n, "mean": x.mean(), "t": t})

    out = {}
    out["u3 by z bucket x profile"] = G3.groupby(["inprof", "zb"]).apply(summ).round(4)
    G3["z5b"] = pd.cut(G3["z5"], [-np.inf, -2, -1, 0, 1, 2, np.inf])
    out["u3 by 5d-z bucket x profile"] = G3.groupby(["inprof", "z5b"]).apply(summ).round(4)
    # slopes
    sl = {}
    for p in (0, 1):
        g = G3[G3.inprof == p]
        for side, gg in (("down", g[g.z < 0]), ("up", g[g.z > 0]), ("all", g)):
            res = stats.linregress(gg["z"], gg["u3"])
            sl[f"prof{p}_{side}"] = [len(gg), res.slope, res.slope / res.stderr]
    out["slope u3 on z"] = pd.DataFrame(sl, index=["n", "slope", "t"]).T.round(4)
    # 7-day horizon, grid 7
    G7 = A[A.pos % 7 == 0].dropna(subset=["z", "f7"]).copy()
    d7 = G7.groupby("coin")["f7"].mean()
    G7["u7"] = G7["f7"] - G7["coin"].map(d7)
    G7["zb"] = pd.cut(G7["z"], [-np.inf, -2, -1, 0, 1, 2, np.inf])
    out["u7 by z bucket x profile"] = G7.groupby(["inprof", "zb"]).apply(lambda g: summ(g, "u7")).round(4)
    # weekday daily returns (1-day grid)
    G1 = A.dropna(subset=["f1"]).copy()
    G1["u1"] = G1["f1"] - G1["coin"].map(G1.groupby("coin")["f1"].mean())
    out["u1 by weekday of bar"] = G1.groupby("wd").apply(lambda g: summ(g, "u1")).round(4)
    # vol level: sd tercile within coin
    G3["sdq"] = G3.groupby("coin")["sd"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["u3 by vol tercile x down/up"] = G3.groupby(["sdq", np.sign(G3.z)]).apply(summ).round(4)
    # book
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D)
    out["book by window"] = D.groupby("win").agg(br=("book_return", "mean"), cr=("coin_return", "mean"), n=("book_return", "count")).round(5)
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tt = t.copy(); tt["coin"] = coin; T.append(tt)
    T = pd.concat(T)
    T["fcq"] = pd.qcut(T["entry_forecast"], 4, duplicates="drop")
    out["trades by entry forecast"] = T.groupby("fcq")["net_profit_loss_percent"].agg(["count", "mean", "median"]).round(3)
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"]).round(3)
    out["share in profile"] = A.groupby("coin")["inprof"].mean().round(3)
    return out
