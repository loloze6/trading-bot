def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); v = df["volume"].astype(float)
            r1 = c.pct_change()
            ts = pd.to_datetime(df["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(df)), "ts": ts,
                              "r1": r1, "vr": v / v.rolling(20).mean(),
                              "ret30": c / c.shift(30) - 1, "ret7": c / c.shift(7) - 1,
                              "rng": (df["high"] - df["low"]) / c,
                              "rngr": ((df["high"] - df["low"]) / c) / ((df["high"] - df["low"]) / c).rolling(20).mean(),
                              "fwd3": c.shift(-3) / c - 1, "fwd1": c.shift(-1) / c - 1,
                              "fwd7": c.shift(-7) / c - 1,
                              "alloc": df["postRebalance_current_allocation"],
                              "wd": ts.dt.weekday, "yr": ts.dt.year})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    def demean(h, col):
        m = A[A.pos % h == 0].groupby("coin")[col].mean()
        return A[col] - A["coin"].map(m)
    A["fwd3d"] = demean(3, "fwd3"); A["fwd7d"] = demean(7, "fwd7")
    G3 = A[A.pos % 3 == 0].dropna(subset=["fwd3d"]); G7 = A[A.pos % 7 == 0].dropna(subset=["fwd7d"])
    def slope(df, key, y="fwd3d"):
        d = df.dropna(subset=[key, y])
        if len(d) < 30: return pd.Series({"slope": np.nan, "t": np.nan, "n": len(d)})
        r = stats.linregress(d[key], d[y]); return pd.Series({"slope": r.slope, "t": r.slope / r.stderr, "n": len(d)})
    out = {}
    # weekday: cross-coin daily mean per date, then t by weekday
    X = A.dropna(subset=["fwd1"]).copy(); X["dt"] = X.ts.dt.normalize()
    dm = X.groupby(["dt"]).agg(f=("fwd1", "mean"), wd=("wd", "first"), yr=("yr", "first"))
    g = dm.groupby("wd")["f"].agg(["mean", "count", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["wd_datemean"] = g.drop(columns="std")
    dm["early"] = dm.yr <= 2021
    out["wd_by_half_mean"] = dm.groupby(["wd", "early"])["f"].mean().unstack()
    out["wd_ThuFri_minus_rest_by_coin"] = X.groupby("coin").apply(lambda d: pd.Series({
        "diff": d[d.wd.isin([3, 4])].fwd1.mean() - d[~d.wd.isin([3, 4])].fwd1.mean(),
        "t": stats.ttest_ind(d[d.wd.isin([3, 4])].fwd1, d[~d.wd.isin([3, 4])].fwd1, equal_var=False).statistic}))
    # momentum / range slopes by coin
    out["ret30_by_coin"] = G3.groupby("coin").apply(lambda d: slope(d, "ret30"))
    out["ret7_by_coin"] = G3.groupby("coin").apply(lambda d: slope(d, "ret7"))
    out["rngr_by_coin"] = G3.groupby("coin").apply(lambda d: slope(d, "rngr"))
    out["slopes_7d"] = pd.DataFrame({"ret30": slope(G7, "ret30", "fwd7d"), "ret7": slope(G7, "ret7", "fwd7d"),
                                     "rngr": slope(G7, "rngr", "fwd7d"), "vr_up": slope(G7[G7.ret30 > 0], "vr", "fwd7d"),
                                     "rngr_all3": slope(G3, "rngr")}).T
    # ret7 split by years
    out["ret7_by_half"] = G3.assign(e=G3.yr <= 2021).groupby("e").apply(lambda d: slope(d, "ret7"))
    # book largest gain/loss days: what preceded
    D = pd.concat([df.assign(coin=c, w=w) for c, ws in days.items() for w, df in ws.items()]).dropna(subset=["book_return"])
    q = D.book_return.quantile([0.02, 0.98])
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    out["book_extremes_weekday"] = pd.DataFrame({"top": D[D.book_return >= q[0.98]].wd.value_counts().sort_index(),
                                                 "bottom": D[D.book_return <= q[0.02]].wd.value_counts().sort_index()})
    bw = D.groupby("wd")["book_return"].agg(["mean", "count", "std"]); bw["t"] = bw["mean"] / (bw["std"] / np.sqrt(bw["count"]))
    out["book_by_weekday"] = bw.drop(columns="std")
    return out
