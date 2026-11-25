def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; r1 = c / c.shift(1) - 1
            rng = (b["high"] - b["low"]) / c
            rm = rng / rng.shift(1).rolling(14, min_periods=10).mean()
            cl = (b["close"] - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            d = pd.DataFrame({"coin": coin, "win": w, "r1": r1, "rm": rm, "cl": cl,
                              "r5": c / c.shift(5) - 1, "tr60": c / c.shift(60) - 1,
                              "vol20": r1.rolling(20).std(), "vol60": r1.rolling(60).std(),
                              "nx1": c.shift(-1) / c - 1, "nx3": c.shift(-3) / c - 1,
                              "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                              "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                              "yr": pd.to_datetime(b["timestamp"]).dt.year, "pos": np.arange(len(b))})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["nx1"].mean(); D["ex1"] = D["nx1"] - D["coin"].map(mu)
    mu3 = D[D.pos % 3 == 0].groupby("coin")["nx3"].mean(); D["ex3"] = D["nx3"] - D["coin"].map(mu3)
    def summ(g, col="ex1"):
        x = g[col].dropna(); n = len(x)
        return pd.Series({"n": n, "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    dn = D[D.r1 < 0].copy()
    dn["fallQ"] = dn.groupby("coin")["r1"].transform(lambda s: pd.qcut(-s, 3, labels=["small", "mid", "large"]))
    dn["rmQ"] = dn.groupby("coin")["rm"].transform(lambda s: pd.qcut(s, 3, labels=["narrow", "mid", "wide"]))
    dn["clQ"] = pd.cut(dn["cl"], [-0.01, 0.2, 0.5, 1.01], labels=["lowclose", "midclose", "highclose"])
    up = D[D.r1 > 0].copy()
    up["riseQ"] = up.groupby("coin")["r1"].transform(lambda s: pd.qcut(s, 3, labels=["small", "mid", "large"]))
    up["rmQ"] = up.groupby("coin")["rm"].transform(lambda s: pd.qcut(s, 3, labels=["narrow", "mid", "wide"]))
    D["volQ"] = D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=["lowvol", "midvol", "highvol"]))
    dn["volQ"] = D.loc[dn.index, "volQ"]
    D["trend"] = pd.cut(D["tr60"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    dn["trend"] = D.loc[dn.index, "trend"]
    dn["r5Q"] = dn.groupby("coin")["r5"].transform(lambda s: pd.qcut(s, 3, labels=["5d_down", "5d_mid", "5d_up"]))
    out = {}
    out["down fall x range"] = dn.groupby(["fallQ", "rmQ"]).apply(summ).round(3)
    out["down fall x closeloc"] = dn.groupby(["fallQ", "clQ"]).apply(summ).round(3)
    out["down large fall 3d ex (grid)"] = dn[(dn.pos % 3 == 0)].groupby(["fallQ", "rmQ"]).apply(lambda g: summ(g, "ex3")).round(3)
    out["up rise x range"] = up.groupby(["riseQ", "rmQ"]).apply(summ).round(3)
    out["down fall x vol"] = dn.groupby(["fallQ", "volQ"]).apply(summ).round(3)
    out["down large fall x trend"] = dn[dn.fallQ == "large"].groupby("trend").apply(summ).round(3)
    out["down large fall x 5d"] = dn[dn.fallQ == "large"].groupby("r5Q").apply(summ).round(3)
    out["all by weekday"] = D.groupby("wd").apply(summ).round(3)
    out["fc>0 by weekday"] = D[D.fc > 0].groupby("wd").apply(summ).round(3)
    out["fc>0 by year"] = D[D.fc > 0].groupby("yr").apply(summ).round(3)
    out["fc>0 by coin"] = D[D.fc > 0].groupby("coin").apply(summ).round(3)
    D["fcQ"] = pd.qcut(D.loc[D.fc > 0, "fc"], 5, labels=False)
    out["fc quintiles"] = D[D.fc > 0].groupby("fcQ").apply(summ).round(3)
    out["all by volQ"] = D.groupby("volQ").apply(summ).round(3)
    return out
