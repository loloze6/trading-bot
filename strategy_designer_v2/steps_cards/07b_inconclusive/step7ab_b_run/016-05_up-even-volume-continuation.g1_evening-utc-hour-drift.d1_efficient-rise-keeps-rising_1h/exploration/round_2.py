def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 72
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values.astype(float)
            f = df["forecast"].values.astype(float)
            n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            dif = np.abs(np.diff(c, prepend=np.nan))
            s = pd.Series(dif).rolling(72).sum().values
            r72 = np.full(n, np.nan); r72[72:] = c[72:] / c[:-72] - 1
            er = np.full(n, np.nan); er[72:] = np.abs(c[72:] - c[:-72]) / s[72:]
            # hourly vol over past 30 days
            lr = np.diff(np.log(c), prepend=np.nan)
            vol = pd.Series(lr).rolling(720, min_periods=200).std().values * np.sqrt(72)
            for i in range(0, n, H):
                rec = {"coin": coin, "w": w, "year": ts.iloc[i].year, "f": f[i], "r72": r72[i], "er": er[i], "vol": vol[i]}
                for h in (72, 144):
                    rec["fwd%d" % h] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    for h in (72, 144):
        d["ex%d" % h] = d["fwd%d" % h] - d.groupby("coin")["fwd%d" % h].transform("mean")
    d["usual"] = d.groupby("coin")["fwd72"].transform("std")
    d["z"] = d.r72 / d.vol
    d["str"] = d.ex72 / d.usual

    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    out = {}
    rises = d[d.r72 > 0].copy()
    rises["zq"] = pd.qcut(rises.z, 5, labels=False, duplicates="drop")
    out["rises_by_z_quintile"] = rises.groupby("zq").apply(lambda g: pd.Series({"n": g.ex72.count(), "z": g.z.mean(), "r72": g.r72.mean(), "er": g.er.mean(), "ex72": g.ex72.mean(), "t72": tt(g.ex72)["t"], "ex144": g.ex144.mean(), "str": g.str.mean()}))
    top = rises[rises.zq == 4]
    out["top_z_by_coin"] = top.groupby("coin")["ex72"].apply(tt).unstack()
    out["top_z_by_year"] = top.groupby("year")["ex72"].apply(tt).unstack()
    rises["rq"] = pd.qcut(rises.r72, 5, labels=False)
    topr = rises[rises.rq == 4]
    out["top_r72_by_coin"] = topr.groupby("coin")["ex72"].apply(tt).unstack()
    out["top_r72_by_year"] = topr.groupby("year")["ex72"].apply(tt).unstack()
    # graded test: z-weighted
    x = rises.dropna(subset=["z", "ex72"])
    sl = stats.linregress(x.z, x.ex72)
    out["ols_ex72_on_z"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(x)})
    sl2 = stats.linregress(x.er, x.ex72)
    out["ols_ex72_on_er"] = pd.Series({"slope": sl2.slope, "t": sl2.slope / sl2.stderr})
    # multivariate: ex72 on z and er
    X = np.column_stack([np.ones(len(x)), x.z, x.er])
    b, *_ = np.linalg.lstsq(X, x.ex72.values, rcond=None)
    res = x.ex72.values - X @ b
    cov = np.linalg.inv(X.T @ X) * res.var(ddof=3)
    out["ols_ex72_on_z_and_er"] = pd.Series({"b_z": b[1], "t_z": b[1] / np.sqrt(cov[1, 1]), "b_er": b[2], "t_er": b[2] / np.sqrt(cov[2, 2])})
    # er within top z quintile
    top = top.copy()
    top["et"] = pd.qcut(top.er, 3, labels=False)
    out["top_z_by_er_tercile"] = top.groupby("et").agg(n=("ex72", "count"), er=("er", "mean"), ex72=("ex72", "mean"))
    # main-measure analogue weighted by z on rises
    out["z_weighted_main"] = tt(x.z * x.ex72)
    return out
