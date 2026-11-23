def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; h = b["high"]; l = b["low"]
            r1 = c / c.shift(1) - 1
            rng = (h - l) / c
            rr = rng / rng.rolling(30, min_periods=15).mean()
            vol = r1.rolling(30, min_periods=15).std()
            vol90 = r1.rolling(90, min_periods=45).std()
            fr3 = c.shift(-3) / c - 1
            fr1 = c.shift(-1) / c - 1
            mom30 = c / c.shift(30) - 1
            hi30 = c / h.rolling(30, min_periods=15).max() - 1
            clv = (c - l) / (h - l).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "r1": r1, "rr": rr,
                              "z1": r1 / vol.shift(1), "volrel": vol / vol90, "fr3": fr3, "fr1": fr1,
                              "mom30": mom30, "hi30": hi30, "clv": clv, "fc": b["forecast"],
                              "alloc": b["postRebalance_current_allocation"],
                              "wd": ts.dt.weekday, "yr": ts.dt.year})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    G = A[A["pos"] % 3 == 0].dropna(subset=["fr3"]).copy()
    G["ex"] = G["fr3"] - G.groupby("coin")["fr3"].transform("mean")
    out = {}
    def slope(df, x):
        df = df.dropna(subset=[x, "ex"])
        if len(df) < 30: return (np.nan, np.nan, len(df))
        s = stats.linregress(df[x], df["ex"])
        return (s.slope, s.slope / s.stderr, len(df))
    res = {}
    up = G[G.r1 > 0]; dn = G[G.r1 < 0]
    for name, df, x in [("rr_up", up, "rr"), ("rr_dn", dn, "rr"), ("rr_all", G, "rr"),
                        ("z1_all", G, "z1"), ("z1_up", up, "z1"), ("z1_dn", dn, "z1"),
                        ("volrel_all", G, "volrel"), ("mom30_all", G, "mom30"),
                        ("hi30_all", G, "hi30"), ("clv_all", G, "clv"), ("clv_dn", dn, "clv"),
                        ("clv_up", up, "clv"), ("fc_all", G, "fc")]:
        s, t, n = slope(df, x); res[name] = {"slope": s, "t": t, "n": n}
    out["slopes"] = pd.DataFrame(res).T
    # quintiles of z1 overall
    G["z1q"] = pd.qcut(G["z1"], 5, labels=False)
    out["z1_quint"] = G.groupby("z1q")["ex"].agg(["mean", "count", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    G["clvq"] = pd.qcut(G["clv"], 5, labels=False)
    out["clv_quint"] = G.groupby("clvq")["ex"].agg(["mean", "count", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    G["vq"] = pd.qcut(G["volrel"], 5, labels=False)
    out["volrel_quint"] = G.groupby("vq")["ex"].agg(["mean", "count", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    out["weekday"] = G.groupby("wd")["ex"].agg(["mean", "count", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    # range ratio quintiles by sign
    G["rrq"] = pd.qcut(G["rr"], 5, labels=False)
    G["sgn"] = np.sign(G["r1"])
    out["rr_by_sign"] = G.groupby(["sgn", "rrq"])["ex"].agg(["mean", "count", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    # book
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; D.append(d)
    D = pd.concat(D, ignore_index=True)
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    bk = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    bk["yr"] = pd.to_datetime(bk["day"]).dt.year
    out["book_by_year"] = bk.groupby("yr")[["book_return", "coin_return"]].agg(["mean", "count"])
    out["book_by_coin"] = D.groupby("coin")[["book_return", "coin_return"]].mean()
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T, ignore_index=True)
    out["trades_side"] = T.groupby("side")[["profit_loss_percent", "net_profit_loss_percent", "duration_minutes"]].agg(["mean", "count"])
    return out
