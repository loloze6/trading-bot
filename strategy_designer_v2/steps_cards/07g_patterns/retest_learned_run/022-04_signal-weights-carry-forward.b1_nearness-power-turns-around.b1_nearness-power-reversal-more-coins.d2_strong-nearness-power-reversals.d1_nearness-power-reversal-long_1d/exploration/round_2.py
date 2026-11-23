def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            rng = (b["high"] - b["low"]) / c
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "fwd5": c.shift(-5) / c - 1,
                "fwd1": c.shift(-1) / c - 1,
                "fc": b["forecast"].astype(float),
                "r1": r1,
                "r5": c / c.shift(5) - 1,
                "range_z": rng / rng.rolling(20, min_periods=10).mean(),
                "range_z5": rng.rolling(5).mean() / rng.rolling(60, min_periods=30).mean(),
                "clv": ((c - b["low"]) / (b["high"] - b["low"])).replace([np.inf, -np.inf], np.nan),
                "volz": b["volume"] / b["volume"].rolling(20, min_periods=10).mean(),
                "wd": ts.dt.weekday, "year": ts.dt.year,
                "pos": np.arange(len(b)),
            })
            rows.append(d)
    df = pd.concat(rows, ignore_index=True)
    g = df[df["pos"] % 5 == 0].dropna(subset=["fwd5"]).copy()
    g["ex5"] = g["fwd5"] - g["coin"].map(g.groupby("coin")["fwd5"].mean())
    g["s5"] = g["ex5"] / g["coin"].map(g.groupby("coin")["fwd5"].std())
    def zc(x, f):
        return x.groupby("coin")[f].transform(lambda s: (s - s.mean()) / s.std())
    out = {}
    for f in ["range_z", "range_z5", "r5", "volz"]:
        x = g.dropna(subset=[f, "s5"]).copy(); x["fz"] = zc(x, f)
        res = []
        for yr, y in x.groupby("year"):
            sl = stats.linregress(y["fz"], y["s5"])
            res.append({"year": yr, "n": len(y), "slope": sl.slope, "t": sl.slope / sl.stderr})
        sl = stats.linregress(x["fz"], x["s5"])
        res.append({"year": "all", "n": len(x), "slope": sl.slope, "t": sl.slope / sl.stderr})
        out[f"{f} slope by year"] = pd.DataFrame(res)
    # range_z by coin
    x = g.dropna(subset=["range_z", "s5"]).copy(); x["fz"] = zc(x, "range_z")
    res = []
    for cn, y in x.groupby("coin"):
        sl = stats.linregress(y["fz"], y["s5"])
        res.append({"coin": cn, "n": len(y), "slope": sl.slope, "t": sl.slope / sl.stderr})
    out["range_z slope by coin"] = pd.DataFrame(res)
    # range_z split by day's direction
    x["up"] = x["r1"] > 0
    res = []
    for u, y in x.groupby("up"):
        sl = stats.linregress(y["fz"], y["s5"])
        res.append({"day_up": u, "n": len(y), "slope": sl.slope, "t": sl.slope / sl.stderr,
                    "top_quint_mean": y.loc[y["fz"] > y["fz"].quantile(0.8), "s5"].mean()})
    out["range_z slope by day direction"] = pd.DataFrame(res)
    # range_z controlling for r5, fc
    y = x.dropna(subset=["r5"]).copy(); y["r5z"] = zc(y, "r5"); y["fcz"] = zc(y, "fc").fillna(0)
    X = np.column_stack([np.ones(len(y)), y["fz"], y["r5z"], y["fcz"]])
    beta, *_ = np.linalg.lstsq(X, y["s5"].values, rcond=None)
    e = y["s5"].values - X @ beta
    cov = np.linalg.inv(X.T @ X) * (e @ e) / (len(y) - 4)
    out["multi: range_z, r5, fc"] = pd.DataFrame({"beta": beta, "t": beta / np.sqrt(np.diag(cov))},
                                                 index=["const", "range_z", "r5", "fc"])
    # range_z decile raw 5d total move, pct
    x["dec"] = pd.qcut(x["fz"].rank(method="first"), 10, labels=False)
    out["range_z decile: excess 5d % and strength"] = x.groupby("dec").agg(n=("s5", "count"), ex5_pct=("ex5", lambda s: s.mean() * 100), s5=("s5", "mean"))
    # weekday next-day by year (Friday & Monday & Wednesday)
    a = df.dropna(subset=["fwd1"]).copy()
    a["s1"] = (a["fwd1"] - a["coin"].map(a.groupby("coin")["fwd1"].mean())) / a["coin"].map(a.groupby("coin")["fwd1"].std())
    out["weekday x year next-day strength"] = a.pivot_table(index="year", columns="wd", values="s1", aggfunc="mean").round(3)
    return out
