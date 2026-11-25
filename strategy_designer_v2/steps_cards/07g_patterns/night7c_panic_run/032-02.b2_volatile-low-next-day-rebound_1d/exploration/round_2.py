def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]
            d = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"])})
            d["pos"] = np.arange(len(b))
            d["r1"] = c.pct_change()
            d["f1"] = c.shift(-1) / c - 1
            d["f3"] = c.shift(-3) / c - 1
            d["vol20"] = d["r1"].rolling(20).std()
            d["z1"] = d["r1"] / d["vol20"].shift(1)
            r3 = c / c.shift(3) - 1
            d["z3"] = r3 / (d["vol20"].shift(3) * np.sqrt(3))
            rng = (h - l) / c
            d["rng30"] = rng.rolling(30).mean()
            d["rng90"] = rng.rolling(90, min_periods=60).mean()
            d["rngratio"] = d["rng30"] / d["rng90"]
            d["clv"] = ((c - l) / (h - l)).where(h > l)
            d["lowwick"] = (np.minimum(o, c) - l) / c
            d["ret30"] = c / c.shift(30) - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift1 = D.groupby("coin")["f1"].mean()
    D["x1"] = D["f1"] - D["coin"].map(drift1)
    g3 = D[D["pos"] % 3 == 0]
    drift3 = g3.groupby("coin")["f3"].mean()
    D["x3"] = D["f3"] - D["coin"].map(drift3)
    D["day"] = D["ts"].dt.floor("D"); D["year"] = D["ts"].dt.year

    def ct(sub, col="x1"):
        sub = sub.dropna(subset=[col])
        if len(sub) < 5: return pd.Series({"n": len(sub), "days": 0, "mean": np.nan, "t": np.nan})
        m = sub[col].mean()
        g = (sub[col] - m).groupby(sub["day"]).sum()
        D_ = len(g)
        se = np.sqrt((g**2).sum() * D_ / max(D_-1, 1)) / len(sub)
        return pd.Series({"n": len(sub), "days": D_, "mean": m, "t": m / se if se > 0 else np.nan})

    out = {}
    dn = D[D["z1"] < 0].copy()
    dn["zb"] = pd.cut(dn["z1"], [-np.inf, -3, -2, -1.5, -1, -0.5, 0])
    out["down_day_z_bins_next1"] = dn.groupby("zb").apply(ct)
    out["down_day_z_bins_next3_grid"] = dn[dn["pos"] % 3 == 0].groupby("zb").apply(lambda s: ct(s, "x3"))
    big = D[D["z1"] < -1.5].copy()
    out["bigdown_by_year"] = big.groupby("year").apply(ct)
    out["bigdown_by_coin"] = big.groupby("coin").apply(ct)
    out["bigdown_by_rngratio_half"] = big.groupby(pd.qcut(big["rngratio"], 2, labels=["calmer", "wider"])).apply(ct)
    out["bigdown_by_ret30_sign"] = big.groupby(big["ret30"] < 0).apply(ct)
    out["bigdown_by_clv_half"] = big.groupby(pd.qcut(big["clv"], 2, labels=["closed_low", "closed_high"])).apply(ct)
    sp = D.dropna(subset=["z1", "x1"])
    sp2 = dn.dropna(subset=["z1", "x1"])
    out["spearman"] = pd.Series({"all_z1_x1": stats.spearmanr(sp["z1"], sp["x1"])[0],
                                 "down_z1_x1": stats.spearmanr(sp2["z1"], sp2["x1"])[0],
                                 "n_down": len(sp2)})
    dn3 = D[D["z3"] < 0].copy()
    out["z3_bins_next1"] = dn3.groupby(pd.cut(dn3["z3"], [-np.inf, -2.5, -1.5, -0.75, 0])).apply(ct)
    out["clv_quintile_next1"] = D.groupby(pd.qcut(D["clv"], 5, labels=False)).apply(ct)
    return out
