def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            o, h, l, c = b["open"], b["high"], b["low"], b["close"]
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "oc": c / o - 1,
                "rng": (h - l) / o,
                "clv": (c - l) / (h - l).replace(0, np.nan),
                "r1": c.shift(-1) / c - 1,
                "r2": c.shift(-2) / c - 1,
                "r1b": c.shift(-2) / c.shift(-1) - 1,
                "ret5": c / c.shift(5) - 1,
                "inprof": (b["regime"] == "unknown").astype(int),
                "fc": b["forecast"],
                "alloc": b["postRebalance_current_allocation"],
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
            })
            rows.append(d)
    df = pd.concat(rows, ignore_index=True)
    drift = df.groupby("coin")["r1"].mean()
    df["x1"] = df["r1"] - df["coin"].map(drift)
    df["x1b"] = df["r1b"] - df["coin"].map(drift)
    sd = df.groupby("coin")["r1"].std()
    df["ocz"] = df["oc"] / df["coin"].map(sd)
    out = {}

    def tab(sub, key, col="x1"):
        g = sub.dropna(subset=[col]).groupby(key)[col]
        r = g.agg(["count", "mean", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r.drop(columns="std").round(5)

    # 1) oc quintile buckets by profile
    df["ocq"] = pd.qcut(df["oc"], 10, labels=False, duplicates="drop")
    out["oc decile next-day excess, in profile"] = tab(df[df.inprof == 1], "ocq")
    out["oc decile next-day excess, out of profile"] = tab(df[df.inprof == 0], "ocq")
    out["oc decile, day-after-next excess, in profile"] = tab(df[df.inprof == 1], "ocq", "x1b")

    # 2) regression slopes of x1 on oc, in/out profile, separately for down and up days
    res = {}
    for p in [0, 1]:
        for side, m in [("down", df.oc < 0), ("up", df.oc > 0)]:
            s = df[(df.inprof == p) & m].dropna(subset=["x1"])
            lr = stats.linregress(s["oc"], s["x1"])
            res[f"prof{p}_{side}"] = [len(s), lr.slope, lr.slope / lr.stderr]
    out["slope x1 on oc"] = pd.DataFrame(res, index=["n", "slope", "t"]).T.round(4)

    # 3) range and close location given down day, in profile
    s = df[(df.inprof == 1) & (df.oc < 0)].dropna(subset=["x1"]).copy()
    s["clvq"] = pd.qcut(s["clv"], 3, labels=False, duplicates="drop")
    out["in-prof down days by close location tercile"] = tab(s, "clvq")
    s["r5q"] = pd.qcut(s["ret5"], 3, labels=False, duplicates="drop")
    out["in-prof down days by 5d return tercile"] = tab(s, "r5q")
    out["in-prof down days by weekday"] = tab(s, "wd")
    out["in-prof down days by year"] = tab(s, "year")
    out["in-prof down days by coin"] = tab(s, "coin")

    # 4) out of profile large drops (bottom decile) by weekday / coin
    so = df[(df.inprof == 0) & (df.ocq == 0)]
    out["out-prof bottom-decile drop by coin"] = tab(so, "coin")

    # 5) all days by weekday
    out["all days next-day excess by weekday"] = tab(df, "wd")

    # 6) book daily returns: largest gains/losses
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["win"] = w
            dd.append(t)
    D = pd.concat(dd, ignore_index=True)
    bk = D.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book daily: n, mean, share>0 on nonzero"] = pd.Series({
        "n": len(bk), "mean": bk.mean(),
        "share_pos_nonzero": (bk[bk != 0] > 0).mean(),
        "top10_sum_share_of_total": bk.nlargest(10).sum() / bk.sum(),
        "bottom10_sum": bk.nsmallest(10).sum()})
    return out
