def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    def tt(x):
        x = pd.Series(x).dropna(); n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(20).std()
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)), "ts": ts,
                "r1": r1, "z1": r1 / sd, "m30": (c / c.shift(30) - 1) / sd,
                "m60": c / c.shift(60) - 1, "fwd5": c.shift(-5) / c - 1,
                "wd": ts.dt.dayofweek, "year": ts.dt.year,
                "alloc": b["postRebalance_current_allocation"], "fwd1": c.shift(-1) / c - 1}))
    A = pd.concat(rows, ignore_index=True)
    # weekday by coin (bar's own return on its weekday)
    out["Sat (wd5) bar return by coin"] = A[A["wd"] == 5].groupby("coin")["r1"].apply(tt).unstack()
    out["Sat minus other days by coin, welch t"] = A.groupby("coin").apply(lambda d: pd.Series({
        "diff": d.loc[d.wd == 5, "r1"].mean() - d.loc[d.wd != 5, "r1"].mean(),
        "t": stats.ttest_ind(d.loc[d.wd == 5, "r1"].dropna(), d.loc[d.wd != 5, "r1"].dropna(), equal_var=False).statistic}))
    out["Sat bar return by year (pooled coins)"] = A[A["wd"] == 5].groupby("year")["r1"].apply(tt).unstack()
    # cross-coin-averaged per timestamp to remove correlation
    X = A.groupby("ts").agg(r1=("r1", "mean"), wd=("wd", "first"))
    out["coin-avg return by weekday (one obs per day)"] = X.groupby("wd")["r1"].apply(tt).unstack()
    # vol-scaled: Sat return in usual moves
    A["zr"] = A["z1"]
    out["Sat z-return by coin"] = A[A["wd"] == 5].groupby("coin")["zr"].apply(tt).unstack()
    # momentum slope conditional on 60-day return sign
    G = A[A["pos"] % 5 == 0].copy()
    drift = G.groupby("coin")["fwd5"].mean()
    G["ex5"] = G["fwd5"] - G["coin"].map(drift)
    G = G.dropna(subset=["ex5", "m30", "m60"])
    def slope(df, x="m30"):
        df = df.dropna(subset=[x, "ex5"])
        if len(df) < 10: return pd.Series({"n": len(df)})
        r = stats.linregress(df[x], df["ex5"])
        return pd.Series({"n": len(df), "slope": r.slope, "t": r.slope / r.stderr})
    G["reg60"] = np.where(G["m60"] > 0, "up60", "down60")
    out["slope ex5 on m30 by 60d regime"] = G.groupby("reg60").apply(slope)
    G["m60q"] = G.groupby("coin")["m60"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["slope ex5 on m30 by 60d tercile"] = G.groupby("m60q").apply(slope)
    out["ex5 by 60d tercile"] = G.groupby("m60q")["ex5"].apply(tt).unstack()
    # book on long vs short by 60d regime
    A["g"] = A["alloc"] * A["fwd1"]
    A["reg60"] = np.where(A["m60"] > 0, "up60", np.where(A["m60"] <= 0, "down60", "na"))
    A["side"] = np.where(A["alloc"] > 1e-9, "long", np.where(A["alloc"] < -1e-9, "short", "flat"))
    out["bar gain by side x 60d regime"] = A[A.side != "flat"].groupby(["side", "reg60"])["g"].apply(tt).unstack()
    return out
