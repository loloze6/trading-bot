def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float)
            r1 = c.pct_change()
            vr = v / v.shift(1).rolling(20, min_periods=20).mean()
            sd = r1.shift(1).rolling(20, min_periods=15).std()
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]),
                "r1": r1, "vr": vr, "z": r1 / sd,
                "cl": (c - l) / (h - l).replace(0, np.nan),
                "tr60": c / c.shift(60) - 1,
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1,
                "alloc": b["postRebalance_current_allocation"],
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")
    D["wd"] = D["ts"].dt.dayofweek
    D["year"] = D["ts"].dt.year
    G = D[(D["pos"] % 2 == 0)].copy()
    G["ex2"] = G["f2"] - G.groupby("coin")["f2"].transform("mean")
    D["ex1"] = D["f1"] - D.groupby("coin")["f1"].transform("mean")

    def ct(x, day):
        m = pd.DataFrame({"x": x, "d": day}).dropna()
        if len(m) < 10: return (np.nan, np.nan, len(m))
        mu = m["x"].mean(); S = (m["x"] - mu).groupby(m["d"]).sum()
        se = np.sqrt((S ** 2).sum()) / len(m)
        return (mu, mu / se if se > 0 else np.nan, len(m))

    def table(df, key, val):
        out = []
        for k, g in df.groupby(key, observed=True):
            mu, t, n = ct(g[val], g["day"])
            out.append({"grp": str(k), "mean%": round(mu * 100, 3), "t": round(t, 2), "n": n})
        return pd.DataFrame(out)

    res = {}
    G2 = G.dropna(subset=["vr", "ex2", "r1"]).copy()
    G2["vq"] = pd.qcut(G2["vr"], 5, labels=False)
    G2["sgn"] = np.where(G2["r1"] < 0, "down", "up")
    res["ex2 by vol quintile x sign"] = table(G2, ["sgn", "vq"], "ex2")
    G2["zq"] = pd.qcut(G2["z"], 7, labels=False)
    res["ex2 by scaled day return septile"] = table(G2.dropna(subset=["zq"]), "zq", "ex2")
    dn = G2[G2["sgn"] == "down"].dropna(subset=["cl"]).copy()
    dn["clq"] = pd.qcut(dn["cl"], 4, labels=False)
    res["down days ex2 by close location quartile"] = table(dn, "clq", "ex2")
    dn["zq"] = pd.qcut(dn["z"], 4, labels=False)
    res["down days ex2 by fall size quartile x heavy(vq>=3)"] = table(dn.assign(hv=(dn["vq"] >= 3).astype(int)), ["zq", "hv"], "ex2")
    D1 = D.dropna(subset=["ex1"])
    res["ex1 all bars by weekday of bar"] = table(D1, "wd", "ex1")
    T = G2.dropna(subset=["tr60"]).copy()
    T["trend"] = np.where(T["tr60"] > 0.1, "rising", np.where(T["tr60"] < -0.1, "falling", "choppy"))
    res["down days ex2 by trend x vol tercile"] = table(T[T["sgn"] == "down"].assign(vt=lambda x: pd.qcut(x["vr"], 3, labels=False)), ["trend", "vt"], "ex2")
    res["up days ex2 by trend x vol tercile"] = table(T[T["sgn"] == "up"].assign(vt=lambda x: pd.qcut(x["vr"], 3, labels=False)), ["trend", "vt"], "ex2")
    res["down heavy(vq4) ex2 by year"] = table(G2[(G2["sgn"] == "down") & (G2["vq"] == 4)], "year", "ex2")
    # book daily
    dd = []
    for coin, ws in data["days"].items():
        for w, x in ws.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    DD = pd.concat(dd, ignore_index=True)
    DD["day"] = pd.to_datetime(DD["day"])
    bk = DD.groupby("day")[["book_return", "coin_return"]].mean().dropna()
    bk["wd"] = bk.index.dayofweek
    res["book daily by weekday"] = bk.groupby("wd").agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"), n=("book_return", "size")).round(5)
    q = bk["book_return"].quantile([0.05, 0.95])
    res["coin ret on book worst/best 5% days"] = pd.DataFrame({
        "worst_book": [bk.loc[bk.book_return <= q.iloc[0], "book_return"].mean(), bk.loc[bk.book_return <= q.iloc[0], "coin_return"].mean()],
        "best_book": [bk.loc[bk.book_return >= q.iloc[1], "book_return"].mean(), bk.loc[bk.book_return >= q.iloc[1], "coin_return"].mean()]},
        index=["book", "coin"]).round(4)
    res["book corr with coin daily"] = float(bk[["book_return", "coin_return"]].corr().iloc[0, 1])
    return res
