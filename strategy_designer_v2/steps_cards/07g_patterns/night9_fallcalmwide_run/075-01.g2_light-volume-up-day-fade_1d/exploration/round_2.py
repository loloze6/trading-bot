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
            d["r60"] = c / c.shift(60) - 1
            sd = d["r1"].rolling(30).std()
            d["agit"] = sd > sd.rolling(90, min_periods=60).median()
            d["sd20"] = d["r1"].rolling(20).std()
            d["z1"] = d["r1"] / d["sd20"].shift(1)
            d["pos"] = np.arange(len(d))
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["nxt"].mean()
    D["u"] = D["nxt"] - D["coin"].map(drift)
    D["day"] = D["ts"].dt.floor("D")
    D["year"] = D["ts"].dt.year
    D = D.dropna(subset=["u", "vr", "r1"])
    D["vq"] = pd.qcut(D["vr"], 5, labels=False)
    D["side"] = np.where(D["r1"] > 0, "up", "down")
    D["trend"] = np.where(D["r60"] > 0.10, "rising", np.where(D["r60"] < -0.10, "falling", "choppy"))
    D.loc[D["r60"].isna(), "trend"] = "na"
    D["ag"] = np.where(D["agit"], "agit", "calm")

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

    res = {}
    U = D[D["side"] == "up"].copy(); Dn = D[D["side"] == "down"].copy()
    U["cq"] = pd.qcut(U["clv"], 3, labels=False, duplicates="drop")
    res["up: close-loc tercile x vol light(q0-1)/rest"] = tab(U.assign(light=U["vq"] <= 1).dropna(subset=["cq"]), ["light", "cq"])
    res["up light(q0-1) by trend"] = tab(U[U["vq"] <= 1], "trend")
    res["up light(q0-1) by agit"] = tab(U[U["vq"] <= 1], "ag")
    res["up light by year"] = tab(U[U["vq"] <= 1], "year")
    res["down heavy(q4) by trend x agit"] = tab(Dn[Dn["vq"] == 4], ["trend", "ag"])
    res["down heavy by year"] = tab(Dn[Dn["vq"] == 4], "year")
    # graded corr: down days, vr vs u, per trend
    out = []
    for k, g in Dn.groupby("trend"):
        g = g.dropna(subset=["vr"])
        x = g["vr"] - g["vr"].mean()
        prod = (x * (g["u"] - g["u"].mean()))
        m, t, n = ct(prod, g["day"])
        out.append({"trend": k, "cov*1e4": round(m * 1e4, 3), "t": round(t, 2), "n": n})
    res["down: vr x u covariance by trend"] = pd.DataFrame(out)
    # heavy-vol up days by z (large up on heavy volume)
    U["zq"] = pd.qcut(U["z1"], 3, labels=False)
    res["up: z tercile x vq"] = tab(U.dropna(subset=["zq"]), ["zq", "vq"])
    return res
