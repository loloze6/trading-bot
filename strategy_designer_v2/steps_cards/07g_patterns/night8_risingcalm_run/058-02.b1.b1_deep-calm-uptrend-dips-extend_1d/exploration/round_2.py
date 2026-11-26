def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=20).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "rc": np.where(b["regime"].astype(str) == "unknown", "rc", "other"),
                "z1": r1 / sd,
                "z2": (c / c.shift(2) - 1) / (sd * np.sqrt(2)),
                "clv": (c - l) / (h - l).replace(0, np.nan),
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1, "f3": c.shift(-3) / c - 1,
                "yr": ts.dt.year, "dkey": ts.dt.floor("D").astype("int64"),
                "fc": b["forecast"].astype(float),
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    def clus_t(d, col):
        d = d.dropna(subset=[col])
        if len(d) < 3: return (len(d), np.nan, np.nan, 0)
        s = d.groupby("dkey")[col].apply(lambda v: (v - d[col].mean()).sum())
        se = np.sqrt((s ** 2).sum()) / len(d)
        return (len(d), 100 * d[col].mean(), d[col].mean() / se, d["dkey"].nunique())
    # horizon grids, excess over coin mean on same grid
    res = []
    for hz in [1, 2, 3]:
        g = A[A["pos"] % hz == 0].dropna(subset=["f%d" % hz, "z1"]).copy()
        m = g.groupby("coin")["f%d" % hz].mean()
        g["x"] = g["f%d" % hz] - g["coin"].map(m)
        g["zb"] = pd.cut(g["z1"], [-99, -1, 0, 1, 99])
        for (rc, zb), d in g.groupby(["rc", "zb"], observed=True):
            n, mu, t, nd = clus_t(d, "x")
            res.append({"h": hz, "rc": rc, "z1bin": str(zb), "n": n, "mean%": mu, "t_day": t, "days": nd})
        # graded: product -z1 * x in rc, among down days
        dd = g[(g["rc"] == "rc") & (g["z1"] < 0)].copy()
        dd["p"] = -dd["z1"] * dd["x"]
        n, mu, t, nd = clus_t(dd, "p")
        res.append({"h": hz, "rc": "rc_down_product", "z1bin": "-z1*x", "n": n, "mean%": mu, "t_day": t, "days": nd})
        dd = g[(g["rc"] == "other") & (g["z1"] < 0)].copy()
        dd["p"] = -dd["z1"] * dd["x"]
        n, mu, t, nd = clus_t(dd, "p")
        res.append({"h": hz, "rc": "other_down_product", "z1bin": "-z1*x", "n": n, "mean%": mu, "t_day": t, "days": nd})
    out["rebound by horizon"] = pd.DataFrame(res)
    g = A.dropna(subset=["f1", "z1"]).copy()
    g["x"] = g["f1"] - g["coin"].map(g.groupby("coin")["f1"].mean())
    rc = g[g["rc"] == "rc"].copy()
    rcd = rc[rc["z1"] < 0].copy(); rcd["p"] = -rcd["z1"] * rcd["x"]
    out["rc down product by year"] = rcd.groupby("yr").apply(lambda d: pd.Series(dict(zip(["n", "mean%", "t", "days"], clus_t(d, "p")))))
    out["rc down product by coin"] = rcd.groupby("coin").apply(lambda d: pd.Series(dict(zip(["n", "mean%", "t", "days"], clus_t(d, "p")))))
    out["rc down product by window"] = rcd.groupby("win").apply(lambda d: pd.Series(dict(zip(["n", "mean%", "t", "days"], clus_t(d, "p")))))
    # close location on down days in rc
    rcd["clvb"] = pd.cut(rcd["clv"], [-0.01, 0.33, 0.66, 1.01])
    out["rc down day x1 by close location"] = rcd.groupby("clvb", observed=True).apply(lambda d: pd.Series(dict(zip(["n", "mean%", "t", "days"], clus_t(d, "x")))))
    # 2-day dip
    rc2 = rc.dropna(subset=["z2"]).copy(); rc2["zb2"] = pd.cut(rc2["z2"], [-99, -1, 0, 1, 99])
    out["rc x1 by 2-day z"] = rc2.groupby("zb2", observed=True).apply(lambda d: pd.Series(dict(zip(["n", "mean%", "t", "days"], clus_t(d, "x")))))
    out["rc mean x1 all"] = 100 * rc["x"].mean()
    return out
