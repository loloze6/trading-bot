def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(b)
            r14 = c / c.shift(14) - 1
            z14 = (r14 - r14.rolling(60, min_periods=20).mean()) / r14.rolling(60, min_periods=20).std()
            hi30 = c / c.rolling(30, min_periods=10).max() - 1
            r1 = c.pct_change()
            vol20 = r1.rolling(20, min_periods=10).std()
            vrel = b["volume"].astype(float) / b["volume"].astype(float).rolling(20, min_periods=10).mean()
            f7 = c.shift(-7) / c - 1
            f1 = c.shift(-1) / c - 1
            pos = b["postRebalance_current_allocation"].astype(float)
            wd = pd.to_datetime(b["timestamp"]).dt.dayofweek
            yr = pd.to_datetime(b["timestamp"]).dt.year
            df = pd.DataFrame(dict(coin=coin, w=w, i=np.arange(n), z14=z14, r14=r14, hi30=hi30, r1=r1,
                                   vol20=vol20, vrel=vrel, f7=f7, f1=f1, pos=pos, fc=b["forecast"].astype(float),
                                   wd=wd, yr=yr))
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    m7 = D.groupby("coin")["f7"].transform(lambda s: s[D.loc[s.index, "i"] % 7 == 0].mean())
    m1 = D.groupby("coin")["f1"].transform("mean")
    D["x7"] = D["f7"] - m7
    D["x1"] = D["f1"] - m1
    G = D[(D.i % 7 == 0)].dropna(subset=["x7"])
    out = {}
    def tab(g, col, q=5):
        gg = g.dropna(subset=[col]).copy()
        gg["b"] = gg.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        t = gg.groupby("b")["x7"].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t
    out["x7 by z14 quintile (per coin)"] = tab(G, "z14")
    out["x7 by nearness to 30d high quintile"] = tab(G, "hi30")
    out["x7 by vol20 quintile"] = tab(G, "vol20")
    out["x7 by rel volume quintile"] = tab(G, "vrel")
    out["x7 by forecast sign"] = G.groupby(np.sign(G.fc))["x7"].agg(["mean", "count", "std"])
    # slopes
    sl = {}
    for col in ["z14", "hi30", "vol20", "vrel", "r1"]:
        g = G.dropna(subset=[col])
        r = stats.linregress(g[col], g["x7"])
        sl[col] = {"slope": r.slope, "t": r.slope / r.stderr, "n": len(g)}
    out["slopes x7 on feature"] = pd.DataFrame(sl).T
    # per coin z14 slope
    pc = {}
    for coin, g in G.dropna(subset=["z14"]).groupby("coin"):
        r = stats.linregress(g["z14"], g["x7"]); r2 = stats.linregress(g.dropna(subset=["hi30"])["hi30"], g.dropna(subset=["hi30"])["x7"])
        pc[coin] = {"z14_t": r.slope / r.stderr, "hi30_t": r2.slope / r2.stderr, "n": len(g)}
    out["per coin t"] = pd.DataFrame(pc).T
    # 1-day: large moves -> next day
    D1 = D.dropna(subset=["x1", "r1", "vol20"]).copy()
    D1["zr1"] = D1.r1 / D1.vol20
    D1["b"] = pd.cut(D1.zr1, [-99, -2, -1, 0, 1, 2, 99])
    t = D1.groupby("b")["x1"].agg(["mean", "count", "std"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    out["next-day x1 by today's move/vol"] = t
    t = D1.groupby("wd")["x1"].agg(["mean", "count", "std"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    out["next-day x1 by weekday of decision bar"] = t
    # book
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bk.append(d.assign(coin=coin, w=w))
    B = pd.concat(bk, ignore_index=True)
    B["yr"] = pd.to_datetime(B["day"]).dt.year
    yb = B.groupby("yr")[["book_return", "coin_return"]].mean()
    out["book & coin mean daily by year"] = yb
    out["book mean daily by coin"] = B.groupby("coin")[["book_return", "coin_return"]].agg(["mean"])
    # position-side contribution
    D["g"] = D.pos * D.f1
    out["gain by position side"] = D.dropna(subset=["g"]).groupby(np.sign(D.pos))["g"].agg(["mean", "sum", "count"])
    return out
