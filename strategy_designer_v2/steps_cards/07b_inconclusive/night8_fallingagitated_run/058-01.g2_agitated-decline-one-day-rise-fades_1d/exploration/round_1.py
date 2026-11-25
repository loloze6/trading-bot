def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for h in [1, 2, 3, 5, 10]:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = (np.mean(rs), np.std(rs))
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            r1 = df["close"].pct_change()
            vol = r1.rolling(30).std()
            z = (r1 / vol).values
            prof = (df["regime"] == "unknown").values
            fc = df["forecast"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            day = pd.to_datetime(df["timestamp"]).dt.floor("D").values
            for h in [1, 2, 3, 5, 10]:
                m, s = drift[(coin, h)]
                for i in range(0, len(c) - h, h):
                    if prof[i] and np.isfinite(z[i]):
                        um = -(c[i + h] / c[i] - 1 - m)
                        rows.append(dict(coin=coin, w=w, yr=yr[i], day=day[i], h=h, z=z[i], fc=fc[i],
                                         up=z[i] > 0, um=um, st=um / s, tot=-(c[i + h] / c[i] - 1)))
    d = pd.DataFrame(rows)

    def ct(g):
        s = g.groupby("day")["um"].sum()
        n = len(g); G = len(s)
        if G < 3: return np.nan
        mean = g["um"].mean()
        dev = g.groupby("day")["um"].apply(lambda x: (x - mean).sum())
        se = np.sqrt(G / (G - 1) * (dev ** 2).sum()) / n
        return mean / se

    def summ(g):
        return pd.Series(dict(n=len(g), days=g["day"].nunique(), um=g["um"].mean(),
                              strength=g["st"].mean(), t=ct(g)))

    up = d[d.up]
    out["up days in profile by horizon"] = up.groupby("h").apply(summ)
    out["down days in profile by horizon (short sign)"] = d[~d.up].groupby("h").apply(summ)
    u3 = up[up.h == 3].copy()
    u3["zbin"] = pd.qcut(u3["z"], 4, labels=["q1", "q2", "q3", "q4"])
    out["h3 up by z quartile"] = u3.groupby("zbin").apply(summ)
    out["h3 up by coin"] = u3.groupby("coin").apply(summ)
    out["h3 up by year"] = u3.groupby("yr").apply(summ)
    u1 = up[up.h == 1].copy()
    u1["zbin"] = pd.qcut(u1["z"], 4, labels=["q1", "q2", "q3", "q4"])
    out["h1 up by z quartile"] = u1.groupby("zbin").apply(summ)
    u5 = up[up.h == 5].copy()
    u5["zbin"] = pd.qcut(u5["z"], 4, labels=["q1", "q2", "q3", "q4"])
    out["h5 up by z quartile"] = u5.groupby("zbin").apply(summ)
    out["h3 z quartile edges"] = u3["z"].quantile([0.25, 0.5, 0.75])
    return out
