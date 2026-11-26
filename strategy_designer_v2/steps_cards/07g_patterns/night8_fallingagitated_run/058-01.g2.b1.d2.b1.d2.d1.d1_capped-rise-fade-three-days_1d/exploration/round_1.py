def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]),
                "regime": b["regime"].astype(str),
                "z1": r1 / sd,
                "z3": (c / c.shift(3) - 1) / (sd * np.sqrt(3)),
                "z5": (c / c.shift(5) - 1) / (sd * np.sqrt(5)),
                "f3": c.shift(-3) / c - 1,
                "f1": c.shift(-1) / c - 1,
                "rng": (b["high"] - b["low"]) / c,
                "clpos": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "sd": sd,
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            rows.append(df)
    P = pd.concat(rows, ignore_index=True)
    g = P[P["pos"] % 3 == 0].copy()
    drift = g.groupby("coin")["f3"].mean()
    usual = g.groupby("coin")["f3"].std()
    g["u3"] = g["f3"] - g["coin"].map(drift)
    g["s3"] = g["u3"] / g["coin"].map(usual)
    g["inprof"] = g["regime"] != "chop"
    g["day"] = g["ts"].dt.floor("D")
    out = {}
    out["regime counts"] = P["regime"].value_counts()

    def stats(sub, key):
        def f(x):
            x = x.dropna(subset=["u3"])
            ds = x.groupby("day")["u3"].sum() - 0  # day-sum of deviations
            m = x["u3"].mean(); n = len(x); G = len(ds)
            dev = x["u3"] - m
            dsum = dev.groupby(x["day"]).sum()
            se = np.sqrt((dsum**2).sum() * G / max(G - 1, 1)) / n if n else np.nan
            return pd.Series({"n": n, "days": G, "mean_u3": m, "t_cl": m / se if se else np.nan,
                              "strength": x["s3"].mean(), "mean_f3": x["f3"].mean()})
        return sub.groupby(key).apply(f)

    gp = g[g["inprof"]].copy()
    gp["z1b"] = pd.cut(gp["z1"], [-9, -2, -1, -0.5, 0, 0.5, 1, 2, 9])
    gp["z3b"] = pd.cut(gp["z3"], [-9, -2, -1, -0.5, 0, 0.5, 1, 2, 9])
    gp["z5b"] = pd.cut(gp["z5"], [-9, -2, -1, -0.5, 0, 0.5, 1, 2, 9])
    out["inprof by z1"] = stats(gp, "z1b")
    out["inprof by z3"] = stats(gp, "z3b")
    out["inprof by z5"] = stats(gp, "z5b")
    go = g[~g["inprof"]].copy()
    go["z3b"] = pd.cut(go["z3"], [-9, -2, -1, -0.5, 0, 0.5, 1, 2, 9])
    out["outprof by z3"] = stats(go, "z3b")
    gp["clb"] = pd.cut(gp["clpos"], [0, 0.2, 0.4, 0.6, 0.8, 1.0001])
    out["inprof by close position"] = stats(gp, "clb")
    gp["wd"] = gp["ts"].dt.weekday
    out["inprof by weekday"] = stats(gp, "wd")
    gp["yr"] = gp["ts"].dt.year
    out["inprof by year"] = stats(gp, "yr")
    # book daily
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D, ignore_index=True)
    bk = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book by window"] = bk.groupby(level=0).agg(["mean", "count"])
    return out
