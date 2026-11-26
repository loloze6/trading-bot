def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            p7 = c / c.shift(7) - 1
            p30 = c / c.shift(30) - 1
            er = (c - c.shift(30)).abs() / c.diff().abs().rolling(30).sum()
            sd30 = r1.rolling(30).std()
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "r1": r1, "p7": p7, "p30": p30,
                               "er": er, "sd30": sd30, "sc": p7 / (sd30 * np.sqrt(7)),
                               "f1": c.shift(-1) / c - 1, "f3": c.shift(-3) / c - 1, "f7": c.shift(-7) / c - 1,
                               "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                               "yr": pd.to_datetime(b["timestamp"]).dt.year})
            df["z1"] = df["r1"] / df["sd30"].shift(1)
            df["vrel"] = df["sd30"] / df["sd30"].rolling(180, min_periods=60).median()
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    # 1) down-day bounce, clustered by day
    def clt(g, col):
        g = g.dropna(subset=[col])
        m = g.groupby("coin")[col].transform("mean")
        g = g.assign(ex=g[col] - A.groupby("coin")[col].transform("mean").loc[g.index])
        d = g.groupby("day")["ex"].sum()
        n = len(g)
        mean = g["ex"].mean()
        se = np.sqrt((d ** 2).sum()) / n
        return pd.Series({"n": n, "days": len(d), "mean_ex": mean, "t_day": mean / se})
    A["zb"] = pd.cut(A["z1"], [-50, -3, -2, -1, 0, 1, 2, 3, 50])
    out["f1_by_z_clustered"] = A.dropna(subset=["zb"]).groupby("zb", observed=True).apply(lambda g: clt(g, "f1"))
    out["f3_by_z_clustered"] = A.dropna(subset=["zb"]).groupby("zb", observed=True).apply(lambda g: clt(g, "f3"))
    big = A[A["z1"] <= -2]
    out["bigdown_f1_by_coin"] = big.groupby("coin").apply(lambda g: clt(g, "f1"))
    out["bigdown_f1_by_year"] = big.groupby("yr").apply(lambda g: clt(g, "f1"))
    out["bigdown_f1_by_er"] = big.assign(e=pd.cut(big["er"], [0, 0.2, 0.4, 1.01])).dropna(subset=["e"]).groupby("e", observed=True).apply(lambda g: clt(g, "f1"))
    # graded slope of f1 on z1 for z1<0, day clustered approx via day-mean regression
    neg = A[(A["z1"] < 0)].dropna(subset=["f1", "z1"])
    s = stats.linregress(neg["z1"], neg["f1"])
    out["neg_z_slope"] = pd.Series({"n": len(neg), "slope": s.slope, "t": s.slope / s.stderr})
    # 2) weekday clustered
    A["wd"] = A["day"].dt.dayofweek
    out["weekday_f1_clustered"] = A.groupby("wd").apply(lambda g: clt(g, "f1"))
    # 3) continuation by own-history vol level on 7-bar grid, agree, er<0.3
    G = A[A["pos"] % 7 == 0].dropna(subset=["f7", "sc", "er", "vrel"]).copy()
    G["ex"] = G["f7"] - G.groupby("coin")["f7"].transform("mean")
    Ga = G[(np.sign(G["p7"]) == np.sign(G["p30"])) & (G["er"] < 0.3)].copy()
    Ga["vb"] = pd.qcut(Ga["vrel"], 3, labels=["low", "mid", "high"])
    def sl(g):
        s = stats.linregress(g["sc"], g["ex"]); sx = np.sign(g["sc"]) * g["ex"]
        d = (g.assign(sx=sx - sx.mean()).groupby("day")["sx"].sum())
        return pd.Series({"n": len(g), "slope": s.slope, "t_slope": s.slope / s.stderr, "signed": sx.mean(),
                          "t_day": sx.mean() / (np.sqrt((d ** 2).sum()) / len(g))})
    out["cont_by_ownvol"] = Ga.groupby("vb", observed=True).apply(sl)
    out["cont_by_ownvol_yr"] = Ga.assign(lo=Ga["vb"] == "low").groupby(["lo", "yr"]).apply(sl)
    # 4) book largest days
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; D.append(d)
    D = pd.concat(D, ignore_index=True)
    bk = D.groupby(["w", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).dropna().reset_index()
    bk["nb"] = bk.groupby("w")["cr"].shift(-1); bk["pb"] = bk.groupby("w")["cr"].shift(1)
    q = bk["br"].quantile([0.02, 0.98])
    out["book_extremes"] = pd.DataFrame({
        "worst2pct": bk[bk["br"] <= q[0.02]][["br", "cr", "pb", "nb"]].mean(),
        "best2pct": bk[bk["br"] >= q[0.98]][["br", "cr", "pb", "nb"]].mean()})
    out["book_share_of_sum_top5pct"] = float(bk.loc[bk["br"] >= bk["br"].quantile(0.95), "br"].sum() / bk["br"].sum())
    return out
