def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            r = c.pct_change()
            rng = (h - l) / c.shift(1)
            w20 = rng / rng.rolling(20, min_periods=10).mean()
            sd20 = r.rolling(20, min_periods=10).std()
            ret5 = c / c.shift(5) - 1
            df = pd.DataFrame({"coin": coin, "win": w, "ts": b["timestamp"], "r": r,
                               "nxt": c.shift(-1) / c - 1, "nxt3": c.shift(-3) / c - 1,
                               "w20": w20, "ret5": ret5, "z5": ret5 / (sd20 * np.sqrt(5)),
                               "z": r / sd20, "regime": b["regime"]})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["day"] = pd.to_datetime(d["ts"]).dt.floor("D")
    d["drift"] = d["coin"].map(d.groupby("coin")["r"].mean())
    d["u1"] = d["nxt"] - d["drift"]
    d["u3"] = d["nxt3"] - 3 * d["drift"]
    d["t1"] = d["nxt"]
    d["falling"] = d["regime"].isin(["trending", "unknown"])
    d = d.dropna(subset=["r", "z5"])

    def ct(s, days):
        x = pd.DataFrame({"v": s - s.mean(), "d": days}).dropna()
        g = x.groupby("d")["v"].sum(); G = len(g)
        if G < 3: return np.nan
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(x)
        return s.mean() / se

    def summ(sub, col="u1"):
        sub = sub.dropna(subset=[col])
        return pd.Series({"n": len(sub), "days": sub["day"].nunique(), "mean%": 100 * sub[col].mean(),
                          "t_day": ct(sub[col], sub["day"])})

    out = {}
    f = d[d["falling"]].copy()
    f["q5"] = pd.qcut(f["z5"].rank(method="first"), 5, labels=False)
    out["falling_by_z5Q_u1"] = f.groupby("q5").apply(summ)
    out["falling_by_z5Q_u3"] = f.groupby("q5").apply(lambda s: summ(s, "u3"))
    out["falling_by_z5Q_total1"] = f.groupby("q5").apply(lambda s: summ(s, "t1"))
    nf = d[~d["falling"]].copy()
    nf["q5"] = pd.qcut(nf["z5"].rank(method="first"), 5, labels=False)
    out["notfalling_by_z5Q_u1"] = nf.groupby("q5").apply(summ)
    top = f[f["q5"] == 4]
    out["falling_topz5_by_window"] = top.groupby("win").apply(summ)
    out["falling_topz5_by_up"] = top.groupby(top["r"] > 0).apply(summ)
    g = f.dropna(subset=["u1"])
    out["falling_corr_z5_u1"] = pd.Series({"spearman": g["z5"].corr(g["u1"], method="spearman"),
                                          "n": len(g)})
    return out
