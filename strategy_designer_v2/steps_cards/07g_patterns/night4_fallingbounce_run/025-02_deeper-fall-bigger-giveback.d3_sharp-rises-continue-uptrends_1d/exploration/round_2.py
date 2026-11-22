def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            d = df.copy()
            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            c = d["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(20, min_periods=15).std()
            n = len(d)
            rows.append(pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n), "yr": ts.dt.year.values,
                "z": (r1 / vol).values,
                "r5": (c / c.shift(5) - 1).values,
                "r90": (c / c.shift(90) - 1).values,
                "dd20": (c / c.rolling(20, min_periods=10).max() - 1).values,
                "dd60": (c / c.rolling(60, min_periods=30).max() - 1).values,
                "f1": (c.shift(-1) / c - 1).values,
                "f5": (c.shift(-5) / c - 1).values,
                "f10": (c.shift(-10) / c - 1).values,
                "trend": (d["regime"] == "trending").astype(int).values,
            }))
    A = pd.concat(rows, ignore_index=True)
    for h in (1, 5, 10):
        dr = A[A.pos % h == 0].groupby("coin")[f"f{h}"].mean()
        A[f"u{h}"] = A[f"f{h}"] - A.coin.map(dr)
    res = {}
    def reg(df, y, x):
        df = df.dropna(subset=[y, x])
        if len(df) < 20: return pd.Series({"n": len(df), "slope": np.nan, "t": np.nan})
        r = stats.linregress(df[x], df[y])
        return pd.Series({"n": len(df), "slope": r.slope, "t": r.slope / r.stderr})
    G1 = A.dropna(subset=["u1", "z"])
    # one-day reversal: u1 on z
    res["u1 on z, all"] = reg(G1, "u1", "z").round(5)
    res["u1 on z by trend"] = G1.groupby("trend").apply(lambda g: reg(g, "u1", "z")).round(5)
    res["u1 on z by coin"] = G1.groupby("coin").apply(lambda g: reg(g, "u1", "z")).round(5)
    res["u1 on z by year"] = G1.groupby("yr").apply(lambda g: reg(g, "u1", "z")).round(5)
    G5 = A[A.pos % 5 == 0]
    res["u5 on z by trend"] = G5.groupby("trend").apply(lambda g: reg(g, "u5", "z")).round(5)
    # nearness to 20d / 60d high -> u10
    G10 = A[A.pos % 10 == 0]
    res["u10 on dd20, all"] = reg(G10, "u10", "dd20").round(5)
    res["u10 on dd20 by coin"] = G10.groupby("coin").apply(lambda g: reg(g, "u10", "dd20")).round(5)
    res["u10 on dd20 by year"] = G10.groupby("yr").apply(lambda g: reg(g, "u10", "dd20")).round(5)
    res["u10 on dd20 by trend"] = G10.groupby("trend").apply(lambda g: reg(g, "u10", "dd20")).round(5)
    res["u10 on dd60 by trend"] = G10.groupby("trend").apply(lambda g: reg(g, "u10", "dd60")).round(5)
    res["u10 on r5 by trend"] = G10.groupby("trend").apply(lambda g: reg(g, "u10", "r5")).round(5)
    # at-high share: dd20==0
    G = G10.dropna(subset=["dd20", "u10"]).copy()
    G["athigh"] = (G.dd20 >= -1e-12).astype(int)
    t = G.groupby("athigh")["u10"].agg(["count", "mean", "std"])
    t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    res["u10 at 20d high (close = max)"] = t.round(4)
    return res
