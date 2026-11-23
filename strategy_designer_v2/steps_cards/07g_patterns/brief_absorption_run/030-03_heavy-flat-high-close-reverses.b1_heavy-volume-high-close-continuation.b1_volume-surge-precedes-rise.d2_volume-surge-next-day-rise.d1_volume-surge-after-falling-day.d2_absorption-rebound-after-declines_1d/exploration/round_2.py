def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"]; r = c.pct_change()
            f = pd.DataFrame({
                "coin": coin, "win": w, "ret": r,
                "nxt": c.shift(-1) / c - 1,
                "nxt3": c.shift(-3) / c - 1,
                "vol20": r.rolling(20, min_periods=10).std().shift(1),
                "vr": b["volume"] / b["volume"].rolling(20, min_periods=10).mean().shift(1),
                "clv": ((c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)) * 2 - 1,
                "rng": (b["high"] - b["low"]) / c,
                "fc": b["forecast"],
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "p": np.arange(len(b)),
            })
            rows.append(f)
    d = pd.concat(rows, ignore_index=True)
    d["ex"] = d["nxt"] - d.groupby("coin")["nxt"].transform("mean")
    d["z"] = d["ret"] / d["vol20"]
    d["rng_z"] = d["rng"] / d["vol20"]
    d["lvr"] = np.log(d["vr"])
    d = d.replace([np.inf, -np.inf], np.nan).dropna(subset=["ex", "z", "clv", "lvr", "rng_z"])
    for col in ["z", "rng_z", "lvr"]:
        d[col] = d[col].clip(d[col].quantile(0.01), d[col].quantile(0.99))
    d["clv_vr"] = -d["clv"] * d["lvr"].clip(lower=0)  # low close x heavy volume
    out = {}
    def ols(df, cols):
        X = np.column_stack([np.ones(len(df))] + [df[c].values for c in cols])
        y = df["ex"].values
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        res = y - X @ beta
        s2 = res @ res / (len(y) - X.shape[1])
        se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
        return pd.DataFrame({"beta": beta, "t": beta / se}, index=["const"] + cols)
    out["multi: z clv lvr rng_z"] = ols(d, ["z", "clv", "lvr", "rng_z"])
    out["multi + fc + clv_vr"] = ols(d.assign(fc=d["fc"].fillna(0)), ["z", "clv", "lvr", "rng_z", "fc", "clv_vr"])
    up = d[d["ret"] > 0]
    out["up days only"] = ols(up, ["z", "clv", "lvr", "rng_z"])
    out["up days fc==0 n"] = float((up["fc"] == 0).mean())
    # graded low-close x heavy volume signal on up days
    up = up.copy()
    up["sq"] = pd.qcut(up["clv_vr"].rank(method="first"), 5, labels=False)
    a = up.groupby("sq")["ex"].agg(["mean", "count", "std"]); a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["up days: clv_vr quintile"] = a
    # all days clv_vr quintile
    d["sq"] = pd.qcut(d["clv_vr"].rank(method="first"), 5, labels=False)
    a = d.groupby("sq")["ex"].agg(["mean", "count", "std"]); a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["all days: clv_vr quintile"] = a
    # stability: slope of ex on -clv per coin and per year
    def sl(g, col):
        if len(g) < 30: return np.nan
        res = stats.linregress(g[col], g["ex"]); return res.slope / res.stderr
    out["t of clv slope by coin"] = d.groupby("coin").apply(lambda g: sl(g, "clv"))
    out["t of clv slope by year"] = d.groupby("year").apply(lambda g: sl(g, "clv"))
    out["t of clv_vr slope by coin"] = d.groupby("coin").apply(lambda g: sl(g, "clv_vr"))
    out["t of clv_vr slope by year"] = d.groupby("year").apply(lambda g: sl(g, "clv_vr"))
    out["t of rng_z slope by coin"] = d.groupby("coin").apply(lambda g: sl(g, "rng_z"))
    # 3-day non-overlap, clv_vr
    g = d[d["p"] % 3 == 0].dropna(subset=["nxt3"]).copy()
    g["ex3"] = g["nxt3"] - g.groupby("coin")["nxt3"].transform("mean")
    res = stats.linregress(g["clv_vr"], g["ex3"])
    out["3d nonoverlap clv_vr slope"] = pd.Series({"slope": res.slope, "t": res.slope / res.stderr, "n": len(g)})
    res = stats.linregress(g["clv"], g["ex3"])
    out["3d nonoverlap clv slope"] = pd.Series({"slope": res.slope, "t": res.slope / res.stderr, "n": len(g)})
    # mean ex by quintile of clv_vr in top quintile: avg move size vs cost
    out["top clv_vr quint mean nxt (total)"] = float(d[d["sq"] == 4]["nxt"].mean())
    return out
