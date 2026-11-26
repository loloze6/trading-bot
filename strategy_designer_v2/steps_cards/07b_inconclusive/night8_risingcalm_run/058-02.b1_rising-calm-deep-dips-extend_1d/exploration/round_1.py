def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    allgrid = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            n = len(c)
            hi5 = pd.Series(c).rolling(5, min_periods=5).max().values
            r = pd.Series(c).pct_change()
            sd30 = r.rolling(30, min_periods=20).std().values
            raw = (c - hi5) / hi5 / sd30
            ts = pd.to_datetime(df["timestamp"])
            for h in [1, 2, 3, 5, 10]:
                for i in range(0, n - h, h):
                    allgrid.append((coin, h, c[i + h] / c[i] - 1))
            for i in range(0, n - 5, 5):
                f = {}
                for h in [1, 2, 3, 5, 10]:
                    f[h] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                rows.append(dict(coin=coin, win=w, year=ts[i].year, day=ts[i].normalize(),
                                 regime=df["regime"].iloc[i], fc=df["forecast"].iloc[i],
                                 raw=raw[i], **{f"r{h}": f[h] for h in f}))
    d = pd.DataFrame(rows)
    g = pd.DataFrame(allgrid, columns=["coin", "h", "ret"])
    drift = g.groupby(["coin", "h"])["ret"].mean()
    for h in [1, 2, 3, 5, 10]:
        d[f"x{h}"] = d[f"r{h}"] - d["coin"].map(drift.xs(h, level="h"))
    out = {}
    def slope(sub, y, x="raw"):
        s = sub[[x, y, "day"]].dropna()
        if len(s) < 10: return (len(s), np.nan, np.nan, np.nan)
        X = s[x].values; Y = s[y].values
        Xc = X - X.mean(); b = (Xc * (Y - Y.mean())).sum() / (Xc ** 2).sum()
        e = Y - Y.mean() - b * Xc
        sc = pd.Series(Xc * e).groupby(s["day"].values).sum()
        G = len(sc); se = np.sqrt((sc ** 2).sum() / (Xc ** 2).sum() ** 2 * G / (G - 1))
        return (len(s), b, b / se, s[y].mean())
    rc = d[(d.regime == "unknown") & (d.raw < 0)]
    oth = d[(d.regime != "unknown") & (d.raw < 0)]
    res = []
    for h in [1, 2, 3, 5, 10]:
        n1, b1, t1, m1 = slope(rc, f"x{h}")
        n2, b2, t2, m2 = slope(oth, f"x{h}")
        res.append(dict(h=h, rc_n=n1, rc_slope=b1, rc_t=t1, rc_meanx=m1, oth_n=n2, oth_slope=b2, oth_t=t2, oth_meanx=m2))
    out["slope_on_raw_by_horizon (neg slope = deeper->higher)"] = pd.DataFrame(res)
    res = []
    for k, s in rc.groupby("coin"):
        n1, b1, t1, m1 = slope(s, "x5"); res.append(dict(coin=k, n=n1, slope=b1, t=t1, meanx5=m1))
    out["rc_by_coin_x5"] = pd.DataFrame(res)
    res = []
    for k, s in rc.groupby("year"):
        n1, b1, t1, m1 = slope(s, "x5"); res.append(dict(year=k, n=n1, slope=b1, t=t1, meanx5=m1))
    out["rc_by_year_x5"] = pd.DataFrame(res)
    rc2 = rc.copy(); rc2["q"] = pd.qcut(rc2.raw, 4, labels=["deepest", "q2", "q3", "shallow"])
    out["rc_by_depth_quartile"] = rc2.groupby("q")[["raw", "x1", "x3", "x5", "x10"]].agg(["mean", "count"]).round(4)
    oth2 = oth.copy(); oth2["q"] = pd.qcut(oth2.raw, 4, labels=["deepest", "q2", "q3", "shallow"])
    out["other_regimes_by_depth_quartile"] = oth2.groupby("q")[["raw", "x3", "x5", "x10"]].mean().round(4)
    athigh = d[(d.regime == "unknown") & (d.raw >= 0)]
    out["rc_at_high_mean_x5_n"] = f"{athigh.x5.mean():.4f} n={athigh.x5.notna().sum()}"
    return out
