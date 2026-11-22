def explore(data):
    import numpy as np, pandas as pd
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
            d = {"coin": coin, "w": w, "z": z, "fall": fall, "ret90": ret90,
                 "yr": ts.dt.year, "wd": ts.dt.weekday, "dkey": ts.dt.floor("D").astype("int64"),
                 "pos": np.arange(len(b))}
            for h in (1, 3, 5, 10):
                d["f%d" % h] = c.shift(-h) / c - 1
            rows.append(pd.DataFrame(d))
    A = pd.concat(rows, ignore_index=True)
    out = {}
    def summ(x):
        x = x.dropna(); n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    res = {}
    for h in (1, 3, 5, 10):
        G = A[(A.pos % h == 0) & A["f%d" % h].notna()].copy()
        dr = G.groupby("coin")["f%d" % h].mean()
        G["u"] = G["f%d" % h] - G.coin.map(dr)
        G["zb"] = pd.cut(G.z, [-np.inf, 0, 1, 1.5, 2, 3, np.inf])
        s = G.groupby(["fall", "zb"]).u.apply(summ).unstack()
        res[h] = s
    for h in (1, 3, 5, 10):
        out["u%d by fall x z (fine)" % h] = res[h].round(4)
    # 5-day, big rise (z>1) split by fall, by year and coin
    G = A[(A.pos % 5 == 0) & A.f5.notna()].copy()
    dr = G.groupby("coin").f5.mean()
    G["u"] = G.f5 - G.coin.map(dr)
    B = G[G.z > 1.5]
    out["z>1.5: u5 by fall x year"] = B.groupby(["fall", "yr"]).u.apply(summ).unstack().round(4)
    out["z>1.5 rising: u5 by coin"] = B[~B.fall.astype(bool)].groupby("coin").u.apply(summ).unstack().round(4)
    # date-clustered: average per day key the u of z>1.5 cases, then t over days
    for fl in (False, True):
        C = B[B.fall == fl].groupby("dkey").u.mean()
        out["z>1.5 fall=%s day-clustered" % fl] = summ(C).round(4)
    # graded inside rising: corr z (z>0) vs u, and by ret90 strength
    R = G[(~G.fall.astype(bool)) & (G.z > 0)]
    out["rising, z>0: corr z,u5 and n"] = pd.Series({"corr": R[["z", "u"]].corr().iloc[0, 1], "n": len(R)}).round(4)
    F = G[(G.fall.astype(bool)) & (G.z > 0)]
    out["falling, z>0: corr z,u5 and n"] = pd.Series({"corr": F[["z", "u"]].corr().iloc[0, 1], "n": len(F)}).round(4)
    # ret90 extremes rebound by year
    G["r90b"] = pd.cut(G.ret90, [-np.inf, -0.5, -0.1, 0.1, 0.6, np.inf])
    out["u5 by ret90 bucket x year"] = G.groupby(["r90b", "yr"]).u.mean().unstack().round(4)
    # weekday day-clustered
    A1 = A[A.f1.notna()].copy()
    A1["u1"] = A1.f1 - A1.coin.map(A1.groupby("coin").f1.mean())
    D = A1.groupby(["wd", "dkey"]).u1.mean().reset_index()
    out["u1 by weekday, day-clustered"] = D.groupby("wd").u1.apply(summ).unstack().round(5)
    return out
