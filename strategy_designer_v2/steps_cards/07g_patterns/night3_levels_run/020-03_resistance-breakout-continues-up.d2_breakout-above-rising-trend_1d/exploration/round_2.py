def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    recs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            ts = pd.to_datetime(b["timestamp"])
            f = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n),
                "r1": c.pct_change(),
                "r20p": c / c.shift(20) - 1,
                "dist50": c / c.rolling(50, min_periods=50).mean() - 1,
                "vol20": c.pct_change().rolling(20).std(),
                "fwd5": c.shift(-5) / c - 1,
                "fwd1": c.shift(-1) / c - 1,
                "fwd10": c.shift(-10) / c - 1,
                "trend": (b["regime"] == "trending").astype(int),
                "fc": b["forecast"].astype(float),
                "wd": ts.dt.weekday, "yr": ts.dt.year,
            })
            f["d50v"] = f["dist50"] / (f["vol20"] * np.sqrt(50))
            f["r1v"] = f["r1"] / f["vol20"]
            recs.append(f)
    ALL = pd.concat(recs)
    res = {}
    # daily returns by weekday, every day (1-day non-overlapping), per coin
    ALL["ex1"] = ALL["fwd1"] - ALL.groupby("coin")["fwd1"].transform("mean")
    def tt(s):
        s = s.dropna()
        return pd.Series({"mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))), "n": len(s)})
    # weekday of the day whose return it is: fwd1 from bar t is the return of day t+1
    ALL["wd_next"] = (ALL["wd"] + 1) % 7
    res["daily_ret_by_weekday"] = ALL.groupby("wd_next")["ex1"].apply(tt).unstack().round(4)
    res["daily_ret_weekday_x_coin_t"] = ALL.groupby(["coin", "wd_next"])["ex1"].apply(lambda s: s.mean() / (s.std() / np.sqrt(s.count()))).unstack().round(2)
    ALL["half"] = np.where(ALL["yr"] <= 2021, "early", "late")
    res["daily_ret_weekday_x_half"] = ALL.groupby(["half", "wd_next"])["ex1"].mean().unstack().round(4)
    # grid 5
    G = ALL[ALL["pos"] % 5 == 0].dropna(subset=["fwd5"]).copy()
    G["ex5"] = G["fwd5"] - G.groupby("coin")["fwd5"].transform("mean")
    G["usual"] = G.groupby("coin")["fwd5"].transform("std")
    # trending breakouts: by vol-scaled distance terciles, and raw distance
    T = G[G["trend"] == 1].copy()
    T["q_d50"] = pd.qcut(T["dist50"].rank(method="first"), 3, labels=False)
    res["trend_by_dist50_tercile"] = T.groupby("q_d50").apply(lambda d: pd.Series({"mean": d["ex5"].mean(), "t": d["ex5"].mean()/(d["ex5"].std()/np.sqrt(len(d))), "n": len(d), "d50": d["dist50"].mean()})).round(4)
    T["q_d50v"] = pd.qcut(T["d50v"].rank(method="first"), 3, labels=False)
    res["trend_by_d50v_tercile"] = T.groupby("q_d50v")["ex5"].apply(tt).unstack().round(4)
    res["trend_corr"] = pd.Series({"spearman_dist50": stats.spearmanr(T["dist50"], T["ex5"], nan_policy="omit")[0],
                                   "spearman_d50v": stats.spearmanr(T["d50v"], T["ex5"], nan_policy="omit")[0],
                                   "spearman_r1v": stats.spearmanr(T["r1v"], T["ex5"], nan_policy="omit")[0], "n": len(T)}).round(3)
    # all bars above SMA50: dist50 tercile among positive vs ex5, and 10-day
    P = G[G["dist50"] > 0].copy()
    P["q"] = pd.qcut(P["d50v"].rank(method="first"), 5, labels=False)
    res["above50_by_d50v_q"] = P.groupby("q")["ex5"].apply(tt).unstack().round(4)
    # big up day continuation, vol-scaled, per coin and half
    G["q_r1v"] = G.groupby("coin")["r1v"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    res["r1v_q"] = G.groupby("q_r1v")["ex5"].apply(tt).unstack().round(4)
    res["r1v_top_by_coin"] = G[G["q_r1v"] == 4].groupby("coin")["ex5"].apply(tt).unstack().round(4)
    res["r1v_top_by_half"] = G[G["q_r1v"] == 4].groupby("half")["ex5"].apply(tt).unstack().round(4)
    res["r1v_spearman"] = pd.Series({"rho": stats.spearmanr(G["r1v"], G["ex5"], nan_policy="omit")[0], "n": G["r1v"].notna().sum()}).round(4)
    # trending cases by coin and half
    res["trend_by_coin"] = T.groupby("coin")["ex5"].apply(tt).unstack().round(4)
    res["trend_by_half"] = T.groupby("half")["ex5"].apply(tt).unstack().round(4)
    return res
