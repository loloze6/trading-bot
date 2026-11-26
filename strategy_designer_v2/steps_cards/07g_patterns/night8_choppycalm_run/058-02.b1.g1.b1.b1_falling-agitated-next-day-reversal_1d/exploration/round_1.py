def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(20, min_periods=15).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "z": r / sd, "r1": r,
                "n1": c.shift(-1) / c - 1, "n2": c.shift(-2) / c - 1, "n3": c.shift(-3) / c - 1,
                "tr60": c / c.shift(60) - 1,
                "vrel": r.rolling(10).std() / r.rolling(60, min_periods=40).std(),
                "clv": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "inprof": (b["regime"] == "unknown").astype(int),
                "pos": b["postRebalance_current_allocation"].astype(float),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    mu = d.groupby("coin")["n1"].transform("mean")
    d["x1"] = d["n1"] - mu
    d["fade"] = -np.sign(d["z"]) * d["x1"]   # gain of a fade, excess
    d = d.dropna(subset=["z", "x1"])
    d["day"] = d["ts"].dt.floor("D")

    def summ(g):
        s = g["fade"]
        return pd.Series({"n": len(s), "mean_fade": s.mean(),
                          "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})

    d["zq"] = pd.qcut(d["z"], 10, labels=False)
    out = {}
    out["fade by z decile"] = d.groupby("zq").apply(summ).join(d.groupby("zq")["z"].mean().rename("zmean")).join(d.groupby("zq")["x1"].mean().rename("next_excess"))
    out["fade by profile flag"] = d.groupby("inprof").apply(summ)
    d["trb"] = pd.cut(d["tr60"], [-10, -0.3, -0.1, 0.1, 0.3, 100])
    out["fade |z|>1 by 60d trend"] = d[d["z"].abs() > 1].groupby("trb").apply(summ)
    d["vb"] = pd.qcut(d["vrel"], 4, labels=False)
    out["fade |z|>1 by vol-ratio quartile"] = d[d["z"].abs() > 1].groupby("vb").apply(summ)
    d["side"] = np.where(d["z"] > 0, "up", "down")
    out["fade |z|>1 side x profile"] = d[d["z"].abs() > 1].groupby(["side", "inprof"]).apply(summ)
    d["clvb"] = pd.cut(d["clv"], [0, 0.2, 0.4, 0.6, 0.8, 1.0], include_lowest=True)
    out["next excess by close location, down days z<-1"] = d[d["z"] < -1].groupby("clvb")["x1"].agg(["count", "mean"])
    out["next excess by close location, up days z>1"] = d[d["z"] > 1].groupby("clvb")["x1"].agg(["count", "mean"])
    out["next excess by close location all"] = d.groupby("clvb")["x1"].agg(["count", "mean", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))])
    d["wd"] = d["ts"].dt.weekday
    out["next excess by weekday"] = d.groupby("wd")["x1"].agg(["count", "mean", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))])
    out["fade |z|>1 by weekday"] = d[d["z"].abs() > 1].groupby("wd").apply(summ)
    out["fade |z|>1 by year"] = d[d["z"].abs() > 1].groupby(d["ts"].dt.year).apply(summ)
    # book days
    bd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; bd.append(x)
    bd = pd.concat(bd)
    bk = bd.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book daily: n, mean, sd"] = pd.Series({"n": len(bk), "mean": bk.mean(), "sd": bk.std(),
                                                "top10 share of sum": bk.sort_values().iloc[-10:].sum() / bk.sum(),
                                                "bot10 sum": bk.sort_values().iloc[:10].sum()})
    out["book by window"] = bk.groupby(level=0).agg(["count", "mean", "sum"])
    return out
