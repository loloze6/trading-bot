def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]
            rng = (h - l) / c.shift(1)
            mr = rng.rolling(20, min_periods=20).mean()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "r0": c / c.shift(1) - 1,
                "ratio": rng / mr,
                "clv": (c - l) / (h - l).replace(0, np.nan),
                "n1": c.shift(-1) / c - 1,
                "n2": c.shift(-2) / c.shift(-1) - 1,
                "n3": c.shift(-3) / c.shift(-2) - 1,
                "ret20": c / c.shift(20) - 1,
                "regime": b["regime"].astype(str),
                "alloc": b["postRebalance_current_allocation"],
            })
            df["vol20"] = df["r0"].rolling(20).std()
            df["vol60"] = df["r0"].rolling(60).std()
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["n1"].transform("mean")
    d["u1"] = d["n1"] - drift
    d["u2"] = d["n2"] - d.groupby("coin")["n2"].transform("mean")
    d["day"] = d["ts"].dt.floor("D")
    d["inprof"] = d["regime"] != "chop"

    def tpool(sub, col):
        s = sub.dropna(subset=[col]).groupby("day")[col].sum()
        n = sub[col].notna().sum()
        if n < 5: return (n, np.nan, np.nan)
        m = sub[col].mean()
        se = np.sqrt((s - s.mean()*0 - 0).pow(2).sum()) / n if False else s.std(ddof=1) * np.sqrt(len(s)) / n
        return (int(n), m, m / se if se > 0 else np.nan)

    out = {}
    # 1. up days by ratio tercile, inside vs outside profile
    up = d[(d["r0"] > 0) & d["ratio"].notna()].copy()
    up["rq"] = pd.qcut(up["ratio"], 4, labels=["q1", "q2", "q3", "q4"])
    res = []
    for (p, q), g in up.groupby(["inprof", "rq"], observed=True):
        n, m, t = tpool(g, "u1"); n2, m2, t2 = tpool(g, "u2")
        res.append([p, q, n, m, t, m2, t2, g["ratio"].mean()])
    out["up_days_ratio_q_by_profile"] = pd.DataFrame(res, columns=["in_falling_agit", "q", "n", "u1", "t1", "u2", "t2", "ratio"])
    dn = d[(d["r0"] < 0) & d["ratio"].notna()].copy()
    dn["rq"] = pd.qcut(dn["ratio"], 4, labels=["q1", "q2", "q3", "q4"])
    res = []
    for (p, q), g in dn.groupby(["inprof", "rq"], observed=True):
        n, m, t = tpool(g, "u1"); n2, m2, t2 = tpool(g, "u2")
        res.append([p, q, n, m, t, m2, t2])
    out["down_days_ratio_q_by_profile"] = pd.DataFrame(res, columns=["in_falling_agit", "q", "n", "u1", "t1", "u2", "t2"])
    # 2. outside profile: wide up days by 20d trend sign
    o = up[(~up["inprof"]) & (up["ratio"] > 1)].copy()
    o["tr"] = pd.cut(o["ret20"], [-9, -0.1, 0, 0.1, 9], labels=["<-10", "-10..0", "0..10", ">10"])
    res = []
    for q, g in o.groupby("tr", observed=True):
        n, m, t = tpool(g, "u1"); res.append([q, n, m, t])
    out["outside_wide_up_by_ret20"] = pd.DataFrame(res, columns=["ret20", "n", "u1", "t1"])
    # 3. close location of wide up days (all profiles)
    wu = up[up["ratio"] > 1].copy()
    wu["cq"] = pd.cut(wu["clv"], [0, 0.33, 0.66, 1.01], labels=["low", "mid", "high"])
    res = []
    for (p, q), g in wu.groupby(["inprof", "cq"], observed=True):
        n, m, t = tpool(g, "u1"); res.append([p, q, n, m, t])
    out["wide_up_by_closeloc"] = pd.DataFrame(res, columns=["inprof", "clv", "n", "u1", "t1"])
    # 4. all days: next-day by r0 decile (all profiles), correlation
    d["r0q"] = pd.qcut(d["r0"], 10, labels=False, duplicates="drop")
    res = []
    for q, g in d.dropna(subset=["r0q"]).groupby("r0q"):
        n, m, t = tpool(g, "u1"); res.append([q, g["r0"].mean(), n, m, t])
    out["next_by_r0_decile_all"] = pd.DataFrame(res, columns=["dec", "r0", "n", "u1", "t1"])
    # 5. weekday
    d["wd"] = d["ts"].dt.dayofweek
    res = []
    for q, g in d.groupby("wd"):
        n, m, t = tpool(g, "u1"); res.append([q, n, m, t])
    out["next_by_weekday_of_signal"] = pd.DataFrame(res, columns=["wd", "n", "u1", "t1"])
    # 6. vol regime: vol20/vol60
    d["vr"] = d["vol20"] / d["vol60"]
    d["vrq"] = pd.qcut(d["vr"], 4, labels=False, duplicates="drop")
    res = []
    for (q, s), g in d.dropna(subset=["vrq"]).groupby(["vrq", d["r0"] > 0]):
        n, m, t = tpool(g, "u1"); res.append([q, s, n, m, t])
    out["next_by_volratio_q_and_sign"] = pd.DataFrame(res, columns=["vrq", "up", "n", "u1", "t1"])
    out["regime_counts"] = d["regime"].value_counts()
    # 7. book by window/year
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["win"] = w; x["coin"] = coin; dd.append(x)
    dd = pd.concat(dd)
    bk = dd.groupby(["win", "day"])["book_return"].mean().reset_index()
    out["book_by_window"] = bk.groupby("win")["book_return"].agg(["mean", "std", "count"])
    return out
