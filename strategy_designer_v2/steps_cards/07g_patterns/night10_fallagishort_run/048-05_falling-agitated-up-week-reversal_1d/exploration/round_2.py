def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    recs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            b["s1"] = r1 / sd30
            b["s2"] = (c / c.shift(2) - 1) / (sd30 * np.sqrt(2))
            b["s3"] = (c / c.shift(3) - 1) / (sd30 * np.sqrt(3))
            b["sw"] = (c / c.shift(7) - 1) / (sd30 * np.sqrt(7))
            b["inprof"] = b["regime"].isin(["mean_reversion", "unknown"])
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            for H in [1, 2, 3, 5]:
                b["fwd%d" % H] = c.shift(-H) / c - 1
            b["coin"] = coin; b["win"] = w; b["i"] = np.arange(len(b))
            recs.append(b)
    B = pd.concat(recs)
    def cm(H):
        g = B[B["i"] % H == 0].dropna(subset=["fwd%d" % H])
        return g.groupby("coin")["fwd%d" % H].mean()
    res = {}
    for H in [1, 2, 3, 5]:
        m = cm(H)
        for off in range(min(H, 3)):
            g = B[(B["i"] % H == off) & B["inprof"]].dropna(subset=["fwd%d" % H, "s1"]).copy()
            g["y"] = g["fwd%d" % H] - g["coin"].map(m)
            for col in ["s1", "s3", "sw"]:
                d = g.dropna(subset=[col])
                sl = stats.linregress(d[col], d["y"])
                up = d[d[col] > 0]
                slu = stats.linregress(up[col], up["y"])
                res[(H, off, col)] = {"n": len(d), "slope_t_all": sl.slope / sl.stderr,
                                     "n_up": len(up), "slope_t_up": slu.slope / slu.stderr,
                                     "mean_y_up": up["y"].mean()}
    out["slopes by horizon, offset, measure"] = pd.DataFrame(res).T
    # main grid H=3 offset 0, s1 up side detail
    m = cm(3)
    g = B[(B["i"] % 3 == 0) & B["inprof"]].dropna(subset=["fwd3", "s1"]).copy()
    g["y"] = g["fwd3"] - g["coin"].map(m)
    up = g[g["s1"] > 0].copy()
    up["dev"] = up["y"] * up["s1"]
    out["s1 up: by coin"] = up.groupby("coin").apply(lambda d: pd.Series({"n": len(d), "mean_y": d["y"].mean(), "corr": d[["s1", "y"]].corr().iloc[0, 1]}))
    out["s1 up: by year"] = up.groupby("year").apply(lambda d: pd.Series({"n": len(d), "mean_y": d["y"].mean(), "corr": d[["s1", "y"]].corr().iloc[0, 1] if len(d) > 2 else np.nan}))
    up["t3"] = pd.qcut(up["s1"], 3, labels=False)
    out["s1 up terciles"] = up.groupby("t3").agg(lo=("s1", "min"), hi=("s1", "max"), n=("y", "size"), mean_y=("y", "mean"), mean_fwd=("fwd3", "mean"))
    # day-clustered t of weighted mean y (weight s1) on up side
    dd = up.groupby("day").apply(lambda d: (d["y"] * d["s1"]).sum())
    out["s1-weighted y, day clustered"] = pd.Series({"days": len(dd), "t": dd.mean() / (dd.std() / np.sqrt(len(dd))),
                                                    "weighted mean y": (up["y"] * up["s1"]).sum() / up["s1"].sum()})
    # in profile on all coins combined: s1 up, conditional on week sign
    up["wk_up"] = up["sw"] > 0
    out["s1 up split by week sign"] = up.groupby("wk_up").apply(lambda d: pd.Series({"n": len(d), "mean_y": d["y"].mean(), "corr": d[["s1", "y"]].corr().iloc[0, 1]}))
    # outside profile control
    o = B[(B["i"] % 3 == 0) & ~B["inprof"]].dropna(subset=["fwd3", "s1"]).copy()
    o["y"] = o["fwd3"] - o["coin"].map(m)
    ou = o[o["s1"] > 0]
    slo = stats.linregress(ou["s1"], ou["y"])
    out["outside profile s1 up"] = pd.Series({"n": len(ou), "slope_t": slo.slope / slo.stderr, "mean_y": ou["y"].mean()})
    return out
