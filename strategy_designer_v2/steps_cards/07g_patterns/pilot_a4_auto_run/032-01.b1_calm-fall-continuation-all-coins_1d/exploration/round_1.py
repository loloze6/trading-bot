def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "fc": c.pct_change(1).values,
                "r1": (c.shift(-1)/c - 1).values,
                "r3": (c.shift(-3)/c - 1).values,
                "r5": (c.shift(-5)/c - 1).values,
                "ret5": (c/c.shift(5) - 1).values,
                "ret10": (c/c.shift(10) - 1).values,
                "ret30": (c/c.shift(30) - 1).values,
                "pos30": ((c - c.rolling(30).min())/(c.rolling(30).max()-c.rolling(30).min())).values,
                "clv": ((c - b["low"])/(b["high"]-b["low"])).values,
                "rng": ((b["high"]-b["low"])/c).values,
                "volr": (b["volume"]/b["volume"].rolling(20).mean()).values,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday.values,
                "yr": pd.to_datetime(b["timestamp"]).dt.year.values,
                "inprof": (b["regime"] == "unknown").values,
                "pos": np.arange(len(b)),
            })
            d["rngz"] = d["rng"]/pd.Series(d["rng"]).rolling(20).mean()
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu1 = D.groupby("coin")["r1"].mean()
    D["x1"] = D["r1"] - D["coin"].map(mu1)
    for h in (3, 5):
        g = D[D["pos"] % h == 0].groupby("coin")["r%d" % h].mean()
        D["x%d" % h] = D["r%d" % h] - D["coin"].map(g)
    F = D[D["inprof"]].copy()
    out = {}
    out["counts"] = F.groupby("coin").size()
    def tq(col, ycol="x1", h=1, q=5):
        S = F[(F["pos"] % h == 0)].dropna(subset=[col, ycol])
        S = S.assign(b=pd.qcut(S[col].rank(method="first"), q, labels=False))
        g = S.groupby("b")[ycol].agg(["mean", "count", "std"])
        g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
        g["xmean"] = S.groupby("b")[col].mean()
        r, p = stats.spearmanr(S[col], S[ycol])
        g.loc["rho"] = [r, len(S), np.nan, p, np.nan]
        return g
    for col in ["ret30", "ret10", "ret5", "fc", "pos30", "clv", "rngz", "volr"]:
        out["x1 by " + col] = tq(col)
    for col in ["ret30", "ret5", "fc", "pos30"]:
        out["x3 by " + col] = tq(col, "x3", 3)
    out["x1 by weekday"] = F.groupby("wd")["x1"].agg(["mean", "count"])
    out["x1 by year"] = F.groupby("yr")["x1"].agg(["mean", "count"])
    out["x1 by coin"] = F.groupby("coin")["x1"].agg(["mean", "count"])
    out["x1 outside profile"] = D[~D["inprof"]].groupby("coin")["x1"].agg(["mean", "count"])
    return out
