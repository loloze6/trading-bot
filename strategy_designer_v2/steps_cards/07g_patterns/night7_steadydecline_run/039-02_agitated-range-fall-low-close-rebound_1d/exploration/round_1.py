def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        # coin mean daily return over all windows
        allr = []
        for w, b in wins.items():
            allr.append(b["close"].pct_change().dropna())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c, h, l, o = b["close"], b["high"], b["low"], b["open"]
            rng = (h - l)
            mr = rng.shift(1).rolling(30, min_periods=20).mean()
            r1 = c.pct_change()
            d = pd.DataFrame({
                "coin": coin, "win": w, "ts": b["timestamp"],
                "r1": r1,
                "fall_rng": (-(c - c.shift(1)) / mr),
                "loc": ((h - c) / rng.replace(0, np.nan)),  # 1 = close at low
                "agit": (b["regime"] != "chop").astype(int),
                "fc": b["forecast"],
                "alloc": b["postRebalance_current_allocation"],
                "nx1": c.shift(-1) / c - 1,
                "nx2": c.shift(-2) / c.shift(-1) - 1,
                "nx3": c.shift(-3) / c - 1,
                "r5": c / c.shift(5) - 1,
                "vol10": r1.rolling(10).std(),
            })
            d["ex1"] = d["nx1"] - mu
            d["ex2"] = d["nx2"] - mu
            d["ex3"] = d["nx3"] - 3 * mu
            d["wd"] = pd.to_datetime(b["timestamp"]).dt.dayofweek
            d["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)

    def ct(x, col):
        x = x.dropna(subset=[col])
        if len(x) < 5:
            return pd.Series({"n": len(x), "mean%": np.nan, "t": np.nan})
        m = x[col].mean()
        g = (x[col] - m).groupby(x["ts"]).sum()
        se = np.sqrt((g ** 2).sum()) / len(x)
        return pd.Series({"n": len(x), "days": x["ts"].nunique(), "mean%": 100 * m, "t": m / se if se > 0 else np.nan})

    out = {}
    dn = D[D["r1"] < 0].copy()
    dn["fallq"] = pd.qcut(dn["fall_rng"], 4, labels=["f1small", "f2", "f3", "f4big"])
    dn["locq"] = pd.cut(dn["loc"], [-0.01, 0.5, 0.8, 1.01], labels=["mid/high", "nearlow", "atlow"])
    out["down: agit x fallq x loc, ex1"] = dn.groupby(["agit", "fallq", "locq"]).apply(lambda x: ct(x, "ex1")).round(3)
    up = D[D["r1"] > 0].copy()
    up["riseq"] = pd.qcut(-up["fall_rng"], 4, labels=["r1small", "r2", "r3", "r4big"])
    up["locq"] = pd.cut(up["loc"], [-0.01, 0.2, 0.5, 1.01], labels=["athigh", "nearhigh", "mid/low"])
    out["up: agit x riseq x loc, ex1"] = up.groupby(["agit", "riseq", "locq"]).apply(lambda x: ct(x, "ex1")).round(3)
    sig = D[D["fc"] > 0]
    out["signal: ex1 ex2 ex3"] = pd.DataFrame({k: ct(sig, k) for k in ["ex1", "ex2", "ex3"]}).round(3)
    sig = sig.copy(); sig["fcq"] = pd.qcut(sig["fc"], 4, labels=False)
    out["signal by fc quartile ex1"] = sig.groupby("fcq").apply(lambda x: ct(x, "ex1")).round(3)
    out["signal by year ex1"] = sig.groupby("yr").apply(lambda x: ct(x, "ex1")).round(3)
    out["signal by coin ex1"] = sig.groupby("coin").apply(lambda x: ct(x, "ex1")).round(3)
    out["weekday all ex1 (next day after bar weekday)"] = D.groupby(["agit", "wd"]).apply(lambda x: ct(x, "ex1")).round(3)
    D["r5q"] = D.groupby("coin")["r5"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["5d return quintile x agit, ex1"] = D.groupby(["agit", "r5q"]).apply(lambda x: ct(x, "ex1")).round(3)
    out["5d return quintile x agit, ex3"] = D.groupby(["agit", "r5q"]).apply(lambda x: ct(x, "ex3")).round(3)
    return out
