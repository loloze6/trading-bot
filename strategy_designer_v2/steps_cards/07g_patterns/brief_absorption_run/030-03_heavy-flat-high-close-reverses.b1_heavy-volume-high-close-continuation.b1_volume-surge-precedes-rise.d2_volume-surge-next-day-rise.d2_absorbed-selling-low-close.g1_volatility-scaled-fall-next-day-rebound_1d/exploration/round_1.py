def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol20 = r.rolling(20, min_periods=10).std()
            z = r / vol20
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            clv = (2 * b["close"] - b["high"] - b["low"]) / rng
            v = b["volume"].astype(float)
            vrel = np.log(v / v.rolling(20, min_periods=10).mean())
            r5 = c / c.shift(5) - 1
            z5 = r5 / (vol20 * np.sqrt(5))
            nxt = c.shift(-1) / c - 1
            nxt3 = c.shift(-3) / c - 1
            ts = pd.to_datetime(b["timestamp"], utc=True)
            df = pd.DataFrame({"coin": coin, "win": w, "z": z, "clv": clv, "vrel": vrel,
                               "z5": z5, "vol20": vol20, "nxt": nxt, "nxt3": nxt3,
                               "wd": ts.dt.dayofweek, "year": ts.dt.year,
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "fc": b["forecast"].astype(float),
                               "pos3": (np.arange(len(b)) % 3 == 0)})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    mu = d.groupby("coin")["nxt"].transform("mean")
    d["ex"] = d["nxt"] - mu
    d = d.dropna(subset=["z", "clv", "vrel", "ex"])
    def summ(g, col="ex"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    d["zq"] = pd.qcut(d["z"], 10, labels=False)
    out["by z decile"] = d.groupby("zq").apply(summ)
    d["clvq"] = pd.qcut(d["clv"], 5, labels=False)
    out["by clv quintile"] = d.groupby("clvq").apply(summ)
    d["vq"] = pd.qcut(d["vrel"], 3, labels=False)
    out["clv x vol tercile (mean%)"] = d.groupby(["vq", "clvq"]).apply(summ).reset_index()
    flat = d[d["z"].abs() < 0.5]
    out["flat days: vol hi, clv quint"] = flat[flat["vq"] == 2].groupby("clvq").apply(summ)
    neg = d[d["z"] < -1]
    out["falls z<-1 by clv tercile"] = neg.groupby(pd.qcut(neg["clv"], 3, labels=False)).apply(summ)
    out["falls z<-1 by vol tercile"] = neg.groupby("vq").apply(summ)
    d["z5q"] = pd.qcut(d["z5"], 5, labels=False)
    out["by 5d z quintile"] = d.groupby("z5q").apply(summ)
    out["by weekday"] = d.groupby("wd").apply(summ)
    d["volq"] = d.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["falls z<-1 by vol level"] = d[d["z"] < -1].groupby("volq").apply(summ)
    out["by coin, falls z<-1"] = d[d["z"] < -1].groupby("coin").apply(summ)
    out["by year, falls z<-1"] = d[d["z"] < -1].groupby("year").apply(summ)
    return out
