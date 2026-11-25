def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    h = 3
    drift = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - h, h):
                rs.append(c[i + h] / c[i] - 1)
        drift[coin] = (np.mean(rs), np.std(rs))
    rows = []
    for coin, wins in bars.items():
        m, s = drift[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            r1 = df["close"].pct_change()
            vol = r1.rolling(30).std()
            z = (r1 / vol).values
            fc = df["forecast"].fillna(0).values
            day = pd.to_datetime(df["timestamp"]).dt.floor("D").values
            # plan's case: forecast falls >= 2 from its highest (least short) since last bet, reset at flat
            ref = 0.0
            sig = np.zeros(len(c), bool)
            for i in range(len(c)):
                if fc[i] == 0:
                    ref = 0.0
                    continue
                if fc[i] <= ref - 2:
                    sig[i] = True
                    ref = fc[i]
            for g0 in range(0, len(c) - h, h):
                idx = [i for i in range(g0, g0 + h) if sig[i] and i + h < len(c)]
                if not idx: continue
                i = idx[0]
                um = -(c[i + h] / c[i] - 1 - m)
                um1 = -(c[i + 1] / c[i] - 1 - drift[coin][0] / 3)
                rows.append(dict(coin=coin, w=w, day=day[i], z=z[i], fc=abs(fc[i]), um=um, um1=um1, st=um / s))
    d = pd.DataFrame(rows).dropna(subset=["z"])

    def ct(g, col="um"):
        n = len(g); mean = g[col].mean()
        dev = g.groupby("day")[col].apply(lambda x: (x - mean).sum())
        G = len(dev)
        if G < 3: return np.nan
        se = np.sqrt(G / (G - 1) * (dev ** 2).sum()) / n
        return mean / se

    def summ(g):
        return pd.Series(dict(n=len(g), days=g["day"].nunique(), um=g["um"].mean(),
                              strength=g["st"].mean(), t=ct(g), um1=g["um1"].mean(), t1=ct(g, "um1")))
    out["plan cases all"] = summ(d)
    d["fq"] = pd.qcut(d["fc"].rank(method="first"), 4, labels=["f1", "f2", "f3", "f4"])
    d["zq"] = pd.qcut(d["z"], 4, labels=["z1", "z2", "z3", "z4"])
    out["by forecast quartile"] = d.groupby("fq").apply(summ)
    out["by raw z quartile"] = d.groupby("zq").apply(summ)
    out["corr fc vs z (spearman)"] = d[["fc", "z"]].corr(method="spearman").iloc[0, 1]
    zm = d["z"].median()
    out["raw z larger minus smaller half um"] = d[d.z > zm]["um"].mean() - d[d.z <= zm]["um"].mean()
    out["by coin"] = d.groupby("coin").apply(summ)
    return out
