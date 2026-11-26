def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            hi7 = c.rolling(7).max(); lo7 = c.rolling(7).min()
            r1 = c.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "i": np.arange(len(b)), "regime": b["regime"],
                "pos7": (c - lo7) / (hi7 - lo7), "r7": c / c.shift(7) - 1,
                "r7z": (c / c.shift(7) - 1) / (r1.rolling(30, min_periods=20).std() * np.sqrt(7)),
                "tr60": c / c.shift(60) - 1,
                "fwd7": c.shift(-7) / c - 1, "fwd1": c.shift(-1) / c - 1,
                "yr": ts.dt.year, "wd": ts.dt.weekday, "day": ts.dt.floor("D")})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["inprof"] = A.regime.isin(["trending", "unknown"])
    A["trend"] = np.where(A.tr60 > 0.10, "rising", np.where(A.tr60 < -0.10, "falling", np.where(A.tr60.notna(), "choppy", "na")))
    d7 = A.loc[A.i % 7 == 0, "fwd7"].mean()
    out = {}
    res = []
    for off in range(7):
        G = A[(A.i % 7 == off) & A.fwd7.notna() & ~A.inprof].dropna(subset=["pos7"]).copy()
        G["ex"] = G.fwd7 - d7
        rr, pv = stats.spearmanr(G.pos7, G.ex)
        q = pd.qcut(G.pos7, 4, labels=False, duplicates="drop")
        lo = G.ex[q == 0]; hi = G.ex[q == q.max()]
        res.append({"off": off, "rho_pos7": rr, "p": pv, "n": len(G), "lowq": lo.mean(),
                    "hiq": hi.mean(), "welch_hi_lo": stats.ttest_ind(hi, lo, equal_var=False).statistic})
        g2 = G.dropna(subset=["r7z"])
        res[-1]["rho_r7z"] = stats.spearmanr(g2.r7z, g2.ex)[0]
    out["outprof_pos7_offsets"] = pd.DataFrame(res)
    G = A[(A.i % 7 == 0) & A.fwd7.notna()].dropna(subset=["pos7"]).copy()
    G["ex"] = G.fwd7 - d7
    G["pq"] = pd.qcut(G.pos7, 4, labels=False, duplicates="drop")
    out["pos7_by_trend"] = G.groupby(["trend", "pq"]).ex.agg(["count", "mean"])
    out["pos7_lowq_by_year"] = G[G.pq == 0].groupby("yr").ex.agg(["count", "mean"])
    Q = A[A.fwd1.notna()].copy(); Q["ex"] = Q.fwd1 - Q.fwd1.mean()
    Q["late"] = Q.wd.isin([3, 4])
    out["thufri_minus_rest_by_year"] = Q.groupby("yr").apply(lambda g: pd.Series({
        "diff": g.ex[g.late].mean() - g.ex[~g.late].mean(),
        "t": stats.ttest_ind(g.ex[g.late], g.ex[~g.late], equal_var=False).statistic}))
    out["thufri_by_trend"] = Q.groupby(["trend", "late"]).ex.agg(["count", "mean"])
    return out
