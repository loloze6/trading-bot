def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        allr = []
        for w, df in ws.items():
            allr.append(df["close"].astype(float).pct_change().dropna().values)
        mu = np.concatenate(allr).mean()
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            ts = pd.to_datetime(df["timestamp"])
            lr = c.pct_change()
            vol = lr.rolling(20).std()
            d = pd.DataFrame({
                "coin": coin, "w": w, "year": ts.dt.year,
                "fc": df["forecast"].astype(float),
                "reg": df["regime"].astype(str),
                "r1": c.shift(-1) / c - 1 - mu,
                "r2": (c.shift(-2) / c - 1 - 2 * mu),
                "r3": (c.shift(-3) / c - 1 - 3 * mu),
                "last": lr,
                "s5": c / c.shift(5) - 1,
                "s4p": c.shift(1) / c.shift(5) - 1,
                "vol": vol,
                "day": ts.dt.floor("D"),
            })
            rows.append(d)
    d = pd.concat(rows)

    def ols(X, y, g):
        X = np.column_stack([np.ones(len(y))] + [np.asarray(x, float) for x in X]); y = np.asarray(y, float)
        b, *_ = np.linalg.lstsq(X, y, rcond=None); e = y - X @ b
        XtXi = np.linalg.inv(X.T @ X); k = X.shape[1]; meat = np.zeros((k, k))
        for _, idx in pd.Series(range(len(y))).groupby(np.asarray(g)).groups.items():
            s = (X[idx] * e[idx, None]).sum(0); meat += np.outer(s, s)
        V = XtXi @ meat @ XtXi
        return list(b[1:]) + list(b[1:] / np.sqrt(np.diag(V)[1:])) + [len(y)]

    out = {}
    p = d[(d.reg == "unknown") & d.r1.notna() & d.s5.notna() & d.vol.notna()].copy()
    p["dep5"] = (-p.s5 / p.vol).clip(lower=0)
    p["dep4"] = (-p.s4p / p.vol).clip(lower=0)
    p["dlast"] = (-p["last"] / p.vol).clip(lower=0)
    q = p[p.dep5 > 0]
    res = {}
    for h in ["r1", "r2", "r3"]:
        b = q[q[h].notna()]
        res["dep5_" + h] = ols([b.dep5], b[h], b.day) + [np.nan, np.nan]
        res["dep4+dlast_" + h] = ols([b.dep4, b.dlast], b[h], b.day)
    out["in_profile_s5_down"] = pd.DataFrame(res, index=["b1", "b2", "t1", "t2", "n"][:5] if False else None).T if False else \
        pd.DataFrame({k: (v + [np.nan] * 5)[:5] for k, v in res.items()}, index=["b1", "b2|t1", "t1|t2", "t2|n", "n"]).T
    q = q.copy()
    q["dq"] = pd.qcut(q.dep5.rank(method="first"), 4, labels=False)
    out["dep5_quartiles"] = q.groupby("dq").agg(dep5=("dep5", "mean"), r1=("r1", "mean"), r2=("r2", "mean"),
                                                  r3=("r3", "mean"), n=("r1", "size"), sd=("r1", "std"))
    out["dep5_by_year_r1"] = pd.DataFrame({k: ols([g.dep5], g.r1, g.day) for k, g in q.groupby("year")},
                                          index=["slope", "t", "n"]).T
    out["dep5_by_coin_r1"] = pd.DataFrame({k: ols([g.dep5], g.r1, g.day) for k, g in q.groupby("coin") if len(g) > 20},
                                          index=["slope", "t", "n"]).T
    o = d[(d.reg != "unknown") & d.r1.notna() & d.s5.notna() & d.vol.notna()].copy()
    o["dep5"] = (-o.s5 / o.vol).clip(lower=0)
    o = o[o.dep5 > 0]
    out["outside_profile_dep5_r1"] = pd.Series(ols([o.dep5], o.r1, o.day), index=["slope", "t", "n"])
    # non-overlapping check r1 trivially non-overlapping; days count
    out["in_profile_days"] = q.day.nunique()
    return out
