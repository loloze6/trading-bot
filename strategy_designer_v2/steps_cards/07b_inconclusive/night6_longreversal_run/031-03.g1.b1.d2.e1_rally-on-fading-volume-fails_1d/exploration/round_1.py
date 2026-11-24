def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [7, 14, 28]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        for h in H:
            rs = []
            for w, df in ws.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = (np.mean(rs), np.std(rs)) if rs else (np.nan, np.nan)
        for w, df in ws.items():
            c = df["close"].astype(float); v = df["volume"].astype(float)
            ret14 = c / c.shift(14) - 1
            ret60 = c / c.shift(60) - 1
            vr = v.rolling(14).mean() / v.rolling(30).mean() - 1
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            for h in H:
                for i in range(0, n - h, h):
                    if np.isnan(ret14.iloc[i]) or np.isnan(vr.iloc[i]):
                        continue
                    r = c.iloc[i + h] / c.iloc[i] - 1
                    d, s = drift[(coin, h)]
                    rows.append(dict(coin=coin, window=w, h=h, year=ts.iloc[i].year,
                                     day=ts.iloc[i].normalize(), ret14=ret14.iloc[i], ret60=ret60.iloc[i],
                                     vr=vr.iloc[i], ex=r - d, exz=(r - d) / s, f=df["forecast"].iloc[i]))
    X = pd.DataFrame(rows)

    def st(g, col="ex", sign=-1):
        if len(g) < 5:
            return pd.Series(dict(n=len(g), mean=np.nan, t=np.nan, days=np.nan))
        x = sign * g[col]
        dev = (x - x.mean()).groupby(g["day"]).sum()
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / max(G - 1, 1)) / len(x)
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / se if se > 0 else np.nan, days=G))

    out = {}
    up = X[(X.ret14 > 0)]
    sit = up[up.vr < 0]
    out["situation short-side by horizon"] = sit.groupby("h").apply(st)
    out["up14 rising-volume short-side by h"] = up[up.vr >= 0].groupby("h").apply(st)
    out["all up14 short-side by h"] = up.groupby("h").apply(st)
    s14 = sit[sit.h == 14].copy()
    s14["vrq"] = pd.qcut(s14.vr, 4, labels=["driest", "q2", "q3", "mildest"])
    out["sit h14 by vr quartile"] = s14.groupby("vrq").apply(st)
    s14["rq"] = pd.qcut(s14.ret14, 4, labels=["smallup", "q2", "q3", "bigup"])
    out["sit h14 by ret14 quartile"] = s14.groupby("rq").apply(st)
    out["sit h14 by year"] = s14.groupby("year").apply(st)
    out["sit h14 by coin"] = s14.groupby("coin").apply(st)
    s14["r60s"] = np.where(s14.ret60 > 0, "ret60 up", "ret60 down")
    out["sit h14 by ret60 sign"] = s14.dropna(subset=["ret60"]).groupby("r60s").apply(st)
    # brief's own: 60-day move, reversal over 28 days
    a = X[(X.h == 28)].dropna(subset=["ret60"]).copy()
    a["side"] = np.sign(a.ret60)
    a["rev"] = -a.side * a.ex
    a["z60"] = a.groupby("coin").ret60.transform(lambda s: (s - s.mean()) / s.std())
    a["zq"] = pd.qcut(a.z60, 5, labels=["bigdown", "q2", "q3", "q4", "bigup"])
    out["h28 excess (long dir) by ret60 quintile"] = a.groupby("zq").apply(lambda g: st(g, sign=1))
    s = X[X.h == 14].dropna(subset=["ret60"]).copy()
    s["z60"] = s.groupby("coin").ret60.transform(lambda q: (q - q.mean()) / q.std())
    s["zq"] = pd.qcut(s.z60, 5, labels=["bigdown", "q2", "q3", "q4", "bigup"])
    out["h14 excess (long dir) by ret60 quintile"] = s.groupby("zq").apply(lambda g: st(g, sign=1))
    return out
