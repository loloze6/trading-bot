def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            f = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "r1f": c.shift(-1) / c - 1,
                "fwd5": c.shift(-5) / c - 1,
                "near30": c / b["high"].astype(float).rolling(30).max() - 1,
                "near90": c / b["high"].astype(float).rolling(90, min_periods=60).max() - 1,
                "r20": c / c.shift(20) - 1,
                "wd": ts.dt.dayofweek, "yr": ts.dt.year,
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            rows.append(f)
    d = pd.concat(rows, ignore_index=True)
    d["ex1"] = d["r1f"] - d.groupby("coin")["r1f"].transform("mean")
    res = {}
    # next-day return by weekday of the decision close (all bars, overlap-free at 1 day)
    x = d.dropna(subset=["ex1"])
    wd = x.groupby("wd")["ex1"].agg(["size", "mean", "std"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["size"]))
    res["next_day_by_weekday"] = wd.round(5)
    # 5-day by weekday over each of the 5 grid offsets
    out = {}
    for k in range(5):
        g = d[d["pos"] % 5 == k].dropna(subset=["fwd5"]).copy()
        g["ex5"] = g["fwd5"] - g.groupby("coin")["fwd5"].transform("mean")
        s = g.groupby("wd")["ex5"].agg(["size", "mean", "std"])
        out["off%d" % k] = (s["mean"] / (s["std"] / np.sqrt(s["size"]))).round(2)
    res["fwd5_t_by_weekday_per_offset"] = pd.DataFrame(out)
    # next-day by weekday, by year (t)
    p = x.groupby(["yr", "wd"])["ex1"].agg(["size", "mean", "std"])
    p["t"] = p["mean"] / (p["std"] / np.sqrt(p["size"]))
    res["next_day_t_year_x_weekday"] = p["t"].unstack().round(2)
    # by coin: mean next-day excess on decision weekday
    q = x.groupby(["coin", "wd"])["ex1"].mean().unstack() * 100
    res["next_day_pct_coin_x_weekday"] = q.round(3)
    # near30 grading with 5-day grid offset 0
    g = d[d["pos"] % 5 == 0].dropna(subset=["fwd5", "near30"]).copy()
    g["ex5"] = g["fwd5"] - g.groupby("coin")["fwd5"].transform("mean")
    g["q"] = g.groupby("coin")["near30"].transform(lambda s: pd.qcut(s.rank(method="first"), 10, labels=False))
    n = g.groupby("q")["ex5"].agg(["size", "mean", "std"])
    n["t"] = n["mean"] / (n["std"] / np.sqrt(n["size"]))
    res["near30_deciles"] = n.round(4)
    top = g[g.q >= 8]
    ty = top.groupby("yr")["ex5"].agg(["size", "mean"])
    res["near30_top20_by_year"] = ty.round(4)
    res["spearman_near30_ex5"] = pd.Series(stats.spearmanr(g["near30"], g["ex5"])[:2], index=["rho", "p"]).round(4)
    # book by weekday
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["win"] = w; dd.append(t)
    D = pd.concat(dd, ignore_index=True)
    bk = D.groupby(["win", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).dropna().reset_index()
    bk["wd"] = pd.to_datetime(bk["day"]).dt.dayofweek
    bw = bk.groupby("wd").agg(n=("br", "size"), book=("br", "mean"), hold=("cr", "mean"))
    bw["book_t"] = bk.groupby("wd")["br"].mean() / (bk.groupby("wd")["br"].std() / np.sqrt(bw["n"]))
    res["book_by_weekday_of_day"] = bw.round(5)
    return res
