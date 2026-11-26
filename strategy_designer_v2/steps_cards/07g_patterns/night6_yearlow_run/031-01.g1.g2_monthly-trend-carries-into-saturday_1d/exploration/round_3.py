def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            r1 = c / c.shift(1) - 1
            df = pd.DataFrame({
                "coin": coin, "win": w, "wd": ts.dt.weekday.values,
                "year": ts.dt.year.values, "day": ts.dt.floor("D").values,
                "r5": (c / c.shift(5) - 1).values,
                "r20": (c / c.shift(20) - 1).values,
                "r15": (c.shift(5) / c.shift(20) - 1).values,
                "vol20": r1.rolling(20).std().values,
                "nxt": (c.shift(-1) / c - 1).values,
                "nxt2": (c.shift(-2) / c - 1).values,
                "alloc": b["postRebalance_current_allocation"].astype(float).values,
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["mu"] = d.groupby("coin")["nxt"].transform("mean")
    d["ex"] = d["nxt"] - d["mu"]
    d["ex2"] = d["nxt2"] - 2 * d["mu"]
    d["z5"] = d["r5"] / (d["vol20"] * np.sqrt(5))
    d["z15"] = d["r15"] / (d["vol20"] * np.sqrt(15))
    d["z20"] = d["r20"] / (d["vol20"] * np.sqrt(20))

    def tc(sub, val):
        s = sub.dropna(subset=[val])
        x = s.groupby("day")[val].sum()
        n = len(x)
        return pd.Series({"mean_bp": 1e4 * s[val].mean(), "t_day": x.mean() / (x.std() / np.sqrt(n)), "days": n, "cases": len(s)})

    out = {}
    f = d[d.wd == 4].dropna(subset=["z5", "z15", "ex"]).copy()
    for col in ["z5", "z15", "z20"]:
        f["p_" + col] = f[col].clip(-4, 4) * f["ex"]
    out["Fri: z5 vs earlier 15d (z15) vs z20, product t"] = pd.DataFrame({c: tc(f, "p_" + c) for c in ["z5", "z15", "z20"]}).T.round(2)
    # joint regression day-clustered approx: OLS coefficients
    X = np.column_stack([np.ones(len(f)), f["z5"].clip(-4, 4), f["z15"].clip(-4, 4)])
    beta, *_ = np.linalg.lstsq(X, f["ex"].values, rcond=None)
    resid = f["ex"].values - X @ beta
    # cluster by day
    g = f["day"].values
    meat = np.zeros((3, 3))
    for dd in np.unique(g):
        m = g == dd
        sc = X[m].T @ resid[m]
        meat += np.outer(sc, sc)
    bread = np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(bread @ meat @ bread))
    out["Fri joint OLS ex ~ z5 + z15 (bp per z, cluster t)"] = pd.DataFrame({"coef_bp": 1e4 * beta, "t": beta / se}, index=["const", "z5", "z15"]).round(2)
    # z5 by vol tercile on Friday
    f["vt"] = f.groupby("coin")["vol20"].transform(lambda v: pd.qcut(v, 3, labels=False))
    out["Fri z5*ex by vol tercile"] = f.groupby("vt").apply(lambda x: tc(x, "p_z5"))[["mean_bp", "t_day", "cases"]].round(2)
    # Does Friday z5 carry through Sunday (2-day)?
    f["p2"] = f["z5"].clip(-4, 4) * f["ex2"]
    out["Fri z5 * 2-day excess (Sat+Sun)"] = tc(f.dropna(subset=["p2"]), "p2").round(2).to_frame("v")
    # Thursday->Friday z5 (same weekend-adjacent?)
    th = d[d.wd == 3].dropna(subset=["z5", "ex"]).copy()
    th["p"] = th["z5"].clip(-4, 4) * th["ex"]
    out["Thu z5*ex"] = tc(th, "p").round(2).to_frame("v")
    # book: daily book return by year & weekday
    days = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; days.append(x)
    dy = pd.concat(days, ignore_index=True)
    dy["day"] = pd.to_datetime(dy["day"], utc=True)
    bk = dy.groupby(["win", "day"])["book_return"].mean().dropna().reset_index()
    bk["year"] = bk["day"].dt.year
    out["book daily return by year (bp, sharpe)"] = bk.groupby("year")["book_return"].agg(lambda s: pd.Series([1e4 * s.mean()]).iloc[0]).to_frame("bp").join(bk.groupby("year")["book_return"].apply(lambda s: s.mean() / s.std() * np.sqrt(365)).rename("sharpe")).round(2)
    return out
