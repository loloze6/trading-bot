def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            r1 = c.pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            er = (c - c.shift(30)).abs() / c.diff().abs().rolling(30).sum()
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)), "ts": b["timestamp"],
                              "r1": r1, "vol30": vol30, "er": er,
                              "clv": (c - l) / (h - l).replace(0, np.nan),
                              "rng1": (h - l) / c,
                              "rng7": ((h - l) / c).rolling(7).mean(),
                              "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1,
                              "f3": c.shift(-3) / c - 1, "f7": c.shift(-7) / c - 1,
                              "vrank_raw": vol30})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["z1"] = D["r1"] / D["vol30"]
    D["day"] = pd.to_datetime(D["ts"]).dt.floor("D")
    D["year"] = pd.to_datetime(D["ts"]).dt.year
    D["vr"] = D.groupby("coin")["vol30"].rank(pct=True)
    D["rngrel"] = D["rng7"] / D.groupby("coin")["rng7"].transform("median")
    for k in ["f1", "f2", "f3", "f7"]:
        D["u_" + k] = D[k] - D.groupby("coin")[k].transform("mean")

    def ct(df, col):
        g = df.dropna(subset=[col])
        n = len(g)
        if n < 3: return {"n": n, "days": 0, "mean%": np.nan, "t": np.nan}
        m = g[col].mean()
        dev = g.groupby("day")[col].apply(lambda x: (x - m).sum())
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / max(G - 1, 1)) / n
        return {"n": n, "days": G, "mean%": round(m * 100, 3), "t": round(m / se, 2)}

    res = {}
    E = D.dropna(subset=["z1"]).copy()
    E["z1d"] = pd.qcut(E["z1"], 10, labels=False)
    res["u_next1d_by_z1_decile_clustered"] = pd.DataFrame({k: ct(g, "u_f1") for k, g in E.groupby("z1d")}).T
    lo = E[E["z1d"] == 0]
    res["lowest_decile_by_horizon"] = pd.DataFrame({k: ct(lo, "u_" + k) for k in ["f1", "f2", "f3", "f7"]}).T
    res["lowest_decile_by_window"] = pd.DataFrame({k: ct(g, "u_f1") for k, g in lo.groupby("win")}).T
    res["lowest_decile_by_coin"] = pd.DataFrame({k: ct(g, "u_f1") for k, g in lo.groupby("coin")}).T
    res["lowest_decile_by_year"] = pd.DataFrame({k: ct(g, "u_f1") for k, g in lo.groupby("year")}).T
    neg = E[E["z1"] < 0].copy()
    neg["zq"] = pd.qcut(neg["z1"], 5, labels=False)
    res["neg_days_by_z1_quintile"] = pd.DataFrame({k: ct(g, "u_f1") for k, g in neg.groupby("zq")}).T
    lo2 = lo.copy()
    lo2["vq"] = pd.qcut(lo2["vr"], 3, labels=False)
    res["lowest_decile_by_volrank_tercile"] = pd.DataFrame({k: ct(g, "u_f1") for k, g in lo2.groupby("vq")}).T
    lo2["eq"] = pd.qcut(lo2["er"], 3, labels=False)
    res["lowest_decile_by_er_tercile"] = pd.DataFrame({k: ct(g, "u_f1") for k, g in lo2.groupby("eq")}).T
    lo2["cq"] = pd.qcut(lo2["clv"], 3, labels=False, duplicates="drop")
    res["lowest_decile_by_close_location"] = pd.DataFrame({k: ct(g, "u_f1") for k, g in lo2.groupby("cq")}).T
    r, p = stats.spearmanr(neg["z1"], neg["u_f1"], nan_policy="omit")
    res["spearman_z1_vs_next_on_down_days"] = f"rho {r:.4f} p {p:.4g} n {len(neg)}"
    # range effect on 7-day grid
    G = D[(D["pos"] % 7 == 0)].dropna(subset=["rngrel", "u_f7"]).copy()
    G["rq"] = pd.qcut(G["rngrel"], 5, labels=False)
    res["u7_by_rel_range_quintile"] = pd.DataFrame({k: ct(g, "u_f7") for k, g in G.groupby("rq")}).T
    # book: daily return by day after a big fall
    return res
