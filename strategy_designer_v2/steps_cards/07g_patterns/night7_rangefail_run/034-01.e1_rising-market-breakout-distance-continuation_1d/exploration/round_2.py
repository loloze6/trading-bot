def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(20).std()
            hi = c.shift(1).rolling(20).max()
            dist = (c - hi) / hi / vol
            tr60 = (c / c.shift(60) - 1) * 100
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(df)),
                              "day": pd.to_datetime(df["timestamp"]).dt.floor("D"),
                              "dist": dist, "tr60": tr60, "vol": vol})
            for h in (3, 5, 10):
                d[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    for h in (3, 5, 10):
        g = A[A.pos % h == 0]
        A[f"x{h}"] = A[f"f{h}"] - A.coin.map(g.groupby("coin")[f"f{h}"].mean())
        A[f"s{h}"] = A[f"x{h}"] / (A.vol * np.sqrt(h))
    A["prof"] = pd.cut(A.tr60, [-1e9, -10, 10, 1e9], labels=["falling", "choppy", "rising"])
    A["nonrise"] = A.prof.isin(["falling", "choppy"])
    def pooled(df, col):
        s = df[[col, "day"]].dropna()
        if len(s) < 5: return pd.Series({"n": len(s)})
        dd = s.groupby("day")[col].apply(lambda v: (v - s[col].mean()).sum())
        nd = len(dd); se = np.sqrt((dd ** 2).sum()) / len(s)
        return pd.Series({"n": len(s), "days": nd, "mean%": 100 * s[col].mean(),
                          "median%": 100 * s[col].median(), "t_pooled": s[col].mean() / se,
                          "strength": df[col.replace("x", "s")].mean()})
    out = {}
    res = {}
    for h in (3, 5, 10):
        g = A[(A.pos % h == 0) & (A.prof == "rising") & (A.dist > 0)]
        res[f"h{h} all"] = pooled(g, f"x{h}")
        res[f"h{h} noDOGE"] = pooled(g[g.coin != "DOGEUSD"], f"x{h}")
        g2 = A[(A.pos % h == 0) & (A.prof == "rising") & (A.dist <= 0)]
        res[f"h{h} below"] = pooled(g2, f"x{h}")
    out["rising above-high by horizon, pooled"] = pd.DataFrame(res).T
    # slope of x on dist (above high only), by horizon
    sl = {}
    for h in (3, 5, 10):
        g = A[(A.pos % h == 0) & (A.prof == "rising") & (A.dist > 0)].dropna(subset=[f"s{h}", "dist"])
        r = stats.spearmanr(g.dist, g[f"s{h}"])
        sl[f"h{h}"] = {"n": len(g), "spearman": r.correlation, "p": r.pvalue}
    out["rising above-high: rank corr dist vs scaled x"] = pd.DataFrame(sl).T
    # non-rising, below high gradient
    G = A[(A.pos % 3 == 0)].copy()
    G["db"] = pd.cut(G.dist, [-1e9, -6, -4, -2, -0.5, 0, 1e9])
    out["nonrising x3 by dist, pooled"] = G[G.nonrise].groupby("db", observed=True).apply(lambda d: pooled(d, "x3"))
    G5 = A[(A.pos % 5 == 0)].copy(); G5["db"] = pd.cut(G5.dist, [-1e9, -6, -4, -2, -0.5, 0, 1e9])
    out["nonrising x5 by dist, pooled"] = G5[G5.nonrise].groupby("db", observed=True).apply(lambda d: pooled(d, "x5"))
    nr = G[G.nonrise & (G.dist < 0)].dropna(subset=["dist", "s3"])
    r = stats.spearmanr(nr.dist, nr.s3)
    out["nonrising below-high spearman dist vs s3"] = f"n {len(nr)} rho {r.correlation:.3f} p {r.pvalue:.4f}"
    deep = G[G.nonrise & (G.dist <= -4)]
    out["nonrising deep(<=-4) x3 by window"] = deep.groupby("win").x3.agg(["size", "mean"])
    out["nonrising deep(<=-4) x3 by coin"] = deep.groupby("coin").x3.agg(["size", "mean"])
    # falling vs choppy split of deep
    out["deep by profile, pooled"] = deep.groupby("prof", observed=True).apply(lambda d: pooled(d, "x3"))
    # book: concentration of gains
    D = pd.concat([d.assign(coin=c, win=w) for c, ws in days.items() for w, d in ws.items()], ignore_index=True)
    bk = D.groupby(["win", "day"]).book_return.mean().dropna()
    srt = bk.sort_values(ascending=False)
    out["book: share of total gain from top 1%/5% days"] = pd.Series({
        "sum": bk.sum(), "top1%": srt.head(max(1, len(srt)//100)).sum() / bk.sum(),
        "top5%": srt.head(len(srt)//20).sum() / bk.sum(), "ndays": len(bk)})
    out["book mean daily by window"] = bk.groupby(level=0).agg(["size", "mean"])
    return out
