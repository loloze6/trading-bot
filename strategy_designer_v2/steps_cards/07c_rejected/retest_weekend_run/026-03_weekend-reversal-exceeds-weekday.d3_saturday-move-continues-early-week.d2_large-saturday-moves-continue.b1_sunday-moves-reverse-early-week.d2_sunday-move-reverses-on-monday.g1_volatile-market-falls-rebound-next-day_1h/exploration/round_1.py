import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    hs = [6, 12, 24, 48, 72]
    drift = {}
    sd = {}
    # drift per coin per horizon
    for c in bars:
        for h in hs:
            allr = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                allr.append(cl[idx + h] / cl[idx] - 1)
            allr = np.concatenate(allr)
            drift[(c, h)] = np.nanmean(allr); sd[(c, h)] = np.nanstd(allr)
    recs = {h: [] for h in hs}
    for c in bars:
        for w, df in bars[c].items():
            cl = pd.Series(df["close"].values)
            ts = pd.to_datetime(df["timestamp"].values)
            r24 = cl / cl.shift(24) - 1
            mabs = r24.abs().rolling(720, min_periods=240).mean()
            z = r24 / mabs
            vol = (cl.pct_change()).rolling(720, min_periods=240).std()
            for h in hs:
                idx = np.arange(0, len(cl) - h, h)
                fwd = cl.values[idx + h] / cl.values[idx] - 1 - drift[(c, h)]
                d = pd.DataFrame({"coin": c, "win": w, "z": z.values[idx], "vol": vol.values[idx],
                                  "fwd": fwd, "fwdn": fwd / sd[(c, h)],
                                  "year": ts[idx].year, "wd": ts[idx].weekday, "hr": ts[idx].hour})
                recs[h].append(d)
    R = {h: pd.concat(recs[h]).dropna() for h in hs}
    def tt(x):
        x = np.asarray(x); return pd.Series({"mean%": 100*x.mean(), "t": x.mean()/(x.std(ddof=1)/np.sqrt(len(x))), "n": len(x)})
    out = {}
    d = R[24].copy()
    d["zq"] = d.groupby("coin")["z"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["24h fwd by z quintile (0=deep fall)"] = d.groupby("zq")["fwd"].apply(tt).unstack()
    d["side"] = np.where(d.z < 0, "fall", "rise")
    out["coin x side, fwd24"] = d.groupby(["coin", "side"])["fwd"].apply(tt).unstack()
    # graded slope: corr of z with fwd by side
    out["slope by coin and side (corr z, fwdn)"] = d.groupby(["coin","side"]).apply(
        lambda g: pd.Series({"corr": g.z.corr(g.fwdn), "n": len(g)})).unstack()
    out["year x extreme quintiles"] = d[d.zq.isin([0,4])].groupby(["year","zq"])["fwd"].apply(lambda x: 100*x.mean()).unstack()
    d["vq"] = d.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["vol tercile x extreme quintiles"] = d[d.zq.isin([0,4])].groupby(["vq","zq"])["fwd"].apply(tt).unstack()
    d["wkend"] = d.wd.isin([5,6])
    out["signal on weekend? x extreme quintile"] = d[d.zq.isin([0,4])].groupby(["wkend","zq"])["fwd"].apply(tt).unstack()
    hz = []
    for h in hs:
        g = R[h]
        r, p = stats.pearsonr(g.z, g.fwdn)
        lo = g[g.z <= g.groupby("coin").z.transform(lambda s: s.quantile(.2))].fwd
        hi = g[g.z >= g.groupby("coin").z.transform(lambda s: s.quantile(.8))].fwd
        hz.append({"h": h, "corr": r, "n": len(g), "lowQ mean%": 100*lo.mean(), "lowQ t": lo.mean()/(lo.std()/np.sqrt(len(lo))),
                   "highQ mean%": 100*hi.mean(), "highQ t": hi.mean()/(hi.std()/np.sqrt(len(hi)))})
    out["by horizon"] = pd.DataFrame(hz)
    return out
