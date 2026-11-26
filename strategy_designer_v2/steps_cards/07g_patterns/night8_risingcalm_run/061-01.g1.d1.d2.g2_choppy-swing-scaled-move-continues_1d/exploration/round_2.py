def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "z1": r1 / sd30,
                "z5": (c / c.shift(5) - 1) / sd30,
                "f1": c.shift(-1) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "f5": c.shift(-5) / c - 1,
                "chop": (b["regime"] == "unknown").astype(int),
                "tr60": c / c.shift(60) - 1,
                "sd30": sd30,
                "cl": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "year": pd.to_datetime(b["timestamp"]).dt.year,
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for h in (1, 3, 5):
        g = D[D["pos"] % h == 0]
        m = g.groupby("coin")["f%d" % h].mean()
        D["a%d" % h] = D["f%d" % h] - D["coin"].map(m)
    # agitation proxy: sd30 vs coin's median sd30 over the shown windows (descriptive)
    med = D.groupby("coin")["sd30"].median()
    D["agit"] = (D["sd30"] > D["coin"].map(med)).astype(int)
    D["trend"] = np.where(D["chop"] == 1, "choppy",
                  np.where(D["tr60"] > 0.10, "rising", np.where(D["tr60"] < -0.10, "falling", "na")))

    def dayt(df, col):
        df = df.dropna(subset=[col])
        s = df.groupby("day")[col].sum()
        n = len(s)
        if n < 5: return (np.nan, np.nan, len(df))
        return (df[col].mean(), s.mean() / (s.std(ddof=1) / np.sqrt(n)), len(df))

    def slope_t(df, x, y):
        df = df.dropna(subset=[x, y])
        if len(df) < 30: return (np.nan, np.nan, len(df))
        X = df[x].values; Y = df[y].values
        Xc = X - X.mean(); b = (Xc * (Y - Y.mean())).sum() / (Xc ** 2).sum()
        e = (Y - Y.mean()) - b * Xc
        sc = pd.Series(Xc * e).groupby(df["day"].values).sum()
        se = np.sqrt((sc ** 2).sum()) / (Xc ** 2).sum()
        return (b, b / se, len(df))

    out = {}
    res = []
    for tr in ("rising", "falling", "choppy"):
        for ag in (0, 1):
            for h in (1, 3, 5):
                g = D[(D["pos"] % h == 0) & (D["trend"] == tr) & (D["agit"] == ag)].copy()
                b5, t5, n5 = slope_t(g, "z5", "a%d" % h)
                b1, t1, n1 = slope_t(g, "z1", "a%d" % h)
                res.append([tr, ag, h, b5, t5, b1, t1, n5])
    out["slopes_by_profile"] = pd.DataFrame(res, columns=["trend", "agit", "h", "b_z5", "t_z5", "b_z1", "t_z1", "n"])
    # continuation by side of the 5-day move, trend markets, h3
    res = []
    for tr in ("rising", "falling"):
        for h in (3, 5):
            g = D[(D["pos"] % h == 0) & (D["trend"] == tr)].dropna(subset=["z5", "a%d" % h]).copy()
            for side in (-1, 1):
                gg = g[np.sign(g["z5"]) == side].copy()
                gg["x"] = side * gg["a%d" % h]
                q = gg["z5"].abs().quantile(2/3)
                m, t, n = dayt(gg, "x"); mt, tt, nt = dayt(gg[gg["z5"].abs() > q], "x")
                res.append([tr, h, side, m, t, n, mt, tt, nt])
    out["z5_side_trend"] = pd.DataFrame(res, columns=["trend", "h", "side", "mean", "t", "n", "top_mean", "top_t", "top_n"])
    # 1-day reversal by trend, by year (stability)
    g = D[D["trend"].isin(["rising", "falling"])].dropna(subset=["z1", "a1"]).copy()
    g["x"] = np.sign(g["z1"]) * g["a1"]
    res = []
    for y, gg in g.groupby("year"):
        m, t, n = dayt(gg, "x"); res.append([y, m, t, n])
    out["z1_rev1_trend_by_year"] = pd.DataFrame(res, columns=["year", "mean", "t", "n"])
    res = []
    for tr in ("rising", "falling"):
        for side in (-1, 1):
            gg = g[(g["trend"] == tr) & (np.sign(g["z1"]) == side)]
            m, t, n = dayt(gg, "x"); res.append([tr, side, m, t, n])
    out["z1_rev1_trend_side"] = pd.DataFrame(res, columns=["trend", "side", "mean", "t", "n"])
    g = D[(D["pos"] % 3 == 0) & D["trend"].isin(["rising", "falling"])].dropna(subset=["z5", "a3"]).copy()
    g["x"] = np.sign(g["z5"]) * g["a3"]
    res = []
    for y, gg in g.groupby("year"):
        m, t, n = dayt(gg, "x"); res.append([y, m, t, n])
    out["z5_cont3_trend_by_year"] = pd.DataFrame(res, columns=["year", "mean", "t", "n"])
    out["trend_counts"] = D["trend"].value_counts()
    return out
