def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            b["coin"] = coin; b["win"] = w; b["pos"] = np.arange(len(b))
            b["r1"] = c.pct_change()
            b["r3p"] = c / c.shift(3) - 1
            hi30 = c.rolling(30, min_periods=30).max()
            b["pbelow"] = c / hi30 - 1
            sd = b["r1"].rolling(20, min_periods=10).std()
            b["sd20"] = sd
            b["z3"] = b["r3p"] / (sd * np.sqrt(3))
            b["f1"] = c.shift(-1) / c - 1
            b["f2"] = c.shift(-2) / c.shift(-1) - 1
            b["f3"] = c.shift(-3) / c - 1
            b["fa"] = b["regime"].isin(["mean_reversion", "unknown"])
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b)
    d = pd.concat(rows, ignore_index=True)
    drift = {h: d[d["pos"] % h == 0].groupby("coin")["f%d" % h].mean() for h in (1, 3)}
    fa = d[d["fa"]].copy()
    out = {}
    def slope_info(g, feat, y):
        g = g.dropna(subset=[feat, y])
        sl = stats.linregress(g[feat], g[y])
        rho, p = stats.spearmanr(g[feat], g[y])
        return dict(n=len(g), slope_t=sl.slope / sl.stderr, spearman=rho, sp_p=p, mean=g[y].mean(),
                    t_mean=g[y].mean() / (g[y].std() / np.sqrt(len(g))))
    # A: up days only, next-day short, graded by r1 (brief's short half)
    g1 = fa.copy(); g1["s1"] = -(g1["f1"] - g1["coin"].map(drift[1]))
    g1["s2"] = -(g1["f2"] - g1["coin"].map(drift[1]))
    up = g1[g1["r1"] > 0]
    res = {}
    res["up r1->s1"] = slope_info(up, "r1", "s1")
    res["up r1->s1 winsor"] = slope_info(up.assign(r1=up["r1"].clip(upper=up["r1"].quantile(0.95)), s1=up["s1"].clip(*up["s1"].quantile([0.02, 0.98]))), "r1", "s1")
    res["up r1->s2 (day after)"] = slope_info(up, "r1", "s2")
    res["down r1->s1"] = slope_info(g1[g1["r1"] < 0], "r1", "s1")
    out["daily split"] = pd.DataFrame(res).T
    # B: h3 near-high (raw pbelow) and r3p, all three grid offsets
    res = {}
    for off in range(3):
        g = fa[(fa["pos"] % 3) == off].copy()
        g["s"] = -(g["f3"] - g["coin"].map(drift[3]))
        for feat in ["pbelow", "r3p", "z3"]:
            res["%s off%d" % (feat, off)] = slope_info(g, feat, "s")
            gg = g.dropna(subset=[feat, "s"])
            top = gg[gg[feat] >= gg[feat].quantile(0.8)]
            res["%s off%d top20" % (feat, off)] = dict(n=len(top), mean=top["s"].mean(),
                t_mean=top["s"].mean() / (top["s"].std() / np.sqrt(len(top))))
    out["h3 by grid offset"] = pd.DataFrame(res).T
    # C: pbelow h3 grid 0, by coin and by up/down day, and top quintile by coin
    g = fa[fa["pos"] % 3 == 0].copy(); g["s"] = -(g["f3"] - g["coin"].map(drift[3]))
    g = g.dropna(subset=["pbelow", "s"])
    q80 = g["pbelow"].quantile(0.8)
    res = {}
    for coin, gc in g.groupby("coin"):
        res[coin] = slope_info(gc, "pbelow", "s")
        tp = gc[gc["pbelow"] >= q80]; res[coin + " top"] = dict(n=len(tp), mean=tp["s"].mean())
    res["up days"] = slope_info(g[g["r1"] > 0], "pbelow", "s")
    res["down days"] = slope_info(g[g["r1"] <= 0], "pbelow", "s")
    out["pbelow h3 splits"] = pd.DataFrame(res).T
    # D: day-clustered t for pbelow top quintile, all offsets pooled per day
    allg = fa.copy(); allg["s"] = -(allg["f3"] - allg["coin"].map(drift[3]))
    allg = allg.dropna(subset=["pbelow", "s"])
    allg["q"] = pd.qcut(allg["pbelow"], 5, labels=False)
    t = allg.groupby("q")["s"].agg(["size", "mean"])
    out["pbelow quintile all bars (overlapping, info)"] = t
    # E: by window for top quintile grid0
    tp = g[g["pbelow"] >= q80]
    out["top pbelow by window"] = tp.groupby("win")["s"].agg(["size", "mean"])
    return out
