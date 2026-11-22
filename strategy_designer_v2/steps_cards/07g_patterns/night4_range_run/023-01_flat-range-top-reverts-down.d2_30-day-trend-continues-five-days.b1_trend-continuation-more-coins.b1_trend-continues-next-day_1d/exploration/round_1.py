def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            df = pd.DataFrame({"coin": coin, "win": w})
            df["pos"] = np.arange(len(b))
            df["ts"] = pd.to_datetime(b["timestamp"], utc=True)
            df["r1"] = c.pct_change()
            df["f1"] = c.shift(-1) / c - 1
            df["f3"] = c.shift(-3) / c - 1
            df["f5"] = c.shift(-5) / c - 1
            df["r5"] = c / c.shift(5) - 1
            df["vol20"] = df["r1"].rolling(20).std()
            hh = h.rolling(30).max(); ll = l.rolling(30).min()
            df["nmr"] = (c - c.shift(30)).abs() / (hh - ll)
            df["rangepos"] = (c - (hh + ll) / 2) / (hh - ll)
            df["fc"] = b["forecast"].astype(float)
            df["alloc"] = b["postRebalance_current_allocation"].astype(float)
            df["regime"] = b["regime"]
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    mu1 = d.groupby("coin")["f1"].transform("mean")
    d["x1"] = d["f1"] - mu1
    d["z1"] = d["r1"] / d["vol20"]
    d["z5"] = d["r5"] / (d["vol20"] * np.sqrt(5))
    out = {}
    def summ(g, col):
        s = g[col].dropna()
        n = len(s); m = s.mean(); sd = s.std()
        return pd.Series({"n": n, "mean%": 100 * m, "t": m / (sd / np.sqrt(n)) if n > 2 else np.nan})
    # 1: next-day excess by z of today's move
    d["z1q"] = pd.qcut(d["z1"], 10, labels=False, duplicates="drop")
    out["next1_by_z1_decile"] = d.groupby("z1q").apply(lambda g: summ(g, "x1"))
    # 2: next-day excess by 5-day z
    d["z5q"] = pd.qcut(d["z5"], 10, labels=False, duplicates="drop")
    out["next1_by_z5_decile"] = d.groupby("z5q").apply(lambda g: summ(g, "x1"))
    # 3: brief: 5-day fwd (non-overlapping grid) by range position, flat vs trending
    g5 = d[d["pos"] % 5 == 0].copy()
    mu5 = d[d["pos"] % 5 == 0].groupby("coin")["f5"].transform("mean")
    g5["x5"] = g5["f5"] - mu5
    g5["flat"] = np.where(g5["nmr"] < 0.25, "flat", np.where(g5["nmr"] >= 0.5, "trend", "mid"))
    g5["rpq"] = pd.cut(g5["rangepos"], [-0.51, -0.3, -0.1, 0.1, 0.3, 0.51])
    out["fwd5_by_rangepos_flatness"] = g5.groupby(["flat", "rpq"]).apply(lambda g: summ(g, "x5")).reset_index()
    # 4: vol level
    d["volq"] = d.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["next1_by_vol_quintile"] = d.groupby("volq").apply(lambda g: summ(g, "x1"))
    # 5: weekday
    d["wd"] = d["ts"].dt.dayofweek
    out["next1_by_weekday_of_bar"] = d.groupby("wd").apply(lambda g: summ(g, "x1"))
    # 6: forecast deciles active
    a = d[d["fc"] != 0].copy()
    a["fq"] = pd.qcut(a["fc"], 10, labels=False, duplicates="drop")
    a["signed"] = np.sign(a["fc"]) * a["x1"]
    out["active_signed_next1_by_fc_decile"] = a.groupby("fq").apply(lambda g: pd.concat([summ(g, "signed"), pd.Series({"fc_mean": g["fc"].mean()})]))
    # 7: long vs short gains
    a["gain"] = a["alloc"] * a["f1"]
    out["gain_by_side"] = a.groupby(np.sign(a["fc"])).apply(lambda g: summ(g, "gain"))
    # 8: book daily: largest gains/losses
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["win"] = w; t["year"] = pd.to_datetime(t["day"]).dt.year
            dd.append(t)
    dd = pd.concat(dd, ignore_index=True)
    out["book_by_year"] = dd.groupby("year").apply(lambda g: pd.Series({"n": g["book_return"].notna().sum(), "book%": 100 * g["book_return"].mean(), "coin%": 100 * g["coin_return"].mean()}))
    # regime counts
    out["regime_share"] = d["regime"].value_counts(normalize=True)
    return out
