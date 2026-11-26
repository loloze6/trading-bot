def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            allr.append(c[1:] / c[:-1] - 1)
        allc = np.concatenate(allr)
        mu = np.nanmean(allc)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            r1 = np.insert(c[1:] / c[:-1] - 1, 0, np.nan)
            sd = pd.Series(r1).rolling(20).std().values
            z = r1 / sd
            ts = pd.to_datetime(b["timestamp"])
            d = {"coin": coin, "w": w, "f": b["forecast"].astype(float).values, "z": z,
                 "pos": np.arange(n), "day": ts.dt.floor("D").astype(str).values,
                 "year": ts.dt.year.values, "reg": b["regime"].values}
            for h in [1, 2, 3, 5]:
                fw = np.full(n, np.nan)
                fw[:n - h] = c[h:] / c[:-h] - 1
                d["nx%d" % h] = fw - mu * h
            # 60-day trend to check depth of the fall
            tr = np.full(n, np.nan)
            tr[60:] = c[60:] / c[:-60] - 1
            d["tr60"] = tr
            rows.append(pd.DataFrame(d))
    d = pd.concat(rows)
    a = d[(d.f > 0)].copy()

    def cl_slope(g, x, y):
        g = g[[x, y, "day"]].dropna()
        if len(g) < 15:
            return pd.Series({"n": len(g)})
        xv = g[x].values; yv = g[y].values
        xm = xv - xv.mean(); b1 = (xm * (yv - yv.mean())).sum() / (xm ** 2).sum()
        e = yv - yv.mean() - b1 * xm
        s = pd.Series(xm * e).groupby(g.day.values).sum()
        se = np.sqrt((s ** 2).sum()) / (xm ** 2).sum()
        rho, p = stats.spearmanr(xv, yv)
        return pd.Series({"n": len(g), "days": g.day.nunique(), "slope": b1, "t": b1 / se,
                          "mean": yv.mean(), "spearman": rho})

    out = {}
    out["f_slope_1d"] = cl_slope(a, "f", "nx1").to_frame().T
    out["negz_slope_1d"] = cl_slope(a.assign(nz=-a.z), "nz", "nx1").to_frame().T
    a2 = a[a.z > -3]
    out["f_slope_1d_no_z_below_-3"] = cl_slope(a2, "f", "nx1").to_frame().T
    # winsorised y
    aw = a.copy(); lo, hi = aw.nx1.quantile([0.02, 0.98]); aw["nx1"] = aw.nx1.clip(lo, hi)
    out["f_slope_1d_winsor"] = cl_slope(aw, "f", "nx1").to_frame().T
    # horizons, non-overlapping grid per window
    hz = []
    for h in [1, 2, 3, 5]:
        g = a[a.pos % h == 0]
        r = cl_slope(g, "f", "nx%d" % h); r.name = "h%d" % h; hz.append(r)
    out["by_horizon_grid"] = pd.DataFrame(hz)
    out["by_year"] = a.groupby("year").apply(lambda g: cl_slope(g, "f", "nx1"))
    a["trb"] = pd.cut(a.tr60, [-1, -0.4, -0.25, -0.1, 10])
    out["by_trend_depth"] = a.groupby("trb").apply(lambda g: cl_slope(g, "f", "nx1"))
    return out
