def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            r1 = c.pct_change()
            ret7 = c / c.shift(7) - 1
            er = (c - c.shift(30)).abs() / c.diff().abs().rolling(30).sum()
            vol = r1.rolling(30).std()
            volpct = vol.rolling(100, min_periods=40).apply(lambda x: (x[:-1] < x[-1]).mean(), raw=True)
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(c)), "day": ts.dt.floor("D"),
                              "er": er, "vol": vol, "volpct": volpct,
                              "fwd7": c.shift(-7) / c - 1, "fwd1": c.shift(-1) / c - 1, "fwd3": c.shift(-3) / c - 1,
                              "z7": ret7 / (vol * np.sqrt(7)), "z1": r1 / vol, "r1": r1, "ret7": ret7})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    def clust_t(df, col):
        s = df.groupby("day")[col].sum(); n = df.groupby("day")[col].size()
        m = df[col].mean(); N = len(df); G = len(s)
        dev = df.groupby("day")[col].apply(lambda x: (x - m).sum())
        se = np.sqrt((dev**2).sum() * G / (G - 1)) / N
        return m, m / se, N, G
    # grid, signed by z7 sign (momentum direction)
    for off in [0, 3]:
        G_ = A[(A["pos"] % 7) == off].dropna(subset=["fwd7", "z7", "er"]).copy()
        drift = G_.groupby("coin")["fwd7"].mean()
        G_["u7"] = G_["fwd7"] - G_["coin"].map(drift)
        G_["mom"] = np.sign(G_["z7"]) * G_["u7"]
        G_["momw"] = G_["z7"] * G_["u7"]
        res = []
        for reg, g in [("chop", G_[G_.er < 0.3]), ("trend", G_[G_.er >= 0.3]),
                       ("chop_calm", G_[(G_.er < 0.3) & (G_.volpct < 0.5)]),
                       ("chop_agit", G_[(G_.er < 0.3) & (G_.volpct >= 0.5)])]:
            m, t, N, Gd = clust_t(g, "mom")
            m2, t2, _, _ = clust_t(g, "momw")
            res.append({"reg": reg, "n": N, "days": Gd, "sign_mom_u7": m, "t_cl": t, "z7xu7": m2, "t_cl_w": t2})
        out[f"weekly momentum in chop, grid offset {off}"] = pd.DataFrame(res)
        if off == 0:
            ch = G_[G_.er < 0.3]
            out["chop momentum by window"] = ch.groupby("w")["mom"].agg(["count", "mean"])
            out["chop momentum by coin"] = ch.groupby("coin")["mom"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
            ch2 = ch.copy(); ch2["erq"] = pd.qcut(ch2["er"], 3, labels=False)
            out["chop momentum by er tercile"] = ch2.groupby("erq").agg(n=("mom", "size"), mean=("mom", "mean"), er=("er", "mean"))
    # next-day reversal after big down day, daily non-overlap h=1, cluster by day
    D = A.dropna(subset=["fwd1", "z1"]).copy()
    D["u1"] = D["fwd1"] - D["coin"].map(D.groupby("coin")["fwd1"].mean())
    D["rev"] = -D["z1"] * D["u1"]
    res = []
    for name, g in [("all", D), ("z1<-1.5", D[D.z1 < -1.5]), ("z1>1.5", D[D.z1 > 1.5]),
                    ("z1<-1.5 chop", D[(D.z1 < -1.5) & (D.er < 0.3)]), ("z1<-1.5 trend", D[(D.z1 < -1.5) & (D.er >= 0.3)])]:
        m, t, N, Gd = clust_t(g, "u1")
        res.append({"set": name, "n": N, "days": Gd, "mean_u1": m, "t_cl": t, "mean_z1": g["z1"].mean()})
    out["next-day u after big days (clustered)"] = pd.DataFrame(res)
    dn = D[D.z1 < -1.5]
    out["after big down day by window"] = dn.groupby("w")["u1"].agg(["count", "mean"])
    out["after big down day by coin"] = dn.groupby("coin")["u1"].agg(["count", "mean"])
    # 3-day follow on 3-day grid after big down day
    D3 = A[(A["pos"] % 3) == 0].dropna(subset=["fwd3", "z1"]).copy()
    D3["u3"] = D3["fwd3"] - D3["coin"].map(D3.groupby("coin")["fwd3"].mean())
    D3["zb"] = pd.cut(D3["z1"], [-99, -2, -1, 1, 2, 99])
    out["3-day u by today's z (grid 3)"] = D3.groupby("zb")["u3"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    return out
