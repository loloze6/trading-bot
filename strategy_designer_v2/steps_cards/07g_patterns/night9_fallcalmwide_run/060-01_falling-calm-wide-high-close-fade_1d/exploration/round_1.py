def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            rng = (b["high"] - b["low"]) / c
            width = rng / sd
            loc = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            nxt = c.shift(-1) / c - 1
            nxt3 = c.shift(-3) / c - 1
            ret60 = c / c.shift(60) - 1
            df = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                               "r": r, "width": width, "loc": loc, "nxt": nxt, "nxt3": nxt3,
                               "ret60": ret60, "regime": b["regime"], "fc": b["forecast"],
                               "sd": sd, "sd_rank": sd.rolling(90, min_periods=40).rank(pct=True)})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["day"] = d["ts"].dt.floor("D")
    drift = d.groupby("coin")["nxt"].mean()
    d["unx"] = d["nxt"] - d["coin"].map(drift)
    d["inprof"] = d["regime"] != "chop"
    d = d.dropna(subset=["unx", "width", "loc"])

    def stat(g, col="unx"):
        s = g.groupby("day")[col].sum()
        dev = g[col] - g[col].mean()
        sdv = dev.groupby(g["day"]).sum()
        n = len(sdv)
        se = np.sqrt((sdv ** 2).sum()) / len(g) if len(g) else np.nan
        return pd.Series({"n": len(g), "days": n, "mean%": 100 * g[col].mean(),
                          "t": g[col].mean() / se if se and se > 0 else np.nan})

    out = {}
    d["wq"] = pd.qcut(d["width"], 5, labels=["w1lo", "w2", "w3", "w4", "w5hi"])
    d["lq"] = pd.cut(d["loc"], [-0.01, 0.25, 0.5, 0.75, 1.01], labels=["low", "midlo", "midhi", "high"])
    out["all: width x loc"] = d.groupby(["wq", "lq"], observed=True).apply(stat).round(3)
    p = d[d["inprof"]]
    out["profile falling calm: width x loc"] = p.groupby(["wq", "lq"], observed=True).apply(stat).round(3)
    d["rq"] = pd.qcut(d["r"] / d["sd"], 5, labels=["bigdown", "down", "flat", "up", "bigup"])
    d["tr"] = pd.cut(d["ret60"], [-10, -0.1, 0.1, 100], labels=["falling", "choppy", "rising"])
    out["today scaled ret x trend"] = d.groupby(["tr", "rq"], observed=True).apply(stat).round(3)
    d["vq"] = pd.cut(d["sd_rank"], [0, 0.5, 1.0], labels=["calm", "agit"])
    out["today scaled ret x agitation"] = d.groupby(["vq", "rq"], observed=True).apply(stat).round(3)
    d["wd"] = d["ts"].dt.dayofweek
    out["weekday"] = d.groupby("wd").apply(stat).round(3)
    out["year"] = d.groupby(d["ts"].dt.year).apply(stat).round(3)
    sit = d[d["fc"] < 0]
    out["situation by coin"] = sit.groupby("coin").apply(stat).round(3)
    out["situation by window"] = sit.groupby("win").apply(stat).round(3)
    return out
