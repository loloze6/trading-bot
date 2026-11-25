def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            df = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "r": r, "z": z, "sd": sd,
                "n1": c.shift(-1) / c - 1,
                "n3": c.shift(-3) / c - 1,
                "pos": np.arange(len(b)),
                "agit": (b["regime"] != "chop").astype(int),
                "rng": (b["high"] - b["low"]) / c,
                "clv": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "r5": c / c.shift(5) - 1,
            })
            df["sdrank"] = sd.rolling(90, min_periods=30).rank(pct=True)
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    mu1 = d.groupby("coin")["n1"].transform("mean")
    d["x1"] = d["n1"] - mu1
    mu3 = d[d.pos % 3 == 0].groupby("coin")["n3"].mean()
    d["x3"] = d["n3"] - d["coin"].map(mu3)
    d["day"] = d["ts"].dt.floor("D")

    def ct(sub, col):
        s = sub.dropna(subset=[col])
        if len(s) < 10:
            return (np.nan, np.nan, len(s))
        m = s[col].mean()
        g = (s[col] - m).groupby(s["day"]).sum()
        se = np.sqrt((g ** 2).sum()) / len(s)
        return (m, m / se if se > 0 else np.nan, len(s))

    out = {}
    d["zb"] = pd.cut(d["z"], [-np.inf, -2, -1, -0.5, 0, 0.5, 1, 2, np.inf])
    res = []
    for (a, zb), s in d.groupby(["agit", "zb"], observed=True):
        m, t, n = ct(s, "x1")
        s3 = s[s.pos % 3 == 0]
        m3, t3, n3 = ct(s3, "x3")
        res.append([a, str(zb), n, m, t, n3, m3, t3])
    out["z_bins_next1_next3"] = pd.DataFrame(res, columns=["agit", "zbin", "n", "x1", "t1", "n3", "x3", "t3"])

    # clv (close location) bins
    d["cb"] = pd.qcut(d["clv"], 5, duplicates="drop")
    res = []
    for (a, cb), s in d.groupby(["agit", "cb"], observed=True):
        m, t, n = ct(s, "x1"); res.append([a, str(cb), n, m, t])
    out["clv_bins"] = pd.DataFrame(res, columns=["agit", "clv", "n", "x1", "t1"])

    # range scaled by sd
    d["rs"] = d["rng"] / d["sd"]
    d["rb"] = pd.qcut(d["rs"], 5, duplicates="drop")
    res = []
    for rb, s in d.groupby("rb", observed=True):
        m, t, n = ct(s, "x1"); res.append([str(rb), n, m, t, s["x1"].abs().mean()])
    out["range_bins"] = pd.DataFrame(res, columns=["rng/sd", "n", "x1", "t1", "abs_next"])

    # 5-day return scaled
    d["z5"] = d["r5"] / (d["sd"] * np.sqrt(5))
    d["z5b"] = pd.cut(d["z5"], [-np.inf, -1.5, -0.5, 0.5, 1.5, np.inf])
    res = []
    for (a, b_), s in d.groupby(["agit", "z5b"], observed=True):
        s3 = s[s.pos % 3 == 0]
        m3, t3, n3 = ct(s3, "x3"); m, t, n = ct(s, "x1")
        res.append([a, str(b_), n, m, t, n3, m3, t3])
    out["z5_bins"] = pd.DataFrame(res, columns=["agit", "z5", "n", "x1", "t1", "n3", "x3", "t3"])

    # weekday
    d["wd"] = d["ts"].dt.dayofweek
    res = []
    for wd, s in d.groupby("wd"):
        m, t, n = ct(s, "x1"); res.append([wd, n, m, t])
    out["weekday_next"] = pd.DataFrame(res, columns=["wd_of_signal", "n", "x1", "t1"])

    # per window book
    res = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            res.append([w, coin, dd["book_return"].mean(), dd["coin_return"].mean()])
    bw = pd.DataFrame(res, columns=["win", "coin", "book", "coin_r"])
    out["book_by_window"] = bw.groupby("win")[["book", "coin_r"]].mean()

    # forecast>0 by z bins: gains
    act = d[(d.alloc > 0)]
    act_zb = act.groupby("zb", observed=True)["x1"].agg(["count", "mean"])
    out["held_by_zbin"] = act_zb
    # corr of z with next by agit, per coin
    res = []
    for (coin, a), s in d.dropna(subset=["z", "x1"]).groupby(["coin", "agit"]):
        res.append([coin, a, len(s), stats.spearmanr(s.z, s.x1)[0]])
    out["coin_corr"] = pd.DataFrame(res, columns=["coin", "agit", "n", "rho"])
    return out
