def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            s = pd.Series(r1)
            sd20 = s.rolling(20, min_periods=15).std().shift(1).values
            sd60 = s.rolling(60, min_periods=40).std().shift(1).values
            zr = r1 / sd20
            r90 = np.r_[np.full(90, np.nan), c[90:] / c[:-90] - 1] if n > 90 else np.full(n, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            for t in range(n):
                f5 = c[t + 5] / c[t] - 1 if t + 5 < n else np.nan
                f1 = c[t + 1] / c[t] - 1 if t + 1 < n else np.nan
                rows.append((coin, w, t, t % 5 == 0, b["regime"].iloc[t], zr[t], r1[t], r90[t],
                             sd20[t], sd60[t], f1, f5, ts.iloc[t].dayofweek, ts.iloc[t].year))
    df = pd.DataFrame(rows, columns=["coin", "w", "t", "grid", "regime", "zr", "r1", "r90",
                                     "sd20", "sd60", "f1", "f5", "dow", "year"])
    drift5 = df[df.grid].groupby("coin")["f5"].mean()
    drift1 = df.groupby("coin")["f1"].mean()
    df["x5"] = df["f5"] - df["coin"].map(drift5)
    df["x1"] = df["f1"] - df["coin"].map(drift1)
    usual5 = df[df.grid].groupby("coin")["f5"].std()
    df["s5"] = df["x5"] / df["coin"].map(usual5)

    def summ(d, col):
        m = d[col].mean(); sd = d[col].std(); k = d[col].count()
        return pd.Series({"n": k, "mean": m, "t": m / (sd / np.sqrt(k)) if k > 1 else np.nan})

    g = df[df.grid].dropna(subset=["x5", "zr"]).copy()
    tr = g[(g.regime == "trending") & (g.zr > 1)]
    out["trending z>1: x5 by coin"] = tr.groupby("coin").apply(lambda d: summ(d, "x5")).round(4)
    out["trending z>1: x5 by year"] = tr.groupby("year").apply(lambda d: summ(d, "x5")).round(4)
    out["trending z>1: strength"] = summ(tr, "s5").round(4)
    up = g[g.zr > 0]
    for reg in ["trending", "mean_reversion"]:
        u = up[up.regime == reg]
        sl = stats.linregress(u["zr"], u["x5"])
        out[f"slope x5 on z, up days, {reg}"] = pd.Series({"n": len(u), "slope": sl.slope, "t": sl.slope / sl.stderr})
    # all up days: z x r90 sign interaction graded by r90 size
    u = up.dropna(subset=["r90"]).copy()
    u["q90"] = pd.qcut(u["r90"], 5, labels=False)
    u["bigup"] = u.zr > 1
    out["up days x5 by r90 quintile and z>1"] = u.groupby(["q90", "bigup"]).apply(lambda d: summ(d, "x5")).round(4)
    # low-vol big ups: vol ratio sd20/sd60
    g["vr"] = g["sd20"] / g["sd60"]
    gg = g.dropna(subset=["vr"])
    gg = gg[gg.zr > 1].copy()
    gg["qvr"] = pd.qcut(gg["vr"], 3, labels=False)
    out["z>1 x5 by vol-ratio tercile"] = gg.groupby("qvr").apply(lambda d: summ(d, "x5")).round(4)
    # weekday consistency
    a = df.dropna(subset=["x1"])
    a = a.assign(half=np.where(a.year <= 2021, "early", "late"))
    out["next-day x1 by weekday and half"] = a.groupby(["half", "dow"]).apply(lambda d: summ(d, "x1")).round(4)
    out["next-day x1 by weekday and coin (t)"] = a.groupby(["coin", "dow"]).apply(lambda d: summ(d, "x1")["t"]).unstack().round(2)
    # down-day next-day reversal by half
    a2 = a.dropna(subset=["zr"])
    a2 = a2.assign(zb=pd.cut(a2.zr, [-np.inf, -1, 1, np.inf], labels=["down", "mid", "up"]))
    out["x1 by z band and half"] = a2.groupby(["half", "zb"]).apply(lambda d: summ(d, "x1")).round(4)
    return out
