def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            up = (c.diff() > 0).astype(float)
            share = (v*up).rolling(20).sum() / v.rolling(20).sum()
            ret1 = c.pct_change()
            r20 = c / c.shift(20) - 1
            inprof = (b["regime"] == "unknown")
            yr = pd.to_datetime(b["timestamp"]).dt.year
            n = len(b)
            for h in (2, 5, 10, 20):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, year=yr[i], inprof=bool(inprof[i]),
                                     share=share[i], fc=b["forecast"].iloc[i], r20=r20[i],
                                     ret=c[i+h]/c[i]-1))
    df = pd.DataFrame(rows).dropna(subset=["share", "ret"])
    df["ret_adj"] = df["ret"] - df.groupby(["coin", "h"])["ret"].transform("mean")
    out = {}
    res = []
    for (h, ip), g in df.groupby(["h", "inprof"]):
        s = stats.linregress(g["share"], g["ret_adj"])
        res.append(dict(h=h, inprof=ip, n=len(g), slope=s.slope, t=s.slope/s.stderr,
                        corr=g[["share", "ret_adj"]].corr().iloc[0, 1]))
    out["slope share by horizon and profile"] = pd.DataFrame(res)
    g5 = df[(df.h == 5) & df.inprof].copy()
    g5["q"] = pd.qcut(g5["share"], 4, labels=False)
    out["in-profile h5 by share quartile"] = g5.groupby("q").agg(n=("ret_adj", "size"), share=("share", "mean"),
        mean=("ret_adj", "mean"), sd=("ret_adj", "std"))
    g20 = df[(df.h == 20) & df.inprof].copy()
    g20["q"] = pd.qcut(g20["share"], 3, labels=False)
    out["in-profile h20 by share tercile"] = g20.groupby("q").agg(n=("ret_adj", "size"), mean=("ret_adj", "mean"))
    res = []
    for (coin), g in g5.groupby("coin"):
        s = stats.linregress(g["share"], g["ret_adj"])
        res.append(dict(coin=coin, n=len(g), slope=s.slope, t=s.slope/s.stderr))
    out["in-profile h5 by coin"] = pd.DataFrame(res)
    res = []
    for (y), g in g5.groupby("year"):
        if len(g) > 10:
            s = stats.linregress(g["share"], g["ret_adj"])
            res.append(dict(year=y, n=len(g), slope=s.slope, t=s.slope/s.stderr))
    out["in-profile h5 by year"] = pd.DataFrame(res)
    # interaction with 20d return: share residual vs price
    g5["r20q"] = pd.qcut(g5["r20"], 3, labels=False)
    res = []
    for q, g in g5.groupby("r20q"):
        s = stats.linregress(g["share"], g["ret_adj"])
        res.append(dict(r20q=q, r20=g.r20.mean(), n=len(g), mean=g.ret_adj.mean(), slope=s.slope, t=s.slope/s.stderr))
    out["in-profile h5 by 20d return tercile"] = pd.DataFrame(res)
    s = stats.linregress(g5["r20"], g5["ret_adj"])
    out["in-profile h5 slope on 20d return"] = pd.Series(dict(slope=s.slope, t=s.slope/s.stderr, n=len(g5)))
    out["share in-profile summary"] = g5["share"].describe()
    return out
