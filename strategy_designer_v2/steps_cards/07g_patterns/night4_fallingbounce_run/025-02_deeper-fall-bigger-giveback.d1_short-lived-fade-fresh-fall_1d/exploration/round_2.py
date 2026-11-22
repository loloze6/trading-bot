def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            vol20 = r1.rolling(20, min_periods=15).std()
            ts = pd.to_datetime(df["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "win": w, "wn": int(w[1:]), "pos": np.arange(len(df)),
                "vs": r1 / vol20, "ret30": c / c.shift(30) - 1, "ret90": c / c.shift(90) - 1,
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1, "f5": c.shift(-5) / c - 1,
                "wd": ts.dt.weekday.values, "year": ts.dt.year.values}))
    A = pd.concat(rows, ignore_index=True)
    for h in (1, 2, 5):
        g = A[A["pos"] % h == 0]
        dr = g.groupby("coin")["f%d" % h].mean()
        A["u%d" % h] = A["f%d" % h] - A["coin"].map(dr)
    def summ(g, col):
        x = g[col].dropna(); n = len(x)
        if n < 3: return pd.Series({"n": n, "mean%": np.nan, "t": np.nan})
        return pd.Series({"n": n, "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(n))})
    out = {}
    G2 = A[A.pos % 2 == 0].copy(); G5 = A[A.pos % 5 == 0].copy(); G1 = A.copy()
    G2["half"] = np.where(G2.wn <= 12, "w1-12", "w13-24"); G5["half"] = np.where(G5.wn <= 12, "w1-12", "w13-24")
    bins = [0.3, 1, 1.5, 2, 3, np.inf]
    # big rise in rising month: continuation, graded
    up2 = G2[(G2.ret30 >= 0) & (G2.vs > 0.3)].copy(); up2["b"] = pd.cut(up2.vs, bins)
    out["r30pos rise size -> u2"] = up2.groupby("b").apply(lambda g: summ(g, "u2"))
    up5 = G5[(G5.ret30 >= 0) & (G5.vs > 0.3)].copy(); up5["b"] = pd.cut(up5.vs, bins)
    out["r30pos rise size -> u5"] = up5.groupby("b").apply(lambda g: summ(g, "u5"))
    big = G2[(G2.ret30 >= 0) & (G2.vs > 2)]
    out["r30pos vs>2 u2 by coin"] = big.groupby("coin").apply(lambda g: summ(g, "u2"))
    out["r30pos vs>2 u2 by half"] = big.groupby("half").apply(lambda g: summ(g, "u2"))
    out["corr vs,u2 r30pos vs>0.3 (n, spearman)"] = pd.Series({"n": len(up2.dropna(subset=["u2"])),
        "rho": up2[["vs", "u2"]].corr(method="spearman").iloc[0, 1]})
    # falling month rises
    dn2 = G2[(G2.ret30 < 0) & (G2.vs > 0.3)].copy(); dn2["b"] = pd.cut(dn2.vs, bins)
    out["r30neg rise size -> u2"] = dn2.groupby("b").apply(lambda g: summ(g, "u2"))
    sm = G2[(G2.ret30 < 0) & (G2.vs > 0.3) & (G2.vs <= 1)]
    out["r30neg small rise u2 by coin"] = sm.groupby("coin").apply(lambda g: summ(g, "u2"))
    out["r30neg small rise u2 by half"] = sm.groupby("half").apply(lambda g: summ(g, "u2"))
    # weekday
    G1["half"] = np.where(G1.wn <= 12, "w1-12", "w13-24")
    G1["thfr"] = G1.wd.isin([3, 4]).map({True: "Thu-Fri", False: "other"})
    out["Thu-Fri vs other u1 by coin"] = G1.groupby(["coin", "thfr"]).apply(lambda g: summ(g, "u1")).unstack()
    out["weekday u1 by half"] = G1.groupby(["half", "wd"]).apply(lambda g: summ(g, "u1")).unstack(0)
    return out
