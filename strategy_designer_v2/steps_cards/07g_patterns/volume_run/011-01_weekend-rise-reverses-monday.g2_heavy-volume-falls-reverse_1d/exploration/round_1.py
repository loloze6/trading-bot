import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"]
            r = c.pct_change()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "ret": r,
                "fwd1": c.shift(-1)/c - 1,
                "z": r / r.rolling(20, min_periods=10).std().shift(1),
                "vr": b["volume"] / b["volume"].rolling(60, min_periods=20).mean(),
                "vol20": r.rolling(20, min_periods=10).std(),
                "ret5": c/c.shift(5) - 1,
                "wd": ts.dt.weekday.values,
                "pos": b["postRebalance_current_allocation"],
                "fc": b["forecast"],
            })
            d["idx"] = np.arange(len(d))
            d["fwd3"] = np.where(d["idx"] % 3 == 0, c.shift(-3)/c - 1, np.nan)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["ret"].mean()
    D["ex1"] = D["fwd1"] - D["coin"].map(mu)
    D["ex3"] = D["fwd3"] - 3*D["coin"].map(mu)

    def summ(g, col="ex1"):
        x = g[col].dropna()
        n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(n)) if n > 2 else np.nan})

    out = {}
    D["zq"] = pd.qcut(D["z"], 10, labels=False, duplicates="drop")
    D["vrq"] = pd.qcut(D["vr"], 3, labels=["vrLo", "vrMid", "vrHi"])
    out["next1 by z decile"] = D.groupby("zq").apply(summ)
    out["next1 by z decile x vr tercile"] = D.groupby(["zq", "vrq"]).apply(summ).unstack()["t"]
    out["next1 mean by z decile x vr"] = D.groupby(["zq", "vrq"]).apply(summ).unstack()["mean"]
    out["next3 by z decile"] = D.groupby("zq").apply(lambda g: summ(g, "ex3"))
    out["next1 by weekday"] = D.groupby("wd").apply(summ)
    D["dn"] = D["z"] < -1
    out["next1 big falls (z<-1) by weekday"] = D[D["dn"]].groupby("wd").apply(summ)
    out["next1 big rises (z>1) by weekday"] = D[D["z"] > 1].groupby("wd").apply(summ)
    D["volq"] = D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["next1 by vol quintile"] = D.groupby("volq").apply(summ)
    D["r5q"] = pd.qcut(D["ret5"], 5, labels=False)
    out["next1 by 5d ret quintile"] = D.groupby("r5q").apply(summ)
    out["next1 by vr tercile (all)"] = D.groupby("vrq").apply(summ)
    out["next1 by coin, active bars"] = D[D["fc"] > 0].groupby("coin").apply(summ)
    out["next1 by coin, z<-1"] = D[D["z"] < -1].groupby("coin").apply(summ)
    # book
    br = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd[["day", "book_return", "coin_return"]].copy()
            x["coin"] = coin; x["win"] = w
            br.append(x)
    B = pd.concat(br)
    B["wd"] = pd.to_datetime(B["day"]).dt.weekday
    B["yr"] = pd.to_datetime(B["day"]).dt.year
    out["book by weekday"] = B.groupby("wd")["book_return"].agg(["count", "mean", "sum"])
    out["book by year"] = B.groupby("yr")["book_return"].agg(["count", "mean", "sum"])
    out["book by coin"] = B.groupby("coin")["book_return"].agg(["mean", "std"])
    return out
