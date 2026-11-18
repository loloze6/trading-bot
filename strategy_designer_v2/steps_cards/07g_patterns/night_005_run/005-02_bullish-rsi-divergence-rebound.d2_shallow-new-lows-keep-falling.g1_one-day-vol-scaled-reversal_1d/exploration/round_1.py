def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]
            r = c.pct_change()
            vol = r.rolling(20, min_periods=10).std()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "r": r, "z": r / vol.shift(1),
                "vol": vol,
                "clv": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "fwd1": c.shift(-1) / c - 1,
                "fwd3": c.shift(-3) / c - 1,
                "fwd5": c.shift(-5) / c - 1,
                "r5": c / c.shift(5) - 1,
                "r20": c / c.shift(20) - 1,
                "fc": b["forecast"],
                "pos": b["postRebalance_current_allocation"],
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "i": np.arange(len(b)),
            })
            d["gain"] = d["pos"] * d["fwd1"]
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["fwd1"].transform("mean")
    D["ex1"] = D["fwd1"] - mu
    def summ(g, col="ex1"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    D["zq"] = pd.qcut(D["z"], 10, labels=False)
    out["next1 excess by z decile"] = D.groupby("zq").apply(summ)
    D["fq"] = pd.qcut(D["fc"].rank(method="first"), 10, labels=False)
    out["next1 excess by forecast decile"] = D.groupby("fq").apply(summ)
    # book gain by side
    D["side"] = np.sign(D["pos"])
    out["pos gain by side"] = D.groupby("side")["gain"].agg(["count", "mean", "sum"])
    out["pos gain by coin side"] = D.groupby(["coin", "side"])["gain"].agg(["count", "mean"])
    # multi-day: non-overlapping grids
    for h in [3, 5]:
        g = D[D["i"] % h == 0].copy()
        g["exh"] = g[f"fwd{h}"] - g.groupby("coin")[f"fwd{h}"].transform("mean")
        g["zq"] = pd.qcut(g["z"], 5, labels=False)
        out[f"fwd{h} excess by z quintile (nonoverlap)"] = g.groupby("zq").apply(lambda x: summ(x, "exh"))
    # vol regime
    D["vq"] = D.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False))
    D["ztr"] = np.sign(D["z"])
    out["next1 by vol tercile x day sign"] = D.groupby(["vq", "ztr"]).apply(summ)
    D["r20s"] = np.sign(D["r20"])
    out["next1 by r20 sign x day sign"] = D.groupby(["r20s", "ztr"]).apply(summ)
    out["next1 by weekday"] = D.groupby("wd").apply(summ)
    out["gain by weekday"] = D.groupby("wd")["gain"].agg(["count", "mean"])
    D["cq"] = pd.qcut(D["clv"], 5, labels=False)
    out["next1 by close location quintile"] = D.groupby("cq").apply(summ)
    out["gain by year"] = D.groupby("yr")["gain"].agg(["count", "mean"])
    out["next1 by year x day sign"] = D.groupby(["yr", "ztr"]).apply(summ)
    return out
