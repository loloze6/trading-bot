def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z1 = r / sd
            p5 = (c.shift(1) / c.shift(6) - 1) / (sd * np.sqrt(5))
            f1 = c.shift(-1) / c - 1
            f3 = c.shift(-3) / c - 1
            pos = np.arange(len(b))
            df = pd.DataFrame({"coin": coin, "w": w, "z1": z1, "p5": p5, "f1": f1, "f3": f3,
                               "reg": b["regime"].astype(str), "pos": pos,
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                               "fc": b["forecast"], "rng": (b["high"] - b["low"]) / c / sd,
                               "clv": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                               "alloc": b["postRebalance_current_allocation"]})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["inprof"] = d["reg"].isin(["mean_reversion", "unknown"])
    # drift over all windows per coin
    g3 = d[d["pos"] % 3 == 0].copy()
    drift3 = g3.groupby("coin")["f3"].mean()
    g3["u3"] = g3["f3"] - g3["coin"].map(drift3)
    drift1 = d.groupby("coin")["f1"].mean()
    d["u1"] = d["f1"] - d["coin"].map(drift1)
    def summ(x, col):
        x = x.dropna(subset=[col, "zq"])
        out = x.groupby("zq")[col].agg(["count", "mean", "std"])
        out["t"] = out["mean"] / (out["std"] / np.sqrt(out["count"]))
        return out.drop(columns="std")
    res = {}
    edges = [-np.inf, -2, -1, -0.3, 0.3, 1, 2, np.inf]
    labels = ["<-2", "-2..-1", "-1..-.3", "~0", ".3..1", "1..2", ">2"]
    for name, sub in [("in", g3[g3["inprof"]]), ("out", g3[~g3["inprof"]])]:
        s = sub.copy(); s["zq"] = pd.cut(s["z1"], edges, labels=labels)
        res[f"u3 by z1, profile {name}"] = summ(s, "u3")
    for name, sub in [("in", d[d["inprof"]]), ("out", d[~d["inprof"]])]:
        s = sub.copy(); s["zq"] = pd.cut(s["z1"], edges, labels=labels)
        res[f"u1 by z1 (overlap-free, 1d), profile {name}"] = summ(s, "u1")
    s = g3[g3["inprof"] & (g3["z1"] > 0)].copy()
    s["zq"] = pd.cut(s["p5"], [-np.inf, -1, -0.3, 0.3, 1, np.inf])
    res["in-profile up days: u3 by prior 5d"] = summ(s, "u3")
    s = d[d["inprof"]].copy(); s["zq"] = s["wd"]
    res["in-profile u1 by weekday"] = summ(s, "u1")
    s = d[~d["inprof"]].copy(); s["zq"] = s["wd"]
    res["out-profile u1 by weekday"] = summ(s, "u1")
    s = g3[g3["inprof"]].copy(); s["zq"] = pd.qcut(s["clv"], 4, duplicates="drop")
    res["in-profile u3 by close location"] = summ(s, "u3")
    s = g3[g3["inprof"]].copy(); s["zq"] = pd.qcut(s["rng"], 4, duplicates="drop")
    res["in-profile u3 by range/sd"] = summ(s, "u3")
    res["share in profile"] = float(d["inprof"].mean())
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    dd = pd.concat(dd)
    dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
    bk = dd.groupby(["w", "day"]).agg(br=("book_return", "mean"), wd=("wd", "first"))
    res["book by window"] = bk.groupby("w")["br"].agg(["count", "mean", "std"])
    return res
