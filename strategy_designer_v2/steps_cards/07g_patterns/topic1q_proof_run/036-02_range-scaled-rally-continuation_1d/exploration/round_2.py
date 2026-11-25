def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            rr = ((h - l) / c).rolling(30).mean()
            r1 = c / c.shift(1) - 1
            r2 = c / c.shift(2) - 1
            r3 = c / c.shift(3) - 1
            vol30 = r1.rolling(30).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "s1": r1 / rr, "s2": r2 / rr, "s3": r3 / rr, "tr60": c / c.shift(60) - 1,
                               "vol30": vol30, "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1,
                               "f3": c.shift(-3) / c - 1, "f5": c.shift(-5) / c - 1,
                               "f7": c.shift(-7) / c - 1, "year": ts.dt.year, "wd": ts.dt.weekday,
                               "day": ts.dt.floor("D")})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    # agitation proxy: vol30 vs its own rolling past median within coin (within-window, limited history)
    A["agit"] = A.groupby(["coin", "w"])["vol30"].transform(lambda v: v > v.expanding(30).median())
    for hz in [1, 2, 3, 5, 7]:
        g = A[A.pos % hz == 0].dropna(subset=[f"f{hz}"])
        m = g.groupby("coin")[f"f{hz}"].mean()
        A[f"x{hz}"] = A[f"f{hz}"] - A["coin"].map(m)
    A["tr"] = pd.cut(A["tr60"], [-9, -0.1, 0.1, 99], labels=["fall", "chop", "rise"])
    out = {}
    def summ(g, col):
        x = g[[col, "day"]].dropna()
        d = x.groupby("day")[col].sum()
        return pd.Series({"n": len(x), "days": len(d), "mean%": 100 * x[col].mean(),
                          "t_day": d.mean() / (d.std() / np.sqrt(len(d))) if len(d) > 2 else np.nan})
    F = A[A.tr == "fall"].copy()
    # quintile cut on all bars' s1 (global)
    qs = A["s1"].quantile([0.2, 0.4, 0.6, 0.8]).values
    out["s1 quintile edges"] = pd.Series(qs)
    for hz in [1, 3, 7]:
        g = F[F.pos % hz == 0].dropna(subset=[f"x{hz}", "s1"]).copy()
        g["q"] = np.digitize(g["s1"], qs)
        out[f"fall: x{hz} by s1 quintile"] = g.groupby("q").apply(lambda z: summ(z, f"x{hz}"))
    g = F[F.pos % 3 == 0].dropna(subset=["x3", "s1"]).copy()
    up = g[g.s1 > 0]
    sl = stats.linregress(up["s1"], up["x3"])
    out["fall up-days x3 on s1 slope"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(up)})
    g["top"] = g["s1"] > qs[3]
    T = g[g.top]
    out["fall top-s1 x3 by year"] = T.groupby("year").apply(lambda z: summ(z, "x3"))
    out["fall top-s1 x3 by coin"] = T.groupby("coin").apply(lambda z: summ(z, "x3"))
    out["fall top-s1 x3 by agit"] = T.groupby("agit").apply(lambda z: summ(z, "x3"))
    out["fall top-s1 x3 by window"] = T.groupby("w").apply(lambda z: summ(z, "x3"))
    # same for s2 scaled 2-day rise in falling
    g2 = F[F.pos % 3 == 0].dropna(subset=["x3", "s2"]).copy()
    g2["q"] = pd.qcut(g2["s2"], 5, labels=False)
    out["fall: x3 by s2 quintile"] = g2.groupby("q").apply(lambda z: summ(z, "x3"))
    # other trends top s1, by agitation
    g3 = A[A.pos % 3 == 0].dropna(subset=["x3", "s1"]).copy()
    g3 = g3[g3.s1 > qs[3]]
    out["top-s1 x3 by trend x agit"] = g3.groupby(["tr", "agit"]).apply(lambda z: summ(z, "x3"))
    # weekday next-day by year
    G1 = A.dropna(subset=["x1"])
    out["x1 Wed by year"] = G1[G1.wd == 2].groupby("year").apply(lambda z: summ(z, "x1"))
    out["x1 Thu by year"] = G1[G1.wd == 3].groupby("year").apply(lambda z: summ(z, "x1"))
    return out
