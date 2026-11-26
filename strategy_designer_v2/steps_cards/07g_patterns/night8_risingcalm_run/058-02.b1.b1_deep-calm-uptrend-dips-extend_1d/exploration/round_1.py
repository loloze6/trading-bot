def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=20).std()
            mx5 = c.rolling(5, min_periods=5).max()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "pos": np.arange(len(b)),
                "regime": b["regime"].astype(str),
                "r1": r1, "sd": sd,
                "z1": r1 / sd,
                "dist": (c - mx5) / mx5 / sd,
                "ret5back": c / c.shift(5) - 1,
                "tr20": c / c.shift(20) - 1,
                "f1": c.shift(-1) / c - 1,
                "f5": c.shift(-5) / c - 1,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            df["date"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    # coin means of 5-bar grid returns
    g5 = A[A["pos"] % 5 == 0].dropna(subset=["f5"]).copy()
    m5 = g5.groupby("coin")["f5"].mean()
    g5["x5"] = g5["f5"] - g5["coin"].map(m5)
    m1 = A.dropna(subset=["f1"]).groupby("coin")["f1"].mean()
    A["x1"] = A["f1"] - A["coin"].map(m1)
    g5["rc"] = np.where(g5["regime"] == "unknown", "risingcalm", "other")
    A["rc"] = np.where(A["regime"] == "unknown", "risingcalm", "other")

    def summ(df, col, by):
        def f(s):
            s = s.dropna()
            n = len(s)
            return pd.Series({"n": n, "mean%": 100 * s.mean(),
                              "t": s.mean() / (s.std() / np.sqrt(n)) if n > 2 else np.nan})
        return df.groupby(by)[col].apply(f).unstack()

    out = {}
    out["regime share"] = A["rc"].value_counts(normalize=True)
    # depth bins
    g = g5.dropna(subset=["dist"]).copy()
    g["dbin"] = pd.cut(g["dist"], [-99, -3, -2, -1, -0.3, -1e-9, 0.1])
    out["x5 by depth bin & regime"] = summ(g, "x5", ["rc", "dbin"])
    # large 1-day moves scaled
    a = A.dropna(subset=["z1", "x1"]).copy()
    a["zbin"] = pd.cut(a["z1"], [-99, -2, -1, 0, 1, 2, 99])
    out["next-day x1 by z1 bin & regime"] = summ(a, "x1", ["rc", "zbin"])
    gg = g5.dropna(subset=["z1"]).copy()
    gg["zbin"] = pd.cut(gg["z1"], [-99, -2, -1, 0, 1, 2, 99])
    out["x5 by z1 bin & regime"] = summ(gg, "x5", ["rc", "zbin"])
    # 5-day back return scaled
    gg["b5z"] = gg["ret5back"] / (gg["sd"] * np.sqrt(5))
    gg["bbin"] = pd.cut(gg["b5z"], [-99, -1.5, -0.5, 0.5, 1.5, 99])
    out["x5 by 5d-back z & regime"] = summ(gg.dropna(subset=["b5z"]), "x5", ["rc", "bbin"])
    # weekday
    out["x1 by weekday & regime"] = summ(a, "x1", ["rc", "wd"])
    # vol level tercile within coin
    a["sdq"] = a.groupby("coin")["sd"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=["low", "mid", "high"]))
    out["x1 by vol tercile"] = summ(a, "x1", ["rc", "sdq"])
    # 20-day trend bins
    gg["tbin"] = pd.cut(gg["tr20"] / (gg["sd"] * np.sqrt(20)), [-99, -1, 0, 1, 2, 99])
    out["x5 by 20d trend z & regime"] = summ(gg.dropna(subset=["tbin"]), "x5", ["rc", "tbin"])
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t):
                tt = t.copy(); tt["coin"] = coin; tr.append(tt)
    if tr:
        T = pd.concat(tr)
        out["trades by side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median"])
        out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"])
    return out
