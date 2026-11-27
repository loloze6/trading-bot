def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]
            f = pd.DataFrame({"coin": coin, "win": w, "ts": b["timestamp"].astype(str).str[:10]})
            f["pos"] = np.arange(len(b))
            f["r20"] = c / c.shift(20) - 1
            f["r60"] = c / c.shift(60) - 1
            f["r5"] = c / c.shift(5) - 1
            f["vol30"] = c.pct_change().rolling(30).std()
            f["z20"] = np.log(c / c.shift(20)) / (f["vol30"] * np.sqrt(20))
            for hh in (2, 5, 10):
                f[f"fw{hh}"] = c.shift(-hh) / c - 1
            f["year"] = pd.to_datetime(b["timestamp"]).dt.year
            f["alloc"] = b["postRebalance_current_allocation"]
            rows.append(f)
    D = pd.concat(rows, ignore_index=True)
    D["agit"] = D["vol30"] > D.groupby("coin")["vol30"].transform("median")
    D["trend"] = np.where(D["r60"] > 0.10, "rising", np.where(D["r60"] < -0.10, "falling", np.where(D["r60"].notna(), "choppy", None)))

    def stat(sub, col, drift):
        x = (sub[col] - sub["coin"].map(drift)).dropna()
        s = sub.loc[x.index]; n = len(x)
        if n < 10: return pd.Series({"n": n, "mean": np.nan, "t": np.nan, "days": 0})
        m = x.mean(); S = (x - m).groupby(s["ts"]).sum(); G = len(S)
        se = np.sqrt(G / (G - 1) * (S ** 2).sum()) / n
        return pd.Series({"n": n, "mean": m, "t": m / se, "days": G})

    def slope(sub, xcol, col, drift):
        y = (sub[col] - sub["coin"].map(drift)); x = sub[xcol]
        ok = y.notna() & x.notna() & np.isfinite(x)
        y = y[ok]; x = x[ok]; s = sub[ok]
        if len(y) < 20: return pd.Series({"n": len(y), "beta": np.nan, "t": np.nan})
        xc = x - x.mean(); b = (xc * y).sum() / (xc ** 2).sum()
        e = (y - y.mean() - b * xc) * xc
        S = e.groupby(s["ts"]).sum(); G = len(S)
        se = np.sqrt(G / (G - 1) * (S ** 2).sum()) / (xc ** 2).sum()
        return pd.Series({"n": len(y), "beta": b, "t": b / se, "days": G})

    out = {}
    G = D[D["pos"] % 5 == 0].copy()
    dr5 = G.groupby("coin")["fw5"].mean()
    G["zq"] = pd.cut(G["z20"], [-99, -1.5, -0.75, -0.25, 0.25, 0.75, 1.5, 99])
    out["h5 all by z20"] = G.groupby("zq").apply(lambda s: stat(s, "fw5", dr5))
    out["h5 z20 slope by trend"] = G.groupby("trend").apply(lambda s: slope(s, "z20", "fw5", dr5))
    out["h5 z20 slope by agit"] = G.groupby("agit").apply(lambda s: slope(s, "z20", "fw5", dr5))
    out["h5 z20 slope by trend x agit"] = G.groupby(["trend", "agit"]).apply(lambda s: slope(s, "z20", "fw5", dr5))
    out["h5 z20 slope by year"] = G.groupby("year").apply(lambda s: slope(s, "z20", "fw5", dr5))
    out["h5 z20 slope by coin"] = G.groupby("coin").apply(lambda s: slope(s, "z20", "fw5", dr5))
    out["h5 z20 slope all"] = slope(G, "z20", "fw5", dr5)
    out["h5 r20 slope all"] = slope(G, "r20", "fw5", dr5)
    G10 = D[D["pos"] % 10 == 0].copy(); dr10 = G10.groupby("coin")["fw10"].mean()
    out["h10 z20 slope all"] = slope(G10, "z20", "fw10", dr10)
    out["h10 z20 slope by trend"] = G10.groupby("trend").apply(lambda s: slope(s, "z20", "fw10", dr10))
    ch = G[G.trend == "choppy"].copy()
    ch["zq"] = pd.cut(ch["z20"], [-99, -1, -0.3, 0.3, 1, 99])
    out["h5 choppy by z20"] = ch.groupby("zq").apply(lambda s: stat(s, "fw5", dr5))
    # book by window x coin
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    DD = pd.concat(dd)
    t = DD.groupby(["win", "coin"])["book_return"].sum()
    out["book sum by win x coin (nonzero)"] = t[t.abs() > 0.02]
    tr = []
    for coin, wins in data["trades"].items():
        for w, x in wins.items():
            if len(x): y = x.copy(); y["coin"] = coin; y["win"] = w; tr.append(y)
    T = pd.concat(tr)
    out["trades by win"] = T.groupby("win")["net_profit_loss_percent"].agg(["count", "mean", "sum"])
    return out
