def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            b["coin"] = coin; b["win"] = w; b["pos"] = np.arange(len(b))
            b["r1"] = c.pct_change()
            b["r3"] = c.pct_change(3)
            b["r7"] = c.pct_change(7)
            b["r14"] = c.pct_change(14)
            b["rng"] = (b["high"] - b["low"]) / c
            b["mrng"] = b["rng"].rolling(30, min_periods=20).mean()
            b["s7"] = b["r7"] / b["mrng"]
            b["s1"] = b["r1"] / b["mrng"]
            b["clv"] = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            b["vol30"] = b["r1"].rolling(30, min_periods=20).std()
            b["vol7"] = b["r1"].rolling(7, min_periods=5).std()
            b["vratio"] = b["vol7"] / b["vol30"]
            b["volu"] = b["volume"] / b["volume"].rolling(30, min_periods=20).mean()
            b["dd30"] = c / c.rolling(30, min_periods=20).max() - 1
            b["f3"] = c.shift(-3) / c - 1
            b["f1"] = c.shift(-1) / c - 1
            b["f5"] = c.shift(-5) / c - 1
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b)
    df = pd.concat(rows, ignore_index=True)
    drift3 = df[df.pos % 3 == 0].groupby("coin")["f3"].mean()
    df["x3"] = df["f3"] - df["coin"].map(drift3)
    g = df[(df.pos % 3 == 0) & (df.regime == "unknown")].dropna(subset=["x3"])
    out = {}
    out["regimes share"] = df["regime"].value_counts(normalize=True)
    out["fc cases n, mean x3, t"] = pd.Series({"n": len(g), "mean": g.x3.mean(),
                                         "t": stats.ttest_1samp(g.x3, 0).statistic})
    def bucket(col, q=5):
        h = g.dropna(subset=[col]).copy()
        h["b"] = pd.qcut(h[col], q, labels=False, duplicates="drop")
        a = h.groupby("b").agg(lo=(col, "min"), hi=(col, "max"), n=("x3", "size"),
                               mean=("x3", "mean"), sd=("x3", "std"))
        a["t"] = a["mean"] / (a["sd"] / np.sqrt(a["n"]))
        return a.drop(columns="sd")
    for col in ["r7", "s7", "r1", "s1", "r3", "r14", "clv", "rng", "vratio", "volu", "dd30", "vol30"]:
        out["x3 by " + col] = bucket(col)
    a = g.groupby("wd")["x3"].agg(["size", "mean", "std"]); a["t"] = a["mean"]/(a["std"]/np.sqrt(a["size"]))
    out["x3 by weekday"] = a.drop(columns="std")
    a = g.groupby("yr")["x3"].agg(["size", "mean"]); out["x3 by year"] = a
    a = g.groupby("coin")["x3"].agg(["size", "mean"]); out["x3 by coin"] = a
    # spearman correlations
    cor = {}
    for col in ["r7", "s7", "r1", "s1", "r3", "r14", "clv", "rng", "vratio", "volu", "dd30", "vol30"]:
        h = g.dropna(subset=[col])
        r, p = stats.spearmanr(h[col], h.x3); cor[col] = (r, p, len(h))
    out["spearman x3"] = pd.DataFrame(cor, index=["rho", "p", "n"]).T
    # trades
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    if len(tr):
        out["trades"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["size", "mean", "median"])
        tr["fb"] = pd.qcut(tr["entry_forecast"], 4, labels=False, duplicates="drop")
        out["trades by entry fc"] = tr.groupby("fb")["net_profit_loss_percent"].agg(["size", "mean"])
    return out
