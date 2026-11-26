def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            d = pd.DataFrame()
            d["ts"] = pd.to_datetime(b["timestamp"])
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            d["ret"] = c.pct_change()
            d["fwd1"] = c.shift(-1) / c - 1
            d["fwd3"] = c.shift(-3) / c - 1
            rng = (h - l) / c.shift(1)
            d["rr"] = (h - l) / (h - l).rolling(20).mean()
            d["clv"] = ((c - l) / (h - l)).where(h > l)
            d["vol20"] = d["ret"].rolling(20).std()
            d["zret"] = d["ret"] / d["vol20"].shift(1)
            d["falling"] = (b["regime"] != "chop").astype(int)
            d["coin"] = coin; d["win"] = w
            d["pos"] = b["postRebalance_current_allocation"].astype(float)
            d["fc"] = b["forecast"].astype(float)
            d["wd"] = d["ts"].dt.dayofweek
            d["year"] = d["ts"].dt.year
            d["volu"] = b["volume"].astype(float) / b["volume"].astype(float).rolling(20).mean()
            rows.append(d)
    p = pd.concat(rows, ignore_index=True)
    drift = p.groupby("coin")["fwd1"].mean()
    p["ex1"] = p["fwd1"] - p["coin"].map(drift)
    p["ex1n"] = p["ex1"] / p["vol20"]
    out = {}
    def summ(g):
        x = g["ex1"].dropna()
        return pd.Series({"n": len(x), "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    p["up"] = (p["ret"] > 0).astype(int)
    p["rrq"] = pd.qcut(p["rr"], 5, labels=False)
    out["ex1 by falling, up, rr quintile"] = p.dropna(subset=["rr"]).groupby(["falling","up","rrq"]).apply(summ)
    p["zq"] = pd.qcut(p["zret"], 7, labels=False)
    out["ex1 by falling, zret septile"] = p.dropna(subset=["zret"]).groupby(["falling","zq"]).apply(summ)
    p["clq"] = pd.qcut(p["clv"], 5, labels=False)
    out["ex1 by falling, close-location quintile"] = p.dropna(subset=["clv"]).groupby(["falling","clq"]).apply(summ)
    out["ex1 by weekday"] = p.groupby("wd").apply(summ)
    p["vq"] = p.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["ex1 by falling, vol tercile"] = p.groupby(["falling","vq"]).apply(summ)
    out["share falling"] = float(p["falling"].mean())
    # corr in falling, by year: ret vs ex1
    f = p[p.falling==1].dropna(subset=["zret","ex1"])
    out["falling: slope ex1 on zret by year"] = f.groupby("year").apply(lambda g: pd.Series({"n":len(g),"corr":g["zret"].corr(g["ex1"])}))
    return out
