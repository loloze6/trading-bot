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
            p5 = (c.shift(1) / c.shift(6) - 1) / (sd * np.sqrt(5))
            f1 = c.shift(-1) / c - 1
            f2 = c.shift(-2) / c - 1
            f3 = c.shift(-3) / c - 1
            tr60 = c / c.shift(60) - 1
            df = pd.DataFrame({"coin": coin, "w": w, "z1": z1, "p5": p5, "f1": f1, "f2": f2, "f3": f3,
                               "reg": b["regime"].astype(str), "pos": np.arange(len(b)),
                               "yr": pd.to_datetime(b["timestamp"]).dt.year, "tr60": tr60,
                               "clv": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                               "day": pd.to_datetime(b["timestamp"]).dt.floor("D")})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["inprof"] = d["reg"].isin(["mean_reversion", "unknown"])
    d["u1"] = d["f1"] - d["coin"].map(d.groupby("coin")["f1"].mean())
    g2 = d[d["pos"] % 2 == 0].copy()
    g2["u2"] = g2["f2"] - g2["coin"].map(g2.groupby("coin")["f2"].mean())
    def summ(x, col, key):
        x = x.dropna(subset=[col, key])
        o = x.groupby(key, observed=True)[col].agg(["count", "mean", "std"])
        o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
        return o.drop(columns="std")
    def daypooled(x, col):
        x = x.dropna(subset=[col])
        s = x.groupby("day")[col].sum(); n = len(x); G = len(s)
        m = x[col].mean(); dev = x.groupby("day")[col].apply(lambda v: (v - m).sum())
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / n
        return pd.Series({"n": n, "days": G, "mean": m, "t_daypooled": m / se})
    res = {}
    ip = d[d["inprof"]].copy()
    up = ip[ip["z1"] > 0].copy()
    up["p5q"] = pd.cut(up["p5"], [-np.inf, -1, -0.3, 0.3, np.inf])
    res["in up days: u1 by prior5"] = summ(up, "u1", "p5q")
    up["zq"] = pd.cut(up["z1"], [0, 0.5, 1, 1.5, np.inf])
    res["in up days: u1 by z1"] = summ(up, "u1", "zq")
    res["in up days: u1 by close loc"] = summ(up.assign(cq=pd.cut(up["clv"], [-.01, .33, .66, 1.01])), "u1", "cq")
    res["in up days: u1 by year"] = summ(up, "u1", "yr")
    res["in up days: u1 by window"] = summ(up, "u1", "w")
    res["in up days u1 daypooled"] = daypooled(up, "u1")
    up2 = g2[g2["inprof"] & (g2["z1"] > 0)].copy()
    up2["zq"] = pd.cut(up2["z1"], [0, 0.5, 1, 1.5, np.inf])
    res["in up days: u2 by z1"] = summ(up2, "u2", "zq")
    dn = ip[ip["z1"] < 0].copy()
    res["in down days u1 by year"] = summ(dn, "u1", "yr")
    # out of profile, falling trend (tr60 < -10%) but not agitated / not in profile
    op = d[~d["inprof"] & (d["tr60"] < -0.10) & (d["z1"] > 0)].copy()
    op["zq"] = pd.cut(op["z1"], [0, 0.5, 1, 1.5, np.inf])
    res["falling-but-not-profile up days: u1 by z1"] = summ(op, "u1", "zq")
    # linear slope of u1 on z1 among in-profile up days
    x = up.dropna(subset=["u1", "z1"])
    res["in up days corr(z1,u1)"] = float(np.corrcoef(x["z1"], x["u1"])[0, 1])
    x = ip.dropna(subset=["u1", "z1"])
    res["in all days corr(z1,u1)"] = float(np.corrcoef(x["z1"], x["u1"])[0, 1])
    res["in all days n"] = len(x)
    return res
