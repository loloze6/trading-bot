def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            r = c.pct_change()
            s30 = r.rolling(30, min_periods=20).std()
            rng = (h - l) / c
            pos = np.where(h > l, 2 * (c - (h + l) / 2) / (h - l), 0.0)
            df = pd.DataFrame({
                "coin": coin, "w": w,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "inprof": (b["regime"] == "unknown").astype(int),
                "pos": pos, "rngv": rng / s30, "r0": r / s30,
                "ret60": c / c.shift(60) - 1,
                "vol_rel": s30 / r.rolling(120, min_periods=60).std(),
                "nxt": c.shift(-1) / c - 1,
                "nxt3": c.shift(-3) / c - 1,
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            df["s30"] = s30
            df["prod"] = df["pos"] * df["rngv"]
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["nxt"].transform("mean")
    d["ex"] = d["nxt"] - drift
    d["exz"] = d["ex"] / d["s30"]
    d = d.dropna(subset=["ex", "prod", "s30"])
    out = {}

    def tstat(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    # graded effect: quintiles of prod, in and out of profile
    d["pq"] = d.groupby("inprof")["prod"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["next-day ex by prod quintile, inprof"] = d.groupby(["inprof", "pq"])["ex"].apply(tstat).unstack()

    # trend approximation (60-day return in window) x vol_rel
    d["trend"] = pd.cut(d["ret60"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
    d["agit"] = np.where(d["vol_rel"] > 1, "agit", "calm")
    d["sig"] = -d["prod"]
    def slope(g):
        g = g.dropna(subset=["sig", "exz"])
        if len(g) < 30: return pd.Series({"n": len(g), "corr": np.nan, "t": np.nan})
        rr = stats.pearsonr(g["sig"], g["exz"])[0]
        return pd.Series({"n": len(g), "corr": rr, "t": rr * np.sqrt((len(g) - 2) / (1 - rr ** 2))})
    out["reversal corr by approx profile"] = d.groupby(["trend", "agit"]).apply(slope)

    # side split: low closes vs high closes, wide days (rngv top half), all bars
    d["side"] = np.where(d["pos"] < 0, "lowclose", "highclose")
    d["wide"] = d.groupby("coin")["rngv"].transform(lambda x: (x > x.median()).astype(int))
    out["ex by side x wide x inprof"] = d.groupby(["inprof", "side", "wide"])["ex"].apply(tstat).unstack()

    # returns after large moves (own return in usual moves)
    d["r0q"] = pd.qcut(d["r0"], 7, labels=False)
    out["next-day ex by today's move septile"] = d.groupby("r0q")["ex"].apply(tstat).unstack()
    out["3-day ex by today's move septile"] = d.assign(ex3=d["nxt3"] - 3 * drift).groupby("r0q")["ex3"].apply(tstat).unstack()

    # weekday
    out["next-day ex by weekday"] = d.groupby("wd")["ex"].apply(tstat).unstack()

    # vol level
    d["vq"] = pd.qcut(d["vol_rel"], 5, labels=False, duplicates="drop")
    out["next-day ex by vol_rel quintile"] = d.groupby("vq")["ex"].apply(tstat).unstack()

    # book by side
    dd = d[d["alloc"] != 0]
    dd = dd.assign(g=dd["alloc"] * dd["nxt"], dirn=np.where(dd["alloc"] > 0, "long", "short"))
    out["book gain by side"] = dd.groupby("dirn")["g"].apply(tstat).unstack()
    out["book gain by year"] = dd.groupby("year")["g"].apply(tstat).unstack()
    # trades
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    out["trades by side"] = tr.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return out
