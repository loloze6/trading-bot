import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    h = 24
    drift, sd = {}, {}
    for c in bars:
        allr = []
        for w, df in bars[c].items():
            cl = df["close"].values
            idx = np.arange(0, len(cl) - h, h)
            allr.append(cl[idx + h] / cl[idx] - 1)
        allr = np.concatenate(allr)
        drift[c] = np.nanmean(allr); sd[c] = np.nanstd(allr)
    recs = []
    for c in bars:
        for w, df in bars[c].items():
            cl = pd.Series(df["close"].values)
            ts = pd.to_datetime(df["timestamp"].values)
            r24 = cl / cl.shift(24) - 1
            mabs = r24.abs().rolling(720, min_periods=240).mean()
            z = r24 / mabs
            vol = cl.pct_change().rolling(720, min_periods=240).std()
            idx = np.arange(0, len(cl) - h, h)
            raw = cl.values[idx + h] / cl.values[idx] - 1
            recs.append(pd.DataFrame({"coin": c, "win": w, "z": z.values[idx], "vol": vol.values[idx],
                                      "raw": raw, "fwd": raw - drift[c], "fwdn": (raw - drift[c]) / sd[c],
                                      "year": ts[idx].year, "wd": ts[idx].weekday}))
    d = pd.concat(recs).dropna()
    d["zq"] = d.groupby("coin")["z"].transform(lambda s: pd.qcut(s, 5, labels=False))
    d["vq"] = d.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False))
    def tt(x):
        x = np.asarray(x)
        return pd.Series({"mean%": 100 * x.mean(), "t": x.mean() / (x.std(ddof=1) / np.sqrt(len(x))), "n": len(x)})
    out = {}
    hv = d[d.vq == 2]
    out["high vol: coin x extreme quintile, fwd24"] = hv[hv.zq.isin([0, 4])].groupby(["coin", "zq"])["fwd"].apply(tt).unstack()
    # signed reversal measure: -sign(z)*fwd, its strength, total move
    d["sgn"] = -np.sign(d.z)
    d["unus"] = d.sgn * d.fwd
    d["tot"] = d.sgn * d.raw
    d["str"] = d.sgn * d.fwdn
    ext = d[d.zq.isin([0, 4])]
    out["extremes by vol tercile: unusual, total, strength"] = ext.groupby("vq").agg(
        unusual_pct=("unus", lambda x: 100 * x.mean()), total_pct=("tot", lambda x: 100 * x.mean()),
        strength=("str", "mean"), n=("unus", "size"))
    out["extremes high vol by year: unusual %"] = ext[ext.vq == 2].groupby("year")["unus"].apply(tt).unstack()
    # graded: corr of -z*vol with fwdn, by coin
    d["sig"] = -d.z * d.vol
    out["corr(-z*vol, fwdn) by coin"] = d.groupby("coin").apply(lambda g: pd.Series({"corr": g.sig.corr(g.fwdn), "n": len(g)}))
    # weekend rises by coin
    wk = d[d.wd.isin([5, 6]) & (d.zq == 4)]
    out["weekend top-quintile rise: fwd by coin"] = wk.groupby("coin")["fwd"].apply(tt).unstack()
    out["weekend top-quintile rise by vol tercile"] = wk.groupby("vq")["fwd"].apply(tt).unstack()
    out["weekday by weekday x extreme"] = ext.groupby(["wd", "zq"])["fwd"].apply(lambda x: 100 * x.mean()).unstack()
    return out
