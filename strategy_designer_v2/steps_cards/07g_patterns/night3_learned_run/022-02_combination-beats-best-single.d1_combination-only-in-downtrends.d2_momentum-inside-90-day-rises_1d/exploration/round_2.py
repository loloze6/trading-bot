def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            f = pd.DataFrame({
                "coin": coin, "win": w,
                "regime": b["regime"].values,
                "fc": b["forecast"].astype(float).values,
                "pos": b["postRebalance_current_allocation"].astype(float).values,
                "ret20": (c / c.shift(20) - 1).values,
                "ret28": (c / c.shift(28) - 1).values,
                "vol20": r1.rolling(20).std().values,
                "near20": (c / c.rolling(20).max() - 1).values,
                "near28": (c / c.rolling(28).max() - 1).values,
                "fwd": (c.shift(-H) / c - 1).values,
                "fwd10": (c.shift(-10) / c - 1).values,
                "i": np.arange(len(b)),
            })
            rows.append(f)
    df = pd.concat(rows, ignore_index=True)
    g = df[df["i"] % H == 0].copy()
    drift = g.groupby("coin")["fwd"].mean()
    usual = g.groupby("coin")["fwd"].std()
    g["adj"] = g["fwd"] - g["coin"].map(drift)
    g["adjn"] = g["adj"] / g["coin"].map(usual)
    out = {}
    def z(s, col):
        return s.groupby("coin")[col].transform(lambda x: (x - x.mean()) / x.std())
    # near20 in trending, controlling fc (multiple regression)
    s = g[g["regime"] == "trending"][["coin", "win", "near20", "near28", "fc", "adjn", "adj"]].dropna().copy()
    s["zn"] = z(s, "near20"); s["zf"] = z(s, "fc")
    X = np.column_stack([np.ones(len(s)), s["zn"], s["zf"]])
    beta, *_ = np.linalg.lstsq(X, s["adjn"].values, rcond=None)
    resid = s["adjn"].values - X @ beta
    sig2 = resid @ resid / (len(s) - 3)
    se = np.sqrt(np.diag(sig2 * np.linalg.inv(X.T @ X)))
    out["trending_near20_and_fc_joint"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["const", "near20", "fc"]).assign(n=len(s))
    out["corr_near20_fc_trending"] = float(s[["zn", "zf"]].corr().iloc[0, 1])
    # near20 trending by coin and by half of windows
    res = []
    for coin, x in s.groupby("coin"):
        lr = stats.linregress(x["zn"], x["adjn"]); res.append([coin, lr.slope, lr.slope / lr.stderr, len(x)])
    s["wn"] = s["win"].str[1:].astype(int)
    for nm, x in [("w1-12", s[s["wn"] <= 12]), ("w13-24", s[s["wn"] > 12])]:
        lr = stats.linregress(x["zn"], x["adjn"]); res.append([nm, lr.slope, lr.slope / lr.stderr, len(x)])
    out["near20_trending_by_coin_half"] = pd.DataFrame(res, columns=["grp", "slope", "t", "n"])
    # unknown regime: ret20 reversal and vol, by coin and halves; 10 day too
    u = g[g["regime"] == "unknown"][["coin", "win", "ret20", "vol20", "near20", "adjn", "adj", "fwd10"]].dropna().copy()
    u["zr"] = z(u, "ret20"); u["zv"] = z(u, "vol20")
    u["wn"] = u["win"].str[1:].astype(int)
    res = []
    for feat in ["zr", "zv"]:
        for nm, x in [("all", u), ("w1-12", u[u["wn"] <= 12]), ("w13-24", u[u["wn"] > 12])]:
            lr = stats.linregress(x[feat], x["adjn"]); res.append([feat, nm, lr.slope, lr.slope / lr.stderr, len(x)])
    out["unknown_ret20_vol_halves"] = pd.DataFrame(res, columns=["feat", "grp", "slope", "t", "n"])
    res = []
    for coin, x in u.groupby("coin"):
        lr = stats.linregress(x["zv"], x["adjn"]); res.append([coin, lr.slope, lr.slope / lr.stderr, len(x)])
    out["unknown_vol_by_coin"] = pd.DataFrame(res, columns=["coin", "slope", "t", "n"])
    u["qv"] = u.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["unknown_vol_quintiles"] = u.groupby("qv")["adj"].agg(["mean", "count"])
    # shorts in trending: book gain split by forecast sign
    df["fwd1"] = df.groupby(["coin", "win"])["fwd"].transform(lambda x: x) * 0
    return out
