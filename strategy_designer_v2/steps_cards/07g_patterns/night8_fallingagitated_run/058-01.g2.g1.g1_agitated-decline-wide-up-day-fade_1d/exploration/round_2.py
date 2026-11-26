def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({
                "coin": coin, "win": w, "day": ts.dt.floor("D"), "yr": ts.dt.year,
                "r0": r, "z0": r / sd, "rng": (b["high"] - b["low"]) / c / sd,
                "z2": (c / c.shift(2) - 1) / (sd * np.sqrt(2)),
                "z3": (c / c.shift(3) - 1) / (sd * np.sqrt(3)),
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1,
                "inprof": b["regime"] != "chop", "fc": b["forecast"],
                "pos": np.arange(len(b))}))
    d = pd.concat(rows, ignore_index=True)
    d["u1"] = d["f1"] - d["coin"].map(d.groupby("coin")["f1"].mean())
    d["u2"] = d["f2"] - d["coin"].map(d[d.pos % 2 == 0].groupby("coin")["f2"].mean())
    def ct(s, col):
        s = s.dropna(subset=[col]); n = len(s)
        if n < 10: return pd.Series({"n": n})
        m = s[col].mean(); ds = (s[col] - m).groupby(s["day"]).sum(); D = len(ds)
        return pd.Series({"n": n, "days": D, "mean": m, "t": m / (np.sqrt(D/(D-1)*(ds**2).sum())/n)})
    out = {}
    p = d[d.inprof].dropna(subset=["z0", "u1"]).copy()
    up = p[p.r0 > 0].copy(); dn = p[p.r0 <= 0].copy()
    up["q"] = pd.qcut(up.z0, 4, labels=False)
    out["inprof_up_next1_by_z0_quartile"] = up.groupby("q").apply(lambda x: ct(x, "u1"))
    up["qr"] = pd.qcut(up.rng, 4, labels=False)
    out["inprof_up_next1_by_range_quartile"] = up.groupby("qr").apply(lambda x: ct(x, "u1"))
    dn["q"] = pd.qcut(dn.z0, 4, labels=False)
    out["inprof_down_next1_by_z0_quartile"] = dn.groupby("q").apply(lambda x: ct(x, "u1"))
    # signed z0 as a linear predictor: -z0*u1 (fade) per case
    p["fade"] = -np.sign(p.z0) * p.u1
    p["fadew"] = -p.z0 * p.u1
    out["inprof_fade_sign"] = ct(p, "fade")
    out["inprof_fade_weighted_by_z0"] = ct(p, "fadew")
    out["inprof_fade_by_year"] = p.groupby("yr").apply(lambda x: ct(x, "fade"))
    out["inprof_fade_by_coin"] = p.groupby("coin").apply(lambda x: ct(x, "fade"))
    out["inprof_fade_by_window"] = p.groupby("win").apply(lambda x: ct(x, "fade"))
    # rank corr z0 vs u1 in and out profile
    from scipy.stats import spearmanr
    o = d[~d.inprof].dropna(subset=["z0", "u1"])
    out["spearman_z0_u1"] = pd.Series({"in": spearmanr(p.z0, p.u1)[0], "out": spearmanr(o.z0, o.u1)[0]})
    # 2-day horizon on grid with 2-day rise
    g = d[d.inprof & (d.pos % 2 == 0)].dropna(subset=["z2", "u2"]).copy()
    g["q"] = pd.qcut(g.z2, 4, labels=False)
    out["inprof_next2_by_z2_quartile_grid"] = g.groupby("q").apply(lambda x: ct(x, "u2"))
    # interaction on up days: z0 high vs range high
    up["zh"] = up.z0 > up.z0.median(); up["rh"] = up.rng > up.rng.median()
    out["inprof_up_z0hi_x_rnghi"] = up.groupby(["zh", "rh"]).apply(lambda x: ct(x, "u1"))
    return out
