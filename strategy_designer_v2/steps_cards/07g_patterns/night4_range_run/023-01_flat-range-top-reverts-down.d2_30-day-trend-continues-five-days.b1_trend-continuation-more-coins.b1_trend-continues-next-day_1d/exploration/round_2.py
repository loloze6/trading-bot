def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            df = pd.DataFrame(index=b.index)
            df["coin"] = coin; df["win"] = w
            df["pos"] = np.arange(len(b))
            df["ts"] = pd.to_datetime(b["timestamp"], utc=True)
            df["r1"] = c.pct_change()
            df["f1"] = c.shift(-1) / c - 1
            df["f5"] = c.shift(-5) / c - 1
            df["r5"] = c / c.shift(5) - 1
            df["vol20"] = df["r1"].rolling(20).std()
            hh = h.rolling(30).max(); ll = l.rolling(30).min()
            df["nmr"] = (c - c.shift(30)).abs() / (hh - ll)
            df["rangepos"] = (c - (hh + ll) / 2) / (hh - ll)
            df["fc"] = b["forecast"].astype(float)
            df["alloc"] = b["postRebalance_current_allocation"].astype(float)
            df["regime"] = b["regime"].astype(str)
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["x1"] = d["f1"] - d.groupby("coin")["f1"].transform("mean")
    d["z1"] = d["r1"] / d["vol20"]
    d["z5"] = d["r5"] / (d["vol20"] * np.sqrt(5))
    out = {}
    def summ(s):
        s = s.dropna(); n = len(s)
        if n < 3: return pd.Series({"n": n, "mean%": np.nan, "t": np.nan})
        return pd.Series({"n": n, "mean%": 100 * s.mean(), "t": s.mean() / (s.std() / np.sqrt(n))})
    def tab(df, keys, col):
        return df.groupby(keys)[col].apply(summ).unstack()
    def safe(name, f):
        try: out[name] = f()
        except Exception as e: out[name] = "error: " + str(e)[:150]
    d["z1q"] = pd.qcut(d["z1"], 10, labels=False, duplicates="drop")
    safe("next1_by_z1_decile", lambda: tab(d, "z1q", "x1"))
    d["z5q"] = pd.qcut(d["z5"], 10, labels=False, duplicates="drop")
    safe("next1_by_z5_decile", lambda: tab(d, "z5q", "x1"))
    d["flat"] = np.where(d["nmr"] < 0.25, "flat", np.where(d["nmr"] >= 0.5, "trend", "mid"))
    d["bigmove"] = pd.cut(d["z1"], [-99, -2, -1, 1, 2, 99])
    safe("next1_by_z1band_flatness", lambda: tab(d, ["flat", "bigmove"], "x1"))
    def g5f():
        g5 = d[d["pos"] % 5 == 0].copy()
        g5["x5"] = g5["f5"] - g5.groupby("coin")["f5"].transform("mean")
        g5["rpq"] = pd.cut(g5["rangepos"], [-0.51, -0.3, -0.1, 0.1, 0.3, 0.51])
        return tab(g5, ["flat", "rpq"], "x5")
    safe("fwd5_nonoverlap_by_rangepos_flatness", g5f)
    d["volq"] = d.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    safe("next1_by_vol_quintile", lambda: tab(d, "volq", "x1"))
    d["wd"] = d["ts"].dt.dayofweek
    safe("next1_by_weekday_of_bar", lambda: tab(d, "wd", "x1"))
    a = d[d["fc"] != 0].copy()
    a["signed"] = np.sign(a["fc"]) * a["x1"]
    a["fq"] = pd.qcut(a["fc"].abs(), 5, labels=False, duplicates="drop")
    safe("active_signed_next1_by_absfc_quintile", lambda: tab(a, "fq", "signed"))
    a["gain"] = a["alloc"] * a["f1"]
    a["side"] = np.sign(a["fc"])
    safe("gain_by_side", lambda: tab(a, "side", "gain"))
    safe("signed_next1_by_side", lambda: tab(a, "side", "signed"))
    safe("regime_share", lambda: d["regime"].value_counts(normalize=True))
    def books():
        dd = []
        for coin, wins in data["days"].items():
            for w, t in wins.items():
                t = t.copy(); t["coin"] = coin; t["win"] = w
                t["year"] = pd.to_datetime(t["day"]).dt.year
                dd.append(t)
        dd = pd.concat(dd, ignore_index=True)
        bd = dd.groupby(["win", "day"]).agg(book=("book_return", "mean"), coin=("coin_return", "mean"), year=("year", "first")).dropna()
        yr = bd.groupby("year").agg(n=("book", "size"), book_pct=("book", lambda s: 100 * s.mean()), coin_pct=("coin", lambda s: 100 * s.mean()))
        q = bd["book"].quantile([0.02, 0.98])
        top = bd[bd["book"] >= q.iloc[1]]; bot = bd[bd["book"] <= q.iloc[0]]
        ext = pd.DataFrame({"n": [len(top), len(bot)], "book%": [100 * top["book"].mean(), 100 * bot["book"].mean()],
                            "coin%": [100 * top["coin"].mean(), 100 * bot["coin"].mean()],
                            "share_of_total_gain": [top["book"].sum() / bd["book"].sum(), bot["book"].sum() / bd["book"].sum()]},
                           index=["top2%", "bottom2%"])
        return yr, ext
    try:
        yr, ext = books(); out["book_by_year"] = yr; out["book_extremes"] = ext
    except Exception as e:
        out["book"] = "error: " + str(e)[:150]
    return out
