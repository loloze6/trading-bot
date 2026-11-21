def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    def build(H):
        rows = []
        for coin, wins in data["bars"].items():
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b["close"].astype(float)
                r1 = c.pct_change()
                df = pd.DataFrame({
                    "coin": coin, "win": w,
                    "fwd": c.shift(-H) / c - 1,
                    "r28": c / c.shift(28) - 1,
                    "r5": c / c.shift(5) - 1,
                    "r1": r1,
                    "vol20": r1.rolling(20).std(),
                    "near60": c / c.rolling(60).max(),
                    "fc": b["forecast"],
                })
                df["z28"] = df["r28"] / (df["vol20"] * np.sqrt(28))
                df["z5"] = df["r5"] / (df["vol20"] * np.sqrt(5))
                df = df.iloc[::H]
                rows.append(df)
        g = pd.concat(rows).dropna(subset=["fwd"])
        g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
        g["wn"] = g["win"].str[1:].astype(int)
        return g
    g = build(5)
    def tt(x):
        x = x.dropna()
        return pd.Series({"mean": x.mean(), "n": len(x), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    # interaction r5 within r28>0 with t, and per coin, per half of windows
    p = g[g.r28 > 0].dropna(subset=["r5"]).copy()
    p["q"] = p.groupby("coin")["r5"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["r5_in_r28pos_t"] = p.groupby("q")["ex"].apply(tt).unstack().round(4)
    p["half"] = np.where(p.wn <= 12, "early", "late")
    out["r5top_minus_bot_in_r28pos_by_coin"] = p.groupby("coin").apply(lambda s: pd.Series({
        "diff": s[s.q == 4].ex.mean() - s[s.q == 0].ex.mean(),
        "t": stats.ttest_ind(s[s.q == 4].ex, s[s.q == 0].ex, equal_var=False).statistic})).round(4)
    out["r5top_minus_bot_in_r28pos_by_half"] = p.groupby("half").apply(lambda s: pd.Series({
        "diff": s[s.q == 4].ex.mean() - s[s.q == 0].ex.mean(),
        "t": stats.ttest_ind(s[s.q == 4].ex, s[s.q == 0].ex, equal_var=False).statistic})).round(4)
    # vol-scaled z5 graded in r28pos
    out["corr_z5_ex_r28pos"] = pd.Series({"spearman": stats.spearmanr(p["r5"], p["ex"]).correlation,
                                          "n": len(p)}).round(4)
    out["corr_r5_ex_r28neg"] = pd.Series({"spearman": stats.spearmanr(g[g.r28 <= 0].dropna(subset=["r5"]).r5,
                                          g[g.r28 <= 0].dropna(subset=["r5"]).ex).correlation}).round(4)
    # r28 top fifth by vol level
    s = g.dropna(subset=["r28", "vol20"]).copy()
    s["q28"] = s.groupby("coin")["r28"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    s["vh"] = s.groupby("coin")["vol20"].transform(lambda x: x > x.median())
    out["r28q_by_volhalf"] = s.groupby(["vh", "q28"])["ex"].apply(tt).unstack().round(4)
    # horizon: r28 top fifth at 5,10,20 days
    hz = {}
    for H in [5, 10, 20]:
        gg = build(H).dropna(subset=["r28"]).copy()
        gg["q28"] = gg.groupby("coin")["r28"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
        top = gg[gg.q28 == 4].ex; rest = gg[gg.q28 < 4].ex
        hz[H] = {"top_ex": top.mean(), "rest_ex": rest.mean(), "n_top": len(top),
                 "t": stats.ttest_ind(top, rest, equal_var=False).statistic}
    out["r28top_by_horizon"] = pd.DataFrame(hz).T.round(4)
    # r1 graded within r28 pos
    s = p.dropna(subset=["r1"]).copy()
    s["q1"] = s.groupby("coin")["r1"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["r1_in_r28pos"] = s.groupby("q1")["ex"].apply(tt).unstack().round(4)
    # near60 within r28 pos
    s = p.dropna(subset=["near60"]).copy()
    s["qn"] = s.groupby("coin")["near60"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["near60_in_r28pos"] = s.groupby("qn")["ex"].apply(tt).unstack().round(4)
    # book: largest daily gains/losses
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin
            d["next5"] = d["book_return"].shift(-1).rolling(5).sum().shift(-4)
            dd.append(d)
    D = pd.concat(dd).dropna(subset=["book_return", "next5"])
    D["bq"] = pd.qcut(D["book_return"].rank(method="first"), 10, labels=False)
    out["book_next5_after_decile"] = D.groupby("bq")[["book_return", "next5"]].mean().round(4)
    return out
