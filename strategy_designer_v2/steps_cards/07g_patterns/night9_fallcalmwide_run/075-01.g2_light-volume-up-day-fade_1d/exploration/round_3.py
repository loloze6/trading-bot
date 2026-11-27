def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; v = b["volume"]
            d = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"])})
            d["r1"] = c.pct_change()
            d["nxt"] = c.shift(-1) / c - 1
            d["vr"] = np.log(v / v.shift(1).rolling(20).mean())
            rng = (b["high"] - b["low"])
            d["clv"] = ((c - b["low"]) / rng.replace(0, np.nan))
            d["r30"] = c / c.shift(30) - 1
            d["r60"] = c / c.shift(60) - 1
            d["sd20"] = d["r1"].rolling(20).std()
            d["z1"] = d["r1"] / d["sd20"].shift(1)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["nxt"].mean()
    D["u"] = D["nxt"] - D["coin"].map(drift)
    D["day"] = D["ts"].dt.floor("D")
    D = D.dropna(subset=["u", "vr", "r1"])
    D["vq"] = pd.qcut(D["vr"], 5, labels=False)

    def ct(s, days):
        n = s.notna().sum(); m = s.mean()
        se = np.sqrt(((s - m).groupby(days).sum() ** 2).sum()) / n
        return m, (m / se if se > 0 else np.nan), n

    def tab(df, key):
        out = []
        for k, g in df.groupby(key, observed=True):
            m, t, n = ct(g["u"], g["day"])
            out.append({"grp": str(k), "mean_u%": round(100 * m, 3), "t": round(t, 2), "n": n})
        return pd.DataFrame(out)

    def cov(g, x):
        g = g.dropna(subset=[x])
        xx = g[x] - g[x].mean()
        m, t, n = ct(xx * (g["u"] - g["u"].mean()), g["day"])
        return {"cov*1e4": round(m * 1e4, 3), "t": round(t, 2), "n": n}

    res = {}
    U = D[D["r1"] > 0]; Dn = D[D["r1"] <= 0]
    T = D.dropna(subset=["r30"]).copy()
    T["tr30"] = np.where(T["r30"] > 0.10, "rising", np.where(T["r30"] < -0.10, "falling", "choppy"))
    Ut = T[T["r1"] > 0]; Dt = T[T["r1"] <= 0]
    res["up: vq x 30d trend"] = tab(Ut, ["tr30", "vq"])
    out = []
    for k, g in Ut.groupby("tr30"):
        out.append({"grp": "up " + k, **cov(g, "vr")})
    for k, g in Dt.groupby("tr30"):
        out.append({"grp": "down " + k, **cov(g, "vr")})
    out.append({"grp": "up all", **cov(U, "vr")})
    out.append({"grp": "down all", **cov(Dn, "vr")})
    out.append({"grp": "down all, z1", **cov(Dn, "z1")})
    out.append({"grp": "down heavy q3-4, z1", **cov(Dn[Dn["vq"] >= 3], "z1")})
    res["covariances u with vr / z1"] = pd.DataFrame(out)
    Dh = Dn[Dn["vq"] == 4].copy()
    Dh["cq"] = pd.qcut(Dh["clv"], 3, labels=False, duplicates="drop")
    res["down heavy: close-loc tercile"] = tab(Dh.dropna(subset=["cq"]), "cq")
    res["down heavy q4 by window"] = tab(Dh, "win")
    D["zq"] = pd.qcut(D["z1"], 5, labels=False)
    Dz = D.dropna(subset=["zq"])
    res["down z q0: vq"] = tab(Dz[Dz["zq"] == 0], "vq")
    return res
