def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            r1 = c.pct_change()
            vol20 = r1.rolling(20, min_periods=15).std().shift(1)
            z1 = r1 / vol20
            r20 = c / c.shift(20) - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "r1": r1, "z1": z1, "r20": r20,
                               "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1, "f3": c.shift(-3) / c - 1,
                               "yr": ts.dt.year, "wd": ts.dt.weekday,
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    for k in ["f1", "f2", "f3"]:
        A["ex" + k] = A[k] - A.coin.map(A.groupby("coin")[k].mean())
    res = {}
    def summ(df, key, col):
        g = df.groupby(key)[col]
        return pd.DataFrame({"n": g.count(), "mean%": g.mean() * 100,
                             "t": g.mean() / (g.std() / np.sqrt(g.count()))}).round(3)
    A["qz"] = A.groupby("coin")["z1"].transform(lambda s: pd.qcut(s.rank(method="first"), 20, labels=False))
    res["next-day ex by z1 ventile"] = summ(A.dropna(subset=["exf1", "qz"]), "qz", "exf1")
    # grid samples for 2 and 3 day horizons
    for k, H in [("exf2", 2), ("exf3", 3)]:
        G = A[(A.pos % H == 0)].dropna(subset=[k, "qz"])
        res[k + " by z1 ventile (grid)"] = summ(G[G.qz <= 3], "qz", k)
    low = A[(A.qz <= 1)].dropna(subset=["exf1"])
    res["next-day ex after bottom-10% z1 by coin"] = summ(low, "coin", "exf1")
    res["next-day ex after bottom-10% z1 by year"] = summ(low, "yr", "exf1")
    res["next-day ex after bottom-10% z1 by up20"] = summ(low.assign(reg=np.where(low.r20 > 0, "up", "down")), "reg", "exf1")
    lw = low.groupby("w")["exf1"].mean()
    res["bottom-10% z1: share of windows positive"] = f"{(lw>0).mean():.3f} of {len(lw)} windows"
    # within bottom-10% grading: regress exf1 on z1
    s = low.dropna(subset=["z1"])
    sl = stats.linregress(s.z1, s.exf1)
    res["bottom-10% z1: slope of exf1 on z1"] = f"slope {sl.slope:.5f}, t {sl.slope/sl.stderr:.2f}, n {len(s)}"
    # all bars spearman z1 vs exf1
    s = A.dropna(subset=["z1", "exf1"])
    rho, p = stats.spearmanr(s.z1, s.exf1)
    res["spearman z1 vs next-day ex"] = f"rho {rho:.4f} p {p:.4g} n {len(s)}"
    # weekday by year (coin return)
    A["ex1"] = A["exf1"]
    Wk = A.dropna(subset=["ex1"]).copy(); Wk["wd_next"] = (Wk.wd + 1) % 7
    t = Wk.groupby(["yr", "wd_next"])["ex1"].mean().unstack() * 100
    res["next-day ex% by year x weekday of the day earned"] = t.round(3)
    # book held during reversal days
    res["mean allocation after bottom-10% z1 vs others"] = pd.Series({"bottom": A[A.qz <= 1].alloc.mean(), "others": A[A.qz > 1].alloc.mean()}).round(3)
    return res
