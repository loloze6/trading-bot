def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            d = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"])})
            d["r1"] = c.shift(-1) / c - 1
            d["r5"] = c.shift(-5) / c - 1
            d["pos5"] = np.arange(len(c)) % 5 == 0
            d["prev1"] = c / c.shift(1) - 1
            d["g20"] = c / c.shift(20) - 1
            d["vol20"] = d["prev1"].rolling(20).std()
            d["dlow60"] = c / c.rolling(60, min_periods=60).min() - 1
            d["dhigh60"] = c / c.rolling(60, min_periods=60).max() - 1
            d["nextwd"] = (d["ts"] + pd.Timedelta(days=1)).dt.weekday
            d["year"] = d["ts"].dt.year
            d["fc"] = b["forecast"].astype(float)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu1 = D.groupby("coin")["r1"].mean()
    mu5 = D[D.pos5].groupby("coin")["r5"].mean()
    D["x1"] = D["r1"] - D["coin"].map(mu1)
    D["x5"] = D["r5"] - D["coin"].map(mu5)

    def ct(g, col):
        g = g.dropna(subset=[col])
        n = len(g)
        if n < 5: return pd.Series({"n": n, "mean%": np.nan, "t": np.nan})
        m = g[col].mean()
        cs = (g[col] - m).groupby(g["ts"]).sum()
        se = np.sqrt((cs ** 2).sum()) / n
        return pd.Series({"n": n, "mean%": 100 * m, "t": m / se, "days": cs.size})

    out = {}
    out["by_next_weekday"] = D.groupby("nextwd").apply(lambda g: ct(g, "x1"))
    # grading of g20 positive by next weekday
    res = {}
    for wd, g in D[D.g20 > 0].dropna(subset=["x1"]).groupby("nextwd"):
        s = stats.linregress(g["g20"], g["x1"])
        res[wd] = {"n": len(g), "slope": s.slope, "t": s.slope / s.stderr, "mean%": 100 * g.x1.mean()}
    out["g20pos_slope_by_nextwd"] = pd.DataFrame(res).T
    res = {}
    for wd, g in D[D.g20 <= 0].dropna(subset=["x1"]).groupby("nextwd"):
        s = stats.linregress(g["g20"], g["x1"])
        res[wd] = {"n": len(g), "slope": s.slope, "t": s.slope / s.stderr, "mean%": 100 * g.x1.mean()}
    out["g20neg_slope_by_nextwd"] = pd.DataFrame(res).T
    D["g20q"] = D.groupby("coin")["g20"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["g20q_next1_all"] = D.groupby("g20q").apply(lambda g: ct(g, "x1"))
    out["g20q_next1_sat"] = D[D.nextwd == 5].groupby("g20q").apply(lambda g: ct(g, "x1"))
    out["g20q_next5"] = D[D.pos5].groupby("g20q").apply(lambda g: ct(g, "x5"))
    D["p1q"] = D.groupby("coin")["prev1"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["prev1q_next1"] = D.groupby("p1q").apply(lambda g: ct(g, "x1"))
    D["vq"] = D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["volq_next1"] = D.groupby("vq").apply(lambda g: ct(g, "x1"))
    out["volq_next5"] = D[D.pos5].groupby("vq").apply(lambda g: ct(g, "x5"))
    D["lq"] = D.groupby("coin")["dlow60"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["dlow60q_next5"] = D[D.pos5].groupby("lq").apply(lambda g: ct(g, "x5"))
    out["dlow60q_next1"] = D.groupby("lq").apply(lambda g: ct(g, "x1"))
    out["sat_by_year_g20pos"] = D[(D.nextwd == 5) & (D.g20 > 0)].groupby("year").apply(lambda g: ct(g, "x1"))
    out["sat_by_coin_g20pos"] = D[(D.nextwd == 5) & (D.g20 > 0)].groupby("coin").apply(lambda g: ct(g, "x1"))
    out["sat_by_coin_g20neg"] = D[(D.nextwd == 5) & (D.g20 <= 0)].groupby("coin").apply(lambda g: ct(g, "x1"))
    return out
