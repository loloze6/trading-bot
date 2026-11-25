def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            allr.append(b["close"].astype(float).pct_change())
        drift = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            hl = (b["high"] - b["low"]).astype(float).replace(0, np.nan)
            clv = (c - b["low"]) / hl
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "z": r / sd, "clv": clv,
                               "rngz": (hl / c) / sd,
                               "nx": (c.shift(-1) / c - 1 - drift) / sd,
                               "nxr": c.shift(-1) / c - 1 - drift,
                               "nx2": c.shift(-2) / c - 1 - 2 * drift,
                               "tr60": c / c.shift(60) - 1,
                               "reg": b["regime"].astype(str), "day": ts.dt.floor("D"),
                               "yr": ts.dt.year, "pi": np.arange(len(b))})
            rows.append(df)
    d = pd.concat(rows).dropna(subset=["z", "nxr", "clv"])
    d["prof"] = np.where(d["reg"] == "chop", "out", "in")

    def agg(g, col="nxr"):
        g = g.dropna(subset=[col])
        n = len(g)
        m = g[col].mean()
        dev = (g[col] - m).groupby(g["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / n if n > 2 else np.nan
        return pd.Series({"n": n, "days": g["day"].nunique(), "mean%": 100 * m, "t_day": m / se if se else np.nan})

    out = {}
    d["clvb"] = pd.cut(d["clv"], [0, 0.2, 0.4, 0.6, 0.8, 1.0], include_lowest=True)
    d["sgn"] = np.where(d["z"] > 0, "up", "down")
    out["clv x up/down, in profile"] = d[d.prof == "in"].groupby(["sgn", "clvb"]).apply(agg).round(3)
    out["clv x up/down, out profile"] = d[d.prof == "out"].groupby(["sgn", "clvb"]).apply(agg).round(3)
    lo = d[(d.prof == "in") & (d.clv <= 0.2)]
    out["in, clv<=0.2 by year"] = lo.groupby("yr").apply(agg).round(3)
    out["in, clv<=0.2 by coin"] = lo.groupby("coin").apply(agg).round(3)
    # graded: correlation of (0.5-clv) * range with next day, in profile
    ii = d[d.prof == "in"].copy()
    ii["low_close"] = (0.5 - ii["clv"]) * ii["rngz"]
    ii["lcb"] = pd.qcut(ii["low_close"], 5)
    out["in, quintiles of (0.5-clv)*range/sd"] = ii.groupby("lcb").apply(agg).round(3)
    # regression next-day (in sd units) on z and clv, in profile
    X = ii[["z", "clv"]].assign(c=1.0).dropna()
    y = ii.loc[X.index, "nx"]
    ok = y.notna(); X = X[ok]; y = y[ok]
    beta, *_ = np.linalg.lstsq(X.values, y.values, rcond=None)
    res = y.values - X.values @ beta
    cov = np.linalg.inv(X.values.T @ X.values) * res.var(ddof=3)
    out["in, OLS nx/sd on z and clv"] = pd.DataFrame({"beta": beta, "t": beta / np.sqrt(np.diag(cov))}, index=["z", "clv", "const"]).round(3)
    # out of profile by 60d trend
    o = d[(d.prof == "out") & d.tr60.notna()].copy()
    o["trend"] = np.where(o.tr60 > 0.1, "rising", np.where(o.tr60 < -0.1, "falling", "choppy"))
    o2 = o[o.clv <= 0.2]
    out["out, clv<=0.2 by 60d trend"] = o2.groupby("trend").apply(agg).round(3)
    g2 = d[(d.prof == "in") & (d.pi % 2 == 0)]
    out["in, 2-day after by clv (grid 2)"] = g2.groupby("clvb").apply(lambda g: agg(g, "nx2")).round(3)
    return out
