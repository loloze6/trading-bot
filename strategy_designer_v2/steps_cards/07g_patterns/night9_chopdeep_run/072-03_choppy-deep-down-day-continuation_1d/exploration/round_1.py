def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]
            r = c.pct_change()
            hi = c.rolling(20, min_periods=20).max()
            sd = r.rolling(20, min_periods=20).std()
            depth = (c / hi - 1) / sd
            nxt = c.shift(-1) / c - 1
            rng = (b["high"] - b["low"]) / b["close"]
            clpos = (b["close"] - b["low"]) / (b["high"] - b["low"])
            r5 = c / c.shift(5) - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "r": r, "depth": depth, "nxt": nxt,
                               "rng_z": rng / rng.rolling(20, min_periods=20).mean(),
                               "clpos": clpos, "r5z": r5 / (sd * np.sqrt(5)), "rz": r / sd,
                               "regime": b["regime"], "wd": ts.dt.weekday, "yr": ts.dt.year,
                               "pos": b["postRebalance_current_allocation"]})
            rows.append(df)
    d = pd.concat(rows).dropna(subset=["nxt", "r", "depth"])
    mean_coin = d.groupby("coin")["nxt"].transform("mean")
    d["ex"] = d["nxt"] - mean_coin
    d["chop"] = d["regime"] != "chop"
    d["up"] = d["r"] > 0

    def summ(g):
        x = g["ex"]
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    out = {}
    out["regime counts"] = d["regime"].value_counts()
    d["dq"] = d.groupby(["chop", "up"])["depth"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["depth quintile by choppy/up"] = d.groupby(["chop", "up", "dq"]).apply(summ)
    d["rzq"] = pd.qcut(d["rz"].rank(method="first"), 5, labels=False)
    out["day move z quintile by choppy"] = d.groupby(["chop", "rzq"]).apply(summ)
    d["r5q"] = pd.qcut(d["r5z"].rank(method="first"), 5, labels=False)
    out["5d move z quintile by choppy"] = d.groupby(["chop", "r5q"]).apply(summ)
    d["clq"] = pd.qcut(d["clpos"].rank(method="first"), 5, labels=False)
    out["close position quintile by choppy"] = d.groupby(["chop", "clq"]).apply(summ)
    d["rgq"] = pd.qcut(d["rng_z"].rank(method="first"), 5, labels=False)
    out["range z quintile by choppy"] = d.groupby(["chop", "rgq"]).apply(summ)
    out["weekday"] = d.groupby("wd").apply(summ)
    out["year"] = d.groupby("yr").apply(summ)
    # corr tests
    res = {}
    for name, g in [("all", d), ("chop", d[d.chop]), ("nonchop", d[~d.chop])]:
        for col in ["depth", "rz", "r5z", "clpos", "rng_z"]:
            gg = g[[col, "ex"]].dropna()
            rho, p = stats.spearmanr(gg[col], gg["ex"])
            res[(name, col)] = {"rho": rho, "n": len(gg), "p": p}
    out["spearman"] = pd.DataFrame(res).T
    return out
