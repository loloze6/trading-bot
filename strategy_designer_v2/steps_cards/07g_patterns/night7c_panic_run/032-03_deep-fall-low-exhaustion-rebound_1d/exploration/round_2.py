def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []; rows1 = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            rng = (h - l) / c
            lw = (np.minimum(o, c) - l) / c
            ts = pd.to_datetime(b["timestamp"])
            f = pd.DataFrame({
                "coin": coin, "win": w, "yr": ts.dt.year, "day": ts.dt.floor("D"),
                "pos": np.arange(len(b)),
                "ret1": c.pct_change(), "ret30": c.pct_change(30),
                "lw_abs": lw,
                "lw_frac": lw / (h - l) * c,
                "lw_rel": lw / rng.rolling(20).mean(),
                "rngrel": rng / rng.rolling(20).mean(),
                "dist_high30": c / c.shift(1).rolling(30).max() - 1,
                "dh30_vol": (c / c.shift(1).rolling(30).max() - 1) / rng.rolling(30).mean(),
                "fwd5": c.shift(-H) / c - 1, "fwd1": c.shift(-1) / c - 1,
            })
            rows.append(f[(f.pos % H == 0) & f.fwd5.notna()])
            rows1.append(f[f.fwd1.notna()])
    g = pd.concat(rows); g1 = pd.concat(rows1)
    g["u5"] = g["fwd5"] - g.groupby("coin")["fwd5"].transform("mean")
    g1["u1"] = g1["fwd1"] - g1.groupby("coin")["fwd1"].transform("mean")

    def cl_t(d, col):
        s = d.groupby("day")[col].apply(lambda x: (x - d[col].mean()).sum())
        G = len(s); se = np.sqrt((s**2).sum() * G/(G-1)) / len(d)
        return d[col].mean()/se, G

    out = {}
    # decile grading, pooled ranks within coin
    for ft in ["lw_abs", "lw_frac", "lw_rel", "dist_high30", "dh30_vol"]:
        d = g[[ft, "u5", "coin", "day"]].dropna().copy()
        d["q"] = pd.qcut(d.groupby("coin")[ft].rank(pct=True), 5, labels=False)
        out["q5_" + ft] = d.groupby("q")["u5"].agg(["count", "mean"]).round(4)
    # top-minus-bottom quintile by year and by coin, for lw_abs and dist_high30
    for ft in ["lw_abs", "dist_high30"]:
        d = g[[ft, "u5", "coin", "yr", "day"]].dropna().copy()
        d["r"] = d.groupby("coin")[ft].rank(pct=True)
        res = []
        for key in ["yr", "coin"]:
            for k, x in d.groupby(key):
                rho = stats.spearmanr(x["r"], x["u5"])[0]
                res.append([key, str(k), len(x), round(rho, 3)])
        out["byyrcoin_" + ft] = pd.DataFrame(res, columns=["by", "k", "n", "rho"])
        d["top"] = d["r"] > 0.8
        tq = d[d.top]; t, G = cl_t(tq, "u5")
        out["top_clusterT_" + ft] = f"mean {tq.u5.mean():.4f} t {t:.2f} days {G}"
    # daily reversal: size and by range regime
    d = g1[["ret1", "u1", "rngrel", "coin"]].dropna().copy()
    d["rq"] = pd.qcut(d.groupby("coin")["ret1"].rank(pct=True), 5, labels=False)
    d["vq"] = pd.qcut(d.groupby("coin")["rngrel"].rank(pct=True), 3, labels=["low", "mid", "high"])
    out["rev1_by_ret1q_vol"] = d.pivot_table(index="rq", columns="vq", values="u1", aggfunc="mean").round(4)
    # lower wick conditional on 30d fall
    d = g[["lw_abs", "ret30", "u5", "coin"]].dropna().copy()
    d["lq"] = pd.qcut(d.groupby("coin")["lw_abs"].rank(pct=True), 3, labels=["small", "mid", "big"])
    d["fq"] = pd.qcut(d.groupby("coin")["ret30"].rank(pct=True), 3, labels=["fell", "mid", "rose"])
    out["lw_x_ret30"] = d.pivot_table(index="lq", columns="fq", values="u5", aggfunc=["count", "mean"]).round(4)
    return out
