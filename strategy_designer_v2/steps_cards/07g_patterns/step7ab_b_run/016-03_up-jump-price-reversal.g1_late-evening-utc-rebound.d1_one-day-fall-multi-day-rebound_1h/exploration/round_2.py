def explore(data):
    import numpy as np, pandas as pd
    H = 72
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            lr = np.log(c).diff()
            vol30d = lr.rolling(720, min_periods=200).std()
            vr24 = lr.rolling(24).std() / vol30d
            vr72 = lr.rolling(72).std() / vol30d
            v = b["volume"].astype(float)
            volu = v.rolling(24).sum() / v.rolling(720, min_periods=200).mean() / 24
            r24 = c / c.shift(24) - 1
            fwd = c.shift(-H) / c - 1
            fwd24 = c.shift(-24) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            idx = np.arange(0, len(b), H)
            rows.append(pd.DataFrame({"coin": coin, "win": w,
                "vr24": vr24.iloc[idx].values, "vr72": vr72.iloc[idx].values, "volu": volu.iloc[idx].values,
                "r24": r24.iloc[idx].values, "fwd": fwd.iloc[idx].values, "fwd24": fwd24.iloc[idx].values,
                "year": ts.dt.year.iloc[idx].values}))
    g = pd.concat(rows).dropna(subset=["fwd", "r24", "vr24"])
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g["z"] = g["ex"] / g.groupby("coin")["fwd"].transform("std")
    g["ex24"] = g["fwd24"] - g.groupby("coin")["fwd24"].transform("mean")
    out = {}
    def q(x, col, n):
        return x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), n, labels=False))
    g["q24"] = q(g, "vr24", 5)
    g["d24"] = q(g, "vr24", 10)
    def summ(x, by):
        t = x.groupby(by).agg(z=("z", "mean"), ex_pct=("ex", "mean"), fwd_pct=("fwd", "mean"), ex24=("ex24", "mean"), n=("z", "count"), sd=("z", "std"))
        t["t"] = t["z"] / (t["sd"] / np.sqrt(t["n"]))
        t["ex_pct"] *= 100; t["fwd_pct"] *= 100; t["ex24"] *= 100
        return t.drop(columns="sd").round(4)
    out["vr24 decile"] = summ(g, "d24")
    g["top"] = (g["q24"] == 4).astype(int)
    out["vr24 top-vs-rest by coin"] = g.groupby("coin").apply(lambda d: pd.Series({
        "z_top": d.loc[d.top == 1, "z"].mean(), "z_rest": d.loc[d.top == 0, "z"].mean(),
        "corr_vr_z": d["vr24"].corr(d["z"]), "rankcorr": d["vr24"].rank().corr(d["z"].rank()), "n": len(d)})).round(4)
    out["vr24 top-vs-rest by year"] = g.groupby("year").apply(lambda d: pd.Series({
        "z_top": d.loc[d.top == 1, "z"].mean(), "z_rest": d.loc[d.top == 0, "z"].mean(),
        "rankcorr": d["vr24"].rank().corr(d["z"].rank()), "n": len(d)})).round(4)
    g["dir"] = np.where(g["r24"] < 0, "fall", "rise")
    out["vr24 quintile x 24h direction"] = summ(g, ["dir", "q24"])
    x = g.dropna(subset=["vr72"]).copy(); x["q72"] = q(x, "vr72", 5)
    out["vr72 quintile"] = summ(x, "q72")
    x = g.dropna(subset=["volu"]).copy(); x["qv"] = q(x, "volu", 5)
    out["volume ratio quintile"] = summ(x, "qv")
    # rank correlation pooled within coin
    g["rk"] = g.groupby("coin")["vr24"].rank(pct=True)
    X = np.column_stack([np.ones(len(g)), g["rk"] - 0.5])
    beta, *_ = np.linalg.lstsq(X, g["z"].values, rcond=None)
    res = g["z"].values - X @ beta
    se = np.sqrt(np.diag(res @ res / (len(g) - 2) * np.linalg.inv(X.T @ X)))
    out["z on vr24 rank: slope, t"] = f"{beta[1]:.4f}, {beta[1]/se[1]:.2f}, n={len(g)}"
    # window-level sign consistency
    wsum = g.groupby("win").apply(lambda d: d["vr24"].rank().corr(d["z"].rank()))
    out["windows with positive rankcorr"] = f"{(wsum>0).sum()} of {len(wsum)}"
    return out
