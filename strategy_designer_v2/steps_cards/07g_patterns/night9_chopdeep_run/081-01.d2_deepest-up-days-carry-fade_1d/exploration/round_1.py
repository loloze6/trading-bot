def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c / c.shift(1) - 1
            sd = r1.rolling(20, min_periods=15).std()
            hi = c.rolling(20, min_periods=15).max()
            depth = (c / hi - 1) / sd
            d = pd.DataFrame({
                "coin": coin, "w": w, "ts": pd.to_datetime(b["timestamp"]),
                "r1": r1, "sd": sd, "depth": depth, "r1sw": r1 / sd,
                "f1": c.shift(-1) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "tr60": c / c.shift(60) - 1,
                "rng": (b["high"] - b["low"]) / c / sd,
                "clpos": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "pos": b["postRebalance_current_allocation"],
                "pos_i": np.arange(len(b)),
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu1 = D.groupby("coin")["f1"].mean()
    mu3 = D.groupby("coin")["f3"].mean()
    D["x1"] = D["f1"] - D["coin"].map(mu1)
    D["x3"] = D["f3"] - D["coin"].map(mu3)
    D["day"] = D["ts"].dt.floor("D")
    D["wd"] = D["ts"].dt.dayofweek
    D["up"] = D["r1"] > 0

    def summ(g, col="x1"):
        g = g.dropna(subset=[col])
        if len(g) < 5:
            return pd.Series({"n": len(g), "mean": np.nan, "t": np.nan})
        s = g.groupby("day")[col].sum()
        t = s.mean() / (s.std(ddof=1) / np.sqrt(len(s))) if len(s) > 2 else np.nan
        return pd.Series({"n": len(g), "days": len(s), "mean": g[col].mean(), "t": t})

    out = {}
    v = D.dropna(subset=["depth", "x1"]).copy()
    v["dq"] = pd.qcut(v["depth"].rank(method="first"), 5, labels=["deep", "q2", "q3", "q4", "shallow"])
    out["up_by_depth"] = v[v.up].groupby("dq").apply(summ)
    out["down_by_depth"] = v[~v.up].groupby("dq").apply(summ)
    # all days by own return in swing units
    v["rq"] = pd.qcut(v["r1sw"].rank(method="first"), 5, labels=["bigdown", "r2", "r3", "r4", "bigup"])
    out["all_by_r1sw"] = v.groupby("rq").apply(summ)
    out["depthq_x_r1q"] = v.groupby(["dq", "rq"])["x1"].mean().unstack()
    out["depthq_x_r1q_n"] = v.groupby(["dq", "rq"])["x1"].count().unstack()
    # trend profile
    v["trend"] = np.where(v["tr60"] > 0.1, "rising", np.where(v["tr60"] < -0.1, "falling", np.where(v["tr60"].notna(), "choppy", "na")))
    deepup = v[v.up & (v.dq == "deep")]
    out["deepup_by_trend"] = deepup.groupby("trend").apply(summ)
    out["all_up_by_trend"] = v[v.up].groupby("trend").apply(summ)
    out["down_by_trend"] = v[~v.up].groupby("trend").apply(summ)
    # close position in range for deep up days
    deepup2 = deepup.dropna(subset=["clpos"]).copy()
    deepup2["cq"] = pd.qcut(deepup2["clpos"].rank(method="first"), 3, labels=["lowclose", "mid", "highclose"])
    out["deepup_by_closepos"] = deepup2.groupby("cq").apply(summ)
    # 3-day horizon non-overlapping
    v3 = v[v.pos_i % 3 == 0]
    out["up_by_depth_3d"] = v3[v3.up].groupby("dq").apply(lambda g: summ(g, "x3"))
    # weekday all days
    out["all_by_weekday"] = v.groupby("wd").apply(summ)
    out["by_year_deepup"] = deepup.groupby(deepup.ts.dt.year).apply(summ)
    out["by_coin_deepup"] = deepup.groupby("coin").apply(summ)
    return out
