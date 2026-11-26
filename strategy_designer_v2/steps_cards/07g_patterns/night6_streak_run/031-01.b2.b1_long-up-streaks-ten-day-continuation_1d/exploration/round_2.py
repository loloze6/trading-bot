import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            z1 = r1 / vol20.shift(1)
            hi30 = c / c.rolling(30).max() - 1
            hi30z = hi30 / vol20
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(c)), "z1": z1, "r1": r1,
                               "hi30": hi30, "hi30z": hi30z, "year": ts.dt.year, "wd": ts.dt.weekday,
                               "alloc": b["postRebalance_current_allocation"]})
            for h in [1, 3, 5, 10]:
                df["f%d" % h] = c.shift(-h) / c - 1
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    res = {}
    def norm(df, col):
        m = d.groupby("coin")[col].transform("mean"); s = d.groupby("coin")[col].transform("std")
        return (df[col] - m.loc[df.index]) / s.loc[df.index]
    for h in [1, 3, 5, 10]:
        d["e%d" % h] = norm(d, "f%d" % h)
    def summ(df, key, col):
        out = df.groupby(key)[col].agg(["mean", "std", "count"])
        out["t"] = out["mean"] / (out["std"] / np.sqrt(out["count"]))
        return out.round(4)
    d["z1_q"] = d.groupby("coin")["z1"].transform(lambda x: pd.qcut(x.rank(method="first"), 10, labels=False))
    # reversal after large down day: by decile at h=1,3 (grid)
    res["next-day excess by z1 decile"] = summ(d.dropna(subset=["e1", "z1_q"]), "z1_q", "e1")
    g3 = d[(d.pos % 3 == 0)].dropna(subset=["e3", "z1_q"])
    res["3d excess by z1 decile (grid3)"] = summ(g3, "z1_q", "e3")
    low = d[d.z1_q == 0].dropna(subset=["e1"])
    res["next-day excess, lowest z1 decile, by coin"] = summ(low, "coin", "e1")
    res["next-day excess, lowest z1 decile, by year"] = summ(low, "year", "e1")
    neg = d[(d.z1 < 0)].dropna(subset=["e1", "z1"])
    res["slope next-day excess on z1, z1<0: corr,t,n"] = pd.Series({
        "r": stats.pearsonr(neg.z1, neg.e1)[0], "t": stats.linregress(neg.z1, neg.e1).slope / stats.linregress(neg.z1, neg.e1).stderr, "n": len(neg)}).round(4)
    # near 30d high continuation, grid 10 and 5
    g10 = d[(d.pos % 10 == 0)].dropna(subset=["e10", "hi30z"]).copy()
    g10["hq"] = g10.groupby("coin").hi30z.transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    res["10d excess by hi30z quintile (grid10)"] = summ(g10, "hq", "e10")
    top = g10[g10.hq == 4]
    res["10d excess, top hi30z quintile, by coin"] = summ(top, "coin", "e10")
    res["10d excess, top hi30z quintile, by year"] = summ(top, "year", "e10")
    g5 = d[(d.pos % 5 == 0)].dropna(subset=["e5", "hi30z"]).copy()
    g5["hq"] = g5.groupby("coin").hi30z.transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    res["5d excess by hi30z quintile (grid5)"] = summ(g5, "hq", "e5")
    # raw size of lowest z1 decile next day, and of top hi30 10d (pct)
    res["raw mean next-day ret lowest z1 decile minus coin mean"] = float((low.f1 - low.coin.map(d.groupby("coin").f1.mean())).mean())
    res["raw mean 10d ret top hi30z quintile minus coin mean"] = float((top.f10 - top.coin.map(d[d.pos % 10 == 0].groupby("coin").f10.mean())).mean())
    # weekday robustness by year halves
    d["half"] = np.where(d.year <= 2021, "early", "late")
    res["next-day excess by weekday x half"] = d.dropna(subset=["e1"]).groupby(["half", "wd"]).e1.mean().unstack().round(4)
    return res
