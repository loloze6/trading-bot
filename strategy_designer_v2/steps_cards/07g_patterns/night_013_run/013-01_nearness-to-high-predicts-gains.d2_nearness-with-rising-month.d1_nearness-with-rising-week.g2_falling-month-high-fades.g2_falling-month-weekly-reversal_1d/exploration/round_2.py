def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []; drows = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); h = df["high"].astype(float); v = df["volume"].astype(float)
            r1 = c.pct_change()
            ts = pd.to_datetime(df["timestamp"])
            feat = pd.DataFrame({
                "ret7": c / c.shift(7) - 1, "ret30": c / c.shift(30) - 1,
                "near30": c / h.rolling(30).max() - 1, "vol20": r1.rolling(20).std(),
                "volu": v.rolling(7).mean() / v.rolling(60, min_periods=30).mean(),
            })
            idx = np.arange(0, len(df), 7)
            g = feat.iloc[idx].copy(); g["fwd7"] = (c.shift(-7) / c - 1).iloc[idx].values
            g["coin"] = coin; g["w"] = w; g["year"] = ts.iloc[idx].dt.year.values
            g["wn"] = int(w[1:])
            rows.append(g)
            d = pd.DataFrame({"ret1": r1, "fwd1": c.shift(-1) / c - 1, "vol20": feat["vol20"],
                              "wd": ts.dt.weekday, "coin": coin, "year": ts.dt.year, "wn": int(w[1:])})
            drows.append(d)
    G = pd.concat(rows).dropna(subset=["fwd7"])
    G["fwd7x"] = G["fwd7"] - G.groupby("coin")["fwd7"].transform("mean")
    D = pd.concat(drows).dropna(subset=["fwd1"])
    D["fwd1x"] = D["fwd1"] - D.groupby("coin")["fwd1"].transform("mean")
    D["z"] = D["ret1"] / D["vol20"]
    def sl(s, x, y):
        s = s.dropna(subset=[x, y])
        if len(s) < 20: return pd.Series({"slope": np.nan, "t": np.nan, "n": len(s)})
        r = stats.linregress(s[x], s[y]); return pd.Series({"slope": r.slope, "t": r.slope / r.stderr, "n": len(s)})
    out = {}
    up = G[G.ret30 >= 0]
    out["rising month ret7 by coin"] = up.groupby("coin").apply(lambda s: sl(s, "ret7", "fwd7x"))
    out["rising month ret7 by half"] = up.groupby(up.wn > 12).apply(lambda s: sl(s, "ret7", "fwd7x"))
    out["rising month ret7 by year"] = up.groupby("year").apply(lambda s: sl(s, "ret7", "fwd7x"))
    out["volu by coin"] = G.groupby("coin").apply(lambda s: sl(s, "volu", "fwd7x"))
    out["volu by half"] = G.groupby(G.wn > 12).apply(lambda s: sl(s, "volu", "fwd7x"))
    G["vq"] = G.groupby("coin")["volu"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["volu quintile"] = G.groupby("vq")["fwd7x"].agg(["mean", "count", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    # daily z reversal (continuous) by coin and half
    out["z->fwd1x by coin"] = D.groupby("coin").apply(lambda s: sl(s, "z", "fwd1x"))
    out["z->fwd1x by half"] = D.groupby(D.wn > 12).apply(lambda s: sl(s, "z", "fwd1x"))
    # weekday by half
    D["half"] = np.where(D.wn > 12, "h2", "h1")
    out["weekday by half t"] = D.groupby(["wd", "half"])["fwd1x"].apply(lambda s: s.mean()/s.std()*np.sqrt(len(s))).unstack()
    # low-vol near30
    lo = G[G.vol20 <= G.vol20.median()]
    out["lowvol near30 by half"] = lo.groupby(lo.wn > 12).apply(lambda s: sl(s, "near30", "fwd7x"))
    out["lowvol near30 by coin"] = lo.groupby("coin").apply(lambda s: sl(s, "near30", "fwd7x"))
    return out
