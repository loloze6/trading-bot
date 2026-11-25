def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            vol7 = r1.rolling(7).std()
            r7 = c / c.shift(7) - 1
            r30 = c / c.shift(30) - 1
            er = (c - c.shift(30)).abs() / c.diff().abs().rolling(30).sum()
            rng = ((b["high"] - b["low"]) / c).rolling(7).mean()
            volu = b["volume"].astype(float)
            vrel = volu.rolling(7).mean() / volu.rolling(30).mean()
            f7 = c.shift(-7) / c - 1
            f1 = c.shift(-1) / c - 1
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)), "ts": b["timestamp"],
                              "r1": r1, "r7": r7, "r30": r30, "vol30": vol30, "vol7": vol7, "er": er,
                              "rng": rng, "vrel": vrel, "f7": f7, "f1": f1,
                              "regime": b["regime"], "fc": b["forecast"],
                              "alloc": b["postRebalance_current_allocation"]})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["z7"] = D["r7"] / (D["vol30"] * np.sqrt(7))
    D["z30"] = D["r30"] / (D["vol30"] * np.sqrt(30))
    D["volratio"] = D["vol7"] / D["vol30"]
    D["day"] = pd.to_datetime(D["ts"]).dt.floor("D")
    D["wd"] = pd.to_datetime(D["ts"]).dt.weekday
    G = D[(D["pos"] % 7 == 0) & D["f7"].notna()].copy()
    drift = G.groupby("coin")["f7"].mean()
    sd = G.groupby("coin")["f7"].std()
    G["u"] = (G["f7"] - G["coin"].map(drift)) / G["coin"].map(sd)
    G["vrank"] = G.groupby("coin")["vol30"].rank(pct=True)

    def summ(df, key):
        out = {}
        for k, g in df.groupby(key, observed=True):
            g = g.dropna(subset=["u"])
            s = g.groupby("day")["u"].sum()
            n = len(g); m = g["u"].mean()
            dev = g.groupby("day")["u"].apply(lambda x: (x - m).sum())
            G_ = len(dev)
            se = np.sqrt((dev ** 2).sum() * G_ / max(G_ - 1, 1)) / n if n > 1 else np.nan
            out[k] = {"n": n, "days": G_, "mean_strength": round(m, 4), "t": round(m / se, 2) if se else np.nan}
        return pd.DataFrame(out).T

    res = {}
    res["drift_pct_by_coin"] = (drift * 100).round(2)
    G["z7q"] = pd.qcut(G["z7"], 5, labels=False)
    res["by_z7_quintile_all"] = summ(G.dropna(subset=["z7q"]), "z7q")
    G["inreg"] = (G["regime"] == "mean_reversion").astype(int)
    res["by_z7q_in_regime"] = summ(G[G.inreg == 1].dropna(subset=["z7q"]), "z7q")
    res["by_z7q_out_regime"] = summ(G[G.inreg == 0].dropna(subset=["z7q"]), "z7q")
    G["z30q"] = pd.qcut(G["z30"], 5, labels=False)
    res["by_z30_quintile"] = summ(G.dropna(subset=["z30q"]), "z30q")
    G["erq"] = pd.qcut(G["er"], 5, labels=False)
    res["by_er_quintile"] = summ(G.dropna(subset=["erq"]), "erq")
    G["vq"] = pd.qcut(G["vrank"], 5, labels=False)
    res["by_vol_rank_quintile"] = summ(G.dropna(subset=["vq"]), "vq")
    G["vrq"] = pd.qcut(G["volratio"], 5, labels=False)
    res["by_vol7_over_vol30_q"] = summ(G.dropna(subset=["vrq"]), "vrq")
    G["vlq"] = pd.qcut(G["vrel"], 5, labels=False)
    res["by_volume7_over30_q"] = summ(G.dropna(subset=["vlq"]), "vlq")
    res["by_weekday_of_grid"] = summ(G, "wd")
    sp = {}
    for col in ["z7", "z30", "er", "vrank", "volratio", "vrel", "rng"]:
        g = G.dropna(subset=[col, "u"])
        r, p = stats.spearmanr(g[col], g["u"])
        sp[col] = {"rho": round(r, 4), "p": round(p, 4), "n": len(g)}
    res["spearman_with_strength"] = pd.DataFrame(sp).T
    # daily: next-day by weekday and by large 1d move
    D2 = D.dropna(subset=["f1", "r1", "vol30"]).copy()
    D2["z1"] = D2["r1"] / D2["vol30"]
    D2["z1q"] = pd.qcut(D2["z1"], 10, labels=False)
    res["next1d_by_z1_decile_pct"] = D2.groupby("z1q")["f1"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))]).round(5)
    res["next1d_by_weekday_pct"] = D2.groupby("wd")["f1"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))]).round(5)
    return res
