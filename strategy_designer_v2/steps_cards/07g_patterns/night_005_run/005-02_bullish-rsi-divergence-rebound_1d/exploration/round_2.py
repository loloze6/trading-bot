def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            n = len(c); r1 = c.pct_change()
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(n)})
            df["r1p"] = r1
            df["r3p"] = c / c.shift(3) - 1
            df["rng"] = (h - l) / c
            df["clv"] = (c - l) / (h - l).replace(0, np.nan)
            df["vol20"] = r1.rolling(20).std()
            df["z1"] = r1 / df["vol20"].shift(1)
            df["ret30p"] = c / c.shift(30) - 1
            df["dhigh"] = c / c.shift(1).rolling(30).max() - 1
            df["f1"] = c.shift(-1) / c - 1
            df["f3"] = c.shift(-3) / c - 1
            df["f10"] = c.shift(-10) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df["year"] = ts.dt.year; df["wd"] = ts.dt.dayofweek
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    g1 = D.dropna(subset=["f1"]).copy()
    g1["ex1"] = g1["f1"] - g1["coin"].map(g1.groupby("coin")["f1"].mean())

    def spread(d, col, y, q=5):
        d = d.dropna(subset=[col, y]).copy()
        d["b"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        lo = d[d.b == 0][y]; hi = d[d.b == q-1][y]
        t = stats.ttest_ind(lo, hi, equal_var=False)
        rho = stats.spearmanr(d[col], d[y])
        return pd.Series({"low_minus_high": lo.mean()-hi.mean(), "welch_t": t.statistic,
                          "n_each": len(lo), "spearman": rho[0], "spear_p": rho[1]})
    out["rev1_all"] = spread(g1, "r1p", "ex1")
    out["rev1_z_all"] = spread(g1, "z1", "ex1")
    out["rev1_by_coin"] = pd.DataFrame({c: spread(g1[g1.coin == c], "r1p", "ex1") for c in g1.coin.unique()}).T
    out["rev1_by_year"] = pd.DataFrame({y: spread(g1[g1.year == y], "r1p", "ex1") for y in sorted(g1.year.unique())}).T
    # by vol regime
    g1["vt"] = g1.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["rev1_by_voltercile"] = pd.DataFrame({v: spread(g1[g1.vt == v], "r1p", "ex1") for v in [0, 1, 2]}).T
    # close location value
    out["clv_spread"] = spread(g1, "clv", "ex1")
    # 3-day grid
    g3 = D[D.pos % 3 == 0].dropna(subset=["f3"]).copy()
    g3["ex3"] = g3["f3"] - g3["coin"].map(g3.groupby("coin")["f3"].mean())
    out["rev3_r1p"] = spread(g3, "r1p", "ex3")
    out["rev3_r3p"] = spread(g3, "r3p", "ex3")
    # 30d momentum on 10-day grid
    g10 = D[D.pos % 10 == 0].dropna(subset=["f10"]).copy()
    g10["ex10"] = g10["f10"] - g10["coin"].map(g10.groupby("coin")["f10"].mean())
    out["mom30_10d"] = spread(g10, "ret30p", "ex10")
    out["dhigh_10d"] = spread(g10, "dhigh", "ex10")
    # wednesday by year
    wdy = g1[g1.wd == 2].groupby("year")["ex1"].mean()
    out["wed_by_year"] = wdy
    return out
