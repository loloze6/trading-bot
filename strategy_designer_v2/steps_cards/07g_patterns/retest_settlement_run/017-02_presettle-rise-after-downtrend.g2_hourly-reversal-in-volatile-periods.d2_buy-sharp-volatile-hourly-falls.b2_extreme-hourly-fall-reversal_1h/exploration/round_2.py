def explore(data):
    import numpy as np, pandas as pd
    out = {}
    grid = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            df = pd.DataFrame({"coin": coin, "w": w, "year": ts.dt.year, "hour": ts.dt.hour,
                               "vol": r.rolling(20).std(),
                               "vol24": r.rolling(24*7).std(),
                               "p24": c / c.shift(24) - 1,
                               "p12": c / c.shift(12) - 1,
                               "p48": c / c.shift(48) - 1,
                               "f24": c.shift(-24) / c - 1,
                               "f12": c.shift(-12) / c - 1,
                               "f48": c.shift(-48) / c - 1,
                               "r1n": r.shift(-1), "r2n": r.shift(-2)})
            df["pz24"] = df["p24"] / (df["vol24"] * np.sqrt(24))
            grid.append(df.iloc[::24].copy())
            # hour effect cells: in raw return terms
    G = pd.concat(grid, ignore_index=True)
    def tab(df, key, col):
        g = df.groupby(key)[col]
        return pd.DataFrame({"mean": g.mean(), "n": g.count(), "t": g.mean() / (g.std() / np.sqrt(g.count()))})
    G = G.dropna(subset=["f24", "pz24"])
    dr = G.groupby("coin")["f24"].mean(); sd = G.groupby("coin")["f24"].std()
    G["u24"] = (G["f24"] - G["coin"].map(dr)) / G["coin"].map(sd)
    G["x24"] = G["f24"] - G["coin"].map(dr)
    G["d"] = G.groupby("coin")["pz24"].transform(lambda s: pd.qcut(s, 10, labels=False))
    out["by pz24 decile: strength"] = tab(G, "d", "u24")
    out["by pz24 decile: unusual move raw"] = tab(G, "d", "x24")
    out["by pz24 decile: total move raw"] = tab(G, "d", "f24")
    # signed: strength * -sign(p24), graded by |pz24|
    G["rev"] = -np.sign(G["pz24"]) * G["u24"]
    G["aq"] = G.groupby("coin")["pz24"].transform(lambda s: pd.qcut(s.abs(), 5, labels=False))
    out["reversal strength by |pz24| quintile"] = tab(G, "aq", "rev")
    low = G[G["d"] <= 1]
    out["bottom two deciles strength by coin"] = tab(low, "coin", "u24")
    out["bottom two deciles strength by year"] = tab(low, "year", "u24")
    hi = G[G["d"] >= 8]
    out["top two deciles strength by year"] = tab(hi, "year", "u24")
    # correlation of pz24 with u24 by year
    out["spearman pz24 vs u24 by year"] = G.groupby("year").apply(lambda x: x["pz24"].corr(x["u24"], method="spearman")).to_frame("rho")
    out["spearman pz24 vs u24 by coin"] = G.groupby("coin").apply(lambda x: x["pz24"].corr(x["u24"], method="spearman")).to_frame("rho")
    # other horizons
    for h in ["f12", "f48"]:
        H = G.dropna(subset=[h]).copy()
        H["u"] = (H[h] - H["coin"].map(H.groupby("coin")[h].mean())) / H["coin"].map(H.groupby("coin")[h].std())
        out[f"{h} strength by pz24 decile"] = tab(H, "d", "u")
    # volatility interaction for bottom deciles
    G["vq"] = G.groupby("coin")["vol24"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["reversal strength by vol tercile (|pz24| top 2 quintiles)"] = tab(G[G["aq"] >= 3], "vq", "rev")
    return out
