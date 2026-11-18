def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    dd = []
    for coin, wins in data["days"].items():
        for w, g in wins.items():
            g = g.reset_index(drop=True).copy(); g["coin"] = coin; g["win"] = w
            c = g["close"].astype(float)
            g["yr"] = pd.to_datetime(g["day"]).dt.year
            g["r1"] = g["coin_return"]
            g["vol20"] = g["r1"].rolling(20).std()
            g["z1"] = g["r1"] / g["vol20"]
            g["f1"] = c.shift(-1) / c - 1
            g["f3"] = c.shift(-3) / c - 1
            g["pos"] = np.arange(len(g))
            dd.append(g)
    dd = pd.concat(dd, ignore_index=True)
    dd["ex1"] = dd["f1"] - dd.groupby("coin")["f1"].transform("mean")
    x = dd.dropna(subset=["r1", "ex1", "z1"]).copy()
    def sl(d, xc, yc):
        s = stats.linregress(d[xc], d[yc]); return pd.Series(dict(slope=s.slope, t=s.slope/s.stderr, n=len(d)))
    out["f1_on_r1_pooled"] = sl(x, "r1", "ex1")
    out["f1_on_z1_pooled"] = sl(x, "z1", "ex1")
    out["f1_on_z1_by_coin"] = x.groupby("coin").apply(lambda g: sl(g, "z1", "ex1"))
    out["f1_on_z1_by_year"] = x.groupby("yr").apply(lambda g: sl(g, "z1", "ex1"))
    x["zq"] = pd.qcut(x["z1"], 10, labels=False)
    out["ex1_by_z_decile"] = x.groupby("zq").agg(mean_ex1=("ex1", "mean"), n=("ex1", "size"), zlo=("z1", "min"), zhi=("z1", "max"),
                                               t=("ex1", lambda v: v.mean()/v.std()*np.sqrt(len(v))))
    # down vs up side separately
    out["f1_on_z1_down_days"] = sl(x[x.z1 < 0], "z1", "ex1")
    out["f1_on_z1_up_days"] = sl(x[x.z1 > 0], "z1", "ex1")
    # 3-day non-overlapping
    y = dd[dd["pos"] % 3 == 0].dropna(subset=["z1", "f3"]).copy()
    y["ex3"] = y["f3"] - y.groupby("coin")["f3"].transform("mean")
    out["f3_on_z1_nonoverlap"] = sl(y, "z1", "ex3")
    # by vol tercile
    x["vt"] = pd.qcut(x["vol20"], 3, labels=["lo", "mid", "hi"])
    out["f1_on_z1_by_vol"] = x.groupby("vt").apply(lambda g: sl(g, "z1", "ex1"))
    # book: long vs short contribution
    br = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            a = b["postRebalance_current_allocation"].astype(float)
            g = a * (c.shift(-1) / c - 1)
            br.append(pd.DataFrame(dict(a=a, g=g, coin=coin)))
    br = pd.concat(br).dropna()
    br["side"] = np.where(br.a > 0, "long", np.where(br.a < 0, "short", "flat"))
    out["gain_by_side"] = br.groupby(["coin", "side"]).g.agg(["mean", "count", lambda v: v.mean()/v.std()*np.sqrt(len(v))])
    # book worst days context
    dd2 = dd.dropna(subset=["book_return"])
    q = dd2["book_return"].quantile([0.02, 0.98])
    out["coin_ret_on_book_tail_days"] = pd.DataFrame({
        "worst2pct": dd2[dd2.book_return <= q.iloc[0]][["r1", "vol20"]].mean(),
        "best2pct": dd2[dd2.book_return >= q.iloc[1]][["r1", "vol20"]].mean(),
        "all": dd2[["r1", "vol20"]].mean()})
    return out
