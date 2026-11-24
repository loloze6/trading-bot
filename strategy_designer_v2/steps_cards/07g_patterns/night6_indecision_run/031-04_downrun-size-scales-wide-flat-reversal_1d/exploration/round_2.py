def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); o = b["open"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float)
            rng = h - l
            r1 = c.pct_change()
            sd20 = r1.shift(1).rolling(20, min_periods=20).std()
            z1 = r1 / sd20
            rr = rng / rng.rolling(20, min_periods=20).mean()
            body = (c - o).abs() / rng.replace(0, np.nan)
            cloc = (c - l) / rng.replace(0, np.nan)
            r5 = c / c.shift(5) - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                               "day": ts.dt.floor("D"), "year": ts.dt.year,
                               "r1": r1, "z1": z1, "rr": rr, "body": body, "cloc": cloc, "r5": r5,
                               "f1": c.shift(-1) / c - 1, "f3": c.shift(-3) / c - 1,
                               "f5": c.shift(-5) / c - 1})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    for h, f in [(1, "f1"), (3, "f3"), (5, "f5")]:
        g = d[d.pos % h == 0]
        dr = g.groupby("coin")[f].mean()
        d["x%d" % h] = d[f] - d["coin"].map(dr)

    def tday(s, days):
        x = pd.DataFrame({"v": s, "d": days}).dropna()
        if len(x) < 5: return (np.nan, len(x), np.nan, 0)
        m = x.v.mean()
        ds = (x.v - m).groupby(x.d).sum()
        se = np.sqrt((ds ** 2).sum()) / len(x)
        return (m, len(x), m / se if se > 0 else np.nan, x.d.nunique())

    def table(sub, col, val, q=10):
        sub = sub.dropna(subset=[col, val])
        sub = sub.assign(b=pd.qcut(sub[col], q, labels=False, duplicates="drop"))
        out = []
        for k, gg in sub.groupby("b"):
            m, n, t, nd = tday(gg[val], gg["day"])
            out.append({"bin": k, "lo": gg[col].min(), "hi": gg[col].max(), "mean": m, "n": n, "t": t, "days": nd})
        return pd.DataFrame(out)

    res = {}
    res["z1 -> x1 deciles"] = table(d, "z1", "x1", 10)
    G3 = d[d.pos % 3 == 0]
    res["r1 -> x3 grid3"] = table(G3, "r1", "x3", 10)
    big = d[d.r1 <= d.r1.quantile(0.1)]
    out = []
    for k, gg in big.groupby("coin"):
        m, n, t, nd = tday(gg["x1"], gg["day"]); out.append({"coin": k, "mean": m, "n": n, "t": t})
    res["big fall next-day by coin"] = pd.DataFrame(out)
    out = []
    for k, gg in big.groupby("year"):
        m, n, t, nd = tday(gg["x1"], gg["day"]); out.append({"year": k, "mean": m, "n": n, "t": t})
    res["big fall next-day by year"] = pd.DataFrame(out)
    # within big falls: close location (did it close off the low?)
    res["big fall: cloc -> x1"] = table(big, "cloc", "x1", 4)
    res["big fall: rr -> x1"] = table(big, "rr", "x1", 4)
    # big rises
    bigu = d[d.r1 >= d.r1.quantile(0.9)]
    res["big rise: cloc -> x1"] = table(bigu, "cloc", "x1", 4)
    # wide flat after up run graded by r5
    wf = d[(d.rr >= 1.5) & (d.body <= 0.1)]
    res["wide flat: r5 -> x5"] = table(wf, "r5", "x5", 4)
    res["wide flat: r5 -> x1"] = table(wf, "r5", "x1", 4)
    # correlation slope test r1 vs x1 across all, t clustered
    x = d[["r1", "x1", "day"]].dropna()
    X = x.r1 - x.r1.mean(); beta = (X * x.x1).sum() / (X ** 2).sum()
    e = x.x1 - x.x1.mean() - beta * X
    sc = (X * e).groupby(x.day).sum()
    se = np.sqrt((sc ** 2).sum()) / (X ** 2).sum()
    res["slope x1 on r1"] = pd.Series({"beta": beta, "t": beta / se, "n": len(x), "days": x.day.nunique()})
    return res
