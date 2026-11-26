def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True).copy()
            c = df["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30).std()
            hi5 = c.rolling(5).max()
            pb = (c - hi5) / hi5 / sd30
            ret5 = c.pct_change(5)
            ret60 = c / c.shift(60) - 1
            fwd5 = c.shift(-5) / c - 1
            fwd2 = c.shift(-2) / c - 1
            ts = pd.to_datetime(df["timestamp"])
            g = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(df)),
                              "rc": (df["regime"] == "unknown").astype(int),
                              "pb": pb, "r1z": r1 / sd30, "ret5z": ret5 / (sd30 * np.sqrt(5)),
                              "sd30": sd30, "ret60": ret60, "fwd5": fwd5, "fwd2": fwd2,
                              "day": ts.dt.floor("D")})
            rows.append(g)
    A = pd.concat(rows, ignore_index=True)
    for h, col in [(5, "fwd5"), (2, "fwd2")]:
        d = A[A["pos"] % h == 0].groupby("coin")[col].mean()
        A["ex" + str(h)] = A[col] - A["coin"].map(d)
    med = A.groupby("coin")["sd30"].transform("median")
    A["agit"] = np.where(A["sd30"] > med, "agit", "calm")
    A["trend"] = np.where(A["ret60"] > 0.1, "rising", np.where(A["ret60"] < -0.1, "falling", np.where(A["ret60"].isna(), "na", "choppy")))
    A["prof"] = A["trend"] + "_" + A["agit"]
    def clt(df, x, y):
        df = df.dropna(subset=[x, y])
        if len(df) < 20: return pd.Series({"n": len(df), "days": 0, "slope": np.nan, "t": np.nan})
        X = df[x] - df[x].mean(); Y = df[y]
        b = (X * Y).sum() / (X ** 2).sum()
        e = Y - Y.mean() - b * X
        s = (X * e).groupby(df["day"]).sum()
        G = len(s)
        se = np.sqrt((s ** 2).sum() * G / (G - 1)) / (X ** 2).sum()
        return pd.Series({"n": len(df), "days": G, "slope": b, "t": b / se})
    def mean_clt(df, y):
        df = df.dropna(subset=[y])
        s = (df[y] - df[y].mean()).groupby(df["day"]).sum()
        G = len(s)
        se = np.sqrt((s ** 2).sum() * G / (G - 1)) / len(df)
        return pd.Series({"n": len(df), "days": G, "mean": df[y].mean(), "t": df[y].mean() / se})
    out = {}
    G5 = A[A["pos"] % 5 == 0]
    G2 = A[A["pos"] % 2 == 0]
    out["5d momentum slope ex5 on ret5z, by profile"] = G5.groupby("prof").apply(lambda d: clt(d, "ret5z", "ex5")).round(4)
    out["5d momentum slope all"] = clt(G5, "ret5z", "ex5").round(4)
    out["pb slope ex5 on pb, by profile"] = G5.groupby("prof").apply(lambda d: clt(d, "pb", "ex5")).round(4)
    out["pb slope ex5 by rc"] = G5.groupby("rc").apply(lambda d: clt(d, "pb", "ex5")).round(4)
    out["1d move slope ex2 on r1z, by profile"] = G2.groupby("prof").apply(lambda d: clt(d, "r1z", "ex2")).round(4)
    h = G5.copy(); h["athigh"] = (h["pb"] == 0).astype(int)
    out["at 5d high ex5 by rc"] = h.groupby(["rc", "athigh"]).apply(lambda d: mean_clt(d, "ex5")).round(4)
    out["ret5z slope by window half"] = G5.assign(half=np.where(G5["w"].str[1:].astype(int) <= 12, "w7-12", "w13-18")).groupby("half").apply(lambda d: clt(d, "ret5z", "ex5")).round(4)
    out["ret5z slope by coin"] = G5.groupby("coin").apply(lambda d: clt(d, "ret5z", "ex5")).round(4)
    return out
