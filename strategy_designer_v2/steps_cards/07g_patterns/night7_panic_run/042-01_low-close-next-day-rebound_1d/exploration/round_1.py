def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            rng = (h - l)
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]),
                "clv": np.where(rng > 0, (h - c) / rng, np.nan),
                "ret0": c / c.shift(1) - 1,
                "body": (c - o) / rng.replace(0, np.nan),
                "rngpct": rng / c,
                "r1": c.shift(-1) / c - 1,
                "r3": c.shift(-3) / c - 1,
                "r5": c.shift(-5) / c - 1,
                "tr60": c / c.shift(60) - 1,
                "vol": b["volume"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "fc": b["forecast"].astype(float),
            })
            d["vol20"] = d["vol"] / d["vol"].rolling(20, min_periods=10).mean().shift(1)
            d["rng20"] = d["rngpct"] / d["rngpct"].rolling(20, min_periods=10).mean().shift(1)
            d["ret3p"] = c / c.shift(3) - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for k in ["r1", "r3", "r5"]:
        D[k + "x"] = D[k] - D.groupby("coin")[k].transform("mean")
    D["sd1"] = D.groupby("coin")["r1"].transform("std")
    D["z1"] = D["r1x"] / D["sd1"]
    D["wd"] = D["ts"].dt.dayofweek
    D["yr"] = D["ts"].dt.year
    def tt(x):
        x = x.dropna()
        return x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
    out = {}
    D["clvq"] = pd.qcut(D["clv"], 5, labels=False)
    g = D.groupby("clvq")["z1"]
    out["clv quintile -> next-day z"] = pd.DataFrame({"mean_z": g.mean(), "t": g.apply(tt), "n": g.count()})
    # by coin slope
    res = {}
    for coin, x in D.dropna(subset=["clv", "z1"]).groupby("coin"):
        s = stats.linregress(x["clv"], x["z1"]); res[coin] = (s.slope, s.slope / s.stderr, len(x))
    out["by coin slope z1 on clv"] = pd.DataFrame(res, index=["slope", "t", "n"]).T
    # partial: clv vs day's own return
    X = D.dropna(subset=["clv", "z1", "ret0"]).copy()
    X["ret0z"] = X["ret0"] / X.groupby("coin")["ret0"].transform("std")
    A = np.column_stack([np.ones(len(X)), X["clv"] - 0.5, X["ret0z"], X["body"].fillna(0)])
    beta, *_ = np.linalg.lstsq(A, X["z1"].values, rcond=None)
    resid = X["z1"].values - A @ beta
    cov = np.linalg.inv(A.T @ A) * resid.var()
    out["multi z1 ~ clv + ret0z + body"] = pd.DataFrame({"beta": beta, "t": beta / np.sqrt(np.diag(cov))}, index=["c", "clv", "ret0z", "body"])
    # day return quintile
    X["r0q"] = X.groupby("coin")["ret0z"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["ret0 q x clv q mean z1"] = X.assign(cq=pd.qcut(X["clv"], 3, labels=False)).pivot_table(index="r0q", columns="cq", values="z1", aggfunc="mean")
    # range regime
    X2 = D.dropna(subset=["clv", "z1", "rng20"]).copy()
    X2["rq"] = pd.qcut(X2["rng20"], 3, labels=False)
    out["rel range tercile x clv slope"] = X2.groupby("rq").apply(lambda x: pd.Series({"slope": stats.linregress(x["clv"], x["z1"]).slope, "t": (lambda s: s.slope / s.stderr)(stats.linregress(x["clv"], x["z1"])), "n": len(x), "meanz": x["z1"].mean()}))
    X3 = D.dropna(subset=["clv", "z1", "vol20"]).copy()
    X3["vq"] = pd.qcut(X3["vol20"], 3, labels=False)
    out["rel volume tercile x clv slope"] = X3.groupby("vq").apply(lambda x: pd.Series({"slope": stats.linregress(x["clv"], x["z1"]).slope, "t": (lambda s: s.slope / s.stderr)(stats.linregress(x["clv"], x["z1"])), "n": len(x), "meanz": x["z1"].mean()}))
    X4 = D.dropna(subset=["clv", "z1", "tr60"]).copy()
    X4["trend"] = np.where(X4["tr60"] > 0.1, "rising", np.where(X4["tr60"] < -0.1, "falling", "choppy"))
    out["trend x clv slope"] = X4.groupby("trend").apply(lambda x: pd.Series({"slope": stats.linregress(x["clv"], x["z1"]).slope, "t": (lambda s: s.slope / s.stderr)(stats.linregress(x["clv"], x["z1"])), "n": len(x), "meanz": x["z1"].mean()}))
    out["weekday x clv slope"] = D.dropna(subset=["clv", "z1"]).groupby("wd").apply(lambda x: pd.Series({"slope": stats.linregress(x["clv"], x["z1"]).slope, "t": (lambda s: s.slope / s.stderr)(stats.linregress(x["clv"], x["z1"])), "n": len(x), "meanz_next": x["z1"].mean(), "t_meanz": tt(x["z1"])}))
    out["year x clv slope"] = D.dropna(subset=["clv", "z1"]).groupby("yr").apply(lambda x: pd.Series({"slope": stats.linregress(x["clv"], x["z1"]).slope, "t": (lambda s: s.slope / s.stderr)(stats.linregress(x["clv"], x["z1"])), "n": len(x)}))
    # longer horizons non-overlapping
    hres = {}
    for h, k in [(3, "r3x"), (5, "r5x")]:
        x = D[(D["pos"] % h == 0)].dropna(subset=["clv", k])
        x = x.assign(zz=x[k] / x.groupby("coin")[k].transform("std"))
        s = stats.linregress(x["clv"], x["zz"]); hres[h] = (s.slope, s.slope / s.stderr, len(x))
    out["clv slope longer horizons (nonoverlap)"] = pd.DataFrame(hres, index=["slope", "t", "n"]).T
    # 3-day past return quintile -> next day
    X5 = D.dropna(subset=["ret3p", "z1"]).copy()
    X5["q"] = X5.groupby("coin")["ret3p"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["past 3d ret quintile -> next z1"] = X5.groupby("q")["z1"].agg(["mean", tt, "count"])
    # book: daily returns
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    DD = pd.concat(dd)
    DD["wd"] = pd.to_datetime(DD["day"]).dt.dayofweek
    bk = DD.groupby(["win", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean"), wd=("wd", "first")).dropna()
    out["book by weekday"] = bk.groupby("wd")["br"].agg(["mean", tt, "count"])
    out["book by window"] = bk.groupby("win").agg(br=("br", "mean"), cr=("cr", "mean"), n=("br", "count"))
    return out
