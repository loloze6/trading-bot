def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30).std()
            z14 = (c / c.shift(14) - 1) / (sd30 * np.sqrt(14))
            z1 = r1 / sd30
            ret60 = c / c.shift(60) - 1
            sdexp = sd30.expanding().median()
            n = len(b)
            rows.append(pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(n),
                "day": b["timestamp"].astype(str).str[:10], "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "regime": b["regime"].values, "z14": z14, "z1": z1, "ret60": ret60,
                "agit": (sd30 > sdexp).astype(float).where(sd30.notna()),
                "f7": c.shift(-7) / c - 1, "f1": c.shift(-1) / c - 1}))
    A = pd.concat(rows, ignore_index=True)
    for h, col in [(7, "f7"), (1, "f1")]:
        drift = A[A.pos % h == 0].groupby("coin")[col].mean()
        A["u" + str(h)] = A[col] - A["coin"].map(drift)
    A["trend"] = np.where(A.ret60 > 0.1, "rising", np.where(A.ret60 < -0.1, "falling", "choppy"))
    A.loc[A.ret60.isna(), "trend"] = "na"
    A["prof"] = A["trend"] + np.where(A.agit == 1, "_agit", "_calm")
    def clt(D, x, y):
        D = D.dropna(subset=[x, y])
        if len(D) < 20: return pd.Series({"n": len(D)})
        X = D[x] - D[x].mean(); Y = D[y]
        b = (X * (Y - Y.mean())).sum() / (X ** 2).sum()
        e = Y - Y.mean() - b * X
        s = (X * e).groupby(D["day"]).sum()
        G = len(s)
        se = np.sqrt((s ** 2).sum() * G / (G - 1)) / (X ** 2).sum()
        m = D[y].mean(); sm = (D[y] - m).groupby(D["day"]).sum()
        tm = m / (np.sqrt((sm ** 2).sum() * G / (G - 1)) / len(D))
        return pd.Series({"n": len(D), "days": G, "slope%": b * 100, "t_slope": b / se, "mean%": m * 100, "t_mean": tm})
    G7 = A[A.pos % 7 == 0]
    out = {}
    neg = G7[G7.z14 < 0]; pos = G7[G7.z14 > 0]
    out["z14<0 by profile (slope u7 on z14)"] = neg.groupby("prof").apply(lambda D: clt(D, "z14", "u7"))
    out["z14>0 by profile"] = pos.groupby("prof").apply(lambda D: clt(D, "z14", "u7"))
    out["z14<0 by year"] = neg.groupby("yr").apply(lambda D: clt(D, "z14", "u7"))
    out["z14 all slope"] = clt(G7, "z14", "u7")
    out["z14<0 all"] = clt(neg, "z14", "u7")
    dn = A[A.z1 < 0]
    out["z1<0 by profile (slope u1 on z1)"] = dn.groupby("prof").apply(lambda D: clt(D, "z1", "u1"))
    out["z1<0 by year"] = dn.groupby("yr").apply(lambda D: clt(D, "z1", "u1"))
    out["z1<0 all"] = clt(dn, "z1", "u1")
    out["z1>0 all"] = clt(A[A.z1 > 0], "z1", "u1")
    out["z14<0 by coin"] = neg.groupby("coin").apply(lambda D: clt(D, "z14", "u7"))
    return out
