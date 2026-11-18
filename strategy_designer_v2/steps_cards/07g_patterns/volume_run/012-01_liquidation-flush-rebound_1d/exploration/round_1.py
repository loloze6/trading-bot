def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True).copy()
            cl = b["close"]; r1 = cl.pct_change()
            vol20 = r1.rolling(20, min_periods=10).std()
            z = r1 / vol20
            vr = b["volume"] / b["volume"].rolling(30, min_periods=10).mean()
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            wick = (np.minimum(b["open"], cl) - b["low"]) / rng
            upw = (b["high"] - np.maximum(b["open"], cl)) / rng
            r5 = cl / cl.shift(5) - 1
            r20 = cl / cl.shift(20) - 1
            f3 = cl.shift(-3) / cl - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": c, "w": w, "z": z, "vr": vr, "wick": wick, "upw": upw,
                               "r5z": r5 / (vol20 * np.sqrt(5)), "r20": r20, "vol20": vol20,
                               "f3": f3, "fc": b["forecast"], "wd": ts.dt.weekday, "year": ts.dt.year,
                               "pos": np.arange(len(b))})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A["pos"] % 3 == 0)].dropna(subset=["f3"]).copy()
    G["ex"] = G["f3"] - G.groupby("coin")["f3"].transform("mean")
    def summ(g):
        x = g["ex"].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    G["zq"] = pd.qcut(G["z"], 10, labels=False)
    out["ex3 by 1d z decile"] = G.groupby("zq").apply(summ)
    dn = G[G["z"] < -1].copy()
    dn["vrq"] = pd.qcut(dn["vr"], 3, labels=["lowvr", "midvr", "hivr"])
    dn["wkq"] = pd.qcut(dn["wick"], 3, labels=["lowwk", "midwk", "hiwk"])
    out["falls z<-1 by vr tercile"] = dn.groupby("vrq").apply(summ)
    out["falls z<-1 by wick tercile"] = dn.groupby("wkq").apply(summ)
    up = G[G["z"] > 1].copy()
    up["vrq"] = pd.qcut(up["vr"], 3, labels=["lowvr", "midvr", "hivr"])
    up["uwq"] = pd.qcut(up["upw"], 3, labels=["low", "mid", "hi"])
    out["rises z>1 by vr tercile"] = up.groupby("vrq").apply(summ)
    out["rises z>1 by upper wick tercile"] = up.groupby("uwq").apply(summ)
    G["r5q"] = pd.qcut(G["r5z"], 5, labels=False)
    out["ex3 by 5d z quintile"] = G.groupby("r5q").apply(summ)
    G["vq"] = G.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["ex3 by vol quintile"] = G.groupby("vq").apply(summ)
    G["r20q"] = pd.qcut(G["r20"], 5, labels=False)
    out["ex3 by 20d ret quintile"] = G.groupby("r20q").apply(summ)
    G["vrq_all"] = pd.qcut(G["vr"], 5, labels=False)
    out["ex3 by vr quintile all"] = G.groupby("vrq_all").apply(summ)
    out["ex3 forecast>=2 by coin"] = G[G["fc"] >= 2].groupby("coin").apply(summ)
    # weekday daily returns
    D = []
    for c in days:
        for w, d in days[c].items():
            d = d.copy(); d["coin"] = c; d["w"] = w
            d["wd"] = pd.to_datetime(d["day"]).dt.weekday
            D.append(d)
    D = pd.concat(D, ignore_index=True)
    out["coin ret by weekday"] = D.groupby("wd")["coin_return"].agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(x.count()))])
    out["book ret by weekday"] = D.groupby("wd")["book_return"].agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(x.count()))])
    out["book by coin"] = D.groupby("coin")["book_return"].agg(["mean", "std"]).assign(sh=lambda x: x["mean"] / x["std"] * np.sqrt(365))
    out["book by year"] = D.assign(y=pd.to_datetime(D["day"]).dt.year).groupby("y")["book_return"].agg(["count", "mean"])
    return out
