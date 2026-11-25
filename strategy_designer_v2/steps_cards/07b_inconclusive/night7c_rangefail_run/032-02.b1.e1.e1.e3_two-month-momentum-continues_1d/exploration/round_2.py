def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    h = 20
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            lr = np.log(c[1:] / c[:-1])
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, len(df) - h, h):
                r20p = (c[i] / c[i - 20] - 1) if i >= 20 else np.nan
                r60p = (c[i] / c[i - 60] - 1) if i >= 60 else np.nan
                vol20 = np.std(lr[i - 20:i]) if i >= 20 else np.nan
                vol60 = np.std(lr[i - 60:i]) if i >= 60 else np.nan
                rows.append(dict(coin=coin, w=w, f=f[i], r=c[i + h] / c[i] - 1,
                                 year=ts.iloc[i].year, r20p=r20p, r60p=r60p,
                                 vol20=vol20, vol60=vol60))
    d = pd.DataFrame(rows)
    d["ex"] = d["r"] - d.groupby("coin")["r"].transform("mean")
    def slope(g, x="f"):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 10 or g[x].std() == 0:
            return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        r = stats.linregress(g[x], g["ex"])
        return pd.Series(dict(n=len(g), slope=r.slope, t=r.slope / r.stderr))
    out = {}
    # quietness: past 20d |return| relative to coin's own typical, and 20d vol relative to 60d vol
    d["absr20"] = d["r20p"].abs()
    d["absr20_rel"] = d["absr20"] / d.groupby("coin")["absr20"].transform("median")
    d["volratio"] = d["vol20"] / d["vol60"]
    d["t_abs"] = d.groupby("coin")["absr20"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["slope by within-coin |r20| tercile"] = d.groupby("t_abs").apply(slope)
    d["t_vr"] = pd.qcut(d["volratio"], 3, labels=False, duplicates="drop")
    out["slope by vol20/vol60 tercile"] = d.groupby("t_vr").apply(slope)
    d["t_v20"] = d.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["slope by within-coin vol20 tercile"] = d.groupby("t_v20").apply(slope)
    q = d[d["t_abs"] == 0]
    out["quiet tercile: slope by year"] = q.groupby("year").apply(slope)
    out["quiet tercile: slope by coin"] = q.groupby("coin").apply(slope)
    out["quiet tercile: by side"] = q.groupby(np.sign(q["f"]))["ex"].agg(["count", "mean", "std"]).assign(
        t=lambda x: x["mean"] / (x["std"] / np.sqrt(x["count"])))
    out["quiet tercile: slope on raw r60"] = slope(q, "r60p")
    # interaction: ex on f, f*quietness (continuous: -log absr20_rel)
    g = d.dropna(subset=["f", "ex", "absr20_rel"]).copy()
    g["quiet"] = -np.log(g["absr20_rel"].clip(lower=1e-3))
    X = np.column_stack([np.ones(len(g)), g["f"], g["quiet"], g["f"] * g["quiet"]])
    b, res, *_ = np.linalg.lstsq(X, g["ex"].values, rcond=None)
    e = g["ex"].values - X @ b
    s2 = e @ e / (len(g) - 4)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["interaction f x quiet"] = pd.DataFrame(dict(coef=b, t=b / se), index=["const", "f", "quiet", "f*quiet"])
    # outcome signed in forecast direction in quiet tercile, total move
    q2 = q.dropna(subset=["f"])
    sgn = np.sign(q2["f"])
    out["quiet: signed ex mean, t, n"] = pd.Series(dict(mean=(sgn * q2["ex"]).mean(),
        t=(sgn * q2["ex"]).mean() / ((sgn * q2["ex"]).std() / np.sqrt(len(q2))), n=len(q2)))
    rest = d[d["t_abs"] > 0].dropna(subset=["f"])
    s3 = np.sign(rest["f"])
    out["not quiet: signed ex mean, t, n"] = pd.Series(dict(mean=(s3 * rest["ex"]).mean(),
        t=(s3 * rest["ex"]).mean() / ((s3 * rest["ex"]).std() / np.sqrt(len(rest))), n=len(rest)))
    return out
