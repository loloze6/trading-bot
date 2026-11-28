def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            up = (r1 > 0).astype(float); dn = (r1 < 0).astype(float)
            dvol = (v*dn).rolling(20).sum() / dn.rolling(20).sum().replace(0, np.nan)
            uvol = (v*up).rolling(20).sum() / up.rolling(20).sum().replace(0, np.nan)
            ratio = np.log(uvol / dvol)
            nup = up.rolling(20).sum()
            share = (v*up).rolling(20).sum() / v.rolling(20).sum()
            vtrend = np.log(v.rolling(10).mean() / v.rolling(60).mean())
            inprof = (b["regime"] == "unknown")
            yr = pd.to_datetime(b["timestamp"]).dt.year
            n = len(b)
            for h in (3, 5):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, year=yr[i], inprof=bool(inprof[i]),
                                     ratio=ratio[i], nup=nup[i], share=share[i], vtrend=vtrend[i],
                                     ret=c[i+h]/c[i]-1))
    df = pd.DataFrame(rows)
    df["ret_adj"] = df["ret"] - df.groupby(["coin", "h"])["ret"].transform("mean")
    out = {}
    def sl(g, x):
        g = g.dropna(subset=[x, "ret_adj"])
        if len(g) < 8: return dict(n=len(g), slope=np.nan, t=np.nan)
        s = stats.linregress(g[x], g["ret_adj"]); return dict(n=len(g), slope=s.slope, t=s.slope/s.stderr)
    ip = df[df.inprof]
    res = []
    for h in (3, 5):
        for coin, g in ip[ip.h == h].groupby("coin"):
            res.append(dict(h=h, coin=coin, **sl(g, "ratio")))
    out["ratio slope by coin, in profile"] = pd.DataFrame(res)
    res = []
    for h in (3, 5):
        for y, g in ip[ip.h == h].groupby("year"):
            res.append(dict(h=h, year=y, **sl(g, "ratio")))
    out["ratio slope by year, in profile"] = pd.DataFrame(res)
    res = []
    for h in (3, 5):
        res.append(dict(h=h, where="out", **sl(df[(~df.inprof) & (df.h == h)], "ratio")))
        res.append(dict(h=h, where="in, nup", **sl(ip[ip.h == h], "nup")))
    out["ratio out of profile, and up-day count in profile"] = pd.DataFrame(res)
    g = ip[ip.h == 3].dropna(subset=["ratio"]).copy()
    g["q"] = pd.qcut(g["ratio"], 4, labels=False)
    out["h3 in profile by ratio quartile"] = g.groupby("q").agg(n=("ret_adj", "size"), ratio=("ratio", "mean"),
        mean=("ret_adj", "mean"), sd=("ret_adj", "std"))
    res = []
    for h in (3, 5):
        for coin, g in ip[ip.h == h].groupby("coin"):
            res.append(dict(h=h, coin=coin, **sl(g, "vtrend")))
    out["vtrend slope by coin, in profile"] = pd.DataFrame(res)
    return out
