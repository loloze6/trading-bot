def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            sig = r1.rolling(720, min_periods=360).std()
            vr = v / v.rolling(720, min_periods=360).mean()
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            for h in (2, 6, 24):
                idx = np.arange(0, n - h, h)
                fr = (c.shift(-h) / c - 1).values[idx]
                rows.append(pd.DataFrame({"coin": coin, "w": w, "h": h, "z": (r1/sig).values[idx], "vr": vr.values[idx],
                    "sig": sig.values[idx], "fr": fr, "wd": ts.dt.weekday.values[idx], "year": ts.dt.year.values[idx],
                    "m24": ((c / c.shift(24) - 1)/(sig*np.sqrt(24))).values[idx],
                    "m72": ((c / c.shift(72) - 1)/(sig*np.sqrt(72))).values[idx],
                    "m6": ((c / c.shift(6) - 1)/(sig*np.sqrt(6))).values[idx]}))
    df = pd.concat(rows).dropna()
    df["ur"] = df["fr"] - df.groupby(["coin","h"])["fr"].transform("mean")
    df["uz"] = df["ur"] / (df["sig"]*np.sqrt(df["h"]))
    def summ(g):
        return pd.Series({"n": len(g), "mean_ur_%": g.ur.mean()*100, "t": g.ur.mean()/(g.ur.std()/np.sqrt(len(g))), "strength": g.uz.mean()})
    # graded reversal: regression of uz on -m24 at h24, by coin and year
    d = df[df.h==24].copy()
    def slope(g):
        r = stats.linregress(g.m24, g.uz)
        return pd.Series({"n": len(g), "slope": r.slope, "t": r.slope/r.stderr, "corr": r.rvalue})
    out["h24 uz on m24 by coin"] = d.groupby("coin").apply(slope)
    out["h24 uz on m24 by year"] = d.groupby("year").apply(slope)
    out["h24 uz on m24 all"] = slope(d).to_frame().T
    out["h24 uz on m72 all"] = d.assign(m24=d.m72).pipe(slope).to_frame().T
    out["h24 uz on m6 all"] = d.assign(m24=d.m6).pipe(slope).to_frame().T
    d["q"] = pd.qcut(d.m24, 5, labels=False)
    out["h24 m24 quintile by coin (bottom-top mean_ur%)"] = d.groupby(["coin","q"]).ur.mean().unstack()*100
    # down hour heavy volume, h2: graded on -z*vr
    d2 = df[(df.h==2)].copy()
    dn = d2[d2.z < -2.5]
    dn["s"] = -dn.z * dn.vr
    out["h2 down>2.5sd graded"] = slope(dn.assign(m24=dn.s)).to_frame().T
    out["h2 down>2.5sd by coin"] = dn.groupby("coin").apply(summ)
    out["h2 down>2.5sd by year"] = dn.groupby("year").apply(summ)
    up = d2[d2.z > 2.5]
    out["h2 up>2.5sd all"] = summ(up).to_frame().T
    # friday
    out["h24 weekday4 by year"] = d[d.wd==4].groupby("year").apply(summ)
    out["h24 weekday4 by coin"] = d[d.wd==4].groupby("coin").apply(summ)
    # book: trade outcomes by entry forecast quintile
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    tr = pd.concat(tr)
    tr["fq"] = pd.qcut(tr.entry_forecast.rank(method="first"), 5, labels=False)
    out["trades by entry forecast quintile"] = tr.groupby("fq").agg(n=("net_profit_loss_percent","size"), gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"), fc=("entry_forecast","mean"))
    return out
