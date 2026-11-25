def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            hi20 = c.rolling(20, min_periods=20).max(); lo20 = c.rolling(20, min_periods=20).min()
            phi = c.shift(1).rolling(20, min_periods=20).max(); plo = c.shift(1).rolling(20, min_periods=20).min()
            rp = (c - lo20) / (hi20 - lo20) * 2 - 1
            r1 = c.pct_change()
            vol20 = r1.rolling(20, min_periods=15).std()
            brk_up = (c / phi - 1) / vol20
            brk_dn = (c / plo - 1) / vol20
            r60 = c / c.shift(60) - 1
            vol30 = r1.rolling(30, min_periods=25).std()
            vrank = vol30.rolling(120, min_periods=60).rank(pct=True)
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "rp": rp,
                "brk_up": brk_up, "brk_dn": brk_dn, "r60": r60, "vrank": vrank,
                "f5": c.shift(-5) / c - 1, "f1": c.shift(-1) / c - 1, "wd": ts.dt.weekday,
                "yr": ts.dt.year, "day": ts.dt.floor("D")}))
    D = pd.concat(rows, ignore_index=True)
    drift5 = D[D.pos % 5 == 0].groupby("coin")["f5"].mean()
    drift1 = D.groupby("coin")["f1"].mean()
    D["x5"] = D["f5"] - D["coin"].map(drift5); D["x1"] = D["f1"] - D["coin"].map(drift1)

    def ctt(df, y, x=None):
        df = df.dropna(subset=[y] + ([x] if x else []))
        if len(df) < 30: return pd.Series({"n": len(df)})
        if x is None:
            e = df[y] - df[y].mean(); s = e.groupby(df["day"]).sum()
            G = len(s); se = np.sqrt((s ** 2).sum() * G / (G - 1)) / len(df)
            return pd.Series({"n": len(df), "days": G, "mean%": df[y].mean() * 100, "t_day": df[y].mean() / se})
        X = df[x] - df[x].mean(); yv = df[y]
        b = (X * yv).sum() / (X ** 2).sum(); a = yv.mean()
        e = yv - a - b * X; sc = (X * e).groupby(df["day"]).sum(); G = len(sc)
        se = np.sqrt((sc ** 2).sum() * G / (G - 1)) / (X ** 2).sum()
        return pd.Series({"n": len(df), "days": G, "slope%": b * 100, "t_day": b / se})

    G = D[D.pos % 5 == 0].dropna(subset=["x5"]).copy()
    res = {}
    res["slope x5 on rp, upper half"] = ctt(G[G.rp > 0], "x5", "rp")
    res["slope x5 on rp, lower half"] = ctt(G[G.rp <= 0], "x5", "rp")
    res["x5 at rp==1 (new 20d high)"] = ctt(G[G.rp >= 0.999], "x5")
    res["x5 at rp==-1 (new 20d low)"] = ctt(G[G.rp <= -0.999], "x5")
    up = G[G.brk_up > 0].copy()
    res["slope x5 on breakout size above prior high (vol units)"] = ctt(up, "x5", "brk_up")
    dn = G[G.brk_dn < 0].copy()
    res["slope x5 on breakdown size below prior low (vol units)"] = ctt(dn, "x5", "brk_dn")
    G["tr"] = pd.cut(G["r60"], [-99, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    G["ag"] = np.where(G["vrank"] > 0.5, "agitated", np.where(G["vrank"].notna(), "calm", None))
    G["prof"] = G["tr"].astype(str) + " " + G["ag"].astype(str)
    out = {}
    for p, g in G.groupby("prof"):
        out[p] = ctt(g, "x5", "rp")
    res["slope x5 on rp by profile"] = pd.DataFrame(out).T.round(3)
    out = {}
    for p, g in G.groupby("tr"):
        out[str(p)] = ctt(g, "x5", "rp")
    res["slope x5 on rp by trend"] = pd.DataFrame(out).T.round(3)
    # 60d trend itself as predictor
    res["slope x5 on r60"] = ctt(G, "x5", "r60")
    # weekday day-clustered, and by year consistency
    A = D.dropna(subset=["x1"])
    out = {}
    for wd, g in A.groupby("wd"):
        out[wd] = ctt(g, "x1")
    res["weekday x1 day-clustered"] = pd.DataFrame(out).T.round(3)
    A2 = A[A.wd.isin([0, 4])].copy(); A2["s"] = np.where(A2.wd == 4, 1, -1) * A2["x1"]
    res["(Fri - Mon) signed x1 by year"] = A2.groupby("yr")["s"].agg(["size", "mean"]).assign(mean=lambda d: d["mean"] * 100).round(3)
    return res
