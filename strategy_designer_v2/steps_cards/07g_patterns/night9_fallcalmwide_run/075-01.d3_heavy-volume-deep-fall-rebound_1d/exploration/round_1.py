def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    bk = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            allr.append(b["close"].pct_change())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; r = c.pct_change()
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b))})
            d["ts"] = pd.to_datetime(b["timestamp"])
            d["r"] = r
            d["sr"] = r / r.rolling(30, min_periods=20).std()
            d["vr"] = b["volume"] / b["volume"].rolling(20, min_periods=10).mean()
            d["rng"] = (b["high"] - b["low"]) / c
            d["clv"] = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            d["tr20"] = c / c.shift(20) - 1
            d["f1"] = c.shift(-1) / c - 1 - mu
            d["f3"] = c.shift(-3) / c - 1 - 3 * mu
            d["fc"] = b["forecast"]
            d["alloc"] = b["postRebalance_current_allocation"]
            d["gain"] = d["alloc"] * (c.shift(-1) / c - 1)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["dn"] = D["r"] < 0
    D["day"] = D["ts"].dt.floor("D")
    def tclus(x, key):
        x = x.dropna(); k = key.loc[x.index]
        s = (x - x.mean()).groupby(k).sum()
        n = len(s)
        se = np.sqrt((s**2).sum() * n / (n - 1)) / len(x)
        return x.mean() / se if se > 0 else np.nan
    def tab(sub, col, q=5, y="f1"):
        sub = sub.dropna(subset=[col, y]).copy()
        sub["q"] = pd.qcut(sub[col], q, labels=False, duplicates="drop")
        out = sub.groupby("q").apply(lambda g: pd.Series({"n": len(g), "mid": g[col].median(), "mean": g[y].mean(), "t": tclus(g[y], g["day"])}))
        return out
    res = {}
    res["dn days by volratio"] = tab(D[D.dn], "vr")
    res["up days by volratio"] = tab(D[~D.dn], "vr")
    res["dn days by scaled ret"] = tab(D[D.dn], "sr")
    res["up days by scaled ret"] = tab(D[~D.dn], "sr")
    res["all days by range"] = tab(D, "rng")
    res["dn days by close loc"] = tab(D[D.dn], "clv")
    res["up days by close loc"] = tab(D[~D.dn], "clv")
    res["all by 20d trend"] = tab(D, "tr20")
    # 3-day on grid
    G = D[D.pos % 3 == 0]
    res["f3 dn by scaled ret grid"] = tab(G[G.dn], "sr", 4, "f3")
    res["f3 up by volratio grid"] = tab(G[~G.dn], "vr", 4, "f3")
    D["wd"] = D["ts"].dt.weekday
    res["f1 by weekday"] = D.groupby("wd").apply(lambda g: pd.Series({"n": g.f1.notna().sum(), "mean": g.f1.mean(), "t": tclus(g.f1, g.day)}))
    D["yr"] = D["ts"].dt.year
    res["dn-heavy f1 by year"] = D[D.dn & (D.vr > 1.5)].groupby("yr").apply(lambda g: pd.Series({"n": g.f1.notna().sum(), "mean": g.f1.mean(), "t": tclus(g.f1, g.day)}))
    # book gains attribution
    A = D[D.alloc.abs() > 0].dropna(subset=["gain"])
    A["sq"] = pd.qcut(A["sr"], 5, labels=False, duplicates="drop")
    res["book gain by scaled ret quint (held bars)"] = A.groupby("sq").agg(n=("gain", "size"), gain=("gain", "mean"), alloc=("alloc", "mean"))
    res["book gain by year"] = A.groupby("yr").agg(n=("gain", "size"), gain=("gain", "mean"))
    return res
