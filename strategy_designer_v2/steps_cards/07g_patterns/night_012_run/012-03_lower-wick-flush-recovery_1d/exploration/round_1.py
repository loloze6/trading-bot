def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(20, min_periods=20).std()
            z = r1 / sd
            vr = b["volume"] / b["volume"].shift(1).rolling(20, min_periods=20).mean()
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            clr = (c - b["low"]) / rng
            fwd1 = c.shift(-1) / c - 1
            fwd3 = c.shift(-3) / c - 1
            fwd7 = c.shift(-7) / c - 1
            ret5 = c / c.shift(5) - 1
            ret20 = c / c.shift(20) - 1
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)), "z": z, "vr": vr,
                               "clr": clr, "f1": fwd1, "f3": fwd3, "f7": fwd7, "sd": sd,
                               "r5": ret5, "r20": ret20,
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                               "year": pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    m3 = d[d.pos % 3 == 0].groupby("coin")["f3"].mean()
    m1 = d.groupby("coin")["f1"].mean()
    m7 = d[d.pos % 7 == 0].groupby("coin")["f7"].mean()
    d["x1"] = d.f1 - d.coin.map(m1)
    d["x3"] = d.f3 - d.coin.map(m3)
    d["x7"] = d.f7 - d.coin.map(m7)
    out = {}

    def summ(g, col):
        g = g.dropna(subset=[col])
        n = len(g)
        mu = g[col].mean()
        t = mu / (g[col].std() / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series({"n": n, "mean": mu, "t": t})

    # 1: next-day excess return by z bucket of today's move (all bars, h=1)
    d["zb"] = pd.cut(d.z, [-np.inf, -3, -2, -1, 1, 2, 3, np.inf])
    out["x1_by_zbucket"] = d.groupby("zb", observed=True).apply(lambda g: summ(g, "x1"))
    # 2: 3-day excess on grid by z bucket and volume burst
    g3 = d[d.pos % 3 == 0].copy()
    g3["vb"] = g3.vr >= 2
    out["x3_by_zbucket_vburst"] = g3.groupby(["zb", "vb"], observed=True).apply(lambda g: summ(g, "x3"))
    # 3: sharp falls (z<=-2) on all bars, next 3d by clr tercile and vburst (not grid thinned, report)
    sf = d[(d.z <= -2)].copy()
    sf["vb"] = sf.vr >= 2
    sf["clrb"] = pd.cut(sf.clr, [0, 0.2, 0.4, 1.0], include_lowest=True)
    out["sharpfall_x3_by_clr_vb"] = sf.groupby(["vb", "clrb"], observed=True).apply(lambda g: summ(g, "x3"))
    # 4: sharp rises with vburst
    sr = d[(d.z >= 2)].copy()
    sr["vb"] = sr.vr >= 2
    out["sharprise_x3_x7_vb"] = sr.groupby("vb").apply(lambda g: pd.concat([summ(g, "x3").add_prefix("3_"), summ(g, "x7").add_prefix("7_")]))
    # 5: weekday next-day excess
    out["x1_by_weekday"] = d.groupby("wd").apply(lambda g: summ(g, "x1"))
    # 6: vol level quintile (per coin) -> 7d excess on grid
    d["sdq"] = d.groupby("coin")["sd"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    g7 = d[d.pos % 7 == 0]
    out["x7_by_volquintile"] = g7.groupby("sdq").apply(lambda g: summ(g, "x7"))
    # 7: 20d return quintile -> 7d excess (grid)
    d["r20q"] = d.groupby("coin")["r20"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    g7 = d[d.pos % 7 == 0]
    out["x7_by_r20quintile"] = g7.groupby("r20q").apply(lambda g: summ(g, "x7"))
    # 8: 5d return quintile -> 3d excess (grid)
    d["r5q"] = d.groupby("coin")["r5"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    g3 = d[d.pos % 3 == 0]
    out["x3_by_r5quintile"] = g3.groupby("r5q").apply(lambda g: summ(g, "x3"))
    # 9: book by year
    br = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd[["day", "book_return", "coin_return"]].copy()
            x["year"] = pd.to_datetime(x["day"]).dt.year
            br.append(x)
    br = pd.concat(br)
    out["book_by_year"] = br.groupby("year").agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"),
                                                 n=("book_return", "count"))
    # 10: per-coin x3 after flush (z<=-2, vr>=2), all flush bars
    fl = d[(d.z <= -2) & (d.vr >= 2)]
    out["flush_x3_by_coin"] = fl.groupby("coin").apply(lambda g: summ(g, "x3"))
    return out
