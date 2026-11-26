def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z1 = r / sd
            df = pd.DataFrame({"coin": coin, "w": w, "z1": z1, "zprev": z1.shift(1),
                               "z2sum": (c / c.shift(2) - 1) / (sd * np.sqrt(2)),
                               "f1": c.shift(-1) / c - 1,
                               "reg": b["regime"].astype(str), "pos": np.arange(len(b)),
                               "yr": pd.to_datetime(b["timestamp"]).dt.year,
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                               "day": pd.to_datetime(b["timestamp"]).dt.floor("D")})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["inprof"] = d["reg"].isin(["mean_reversion", "unknown"])
    d["u1"] = d["f1"] - d["coin"].map(d.groupby("coin")["f1"].mean())
    def summ(x, col, key):
        x = x.dropna(subset=[col, key])
        o = x.groupby(key, observed=True)[col].agg(["count", "mean", "std"])
        o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
        return o.drop(columns="std")
    def dp(x, col):
        x = x.dropna(subset=[col]); n = len(x); m = x[col].mean()
        dev = x.groupby("day")[col].apply(lambda v: (v - m).sum()); G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / n
        return pd.Series({"n": n, "days": G, "mean": m, "t_dp": m / se})
    res = {}
    ip = d[d["inprof"]]
    a = ip[(ip["zprev"] < 0) & (ip["z1"] > 0)].copy()
    a["q"] = pd.cut(a["zprev"], [-np.inf, -2, -1, -0.3, 0])
    res["in: up after down day, u1 by yesterday z"] = summ(a, "u1", "q")
    a["q2"] = pd.cut(a["z1"], [0, 0.5, 1, 1.5, np.inf])
    res["in: up after down day, u1 by today z"] = summ(a, "u1", "q2")
    res["in: up after down dp"] = dp(a, "u1")
    b2 = ip[(ip["zprev"] > 0) & (ip["z1"] > 0)]
    res["in: up after up dp"] = dp(b2, "u1")
    dn = ip[ip["z1"] < 0].copy()
    dn["q"] = pd.cut(dn["z1"], [-np.inf, -2, -1, -0.3, 0])
    res["in: down days dp"] = dp(dn, "u1")
    res["in: down days u1 by window"] = summ(dn, "u1", "w")
    op = d[~d["inprof"]]
    res["out: weekday u1 by year (Wed)"] = summ(op[op["wd"] == 2], "u1", "yr")
    res["out: weekday u1 by year (Thu)"] = summ(op[op["wd"] == 3], "u1", "yr")
    res["out: Wed dp"] = dp(op[op["wd"] == 2], "u1")
    res["out: Thu dp"] = dp(op[op["wd"] == 3], "u1")
    return res
