def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    def build(H, off):
        rows = []
        for coin, wins in data["bars"].items():
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b["close"].astype(float); n = len(b)
                r1 = c.pct_change(); r30 = c / c.shift(30) - 1
                hi60 = c.rolling(60, min_periods=60).max(); lo60 = c.rolling(60, min_periods=60).min()
                pos60 = (c - lo60) / (hi60 - lo60)
                hi20 = c.rolling(20, min_periods=20).max(); lo20 = c.rolling(20, min_periods=20).min()
                pos20 = (c - lo20) / (hi20 - lo20)
                rng60 = hi60 / lo60 - 1
                fwd = c.shift(-H) / c - 1
                yr = pd.to_datetime(b["timestamp"]).dt.year
                for i in range(off, n, H):
                    if i + H >= n: break
                    rows.append(dict(coin=coin, win=w, r30=r30[i], r1=r1[i], pos60=pos60[i], pos20=pos20[i],
                                     rng60=rng60[i], fwd=fwd[i], yr=yr[i]))
        g = pd.DataFrame(rows)
        g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
        g["exz"] = g["ex"] / g.groupby("coin")["fwd"].transform("std")
        return g
    def slope_t(d, x):
        d = d.dropna(subset=[x, "exz"])
        s = stats.linregress(d[x], d["exz"]); return round(s.slope / s.stderr, 2), len(d)
    rob = {}
    for H in [1, 3, 5, 10]:
        offs = range(min(H, 5))
        for off in offs:
            g = build(H, off)
            rob[(H, off)] = {**{k: slope_t(g, k)[0] for k in ["pos60", "pos20", "r30", "r1"]}, "n": len(g)}
    out["slope t by horizon/offset"] = pd.DataFrame(rob).T
    g = build(5, 0)
    d = g.dropna(subset=["pos60", "r30", "exz", "rng60"]).copy()
    X = np.column_stack([np.ones(len(d)), d["pos60"] - 0.5, d["r30"]])
    beta, res, *_ = np.linalg.lstsq(X, d["exz"], rcond=None)
    e = d["exz"] - X @ beta; s2 = (e ** 2).sum() / (len(d) - 3)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["joint pos60 + r30 t"] = pd.Series(beta / se, index=["const", "pos60", "r30"]).round(2)
    pc = {}
    for coin, dd in d.groupby("coin"):
        s = stats.linregress(dd["pos60"], dd["exz"]); pc[coin] = [round(s.slope, 3), round(s.slope / s.stderr, 2), len(dd)]
    out["per coin pos60 slope (H5)"] = pd.DataFrame(pc, index=["slope", "t", "n"]).T
    d["half"] = np.where(d["yr"] <= 2021, "2018-2021", "2022-2025")
    out["pos60 slope t by half"] = d.groupby("half").apply(lambda x: slope_t(x, "pos60")[0])
    # range width: does pos60 effect differ in narrow (flat) vs wide ranges
    d["rq"] = d.groupby("coin")["rng60"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    d["pq"] = d.groupby("coin")["pos60"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["exz by range width tercile x pos60 quintile"] = d.pivot_table(index="rq", columns="pq", values="exz", aggfunc="mean").round(3)
    out["pos60 slope t by range tercile"] = d.groupby("rq").apply(lambda x: slope_t(x, "pos60")[0])
    out["pos60 quintile mean ex (H5)"] = d.groupby("pq")["ex"].agg(["mean", "count"]).round(4)
    # 10-day horizon pos60 quintiles
    g10 = build(10, 0).dropna(subset=["pos60", "exz"])
    g10["pq"] = g10.groupby("coin")["pos60"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    t = g10.groupby("pq")["exz"].agg(["mean", "std", "count"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    t["ex"] = g10.groupby("pq")["ex"].mean()
    out["pos60 quintile H10"] = t.round(4)
    return out
