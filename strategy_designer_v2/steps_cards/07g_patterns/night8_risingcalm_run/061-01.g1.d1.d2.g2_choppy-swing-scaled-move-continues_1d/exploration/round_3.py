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
                "z1": r1 / sd30, "sd30": sd30,
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1,
                "tr60": c / c.shift(60) - 1,
                "cl": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "chop": (b["regime"] == "unknown").astype(int),
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for h in (1, 2):
        g = D[D["pos"] % h == 0]
        m = g.groupby("coin")["f%d" % h].mean()
        D["a%d" % h] = D["f%d" % h] - D["coin"].map(m)
    med = D.groupby("coin")["sd30"].median()
    D["agit"] = (D["sd30"] > D["coin"].map(med)).astype(int)
    D["fall"] = ((D["tr60"] < -0.10) & (D["chop"] == 0)).astype(int)

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
    FA = D[(D["fall"] == 1) & (D["agit"] == 1)].dropna(subset=["z1", "a1"])
    up = FA[FA["z1"] > 0].copy()
    dn = FA[FA["z1"] < 0].copy()
    res = []
    for lab, g in (("up", up), ("down", dn)):
        b, t, n = slope_t(g, "z1", "a1"); res.append([lab, "h1", b, t, n])
        g2 = g[g["pos"] % 2 == 0]
        b, t, n = slope_t(g2, "z1", "a2"); res.append([lab, "h2", b, t, n])
    out["FA_slope_by_side"] = pd.DataFrame(res, columns=["side", "h", "b", "t", "n"])
    up["zb"] = pd.qcut(up["z1"], 3, labels=False)
    res = []
    for q in range(3):
        m, t, n = dayt(up[up["zb"] == q], "a1"); res.append([q, up[up["zb"] == q]["z1"].mean(), m, t, n])
    out["FA_up_terciles_a1"] = pd.DataFrame(res, columns=["tercile", "z_mean", "mean_a1", "t", "n"])
    res = []
    for y, g in up.groupby("year"):
        b, t, n = slope_t(g, "z1", "a1"); m, tm, _ = dayt(g, "a1"); res.append([y, b, t, m, tm, n])
    out["FA_up_by_year"] = pd.DataFrame(res, columns=["year", "b", "t", "mean_a1", "t_mean", "n"])
    res = []
    for cn, g in up.groupby("coin"):
        b, t, n = slope_t(g, "z1", "a1"); res.append([cn, b, t, n])
    out["FA_up_by_coin"] = pd.DataFrame(res, columns=["coin", "b", "t", "n"])
    # other falling calm / rising agitated up-days for contrast
    res = []
    for lab, g in (("fall_calm", D[(D["fall"] == 1) & (D["agit"] == 0)]),
                   ("not_fall_agit", D[(D["fall"] == 0) & (D["agit"] == 1)])):
        gg = g[g["z1"] > 0]
        b, t, n = slope_t(gg, "z1", "a1"); res.append([lab, b, t, n])
    out["up_contrast"] = pd.DataFrame(res, columns=["where", "b", "t", "n"])
    return out
