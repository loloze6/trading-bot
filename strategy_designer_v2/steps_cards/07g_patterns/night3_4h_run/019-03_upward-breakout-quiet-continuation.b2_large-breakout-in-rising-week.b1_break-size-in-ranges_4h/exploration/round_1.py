def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        feats = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            rng = (h - l)
            mr180 = rng.rolling(180, min_periods=90).mean()
            hh12 = h.shift(1).rolling(12).max(); ll12 = l.shift(1).rolling(12).min()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "up": (c - hh12) / mr180, "dn": (ll12 - c) / mr180,
                "r42": c / c.shift(42) - 1, "r6": c / c.shift(6) - 1,
                "narrow": rng.shift(1).rolling(12).mean() / mr180,
                "volr": rng.rolling(42).mean() / mr180,
                "barret": c / c.shift(1) - 1,
                "f6": c.shift(-6) / c - 1, "f18": c.shift(-18) / c - 1,
                "hour": pd.to_datetime(b["timestamp"]).dt.hour,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
            })
            df["pos"] = np.arange(len(df))
            feats.append(df)
        cf = pd.concat(feats, ignore_index=True)
        for hz in (6, 18):
            g = cf[cf["pos"] % hz == 0]
            fr = g["f%d" % hz]
            cf.loc[g.index, "d%d" % hz] = fr.mean()
            cf.loc[g.index, "s%d" % hz] = fr.std()
            cf.loc[g.index, "grid%d" % hz] = True
        rows.append(cf)
    A = pd.concat(rows, ignore_index=True)
    for hz in (6, 18):
        A["x%d" % hz] = (A["f%d" % hz] - A["d%d" % hz])
        A["z%d" % hz] = A["x%d" % hz] / A["s%d" % hz]

    def summ(df, key, hz=18):
        g = df[df["grid%d" % hz] == True].dropna(subset=["x%d" % hz])
        res = g.groupby(key).agg(n=("x%d" % hz, "size"),
                                 mean_x=("x%d" % hz, "mean"),
                                 mean_f=("f%d" % hz, "mean"),
                                 strength=("z%d" % hz, "mean"),
                                 sd=("z%d" % hz, "std"))
        res["t_z"] = res["strength"] / (res["sd"] / np.sqrt(res["n"]))
        return res.drop(columns="sd").round(4)

    A["upb"] = pd.cut(A["up"], [-np.inf, 0, 0.5, 1, np.inf], labels=["none", "0-.5", ".5-1", "1+"])
    A["dnb"] = pd.cut(A["dn"], [-np.inf, 0, 0.5, 1, np.inf], labels=["none", "0-.5", ".5-1", "1+"])
    A["wk"] = np.where(A["r42"] > 0, "wk+", "wk-")
    A.loc[A["r42"].isna(), "wk"] = np.nan
    out["up_break x week, 18"] = summ(A, ["wk", "upb"])
    out["down_break x week, 18"] = summ(A, ["wk", "dnb"])
    A["nq"] = A.groupby("coin")["narrow"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    A["dirn"] = np.where(A["up"] > 0, "upbrk", np.where(A["dn"] > 0, "dnbrk", "inside"))
    out["narrowness quintile x break dir, 18"] = summ(A, ["nq", "dirn"])
    A["vq"] = A.groupby("coin")["volr"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["vol quintile, 18"] = summ(A, "vq")
    A["r42q"] = A.groupby("coin")["r42"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["7d return quintile, 18"] = summ(A, "r42q")
    A["r6q"] = A.groupby("coin")["r6"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["1d return quintile, 6"] = summ(A, "r6q", 6)
    A["bq"] = A.groupby("coin")["barret"].transform(lambda s: pd.qcut(s, 10, labels=False, duplicates="drop"))
    out["4h bar return decile, 6"] = summ(A, "bq", 6)
    out["hour, 6"] = summ(A, "hour", 6)
    out["weekday, 6"] = summ(A, "wd", 6)
    out["up break 1+ wk+ by coin, 18"] = summ(A[(A["upb"] == "1+") & (A["wk"] == "wk+")], "coin")
    # book days
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            d["next_coin"] = d["coin_return"].shift(-1); d["prev_coin"] = d["coin_return"].shift(1)
            D.append(d)
    D = pd.concat(D).dropna(subset=["book_return"])
    D["bq"] = pd.qcut(D["book_return"].rank(method="first"), 20, labels=False)
    out["book day 20-tile: coin today/prev/next"] = D.groupby("bq")[["book_return", "coin_return", "prev_coin", "next_coin"]].mean().iloc[[0, 1, 2, 17, 18, 19]].round(4)
    return out
