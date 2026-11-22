def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd20 = r1.rolling(20, min_periods=15).std()
            z = r1 / sd20
            ret90 = c / c.shift(90) - 1
            fall = np.where(ret90.notna(), ret90 < 0, b["regime"].eq("mean_reversion"))
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "w": w, "z": z, "fall": fall, "ret90": ret90,
                "yr": ts.dt.year, "dkey": ts.dt.floor("D").astype("int64"),
                "pos": np.arange(len(b)), "f5": c.shift(-5) / c - 1}))
    A = pd.concat(rows, ignore_index=True)
    G = A[(A.pos % 5 == 0) & A.f5.notna()].copy()
    G["u"] = G.f5 - G.coin.map(G.groupby("coin").f5.mean())
    G["s"] = G.u / G.coin.map(G.groupby("coin").f5.std())
    out = {}
    def rob(x):
        x = x.dropna(); n = len(x)
        lo, hi = x.quantile(0.025), x.quantile(0.975)
        xw = x.clip(lo, hi)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(n)),
                          "median": x.median(), "share>0": (x > 0).mean(),
                          "wins_mean": xw.mean(), "wins_t": xw.mean()/(xw.std()/np.sqrt(n))})
    R = G[~G.fall.astype(bool)].copy()
    R["zb"] = pd.cut(R.z, [-np.inf, 0, 1, 1.5, 2, np.inf])
    out["rising: u5 robust by z"] = R.groupby("zb").u.apply(rob).unstack().round(4)
    out["rising: strength s by z"] = R.groupby("zb").s.apply(rob).unstack().round(4)
    Rp = R[R.z > 0]
    out["rising z>0 spearman z,u"] = pd.Series({"rho": stats.spearmanr(Rp.z, Rp.u).correlation, "n": len(Rp)}).round(4)
    # leave one year out: corr z,u in rising z>0
    loy = {}
    for y in sorted(Rp.yr.unique()):
        X = Rp[Rp.yr != y]
        loy[y] = stats.spearmanr(X.z, X.u).correlation
    out["rising z>0 spearman leave-one-year-out"] = pd.Series(loy).round(4)
    out["rising z>0 spearman by year"] = Rp.groupby("yr").apply(lambda g: pd.Series({"rho": stats.spearmanr(g.z, g.u).correlation, "n": len(g)})).round(4)
    # coin consistency: z>1.5 rising, share of coins positive median
    B = R[R.z > 1.5]
    cm = B.groupby("coin").u.median()
    out["rising z>1.5: coins with positive median"] = pd.Series({"coins": len(cm), "positive": (cm > 0).sum()})
    # deep-fall rebound robustness
    D = G[G.ret90 < -0.5]
    out["ret90<-0.5: u5 robust"] = rob(D.u).round(4)
    out["ret90<-0.5 day-clustered"] = rob(D.groupby("dkey").u.mean()).round(4)
    out["ret90<-0.5 by coin n"] = D.groupby("coin").u.agg(["count", "mean"]).round(4)
    # graded inside rising: ret90 strength among z>1
    Rz = R[R.z > 1].copy()
    Rz["r90b"] = pd.cut(Rz.ret90, [0, 0.2, 0.5, 1.0, np.inf])
    out["rising z>1: u5 by ret90"] = Rz.groupby("r90b").u.apply(rob).unstack().round(4)
    return out
