def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            rng = (h - l).replace(0, np.nan)
            loc = (c - l) / rng
            r1 = c / c.shift(1) - 1
            nxt = c.shift(-1) / c - 1
            f = b["forecast"].astype(float).fillna(0)
            rise = (-(f - f.shift(1).fillna(0))) >= 2
            df = pd.DataFrame({"coin": coin, "win": w, "year": pd.to_datetime(b["timestamp"]).dt.year,
                               "ts": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                               "loc": loc, "r1": r1, "nxt": nxt, "case": rise, "regime": b["regime"].astype(str),
                               "rngpct": rng / c, "body": (c - o) / rng})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["nxt"].mean()
    d["unus"] = -(d["nxt"] - d["coin"].map(drift))
    d = d.dropna(subset=["nxt", "loc", "r1"])
    def summ(x):
        g = x.groupby("ts")["unus"].sum()
        n = len(x); G = len(g)
        m = x["unus"].mean()
        if G < 3: return pd.Series({"n": n, "days": G, "mean": m, "t": np.nan})
        se = np.sqrt((g - g.mean() * 0).pow(2).sum() * 0 + ((g - m * x.groupby("ts").size()) ** 2).sum() * G / (G - 1)) / n
        return pd.Series({"n": n, "days": G, "mean": m, "t": m / se if se > 0 else np.nan})
    cs = d[d["case"]].copy()
    out = {}
    out["cases_all"] = summ(cs)
    cs["locq"] = pd.qcut(cs["loc"], 4, labels=False)
    out["by_loc_quartile"] = cs.groupby("locq").apply(summ)
    cs["r1q"] = pd.qcut(cs["r1"], 4, labels=False)
    out["by_dayret_quartile"] = cs.groupby("r1q").apply(summ)
    cs["rngq"] = pd.qcut(cs["rngpct"], 4, labels=False)
    out["by_range_quartile"] = cs.groupby("rngq").apply(summ)
    out["by_coin"] = cs.groupby("coin").apply(summ)
    out["by_year"] = cs.groupby("year").apply(summ)
    out["by_window"] = cs.groupby("win").apply(summ)
    # in-profile non-cases and up-day high close outside profile
    d["upHigh"] = (d["r1"] > 0) & (d["loc"] > 0.5)
    d["inprof"] = d["regime"].isin(["mean_reversion", "unknown"])
    out["groups_profile_x_uphigh"] = d.groupby(["inprof", "upHigh"]).apply(summ)
    ip = d[d["inprof"]].copy()
    ip["updown"] = np.where(ip["r1"] > 0, "up", "down")
    ip["locb"] = pd.cut(ip["loc"], [-0.01, 0.25, 0.5, 0.75, 1.01], labels=False)
    out["inprof_updown_x_loc"] = ip.groupby(["updown", "locb"]).apply(summ)
    op = d[~d["inprof"] & d["upHigh"]].copy()
    op["r1q"] = pd.qcut(op["r1"], 4, labels=False)
    out["outprof_uphigh_by_dayret"] = op.groupby("r1q").apply(summ)
    out["regime_counts"] = d["regime"].value_counts()
    return out
