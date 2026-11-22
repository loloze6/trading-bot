def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    rows = []
    for coin, wins in bars.items():
        # drift per horizon on non-overlapping grid across all windows
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            vol20 = r1.rolling(20, min_periods=15).std()
            vs = r1 / vol20
            ret30 = c / c.shift(30) - 1
            ret90 = c / c.shift(90) - 1
            ret7 = c / c.shift(7) - 1
            f1 = c.shift(-1) / c - 1
            f2 = c.shift(-2) / c - 1
            f5 = c.shift(-5) / c - 1
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(df)),
                              "vs": vs, "r1": r1, "vol20": vol20, "ret30": ret30, "ret90": ret90, "ret7": ret7,
                              "f1": f1, "f2": f2, "f5": f5, "regime": df["regime"].values,
                              "fc": df["forecast"].astype(float).values,
                              "alloc": df["postRebalance_current_allocation"].astype(float).values,
                              "wd": pd.to_datetime(df["timestamp"]).dt.weekday.values,
                              "year": pd.to_datetime(df["timestamp"]).dt.year.values})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    # drifts per coin on grids
    for h in (1, 2, 5):
        g = A[A["pos"] % h == 0]
        dr = g.groupby("coin")["f%d" % h].mean()
        A["u%d" % h] = A["f%d" % h] - A["coin"].map(dr)
    def summ(g, col):
        x = g[col].dropna()
        n = len(x)
        if n < 3: return pd.Series({"n": n, "mean%": np.nan, "t": np.nan})
        return pd.Series({"n": n, "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(n))})
    G2 = A[A["pos"] % 2 == 0].copy()
    G1 = A.copy()
    G5 = A[A["pos"] % 5 == 0].copy()
    bins = [-np.inf, -2, -1, -0.3, 0.3, 1, 2, np.inf]
    G2["vsb"] = pd.cut(G2["vs"], bins)
    G2["mr"] = G2["regime"].eq("mean_reversion").map({True: "dblfall", False: "other"})
    G2["r30s"] = np.where(G2["ret30"] < 0, "r30neg", np.where(G2["ret30"] >= 0, "r30pos", "na"))
    out["u2 by vs bucket x regime"] = G2.groupby(["mr", "vsb"]).apply(lambda g: summ(g, "u2"))
    out["u2 by vs bucket x ret30 sign"] = G2[G2.r30s != "na"].groupby(["r30s", "vsb"]).apply(lambda g: summ(g, "u2"))
    G5["vsb"] = pd.cut(G5["vs"], bins)
    G5["r30s"] = np.where(G5["ret30"] < 0, "r30neg", np.where(G5["ret30"] >= 0, "r30pos", "na"))
    out["u5 by vs bucket x ret30 sign"] = G5[G5.r30s != "na"].groupby(["r30s", "vsb"]).apply(lambda g: summ(g, "u5"))
    # momentum: 30-day return quintile -> 5-day unusual, per coin ranks
    G5["q30"] = G5.groupby("coin")["ret30"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["u5 by ret30 quintile"] = G5.groupby("q30").apply(lambda g: summ(g, "u5"))
    G5["q7"] = G5.groupby("coin")["ret7"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["u5 by ret7 quintile"] = G5.groupby("q7").apply(lambda g: summ(g, "u5"))
    G1["qv"] = G1.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["u1 by vol tercile"] = G1.groupby("qv").apply(lambda g: summ(g, "u1"))
    out["u1 by weekday"] = G1.groupby("wd").apply(lambda g: summ(g, "u1"))
    out["u1 by year"] = G1.groupby("year").apply(lambda g: summ(g, "u1"))
    # forecast active bars: per coin unusual 2-day short direction
    act = G2[G2["fc"] < 0]
    out["active short bars u2 by coin (rise=bad)"] = act.groupby("coin").apply(lambda g: summ(g, "u2"))
    out["active by year"] = act.groupby("year").apply(lambda g: summ(g, "u2"))
    # book days
    D = []
    for coin, wins in days.items():
        for w, df in wins.items():
            D.append(df.assign(coin=coin, win=w))
    D = pd.concat(D)
    D["day"] = pd.to_datetime(D["day"])
    bk = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book daily mean%, sd%"] = pd.Series({"book_mean%": 100 * bk.book_return.mean(), "book_sd%": 100 * bk.book_return.std(),
                                              "n": len(bk), "share days nonzero": (bk.book_return.abs() > 1e-9).mean()})
    top = bk.book_return.abs().sort_values(ascending=False)
    k = max(1, int(0.05 * len(bk)))
    tops = bk.loc[top.index[:k]]
    out["top5% abs book days: sum share of total"] = pd.Series({"sum_top%": 100 * tops.book_return.sum(), "sum_all%": 100 * bk.book_return.sum(),
                                                                "mean_coin_ret_on_those%": 100 * tops.coin_return.mean(),
                                                                "corr_book_coin_all": bk.book_return.corr(bk.coin_return)})
    return out
