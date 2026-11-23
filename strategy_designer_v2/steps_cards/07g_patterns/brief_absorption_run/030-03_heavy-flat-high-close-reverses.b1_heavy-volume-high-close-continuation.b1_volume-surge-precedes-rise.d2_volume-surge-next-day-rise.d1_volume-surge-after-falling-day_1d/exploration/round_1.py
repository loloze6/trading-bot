import numpy as np
import pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            allr.append(b["close"].pct_change())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            d = pd.DataFrame()
            r = b["close"].pct_change()
            sd = r.rolling(20, min_periods=15).std().shift(1)
            d["z"] = r / sd
            d["vr"] = b["volume"] / b["volume"].rolling(20, min_periods=15).mean().shift(1)
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            d["clv"] = (b["close"] - b["low"]) / rng
            d["rngz"] = (rng / b["close"]) / sd
            d["r5z"] = (b["close"] / b["close"].shift(5) - 1) / (sd * np.sqrt(5))
            d["volreg"] = sd / sd.rolling(120, min_periods=40).median()
            d["nx"] = b["close"].shift(-1) / b["close"] - 1 - mu
            d["nx3"] = b["close"].shift(-3) / b["close"] - 1 - 3 * mu
            d["pos"] = (np.arange(len(b)) % 3 == 0)
            d["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            d["alloc"] = b["postRebalance_current_allocation"]
            d["coin"] = coin; d["win"] = w
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)

    def summ(g, col="nx"):
        x = g[col].dropna()
        n = len(x)
        return pd.Series({"n": n, "mean%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})

    out = {}
    D["zq"] = pd.qcut(D["z"], 7, labels=False)
    out["nx by today z septile"] = D.groupby("zq").apply(summ)
    D["vq"] = pd.qcut(D["vr"], 5, labels=False)
    out["nx by vol ratio quintile"] = D.groupby("vq").apply(summ)
    D["cq"] = pd.qcut(D["clv"], 5, labels=False)
    out["nx by clv quintile"] = D.groupby("cq").apply(summ)
    flat = D[D["z"].abs() < 0.5]
    t = flat.groupby(["vq", "cq"]).apply(summ)
    out["flat days: vq x cq mean%"] = t["mean%"].unstack()
    out["flat days: vq x cq t"] = t["t"].unstack()
    up = D[D["z"] > 0]
    out["up days nx by vq"] = up.groupby("vq").apply(summ)
    dn = D[D["z"] < 0]
    out["down days nx by cq"] = dn.groupby("cq").apply(summ)
    out["up days nx by cq"] = up.groupby("cq").apply(summ)
    D["rq"] = pd.qcut(D["rngz"], 5, labels=False)
    out["nx by range size quintile"] = D.groupby("rq").apply(summ)
    D["r5q"] = pd.qcut(D["r5z"], 5, labels=False)
    out["nx by 5d return quintile"] = D.groupby("r5q").apply(summ)
    out["nx3 (grid) by 5d return quintile"] = D[D["pos"]].groupby("r5q").apply(lambda g: summ(g, "nx3"))
    D["vlq"] = pd.qcut(D["volreg"], 3, labels=False)
    out["down days nx by vol regime x zq"] = D[D["z"] < 0].groupby(["vlq", "zq"]).apply(summ)
    out["nx by weekday"] = D.groupby("wd").apply(summ)
    out["nx by coin, down z<-1"] = D[D["z"] < -1].groupby("coin").apply(summ)
    return out
