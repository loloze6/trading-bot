def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    hourly = []
    for coin, wins in data["bars"].items():
        # coin drift of non-overlapping 48-bar returns
        d48 = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 48, 48)
            d48.extend(c[idx + 48] / c[idx] - 1)
        drift48 = np.mean(d48)
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            ct = ts + pd.Timedelta(hours=1)
            c = df["close"]
            r1 = c / c.shift(1) - 1
            r24 = c / c.shift(24) - 1
            r48p = c / c.shift(48) - 1
            sc = r24.abs().rolling(720, min_periods=240).mean()
            f48 = c.shift(-48) / c - 1
            f24 = c.shift(-24) / c - 1
            volrank = sc / sc.rolling(2000, min_periods=500).median()
            t = pd.DataFrame({"coin": coin, "win": w, "wd": ct.dt.weekday, "hr": ct.dt.hour,
                              "z": r24 / sc, "z48": r48p / sc, "f48": f48 - drift48, "f24": f24,
                              "f48s": (f48 - drift48) / sc, "vr": volrank, "year": ct.dt.year})
            rows.append(t[t["hr"] == 0])
            hourly.append(pd.DataFrame({"hr": ts.dt.hour, "wd": ts.dt.weekday, "r1": r1}))
    A = pd.concat(rows).dropna(subset=["z", "f48"])
    def reg(g, x="z", y="f48"):
        g = g.dropna(subset=[x, y])
        if len(g) < 30: return pd.Series({"n": len(g)})
        s = stats.linregress(g[x], g[y])
        return pd.Series({"n": len(g), "slope": s.slope, "t": s.slope / s.stderr})
    out = {}
    out["fwd48 on prior24 z, by close weekday (0=Mon)"] = A.groupby("wd").apply(reg)
    out["fwd24 on prior24 z, by close weekday"] = A.groupby("wd").apply(lambda g: reg(g, "z", "f24"))
    out["fwd48 on prior48 z (weekend=Mon)"] = A.groupby("wd").apply(lambda g: reg(g, "z48", "f48"))
    M = A[A["wd"] == 0].copy()
    M["volq"] = pd.qcut(M["vr"], 3, labels=["lowvol", "mid", "highvol"])
    out["Monday: by vol tercile"] = M.groupby("volq").apply(reg)
    out["Monday: by coin"] = M.groupby("coin").apply(reg)
    out["Monday: by year"] = M.groupby("year").apply(reg)
    M["zq"] = pd.qcut(M["z"], 5, labels=False)
    out["Monday: f48 by z quintile"] = M.groupby("zq").agg(n=("f48", "size"), z=("z", "mean"), f48=("f48", "mean"))
    H = pd.concat(hourly).dropna()
    hh = H.groupby("hr")["r1"].agg(["mean", "std", "count"])
    hh["t"] = hh["mean"] / (hh["std"] / np.sqrt(hh["count"]))
    out["1h return by start hour"] = hh[["mean", "t", "count"]]
    # book by weekday
    D = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            x = df.copy(); x["wd"] = pd.to_datetime(x["day"]).dt.weekday; D.append(x)
    D = pd.concat(D).dropna(subset=["book_return", "coin_return"])
    bw = D.groupby("wd").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "size"))
    bw["coin_t"] = D.groupby("wd")["coin_return"].apply(lambda s: s.mean() / (s.std() / np.sqrt(len(s))))
    out["daily by weekday"] = bw
    return out
