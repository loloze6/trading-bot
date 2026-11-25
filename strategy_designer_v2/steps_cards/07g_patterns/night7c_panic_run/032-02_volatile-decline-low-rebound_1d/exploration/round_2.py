def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "fwd": c.shift(-H) / c - 1,
                "r30": c / c.shift(30) - 1,
                "r10": c / c.shift(10) - 1,
                "bhi": c / hi.shift(1).rolling(30).max() - 1,
                "bhi10": c / hi.shift(1).rolling(10).max() - 1,
                "bhi60": c / hi.shift(1).rolling(60).max() - 1,
                "vol": c.pct_change().rolling(20).std(),
            })
            df["pos30"] = (c - lo.rolling(30).min()) / (hi.rolling(30).max() - lo.rolling(30).min())
            df = df.iloc[::H]
            rows.append(df)
    d = pd.concat(rows).dropna(subset=["fwd"])
    drift = d.groupby("coin")["fwd"].mean()
    d["ex"] = d["fwd"] - d["coin"].map(drift)

    def ct(x):
        # day-clustered t of mean of ex
        m = x["ex"].mean()
        s = (x["ex"] - m).groupby(x["ts"]).sum()
        G = len(s)
        if G < 3: return pd.Series({"mean": m, "n": len(x), "days": G, "t_cl": np.nan})
        se = np.sqrt((s ** 2).sum() * G / (G - 1)) / len(x)
        return pd.Series({"mean": m, "n": len(x), "days": G, "t_cl": m / se})

    def qtab(col, q=5):
        x = d.dropna(subset=[col]).copy()
        x["b"] = x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        return x.groupby("b").apply(ct).round(4), x

    out = {}
    for col in ["bhi", "bhi10", "bhi60", "pos30", "r30", "r10"]:
        g, x = qtab(col)
        out["clustered ex5 by quintile " + col] = g
    # graded slope: ex on within-coin rank of bhi, day-clustered
    def cslope(col):
        x = d.dropna(subset=[col]).copy()
        x["z"] = x.groupby("coin")[col].transform(lambda s: (s.rank() / len(s)) - 0.5)
        X = x["z"].values; y = x["ex"].values
        Xc = X - X.mean(); beta = (Xc * (y - y.mean())).sum() / (Xc ** 2).sum()
        e = (y - y.mean()) - beta * Xc
        sc = pd.Series(Xc * e).groupby(x["ts"].values).sum()
        G = len(sc)
        se = np.sqrt((sc ** 2).sum() * G / (G - 1)) / (Xc ** 2).sum()
        return beta, beta / se, G
    out["clustered slope ex5 on rank"] = pd.DataFrame({c: cslope(c) for c in ["bhi", "bhi10", "bhi60", "pos30", "r30", "r10"]}, index=["beta", "t_cl", "days"]).round(4)
    # per window: top vs bottom-half of bhi
    x = d.dropna(subset=["bhi"]).copy()
    x["z"] = x.groupby("coin")["bhi"].transform(lambda s: s.rank(pct=True))
    x["top"] = x["z"] > 0.8
    pw = x.groupby(["win", "top"])["ex"].mean().unstack()
    pw["diff"] = pw[True] - pw[False]
    out["per window: ex5 top20% bhi vs rest"] = pw.round(4)
    pc = x.groupby(["coin", "top"])["ex"].mean().unstack(); pc["diff"] = pc[True] - pc[False]
    out["per coin: ex5 top20% bhi vs rest"] = pc.round(4)
    # bhi within high vs low vol
    x["hv"] = x.groupby("coin")["vol"].transform(lambda s: s > s.median())
    out["top20 bhi by vol half"] = x.groupby(["hv", "top"]).apply(ct).round(4)
    return out
