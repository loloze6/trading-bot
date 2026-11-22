def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(b)
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            hi = b["high"].astype(float); lo = b["low"].astype(float)
            hh = hi.rolling(30).max(); ll = lo.rolling(30).min()
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "w": w, "i": np.arange(n), "ts": ts,
                "yr": ts.dt.year, "wd": ts.dt.weekday,
                "z": r1 / vol20, "r30": c / c.shift(30) - 1, "r3": c / c.shift(3) - 1,
                "ratio": (c - c.shift(29)).abs() / (hh - ll),
                "f1": c.shift(-1) / c - 1, "f5": c.shift(-5) / c - 1, "f2": c.shift(-2) / c - 1,
                "vol20": vol20}))
    A = pd.concat(rows, ignore_index=True)
    for h, col in [(1, "f1"), (5, "f5"), (2, "f2")]:
        dr = A[A.i % h == 0].groupby("coin")[col].mean()
        A["e" + col] = A[col] - A["coin"].map(dr)
    out = {}
    def clustered(df, col):
        m = df.groupby("ts")[col].mean().dropna()
        return pd.Series({"mean": m.mean(), "n_dates": len(m), "t_dates": m.mean() / (m.std() / np.sqrt(len(m)))})
    # 1) large down day -> next day rebound
    D = A.dropna(subset=["z", "ef1"]).copy()
    D["zq"] = pd.qcut(D.z, 10, labels=False)
    lo_ = D[D.zq == 0]; hi_ = D[D.zq == 9]
    out["bottom z decile next day, date-clustered"] = clustered(lo_, "ef1").round(4)
    out["bottom z decile next day by year"] = lo_.groupby("yr")["ef1"].agg(["mean", "count"]).round(4)
    out["bottom z decile next day by coin"] = lo_.groupby("coin")["ef1"].agg(["mean", "count"]).round(4)
    # graded: slope of ef1 on min(z,0)
    Dn = D[D.z < 0]
    s = stats.linregress(Dn.z, Dn.ef1)
    out["slope ef1 on z (z<0)"] = pd.Series({"slope": s.slope, "t": s.slope / s.stderr, "n": len(Dn)}).round(5)
    Dn2 = Dn.copy(); Dn2["flat"] = Dn2.ratio <= 0.5
    out["bottom decile by flat"] = lo_.assign(flat=lo_.ratio <= 0.5).groupby("flat")["ef1"].agg(["mean", "count"]).round(4)
    # 2) large up day -> 5-day continuation
    G = A[(A.i % 5 == 0)].dropna(subset=["z", "ef5"]).copy()
    G["zq"] = pd.qcut(G.z, 5, labels=False)
    top = G[G.zq == 4]
    out["top z quintile 5d, date-clustered"] = clustered(top, "ef5").round(4)
    out["top z quintile 5d by year"] = top.groupby("yr")["ef5"].agg(["mean", "count"]).round(4)
    out["top z quintile 5d by coin"] = top.groupby("coin")["ef5"].agg(["mean", "count"]).round(4)
    Gp = G[G.z > 0]
    s = stats.linregress(Gp.z, Gp.ef5)
    out["slope ef5 on z (z>0)"] = pd.Series({"slope": s.slope, "t": s.slope / s.stderr, "n": len(Gp)}).round(5)
    # 3) r30 momentum
    G2 = G.dropna(subset=["r30"]).copy(); G2["q"] = pd.qcut(G2.r30, 5, labels=False)
    t5 = G2[G2.q == 4]
    out["top r30 quintile 5d date-clustered"] = clustered(t5, "ef5").round(4)
    out["top r30 quintile 5d by year"] = t5.groupby("yr")["ef5"].agg(["mean", "count"]).round(4)
    # 4) weekday date-clustered
    out["weekday ef1 date-clustered"] = pd.DataFrame({wd: clustered(D[D.wd == wd], "ef1") for wd in range(7)}).T.round(4)
    # 5) book around its largest days
    bk = pd.concat([d.assign(coin=c, w=w) for c, ws in data["days"].items() for w, d in ws.items()])
    bk = bk.dropna(subset=["book_return"])
    q = bk.book_return.quantile([0.01, 0.99])
    out["coin_return on book worst 1% vs best 1% days"] = pd.Series({
        "worst_book_mean": bk[bk.book_return <= q.iloc[0]].book_return.mean(),
        "worst_coin_mean": bk[bk.book_return <= q.iloc[0]].coin_return.mean(),
        "best_book_mean": bk[bk.book_return >= q.iloc[1]].book_return.mean(),
        "best_coin_mean": bk[bk.book_return >= q.iloc[1]].coin_return.mean()}).round(4)
    return out
