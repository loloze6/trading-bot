def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            d = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"])})
            d["r1"] = c.pct_change()
            d["f1"] = c.shift(-1) / c - 1
            d["vol20"] = d["r1"].rolling(20).std()
            d["z1"] = d["r1"] / d["vol20"].shift(1)
            rng = (h - l) / c
            d["rng30"] = rng.rolling(30).mean()
            d["rng90"] = rng.rolling(90, min_periods=60).mean()
            d["rngratio"] = d["rng30"] / d["rng90"]
            d["rngrel"] = rng / d["rng30"]
            d["clv"] = ((c - l) / (h - l)).where(h > l)
            d["above"] = c / h.shift(1).rolling(30).max() - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["f1"].mean()
    D["x1"] = D["f1"] - D["coin"].map(drift)
    D["day"] = D["ts"].dt.floor("D"); D["year"] = D["ts"].dt.year
    D["clv5"] = pd.qcut(D["clv"], 5, labels=False)

    def ct(sub, col="x1"):
        sub = sub.dropna(subset=[col])
        if len(sub) < 5: return pd.Series({"n": len(sub), "days": 0, "mean": np.nan, "t": np.nan})
        m = sub[col].mean()
        g = (sub[col] - m).groupby(sub["day"]).sum()
        D_ = len(g)
        se = np.sqrt((g**2).sum() * D_ / max(D_-1, 1)) / len(sub)
        return pd.Series({"n": len(sub), "days": D_, "mean": m, "t": m / se if se > 0 else np.nan})

    def sp(sub, a, b="x1"):
        s = sub.dropna(subset=[a, b])
        r, p = stats.spearmanr(s[a], s[b])
        return pd.Series({"n": len(s), "rho": r, "p": p})

    out = {}
    out["clv_rho_by_year"] = D.groupby("year").apply(lambda s: sp(s, "clv"))
    out["clv_rho_by_coin"] = D.groupby("coin").apply(lambda s: sp(s, "clv"))
    out["clv_rho_all"] = sp(D, "clv")
    D["rr2"] = pd.qcut(D["rngratio"], 2, labels=["calmer", "wider"])
    out["clv_q0_minus_q4_by_volhalf"] = D.groupby(["rr2", "clv5"]).apply(ct).reset_index().query("clv5 in [0,4]")
    D["wide_today"] = pd.qcut(D["rngrel"], 2, labels=["narrow_day", "wide_day"])
    out["clv_by_todayrange"] = D.groupby(["wide_today", "clv5"]).apply(ct).reset_index().query("clv5 in [0,4]")
    nh = D[D["above"] > 0]
    out["newhigh_rho_by_year"] = nh.groupby("year").apply(lambda s: sp(s, "above"))
    out["newhigh_rho_all"] = sp(nh, "above")
    return out
