def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    rows1 = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            rng = (h - l) / c
            f = pd.DataFrame({
                "coin": coin, "win": w,
                "pos": np.arange(len(b)),
                "ret1": c.pct_change(),
                "ret5": c.pct_change(5),
                "ret30": c.pct_change(30),
                "rngrel": rng / rng.rolling(20).mean(),
                "rng30_vs_all": rng.rolling(30).mean() / rng.expanding(60).mean(),
                "clv": (c - l) / (h - l),
                "dist_low30": c / c.shift(1).rolling(30).min() - 1,
                "dist_high30": c / c.shift(1).rolling(30).max() - 1,
                "lowerwick": (np.minimum(o, c) - l) / c,
                "upperwick": (h - np.maximum(o, c)) / c,
                "volrel": b["volume"].astype(float) / b["volume"].astype(float).rolling(20).mean(),
                "mr": (b["regime"] == "mean_reversion").astype(int),
                "fc": b["forecast"].astype(float),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "fwd5": c.shift(-H) / c - 1,
                "fwd1": c.shift(-1) / c - 1,
            })
            rows.append(f[(f.pos % H == 0) & f.fwd5.notna()])
            rows1.append(f[f.fwd1.notna()])
    g = pd.concat(rows); g1 = pd.concat(rows1)
    g["u5"] = g["fwd5"] - g.groupby("coin")["fwd5"].transform("mean")
    g["s5"] = g["u5"] / g.groupby("coin")["fwd5"].transform("std")
    g1["u1"] = g1["fwd1"] - g1.groupby("coin")["fwd1"].transform("mean")
    feats = ["ret1", "ret5", "ret30", "rngrel", "rng30_vs_all", "clv", "dist_low30", "dist_high30", "lowerwick", "upperwick", "volrel"]
    sp = []
    for ft in feats:
        d = g[[ft, "u5", "s5", "coin"]].dropna()
        d["r"] = d.groupby("coin")[ft].rank(pct=True)
        q = pd.qcut(d["r"], 5, labels=False)
        r, p = stats.spearmanr(d["r"], d["s5"])
        top = d.loc[q == 4, "u5"]; bot = d.loc[q == 0, "u5"]
        t = stats.ttest_ind(top, bot, equal_var=False).statistic
        d1 = g1[[ft, "u1", "coin"]].dropna()
        d1["r"] = d1.groupby("coin")[ft].rank(pct=True)
        r1, p1 = stats.spearmanr(d1["r"], d1["u1"])
        sp.append([ft, len(d), round(r, 3), round(p, 3), round(bot.mean()*100, 2), round(top.mean()*100, 2), round(t, 2), len(d1), round(r1, 3), round(p1, 3)])
    sp = pd.DataFrame(sp, columns=["feat", "n5", "rho5", "p5", "Q1_u5%", "Q5_u5%", "tQ5-Q1", "n1", "rho1", "p1"])
    # interaction: vol level x past 5d return
    d = g[["ret5", "rngrel", "u5", "coin"]].dropna().copy()
    d["vq"] = pd.qcut(d.groupby("coin")["rngrel"].rank(pct=True), 3, labels=["lowvol", "mid", "highvol"])
    d["rq"] = pd.qcut(d.groupby("coin")["ret5"].rank(pct=True), 3, labels=["down", "mid", "up"])
    inter = d.groupby(["vq", "rq"])["u5"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    inter.columns = ["n", "mean_u5", "t"]
    wd = g1.groupby("wd")["u1"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    wd.columns = ["n", "mean_u1", "t"]
    mr = g.groupby("mr")["u5"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    yr = g.copy()
    return {"spearman_by_feature": sp, "vol_x_ret5": inter, "weekday_1d": wd, "regime_mr_grid": mr}
