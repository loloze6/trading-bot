def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); n = len(b)
            r14 = c / c.shift(14) - 1
            z14 = (r14 - r14.rolling(60, min_periods=20).mean()) / r14.rolling(60, min_periods=20).std()
            r1 = c.pct_change()
            vol20 = r1.rolling(20, min_periods=10).std()
            r28 = c / c.shift(28) - 1
            r7 = c / c.shift(7) - 1
            df = pd.DataFrame(dict(coin=coin, w=w, i=np.arange(n), z14=z14, r14=r14, r28=r28, r7=r7, r1=r1,
                                   vol20=vol20, zr1=r1/vol20, zr14=r14/(vol20*np.sqrt(14)),
                                   yr=pd.to_datetime(b["timestamp"]).dt.year))
            for h in [1, 3, 7, 14]:
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    out = {}
    for h in [1, 3, 7, 14]:
        mh = D[D.i % h == 0].groupby("coin")[f"f{h}"].mean()
        D[f"x{h}"] = D[f"f{h}"] - D.coin.map(mh)
    def slope(g, x, y):
        g = g.dropna(subset=[x, y])
        if len(g) < 20: return (np.nan, np.nan, len(g))
        r = stats.linregress(g[x], g[y]); return (r.slope, r.slope / r.stderr, len(g))
    res = {}
    for feat in ["z14", "zr14", "r14", "r7", "r28"]:
        for h in [3, 7, 14]:
            G = D[D.i % h == 0]
            s, t, n = slope(G, feat, f"x{h}")
            res[f"{feat} h{h}"] = {"slope": s, "t": t, "n": n}
    out["slopes by feature and horizon"] = pd.DataFrame(res).T
    G7 = D[D.i % 7 == 0]
    yy = {}
    for y, g in G7.groupby("yr"):
        s, t, n = slope(g, "zr14", "x7"); s2, t2, _ = slope(g, "z14", "x7")
        yy[y] = {"zr14_t": t, "z14_t": t2, "n": n}
    out["7d momentum t by year"] = pd.DataFrame(yy).T
    # sign split
    sp = {}
    for nm, g in [("z14>0", G7[G7.z14 > 0]), ("z14<0", G7[G7.z14 < 0])]:
        s, t, n = slope(g, "z14", "x7"); sp[nm] = {"slope": s, "t": t, "n": n, "mean_x7": g.x7.mean()}
    out["z14 slope by sign"] = pd.DataFrame(sp).T
    # zr14 deciles pooled
    g = G7.dropna(subset=["zr14", "x7"]).copy()
    g["b"] = pd.qcut(g.zr14, 8, labels=False)
    t = g.groupby("b").agg(lo=("zr14", "min"), hi=("zr14", "max"), m=("x7", "mean"), n=("x7", "count"), s=("x7", "std"))
    t["t"] = t.m / (t.s / np.sqrt(t.n)); out["x7 by zr14 octile"] = t
    # next-day reversal robustness
    D1 = D.dropna(subset=["zr1", "x1"])
    pc = {}
    for coin, g in D1.groupby("coin"):
        s, t, n = slope(g, "zr1", "x1"); pc[coin] = {"t": t, "n": n}
    for y, g in D1.groupby("yr"):
        s, t, n = slope(g, "zr1", "x1"); pc[f"y{y}"] = {"t": t, "n": n}
    s, t, n = slope(D1, "zr1", "x1"); pc["all"] = {"t": t, "n": n, "slope": s}
    out["next-day x1 on zr1: t by coin/year"] = pd.DataFrame(pc).T
    # reversal within momentum: zr1 effect on x1 split by zr14 sign
    rr = {}
    for nm, g in [("zr14>0", D1[D1.zr14 > 0]), ("zr14<0", D1[D1.zr14 < 0])]:
        s, t, n = slope(g, "zr1", "x1"); rr[nm] = {"slope": s, "t": t, "n": n}
    out["next-day reversal by trend sign"] = pd.DataFrame(rr).T
    # momentum per coin zr14
    pz = {}
    for coin, g in G7.groupby("coin"):
        s, t, n = slope(g, "zr14", "x7"); pz[coin] = {"t": t, "n": n}
    out["zr14->x7 t per coin"] = pd.DataFrame(pz).T
    return out
