def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            df = pd.DataFrame({
                "coin": coin, "win": w, "wd": ts.dt.weekday.values,
                "year": ts.dt.year.values,
                "day": ts.dt.floor("D").values,
                "r1": (c / c.shift(1) - 1).values,
                "r5": (c / c.shift(5) - 1).values,
                "r20": (c / c.shift(20) - 1).values,
                "lo60": (c / c.rolling(60, min_periods=60).min() - 1).values,
                "hi60": (c / c.rolling(60, min_periods=60).max() - 1).values,
                "vol20": (c / c.shift(1) - 1).rolling(20).std().values,
                "nxt": (c.shift(-1) / c - 1).values,
                "alloc": b["postRebalance_current_allocation"].astype(float).values,
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["mu"] = d.groupby("coin")["nxt"].transform("mean")
    d["ex"] = d["nxt"] - d["mu"]
    d["z20"] = d["r20"] / (d["vol20"] * np.sqrt(20))
    d["z5"] = d["r5"] / (d["vol20"] * np.sqrt(5))
    d["z1"] = d["r1"] / d["vol20"]
    d["lo60z"] = d["lo60"] / (d["vol20"] * np.sqrt(20))
    d["hi60z"] = d["hi60"] / (d["vol20"] * np.sqrt(20))

    def tday(sub, col):
        s = sub.dropna(subset=[col, "ex"])
        x = (s[col].clip(-4, 4) * s["ex"]).groupby(s["day"]).sum()
        n = len(x)
        return pd.Series({"mean_bp": 1e4 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan, "days": n})

    out = {}
    # 1. signal z * next-day excess, by weekday of signal bar, for several features
    res = {}
    for col in ["z20", "z5", "z1", "lo60z", "hi60z"]:
        for wd in range(7):
            r = tday(d[d.wd == wd], col)
            res[(col, wd)] = r
    t = pd.DataFrame(res).T
    out["feature x next-day excess, by weekday of signal bar (4=Fri)"] = t["t"].unstack().round(2)
    # 2. unconditional next-day excess by weekday of next day
    g = d.dropna(subset=["ex"]).groupby("wd")["ex"]
    out["next-day excess by signal weekday (bp, t, n)"] = pd.DataFrame({"bp": 1e4 * g.mean(), "t": g.mean() / (g.std() / np.sqrt(g.count())), "n": g.count()}).round(2)
    # 3. next-day excess by z1 bucket, all days
    s = d.dropna(subset=["z1", "ex"]).copy()
    s["b"] = pd.cut(s["z1"], [-99, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 99])
    g = s.groupby("b", observed=True)["ex"]
    out["next-day excess by prior-day move z"] = pd.DataFrame({"bp": 1e4 * g.mean(), "t": g.mean() / (g.std() / np.sqrt(g.count())), "n": g.count()}).round(2)
    # 4. lo60 distance buckets
    s = d.dropna(subset=["lo60z", "ex"]).copy()
    s["b"] = pd.qcut(s["lo60z"], 5, duplicates="drop")
    g = s.groupby("b", observed=True)["ex"]
    out["next-day excess by distance to 60d low quintile"] = pd.DataFrame({"bp": 1e4 * g.mean(), "t": g.mean() / (g.std() / np.sqrt(g.count())), "n": g.count()}).round(2)
    # 5. Friday z20 effect by year and vol tercile
    f = d[(d.wd == 4)].dropna(subset=["z20", "ex"]).copy()
    out["Fri z20 x ex by year"] = f.groupby("year").apply(lambda x: tday(x, "z20")).round(2)
    f["vt"] = f.groupby("coin")["vol20"].transform(lambda v: pd.qcut(v, 3, labels=False))
    out["Fri z20 x ex by vol tercile"] = f.groupby("vt").apply(lambda x: tday(x, "z20")).round(2)
    out["Fri z20 x ex by coin"] = f.groupby("coin").apply(lambda x: tday(x, "z20")).round(2)
    # 6. weekend: Friday z20 vs Sunday next return (Saturday signal bar) and 2-day
    return out
