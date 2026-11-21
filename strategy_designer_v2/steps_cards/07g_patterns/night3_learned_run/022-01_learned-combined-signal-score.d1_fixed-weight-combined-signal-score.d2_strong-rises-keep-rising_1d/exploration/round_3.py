def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({"coin": coin, "win": w,
                "fwd": c.shift(-5) / c - 1,
                "r28": c / c.shift(28) - 1,
                "vol20": r1.rolling(20).std(),
                "vol60": r1.rolling(60).std()})
            df["z28"] = df["r28"] / (df["vol20"] * np.sqrt(28))
            df["calm"] = df["vol60"] / df["vol20"]
            rows.append(df.iloc[::5])
    g = pd.concat(rows).dropna(subset=["fwd", "r28", "vol20"])
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g["wn"] = g["win"].str[1:].astype(int)
    g["half"] = np.where(g.wn <= 12, "early", "late")
    def tt(x):
        x = x.dropna()
        return pd.Series({"mean": x.mean(), "n": len(x), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    g["q28"] = g.groupby("coin")["r28"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    g["vh"] = g.groupby("coin")["vol20"].transform(lambda x: x > x.median())
    top = g[g.q28 == 4]
    out["top28_calm_minus_volatile"] = pd.Series({
        "diff": top[~top.vh].ex.mean() - top[top.vh].ex.mean(),
        "welch_t": stats.ttest_ind(top[~top.vh].ex, top[top.vh].ex, equal_var=False).statistic,
        "n_calm": (~top.vh).sum(), "n_vol": top.vh.sum()}).round(4)
    out["top28_calm_by_half"] = top[~top.vh].groupby("half")["ex"].apply(tt).unstack().round(4)
    out["top28_calm_by_coin"] = top[~top.vh].groupby("coin")["ex"].apply(tt).unstack().round(4)
    out["top28_vol_by_coin"] = top[top.vh].groupby("coin")["ex"].apply(tt).unstack().round(4)
    # vol-scaled rise graded
    g["qz"] = g.groupby("coin")["z28"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["z28_quintiles"] = g.groupby("qz")["ex"].apply(tt).unstack().round(4)
    out["z28_by_half_top_minus_rest"] = g.groupby("half").apply(lambda s: pd.Series({
        "diff": s[s.qz == 4].ex.mean() - s[s.qz < 4].ex.mean(),
        "t": stats.ttest_ind(s[s.qz == 4].ex, s[s.qz < 4].ex, equal_var=False).statistic})).round(4)
    pz = g[g.z28 > 0]
    out["spearman_z28_vs_r28_pos"] = pd.Series({
        "z28": stats.spearmanr(pz.z28, pz.ex).correlation,
        "r28": stats.spearmanr(pz.r28, pz.ex).correlation, "n": len(pz)}).round(4)
    # weekday per coin
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["wn"] = int(w[1:]); dd.append(d)
    D = pd.concat(dd).dropna(subset=["coin_return"])
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    D["ex"] = D["coin_return"] - D.groupby("coin")["coin_return"].transform("mean")
    out["sat_by_coin"] = D[D.wd == 5].groupby("coin")["ex"].apply(tt).unstack().round(4)
    out["weekday_t_btc"] = D[D.coin == "BTCUSD"].groupby("wd")["ex"].apply(tt).unstack().round(4)
    return out
