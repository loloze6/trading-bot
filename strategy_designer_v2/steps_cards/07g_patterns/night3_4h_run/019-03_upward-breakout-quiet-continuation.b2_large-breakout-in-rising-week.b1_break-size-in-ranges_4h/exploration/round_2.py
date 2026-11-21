def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        feats = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            rng = h - l
            mr180 = rng.rolling(180, min_periods=90).mean()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "year": ts.dt.year, "wd": ts.dt.weekday,
                               "r6": c / c.shift(6) - 1, "r42": c / c.shift(42) - 1,
                               "r6n": (c - c.shift(6)) / mr180,
                               "f6": c.shift(-6) / c - 1, "f12": c.shift(-12) / c - 1, "f18": c.shift(-18) / c - 1})
            df["sd6"] = (c / c.shift(1) - 1).rolling(180, min_periods=90).std() * np.sqrt(6)
            df["r6z"] = df["r6"] / df["sd6"]
            df["pos"] = np.arange(len(df))
            feats.append(df)
        cf = pd.concat(feats, ignore_index=True)
        for hz in (6, 12, 18):
            g = cf[cf["pos"] % hz == 0]
            fr = g["f%d" % hz]
            cf.loc[g.index, "x%d" % hz] = fr - fr.mean()
            cf.loc[g.index, "z%d" % hz] = (fr - fr.mean()) / fr.std()
            cf.loc[g.index, "grid%d" % hz] = True
        rows.append(cf)
    A = pd.concat(rows, ignore_index=True)

    def summ(df, key, hz=6):
        g = df[df["grid%d" % hz] == True].dropna(subset=["x%d" % hz])
        res = g.groupby(key).agg(n=("x%d" % hz, "size"), mean_x=("x%d" % hz, "mean"),
                                 strength=("z%d" % hz, "mean"), sd=("z%d" % hz, "std"))
        res["t_z"] = res["strength"] / (res["sd"] / np.sqrt(res["n"]))
        return res.drop(columns="sd").round(4)
    out = {}
    A["zq"] = A.groupby("coin")["r6z"].transform(lambda s: pd.qcut(s, 10, labels=False, duplicates="drop"))
    out["1d ret z decile, 1d"] = summ(A, "zq", 6)
    out["1d ret z decile, 2d"] = summ(A, "zq", 12)
    out["1d ret z decile, 3d"] = summ(A, "zq", 18)
    low = A[A["zq"] <= 1]
    out["bottom 2 deciles by coin, 1d"] = summ(low, "coin", 6)
    out["bottom 2 deciles by year, 1d"] = summ(low, "year", 6)
    low = low.assign(wk=np.where(low["r42"] > 0, "wk+", "wk-"))
    out["bottom 2 deciles by week sign, 1d"] = summ(low, "wk", 6)
    out["friday by coin, 1d"] = summ(A[A["wd"] == 4], "coin", 6)
    out["friday by year, 1d"] = summ(A[A["wd"] == 4], "year", 6)
    g = A[(A["grid6"] == True)].dropna(subset=["x6", "r6z"])
    out["corr r6z vs z6 by coin"] = g.groupby("coin").apply(lambda d: d["r6z"].corr(d["z6"])).round(4)
    return out
