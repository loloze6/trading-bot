def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            er = (c - c.shift(30)).abs() / c.diff().abs().rolling(30).sum()
            r7 = c / c.shift(7) - 1
            r30 = c / c.shift(30) - 1
            vol = r1.rolling(30).std()
            vol90 = r1.rolling(90).std()
            s7 = r7 / (vol * np.sqrt(7))
            f1 = c.shift(-1) / c - 1
            f7 = c.shift(-7) / c - 1
            f3 = c.shift(-3) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)), "day": ts.dt.floor("D"),
                               "wd": ts.dt.weekday, "r1": r1, "z1": r1 / vol, "er": er, "r7": r7, "r30": r30,
                               "vol": vol, "volrel": vol / vol90, "s7": s7, "f1": f1, "f3": f3, "f7": f7,
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "regime": b["regime"], "fc": b["forecast"].astype(float)})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    # drifts per coin over all windows (non-overlapping)
    d1 = D.groupby("coin")["f1"].mean()
    d7 = D[D.pos % 7 == 0].groupby("coin")["f7"].mean()
    d3 = D[D.pos % 3 == 0].groupby("coin")["f3"].mean()
    D["x1"] = D["f1"] - D.coin.map(d1)
    D["x7"] = D["f7"] - D.coin.map(d7)
    D["x3"] = D["f3"] - D.coin.map(d3)

    def ct(sub, col):
        s = sub.dropna(subset=[col])
        g = s.groupby("day")[col].sum()
        n = len(s); nd = len(g)
        if nd < 5: return (np.nan, np.nan, n, nd)
        m = s[col].mean()
        se = g.std(ddof=1) * np.sqrt(nd) / n
        return (m, m / se, n, nd)

    def tab(sub, key, col):
        out = {}
        for k, g in sub.groupby(key, observed=True):
            m, t, n, nd = ct(g, col)
            out[str(k)] = {"mean": m, "t": t, "n": n, "days": nd}
        return pd.DataFrame(out).T

    G7 = D[(D.pos % 7 == 0)].dropna(subset=["s7", "er", "x7"]).copy()
    G7["dir_x7"] = np.sign(G7.s7) * G7.x7
    G7["s7q"] = pd.qcut(G7.s7, 5, labels=False)
    G7["erq"] = pd.qcut(G7.er, 3, labels=["lowER", "midER", "hiER"])
    G7["volq"] = G7.groupby("coin")["vol"].transform(lambda v: pd.qcut(v, 3, labels=False))
    G7["vrq"] = pd.qcut(G7.volrel, 3, labels=False)
    res = {}
    res["fwd7 excess by s7 quintile"] = tab(G7, "s7q", "x7")
    res["dir fwd7 by ER tercile"] = tab(G7, "erq", "dir_x7")
    res["dir fwd7 by vol tercile(per coin)"] = tab(G7, "volq", "dir_x7")
    res["dir fwd7 by vol30/vol90 tercile"] = tab(G7, "vrq", "dir_x7")
    G7["sgn_r30"] = np.sign(G7.r30)
    G7["dir30_x7"] = G7.sgn_r30 * G7.x7
    G7["r30q"] = pd.qcut(G7.r30 / (G7.vol * np.sqrt(30)), 5, labels=False)
    res["fwd7 excess by scaled r30 quintile"] = tab(G7, "r30q", "x7")

    G1 = D[D.pos >= 30].dropna(subset=["z1", "x1"]).copy()
    G1["zq"] = pd.qcut(G1.z1, 7, labels=False)
    res["fwd1 excess by z1 (daily move/vol) septile"] = tab(G1, "zq", "x1")
    G3 = D[(D.pos % 3 == 0) & (D.pos >= 30)].dropna(subset=["z1", "x3"]).copy()
    G3["zq"] = pd.qcut(G3.z1, 7, labels=False)
    res["fwd3 excess by z1 septile"] = tab(G3, "zq", "x3")
    res["fwd1 excess by weekday"] = tab(D.dropna(subset=["x1"]), "wd", "x1")
    # book: position-days, gain by s7 sign and regime
    D["gain"] = D.alloc * D.f1
    P = D[D.alloc.abs() > 1e-9].dropna(subset=["gain"]).copy()
    P["side"] = np.where(P.alloc > 0, "long", "short")
    res["book gain per position-bar by side"] = tab(P, "side", "gain")
    res["book gain by coin"] = tab(P, "coin", "gain")
    P["erq"] = pd.qcut(P.er, 3, labels=["lowER", "midER", "hiER"])
    res["book gain by ER tercile"] = tab(P, "erq", "gain")
    return res
