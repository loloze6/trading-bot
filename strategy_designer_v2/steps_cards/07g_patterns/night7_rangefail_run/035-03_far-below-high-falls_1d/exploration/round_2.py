def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            hi = c.shift(1).rolling(20, min_periods=20).max()
            sd = r1.rolling(20, min_periods=20).std()
            dist = (c / hi - 1) / sd
            fwd5 = c.shift(-5) / c - 1
            fwd2 = c.shift(-2) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                               "dist": dist, "r1": r1, "r1z": r1 / sd.shift(1),
                               "r3": c / c.shift(3) - 1,
                               "fwd5": fwd5, "fwd2": fwd2,
                               "day": ts.dt.floor("D"), "wd": ts.dt.weekday,
                               "year": ts.dt.year})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[A["pos"] % 5 == 0].dropna(subset=["fwd5", "dist"]).copy()
    drift = G.groupby("coin")["fwd5"].mean()
    G["ex5"] = G["fwd5"] - G["coin"].map(drift)
    def ct(g, col="ex5"):
        g = g.dropna(subset=[col])
        dev = g[col] - g[col].mean()
        s = dev.groupby(g["day"]).sum()
        G_ = len(s); n = len(g)
        se = np.sqrt((s**2).sum() * G_ / (G_ - 1)) / n if G_ > 1 else np.nan
        return pd.Series({"n": n, "days": G_, "mean": g[col].mean(), "t_cl": g[col].mean() / se})
    out = {}
    G["dq"] = pd.qcut(G["dist"], 6)
    out["ex5 by dist sextile (day-clustered)"] = G.groupby("dq").apply(ct)
    out["ex5 by dist sextile x year"] = G.groupby(["year", pd.cut(G["dist"], [-99, -2, 0, 99])])["ex5"].agg(["mean", "count"]).unstack()
    # deep below high, by last-day move in swings
    deep = G[G["dist"] <= -2].copy()
    deep["r1zq"] = pd.qcut(deep["r1z"], 4)
    out["deep: ex5 by last-day move in swings quartile (cl)"] = deep.groupby("r1zq").apply(ct)
    deep["r3q"] = pd.qcut(deep["r3"], 4)
    out["deep: ex5 by 3-day return quartile (cl)"] = deep.groupby("r3q").apply(ct)
    out["deep & r1>0 by year"] = deep[deep["r1"] > 0].groupby("year")["ex5"].agg(["mean", "count"])
    # near/above high side
    top = G[G["dist"] > -1].copy()
    top["dq2"] = pd.qcut(top["dist"], 4)
    out["near/above high: ex5 by dist quartile (cl)"] = top.groupby("dq2").apply(ct)
    out["near/above high by year"] = top.groupby("year")["ex5"].agg(["mean", "count"])
    # whole range linear: correlation dist vs ex5 by year
    out["corr dist-ex5 by year"] = G.groupby("year").apply(lambda g: g["dist"].corr(g["ex5"]))
    # weekday next-day clustered
    A["fwd1"] = A.groupby(["coin", "win"])["fwd5"].transform(lambda x: x) * 0
    return out
