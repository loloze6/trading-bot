def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float)
            allr.append(c.pct_change().dropna())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.copy()
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30).std()
            d = pd.DataFrame({
                "ts": pd.to_datetime(b["timestamp"]).values,
                "coin": coin, "win": w,
                "r": r.values, "z": (r / sd).values,
                "f1": (c.shift(-1) / c - 1 - mu).values,
                "f3": (c.shift(-3) / c - 1 - 3 * mu).values,
                "tr60": (c / c.shift(60) - 1).values,
                "clv": ((c - b["low"]) / (b["high"] - b["low"])).values,
                "rng": (((b["high"] - b["low"]) / c) / sd).values,
                "regime": b["regime"].values,
                "pos": b["postRebalance_current_allocation"].values,
                "fc": b["forecast"].values,
                "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek.values,
            })
            d["fa"] = d["regime"] == "unknown"
            d["r1prev"] = d["r"].shift(1)
            rows.append(d)
    D = pd.concat(rows).dropna(subset=["z", "f1"])
    zb = pd.cut(D["z"], [-99, -2.5, -1.5, -0.75, 0, 0.75, 1.5, 2.5, 99])
    D["zb"] = zb

    def tday(g, col):
        s = g.groupby("ts")[col].mean().dropna()
        if len(s) < 3: return pd.Series({"mean": np.nan, "t": np.nan, "days": len(s)})
        return pd.Series({"mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))), "days": len(s), "n": g[col].notna().sum()})

    out = {}
    out["f1 by z bucket, falling agitated"] = D[D.fa].groupby("zb", observed=True).apply(lambda g: tday(g, "f1"))
    out["f1 by z bucket, other profiles"] = D[~D.fa].groupby("zb", observed=True).apply(lambda g: tday(g, "f1"))
    out["f3 by z bucket, falling agitated"] = D[D.fa].groupby("zb", observed=True).apply(lambda g: tday(g, "f3"))
    O = D[~D.fa & D.tr60.notna()].copy()
    O["trend"] = np.where(O.tr60 > 0.10, "rising", np.where(O.tr60 < -0.10, "falling", "choppy"))
    out["f1 by trend x z bucket, outside FA"] = O.groupby(["trend", "zb"], observed=True).apply(lambda g: tday(g, "f1")).round(4)
    F = D[D.fa & (D.z < -0.75)].copy()
    F["clvb"] = pd.cut(F["clv"], [-0.01, 0.25, 0.5, 0.75, 1.01])
    out["FA falls: f1 by close location"] = F.groupby("clvb", observed=True).apply(lambda g: tday(g, "f1"))
    F["prevb"] = np.where(F.r1prev < 0, "prev down", "prev up")
    out["FA falls: f1 by previous day sign"] = F.groupby("prevb").apply(lambda g: tday(g, "f1"))
    out["FA falls: f1 by weekday"] = F.groupby("wd").apply(lambda g: tday(g, "f1"))
    out["all bars f1 by weekday"] = D.groupby("wd").apply(lambda g: tday(g, "f1"))
    U = D[D.fa & (D.z > 0.75)].copy()
    U["clvb"] = pd.cut(U["clv"], [-0.01, 0.25, 0.5, 0.75, 1.01])
    out["FA rises: f1 by close location"] = U.groupby("clvb", observed=True).apply(lambda g: tday(g, "f1"))
    out["share of bars FA by window"] = D.groupby("win")["fa"].mean().round(3)
    # book
    days = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["coin"] = coin; x["win"] = w; days.append(x)
    DD = pd.concat(days)
    bk = DD.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book mean daily return by window"] = bk.groupby(level=0).agg(["mean", "count"])
    return out
