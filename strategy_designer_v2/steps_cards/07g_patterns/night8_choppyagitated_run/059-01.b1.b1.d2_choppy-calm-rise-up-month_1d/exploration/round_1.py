def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True).copy()
            c = df["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=30).std()
            df["s7"] = (c / c.shift(7) - 1) / (sd30 * np.sqrt(7))
            df["r30"] = c / c.shift(30) - 1
            df["z1"] = r1 / sd30.shift(1)
            df["f14"] = c.shift(-14) / c - 1
            df["f3"] = c.shift(-3) / c - 1
            df["f1"] = c.shift(-1) / c - 1
            df["sdpct"] = sd30
            df["pos"] = np.arange(len(df))
            df["coin"] = coin; df["win"] = w
            df["prof"] = np.where(df["regime"].isin(["trending", "unknown"]), "cc", "out")
            df["wd"] = pd.to_datetime(df["timestamp"]).dt.weekday
            rows.append(df[["coin", "win", "pos", "s7", "r30", "z1", "f14", "f3", "f1", "regime", "prof", "forecast", "wd", "sdpct", "timestamp"]])
    A = pd.concat(rows, ignore_index=True)
    g14 = A[A["pos"] % 14 == 0].dropna(subset=["f14"]).copy()
    g14["drift"] = g14.groupby("coin")["f14"].transform("mean")
    g14["u14"] = g14["f14"] - g14["drift"]
    out = {}
    def tab(df, key, val, q=None):
        d = df.dropna(subset=[key, val]).copy()
        if q:
            d["b"] = pd.qcut(d[key], q, labels=False, duplicates="drop")
        else:
            d["b"] = d[key]
        t = d.groupby("b")[val].agg(["count", "mean", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        t["key_mean"] = d.groupby("b")[key].mean()
        return t.round(4)
    out["s7 quint -> u14, regime trending"] = tab(g14[g14.regime == "trending"], "s7", "u14", 5)
    out["s7 quint -> u14, regime unknown (cc, r30<=0)"] = tab(g14[g14.regime == "unknown"], "s7", "u14", 5)
    out["s7 quint -> u14, outside profile"] = tab(g14[g14.prof == "out"], "s7", "u14", 5)
    out["s7 quint -> u14, all"] = tab(g14, "s7", "u14", 5)
    out["r30 quint -> u14, all"] = tab(g14, "r30", "u14", 5)
    out["r30 quint -> u14, cc"] = tab(g14[g14.prof == "cc"], "r30", "u14", 5)
    # 3-day grid after large daily moves
    g3 = A[A["pos"] % 3 == 0].dropna(subset=["f3", "z1"]).copy()
    g3["u3"] = g3["f3"] - g3.groupby("coin")["f3"].transform("mean")
    out["z1 quint -> u3, out profile"] = tab(g3[g3.prof == "out"], "z1", "u3", 5)
    out["z1 quint -> u3, cc"] = tab(g3[g3.prof == "cc"], "z1", "u3", 5)
    g1 = A.dropna(subset=["f1", "z1"]).copy()
    g1["u1"] = g1["f1"] - g1.groupby("coin")["f1"].transform("mean")
    out["z1 quint -> u1, all"] = tab(g1, "z1", "u1", 5)
    out["weekday -> u1, all"] = tab(g1, "wd", "u1")
    # vol level
    g14["sdq"] = g14.groupby("coin")["sdpct"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["sd tercile within coin -> u14"] = tab(g14, "sdq", "u14")
    # book by weekday
    D = []
    for coin, wins in days.items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D); D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    out["book_return by weekday"] = tab(D, "wd", "book_return")
    out["book_return by window"] = D.groupby("win")["book_return"].agg(["count", "mean", "sum"]).round(5)
    out["regime counts"] = A["regime"].value_counts()
    return out
