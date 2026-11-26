def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            r14 = c / c.shift(14) - 1
            s14 = r14 / (sd30 * np.sqrt(14))
            r7 = c / c.shift(7) - 1
            s7 = r7 / (sd30 * np.sqrt(7))
            r1s = r1 / sd30
            r60 = c / c.shift(60) - 1
            f5 = c.shift(-5) / c - 1
            f3 = c.shift(-3) / c - 1
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "agit": (b["regime"] == "chop").astype(int),
                               "s14": s14, "s7": s7, "r1s": r1s, "r60": r60,
                               "f5": f5, "f3": f3, "fc": b["forecast"]})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A["pos"] % 5 == 0) & A["f5"].notna()].copy()
    G["ex5"] = G["f5"] - G.groupby("coin")["f5"].transform("mean")
    G["trend"] = np.where(G.r60 > 0.10, "rising", np.where(G.r60 < -0.10, "falling", "choppy"))
    C = G[G.agit == 0].dropna(subset=["s14", "ex5"])
    out = {}
    def ols(d, x, y="ex5"):
        d = d.dropna(subset=[x, y])
        if len(d) < 20: return [len(d), np.nan, np.nan]
        r = stats.linregress(d[x], d[y])
        return [len(d), r.slope, r.slope / r.stderr]
    res = {}
    for nm, d in [("calm all", C), ("calm s14<0", C[C.s14 < 0]), ("calm s14>0", C[C.s14 > 0]),
                  ("agit all", G[G.agit == 1]), ("calm fc<0", C[C.fc < 0])]:
        res[nm + " s14"] = ols(d, "s14")
        res[nm + " s7"] = ols(d, "s7")
        res[nm + " r1s"] = ols(d, "r1s")
    out["slopes n/slope/t"] = pd.DataFrame(res, index=["n", "slope", "t"]).T.round(4)
    # by trend in calm
    tr = {}
    for t_, d in C.groupby("trend"):
        tr[t_] = ols(d, "s14") + [d[d.s14 < -0.8].ex5.mean(), (d.s14 < -0.8).sum(), d[d.s14 > 0.8].ex5.mean(), (d.s14 > 0.8).sum()]
    out["calm by trend: n,slope,t,ex low,n low,ex high,n high"] = pd.DataFrame(tr, index=["n","slope","t","exlo","nlo","exhi","nhi"]).T.round(4)
    # by window slope sign
    wt = {w: ols(d, "s14") for w, d in C.groupby("w")}
    out["calm s14 slope by window"] = pd.DataFrame(wt, index=["n","slope","t"]).T.round(4)
    out["calm s14 slope by coin"] = pd.DataFrame({k: ols(d, "s14") for k, d in C.groupby("coin")}, index=["n","slope","t"]).T.round(4)
    # day-clustered t for calm all slope: residual approach -> use quintile spread by day
    C2 = C.copy(); C2["day"] = C2["pos"].astype(str) + C2["w"]
    # extremes in direction: sign(s14)*ex5 weighted by |s14|
    C2["dirmove"] = np.sign(C2.s14) * C2.ex5
    dm = C2.groupby(["w", "pos"])["dirmove"].mean()
    out["calm directional excess, per-day pooled"] = pd.Series({"n days": len(dm), "mean": dm.mean(), "t": dm.mean()/(dm.std()/np.sqrt(len(dm)))}).round(4)
    # raw 5-day total (with drift) for calm long side
    out["calm total f5 by s14 quintile"] = C.assign(b=pd.qcut(C.s14, 5, labels=False)).groupby("b")["f5"].agg(["count","mean"]).round(4)
    return out
