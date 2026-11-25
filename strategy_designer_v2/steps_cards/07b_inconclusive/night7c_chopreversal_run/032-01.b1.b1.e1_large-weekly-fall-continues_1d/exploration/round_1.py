def explore(data):
    import numpy as np, pandas as pd
    H = 7
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            r = c.pct_change()
            vol = r.rolling(30, min_periods=30).std(ddof=1)
            vsr = (c / c.shift(7) - 1) / (vol * np.sqrt(7))
            er = (c / c.shift(30) - 1).abs() / r.abs().rolling(30).sum()
            vol_rel = vol / vol.rolling(90, min_periods=30).median()
            n = len(c)
            for h in [3, 7, 14]:
                for p in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, year=ts[p].year, day=ts[p].normalize(), h=h,
                                     vsr=vsr[p], er=er[p], volrel=vol_rel[p],
                                     ret=c[p + h] / c[p] - 1, usual=np.nan))
    d = pd.DataFrame(rows)
    # drift and usual move per coin and horizon
    g = d.groupby(["coin", "h"])["ret"]
    d["drift"] = g.transform("mean"); d["usual"] = g.transform("std")
    d["unus"] = d["ret"] - d["drift"]
    d = d.dropna(subset=["vsr"])

    def ct(x):
        # mean and day-clustered t
        if len(x) < 3: return pd.Series(dict(n=len(x), mean=np.nan, t=np.nan, days=0))
        m = x["v"].mean()
        dev = (x["v"] - m).groupby(x["day"]).sum()
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / max(G - 1, 1)) / len(x)
        return pd.Series(dict(n=len(x), mean=m, t=m / se if se > 0 else np.nan, days=G))

    out = {}
    d7 = d[d.h == 7].copy()
    big = d7[d7.vsr <= -2].copy()
    big["v"] = -big["unus"]  # short side
    out["fall>=2 short-side unusual, all"] = ct(big).to_frame().T
    out["fall short-side by coin"] = big.groupby("coin").apply(ct)
    out["fall short-side by year"] = big.groupby("year").apply(ct)
    big["chop"] = np.where(big.er < d7.er.median(), "chop", "trend")
    out["fall short-side by chop"] = big.groupby("chop").apply(ct)
    big["agit"] = np.where(big.volrel > 1, "agitated", "calm")
    out["fall short-side by agitation"] = big.groupby("agit").apply(ct)
    # by depth bucket, all horizons
    d["bucket"] = pd.cut(d.vsr, [-99, -3, -2, -1, 1, 2, 3, 99])
    d["v"] = d["unus"]
    out["unusual (long side) by vsr bucket and horizon"] = d.groupby(["h", "bucket"]).apply(ct)
    # continuous slope: unusual/usual on vsr, by chop
    res = []
    d7 = d[d.h == 7].dropna(subset=["er"]).copy()
    med = d7.er.median()
    for lab, sub in [("all", d7), ("chop", d7[d7.er < med]), ("trend", d7[d7.er >= med]),
                     ("chop&agit", d7[(d7.er < med) & (d7.volrel > 1)])]:
        y = sub.unus / sub.usual; x = sub.vsr
        b = np.cov(x, y)[0, 1] / x.var()
        e = y - y.mean() - b * (x - x.mean())
        se = np.sqrt((e ** 2).sum() / (len(x) - 2) / ((x - x.mean()) ** 2).sum())
        res.append(dict(group=lab, n=len(x), slope=b, t=b / se, corr=np.corrcoef(x, y)[0, 1]))
    out["slope of 7d unusual/usual on vsr"] = pd.DataFrame(res)
    # rises side
    up = d[(d.h == 7) & (d.vsr >= 2)].copy(); up["v"] = -up["unus"]
    out["rise>=2 short-side (reversal) unusual"] = ct(up).to_frame().T
    return out
