def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        allr = []
        for w, df in ws.items():
            c = df["close"].astype(float).values
            allr.append(pd.Series(c).pct_change().dropna().values)
        mu = np.concatenate(allr).mean() if allr else 0.0
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            ts = pd.to_datetime(df["timestamp"])
            d = pd.DataFrame({
                "coin": coin, "w": w, "year": ts.dt.year,
                "fc": df["forecast"].astype(float),
                "reg": df["regime"].astype(str),
                "r1": c.shift(-1) / c - 1 - mu,
                "r2": (c.shift(-2) / c - 1 - 2 * mu) / 2,
                "r3": (c.shift(-3) / c - 1 - 3 * mu) / 3,
                "last": c / c.shift(1) - 1,
                "slide4": c.shift(1) / c.shift(5) - 1,
                "day": ts.dt.floor("D"),
            })
            rows.append(d)
    d = pd.concat(rows)
    a = d[(d.fc > 0) & d.r1.notna()].copy()

    def clus_slope(x, y, g):
        x = np.asarray(x, float); y = np.asarray(y, float)
        X = np.column_stack([np.ones(len(x)), x])
        b, *_ = np.linalg.lstsq(X, y, rcond=None)
        e = y - X @ b
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((2, 2))
        for _, idx in pd.Series(range(len(x))).groupby(np.asarray(g)).groups.items():
            s = (X[idx] * e[idx, None]).sum(0); meat += np.outer(s, s)
        V = XtXi @ meat @ XtXi
        return b[1], b[1] / np.sqrt(V[1, 1]), len(x)

    out = {}
    s = clus_slope(a.fc, a.r1, a.day)
    out["main_BC slope,t,n"] = pd.Series(s, index=["slope", "t", "n"])
    # horizons
    hz = {}
    for h in ["r1", "r2", "r3"]:
        b = a[a[h].notna()]
        hz[h] = clus_slope(b.fc, b[h], b.day)
    out["by_horizon"] = pd.DataFrame(hz, index=["slope", "t", "n"]).T
    # by coin
    bc = {}
    for k, g in a.groupby("coin"):
        if len(g) > 20:
            bc[k] = clus_slope(g.fc, g.r1, g.day) + (g.r1.mean(),)
    out["by_coin"] = pd.DataFrame(bc, index=["slope", "t", "n", "mean_r1"]).T
    by = {}
    for k, g in a.groupby("year"):
        if len(g) > 20:
            by[k] = clus_slope(g.fc, g.r1, g.day) + (g.r1.mean(),)
    out["by_year"] = pd.DataFrame(by, index=["slope", "t", "n", "mean_r1"]).T
    # forecast quintiles
    a["fq"] = pd.qcut(a.fc.rank(method="first"), 4, labels=False)
    out["by_fc_quartile"] = a.groupby("fq").agg(fc=("fc", "mean"), r1=("r1", "mean"), r3=("r3", "mean"), n=("r1", "size"),
                                                 sd=("r1", "std"))
    # latest-day sign
    a["lastsign"] = np.where(a["last"] < 0, "down", "up")
    t = {}
    for k, g in a.groupby("lastsign"):
        t[k] = clus_slope(g.fc, g.r1, g.day) + (g.r1.mean(),)
    out["by_last_sign"] = pd.DataFrame(t, index=["slope", "t", "n", "mean_r1"]).T
    # last day quartile x slide
    a["lq"] = pd.qcut(a["last"].rank(method="first"), 3, labels=["lastlow", "lastmid", "lasthigh"])
    out["grid_fq_lastq_mean_r1"] = a.pivot_table(index="fq", columns="lq", values="r1", aggfunc="mean")
    # outside profile: same relation with raw slide
    o = d[(d.reg != "unknown") & d.r1.notna() & d.slide4.notna() & (d.slide4 < 0)]
    out["outside_profile_depth_slope"] = pd.Series(clus_slope(-o.slide4, o.r1, o.day), index=["slope", "t", "n"])
    i = d[(d.reg == "unknown") & d.r1.notna() & d.slide4.notna() & (d.slide4 < 0)]
    out["inside_profile_rawdepth_slope"] = pd.Series(clus_slope(-i.slide4, i.r1, i.day), index=["slope", "t", "n"])
    out["share_regime_unknown"] = (d.reg == "unknown").mean()
    return out
