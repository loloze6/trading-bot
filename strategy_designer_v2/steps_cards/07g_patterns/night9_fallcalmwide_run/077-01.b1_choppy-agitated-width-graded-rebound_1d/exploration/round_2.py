def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            nxt2 = c.shift(-2) / c - 1
            rng = (h - l)
            width = rng / rng.rolling(30, min_periods=30).mean()
            loc = (c - l) / rng.replace(0, np.nan)
            sd30 = r.rolling(30, min_periods=30).std()
            tr60 = c / c.shift(60) - 1
            tr20 = c / c.shift(20) - 1
            vol_rel = sd30 / sd30.rolling(90, min_periods=60).median()
            rows.append(pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "nxt": nxt, "nxt2": nxt2, "r": r, "width": width, "loc": loc,
                "z": r / sd30, "tr60": tr60, "tr20": tr20, "volrel": vol_rel,
                "upwick": (h - np.maximum(o, c)) / rng.replace(0, np.nan)}))
    df = pd.concat(rows, ignore_index=True).dropna(subset=["nxt"])
    df["ex"] = df["nxt"] - df["coin"].map(df.groupby("coin")["nxt"].mean())
    d2 = df.dropna(subset=["nxt2"])
    df["ex2"] = df["nxt2"] - df["coin"].map(d2.groupby("coin")["nxt2"].mean())
    df["day"] = df["ts"].dt.floor("D"); df["year"] = df["ts"].dt.year

    def ct(sub, col="ex"):
        s = sub.dropna(subset=[col])
        if len(s) < 10:
            return pd.Series({"n": len(s), "days": np.nan, "mean%": np.nan, "t": np.nan})
        v = s[col]; m = v.mean()
        dev = (v - m).groupby(s["day"]).sum(); D = len(dev)
        se = np.sqrt((dev ** 2).sum() * D / (D - 1)) / len(v)
        return pd.Series({"n": len(v), "days": D, "mean%": 100 * m, "t": m / se})

    s = df.dropna(subset=["width", "loc", "z"]).copy()
    out = {}
    s["score"] = s["width"] * (0.5 - s["loc"])  # positive: wide and low close
    s["sq"] = pd.qcut(s["score"], 10, labels=[f"d{i}" for i in range(1, 11)])
    out["score decile (width x (0.5-loc))"] = s.groupby("sq", observed=True).apply(ct)
    out["score decile, 2-day"] = s.groupby("sq", observed=True).apply(ct, col="ex2")
    top = s[s["sq"] == "d10"]
    out["d10 by year"] = top.groupby("year").apply(ct)
    out["d10 by window"] = top.groupby("win").apply(ct)
    out["d10 by coin"] = top.groupby("coin").apply(ct)
    # is it just the fall? split by today's z
    top2 = top.assign(zb=pd.cut(top["z"], [-99, -2, -1, 0, 99]))
    out["d10 by today's z"] = top2.groupby("zb", observed=True).apply(ct)
    # fall z<-1 split by close loc
    fl = s[s["z"] < -1].assign(lb=pd.cut(s["loc"], [-0.01, 0.2, 0.5, 1.01]))
    out["falls z<-1 by close loc"] = fl.groupby("lb", observed=True).apply(ct)
    # agitation/trend for d10
    top3 = top.dropna(subset=["volrel"]).assign(agit=lambda x: np.where(x["volrel"] > 1, "agit", "calm"),
        trend=lambda x: np.where(x["tr20"] > 0.05, "up20", np.where(x["tr20"] < -0.05, "down20", "flat20")))
    out["d10 by agit"] = top3.groupby("agit").apply(ct)
    out["d10 by 20d trend"] = top3.groupby("trend").apply(ct)
    # high-close wide days: negative score bottom decile
    bot = s[s["sq"] == "d1"].dropna(subset=["tr20"]).assign(
        trend=lambda x: np.where(x["tr20"] > 0.05, "up20", np.where(x["tr20"] < -0.05, "down20", "flat20")))
    out["d1 (wide high close) by 20d trend"] = bot.groupby("trend").apply(ct)
    out["d1 by year"] = bot.groupby("year").apply(ct)
    return out
