def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            hh = b["high"].rolling(20, min_periods=20).max()
            ll = b["low"].rolling(20, min_periods=20).min()
            sd = r.rolling(20, min_periods=20).std()
            depth = (c - hh) / hh / sd
            pos = (c - ll) / (hh - ll)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w, "r": r, "nxt": nxt, "depth": depth, "pos": pos,
                "sd": sd, "regime": b["regime"], "alloc": b["postRebalance_current_allocation"],
                "wd": ts.dt.dayofweek, "year": ts.dt.year,
                "rng": (b["high"] - b["low"]) / c,
                "clpos": (c - b["low"]) / (b["high"] - b["low"]),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["falling"] = d["regime"].isin(["mean_reversion", "unknown"])
    mu = d.groupby("coin")["nxt"].mean()
    d["ex"] = d["nxt"] - d["coin"].map(mu)
    d = d.dropna(subset=["ex"])

    def stat(g):
        x = g["ex"]
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    out = {}
    d["up"] = d["r"] > 0
    out["trend_x_up"] = d.groupby(["falling", "up"]).apply(stat)
    dd = d.dropna(subset=["depth"]).copy()
    dd["dq"] = dd.groupby(["falling", "up"])["depth"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["depth_q_by_trend_up"] = dd.groupby(["falling", "up", "dq"]).apply(stat)
    dd["pq"] = dd.groupby(["falling", "up"])["pos"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["rangepos_q_by_trend_up"] = dd.groupby(["falling", "up", "pq"]).apply(stat)
    d["z"] = d["r"] / d["sd"]
    dz = d.dropna(subset=["z"]).copy()
    dz["zq"] = dz.groupby("falling")["z"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["dayz_q_by_trend"] = dz.groupby(["falling", "zq"]).apply(stat)
    dz["cq"] = pd.qcut(dz["clpos"].rank(method="first"), 5, labels=False)
    out["closepos_in_day_by_trend"] = dz.groupby(["falling", "cq"]).apply(stat)
    out["weekday_falling"] = d[d.falling].groupby("wd").apply(stat)
    out["weekday_all"] = d.groupby("wd").apply(stat)
    out["year_falling_up"] = d[d.falling & d.up].groupby("year").apply(stat)
    out["coin_falling_up"] = d[d.falling & d.up].groupby("coin").apply(stat)
    # book
    days = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; days.append(x)
    D = pd.concat(days)
    bk = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book_by_window"] = bk.groupby(level=0).agg(["mean", "count"]) * 1
    q = bk["book_return"]
    out["book_top_bottom_coin"] = pd.Series({
        "book top5% days coin ret%": 100 * bk.loc[q >= q.quantile(.95), "coin_return"].mean(),
        "book bottom5% days coin ret%": 100 * bk.loc[q <= q.quantile(.05), "coin_return"].mean(),
        "corr book coin": q.corr(bk["coin_return"])})
    return out
