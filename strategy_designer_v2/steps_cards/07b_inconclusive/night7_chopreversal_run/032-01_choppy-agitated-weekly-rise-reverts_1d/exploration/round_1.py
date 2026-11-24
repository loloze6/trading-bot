import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values.astype(float)
            reg = df["regime"].astype(str).values
            fc = df["forecast"].values.astype(float)
            n = len(c)
            for h in (3, 7, 14):
                for t in range(0, n, h):
                    if t + h >= n:
                        continue
                    fut = c[t + h] / c[t] - 1
                    past7 = c[t] / c[t - 7] - 1 if t >= 7 else np.nan
                    past3 = c[t] / c[t - 3] - 1 if t >= 3 else np.nan
                    past14 = c[t] / c[t - 14] - 1 if t >= 14 else np.nan
                    rows.append(dict(coin=coin, w=w, h=h, fut=fut, past7=past7, past3=past3,
                                     past14=past14, inprof=(reg[t] == "unknown"), fc=fc[t]))
    d = pd.DataFrame(rows)
    # drift per coin per h (all grid cells)
    d["drift"] = d.groupby(["coin", "h"])["fut"].transform("mean")
    d["unus"] = d["fut"] - d["drift"]
    d["sd"] = d.groupby(["coin", "h"])["fut"].transform("std")
    d["z"] = d["unus"] / d["sd"]

    def summ(g, pcol="past7"):
        g = g.dropna(subset=[pcol])
        if len(g) < 8:
            return pd.Series(dict(n=len(g)))
        r, p = stats.pearsonr(g[pcol], g["unus"])
        tt = r * np.sqrt((len(g) - 2) / max(1e-12, 1 - r * r))
        rev = (-np.sign(g[pcol]) * g["z"])
        return pd.Series(dict(n=len(g), corr=round(r, 3), t=round(tt, 2),
                              rev_strength=round(rev.mean(), 3),
                              rev_t=round(rev.mean() / (rev.std() / np.sqrt(len(g))), 2)))

    out = {}
    d7 = d[d.h == 7]
    out["h7 by profile"] = d7.groupby("inprof").apply(summ)
    out["h7 in-profile by side"] = d7[d7.inprof].assign(side=np.sign(d7.past7)).groupby("side").apply(summ)
    out["h7 out-profile by side"] = d7[~d7.inprof].assign(side=np.sign(d7.past7)).groupby("side").apply(summ)
    out["h7 in-profile by coin"] = d7[d7.inprof].groupby("coin").apply(summ)
    out["h7 in-profile by window"] = d7[d7.inprof].groupby("w").apply(summ)
    out["by horizon, in-profile, matching past"] = pd.DataFrame({
        h: summ(d[(d.h == h) & d.inprof], f"past{h}") for h in (3, 7, 14)}).T
    out["by horizon, out-profile, matching past"] = pd.DataFrame({
        h: summ(d[(d.h == h) & ~d.inprof], f"past{h}") for h in (3, 7, 14)}).T
    # strongest rises in profile
    g = d7[d7.inprof & (d7.past7 > 0)].copy()
    g["q"] = pd.qcut(g.past7.rank(method="first"), 3, labels=["low", "mid", "high"])
    out["h7 in-profile rises by tercile"] = g.groupby("q").agg(n=("z", "size"), past7=("past7", "mean"),
                                                               unus=("unus", "mean"), z=("z", "mean"))
    out["share in profile"] = d7.inprof.mean()
    return out
