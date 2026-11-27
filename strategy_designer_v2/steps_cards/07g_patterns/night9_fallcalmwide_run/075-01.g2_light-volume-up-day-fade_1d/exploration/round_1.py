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
            d["nxt2"] = c.shift(-2) / c - 1
            d["vr"] = np.log(v / v.shift(1).rolling(20).mean())
            rng = (b["high"] - b["low"])
            d["clv"] = ((c - b["low"]) / rng.replace(0, np.nan))
            d["rngr"] = np.log((rng / c) / (rng / c).shift(1).rolling(20).mean())
            d["r5"] = c / c.shift(5) - 1
            d["sd20"] = d["r1"].rolling(20).std()
            d["z1"] = d["r1"] / d["sd20"].shift(1)
            d["alloc"] = b["postRebalance_current_allocation"]
            d["fc"] = b["forecast"]
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["nxt"].mean()
    D["u"] = D["nxt"] - D["coin"].map(drift)
    D["day"] = D["ts"].dt.floor("D")
    D["wd"] = D["ts"].dt.dayofweek
    D = D.dropna(subset=["u"])

    def ct(s, days):
        g = s.groupby(days).sum(); n = s.notna().sum()
        m = s.mean()
        se = np.sqrt(((s - m).groupby(days).sum() ** 2).sum()) / n
        return m, m / se if se > 0 else np.nan, n

    def tab(df, key):
        out = []
        for k, g in df.groupby(key, observed=True):
            m, t, n = ct(g["u"], g["day"])
            out.append({"grp": str(k), "mean_u%": round(100 * m, 3), "t": round(t, 2), "n": n})
        return pd.DataFrame(out)

    E = D.dropna(subset=["vr", "r1"]).copy()
    E["vq"] = pd.qcut(E["vr"], 5, labels=False)
    E["side"] = np.where(E["r1"] > 0, "up", "down")
    res = {}
    res["vol quintile x side"] = tab(E, ["side", "vq"])
    res["vol quintile all"] = tab(E, "vq")
    E["zq"] = pd.qcut(E["z1"], 5, labels=False)
    res["z-return quintile"] = tab(E.dropna(subset=["z1"]), "zq")
    res["z quintile x heavy(vq4)"] = tab(E[E["vq"] == 4].dropna(subset=["zq"]), "zq")
    E["cq"] = pd.qcut(E["clv"], 5, labels=False, duplicates="drop")
    res["close location quintile"] = tab(E.dropna(subset=["cq"]), "cq")
    E["rq"] = pd.qcut(E["rngr"], 5, labels=False)
    res["range ratio quintile"] = tab(E.dropna(subset=["rq"]), "rq")
    res["weekday"] = tab(E, "wd")
    E["r5q"] = pd.qcut(E["r5"], 5, labels=False)
    res["5d return quintile"] = tab(E.dropna(subset=["r5q"]), "r5q")
    res["window"] = tab(E, "win")
    # book days
    bd = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["win"] = w; bd.append(x)
    B = pd.concat(bd)
    bk = B.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    res["book by window"] = bk.groupby(level=0).agg(["mean", "count"]).round(5)
    return res
