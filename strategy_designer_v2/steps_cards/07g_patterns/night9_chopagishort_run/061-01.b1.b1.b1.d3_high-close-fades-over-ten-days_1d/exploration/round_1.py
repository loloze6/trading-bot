def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; out = {}
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; h = b["high"].values; l = b["low"].values; o = b["open"].values
            n = len(b)
            rng = h - l
            loc = np.where(rng > 0, (c - l) / np.where(rng > 0, rng, 1), np.nan)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            for H in (2, 10):
                for i in range(0, n - H, H):
                    rows.append(dict(coin=coin, w=w, H=H, i=i, loc=loc[i], reg=b["regime"].iloc[i],
                                     fwd=c[i + H] / c[i] - 1, r1=r1[i], rng=rng[i] / c[i],
                                     body=(c[i] - o[i]) / c[i],
                                     wd=pd.Timestamp(b["timestamp"].iloc[i]).weekday(),
                                     fc=b["forecast"].iloc[i]))
    df = pd.DataFrame(rows)
    df["ca"] = df["reg"].isin(["mean_reversion", "unknown"])
    for H in (2, 10):
        d = df[df.H == H].copy()
        drift = d.groupby("coin")["fwd"].transform("mean")
        d["ex"] = d["fwd"] - drift
        d["locb"] = pd.cut(d["loc"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01])
        g = d.groupby(["ca", "locb"], observed=True)["ex"].agg(["mean", "count", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        out[f"H{H} excess by profile CA x loc"] = g.round(4)
        d["r1q"] = d.groupby("ca")["r1"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
        g = d.groupby(["ca", "r1q"])["ex"].agg(["mean", "count", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        out[f"H{H} excess by CA x prior-day return quintile"] = g.round(4)
        d["rq"] = d.groupby("ca")["rng"].transform(lambda s: pd.qcut(s, 4, labels=False, duplicates="drop"))
        g = d.groupby(["ca", "rq"])["ex"].agg(["mean", "count", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        out[f"H{H} excess by CA x range quartile"] = g.round(4)
        g = d.groupby(["ca", "wd"])["ex"].agg(["mean", "count", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        out[f"H{H} excess by CA x weekday"] = g.round(4)
    d = df[(df.H == 10) & (df.reg == "mean_reversion")].copy()
    d["ex"] = d["fwd"] - df[df.H == 10].groupby("coin")["fwd"].transform("mean").reindex(d.index)
    d["bodyq"] = pd.qcut(d["body"], 3, labels=False, duplicates="drop")
    g = d.groupby("bodyq")["ex"].agg(["mean", "count"])
    out["H10 in-regime excess by body tercile (pos=up day)"] = g.round(4)
    d["locq"] = pd.qcut(d["loc"], 3, labels=False, duplicates="drop")
    out["H10 in-regime excess by loc tercile"] = d.groupby("locq")["ex"].agg(["mean", "count"]).round(4)
    out["regime counts"] = df[df.H == 10]["reg"].value_counts()
    return out
