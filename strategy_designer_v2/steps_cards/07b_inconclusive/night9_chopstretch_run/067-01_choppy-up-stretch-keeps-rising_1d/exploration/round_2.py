import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for h in [5, 7, 10]:
                for off in range(h):
                    idx = np.arange(off, len(df) - h, h)
                    for i in idx:
                        rows.append(dict(coin=coin, w=w, h=h, off=off, i=i, day=str(df["timestamp"].iloc[i])[:10],
                                         yr=yr.iloc[i], fc=df["forecast"].iloc[i],
                                         chop=df["regime"].iloc[i] != "chop",
                                         ret=c[i + h] / c[i] - 1))
    d = pd.DataFrame(rows)
    base = d[d.off == 0]
    drift = base.groupby(["coin", "h"])["ret"].mean().rename("drift")
    d = d.join(drift, on=["coin", "h"])
    d["ex"] = d["ret"] - d["drift"]
    a = d[d.chop & (d.fc != 0) & d.fc.notna()].copy()
    a["side"] = np.sign(a.fc)
    a["dirx"] = a.side * a.ex

    def daytstat(g):
        s = g.groupby("day")["dirx"].sum()
        nd = len(s); n = len(g)
        m = g["dirx"].mean()
        dev = (g["dirx"] - m).groupby(g["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / n
        return pd.Series(dict(n=n, days=nd, mean=m, t=m / se if se > 0 else np.nan))

    def slope(g):
        g = g.dropna(subset=["fc", "ex"])
        if len(g) < 10: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        s = stats.linregress(g.fc, g.ex)
        return pd.Series(dict(n=len(g), slope=s.slope, t=s.slope / s.stderr))

    out = {}
    a0 = a[a.off == 0]
    out["side mean by h (offset 0)"] = a0.groupby(["h", "side"]).apply(daytstat)
    out["side mean by h, mean over offsets"] = a.groupby(["h", "side", "off"]).apply(lambda g: g.dirx.mean()).groupby(["h", "side"]).agg(["mean", "min", "max", lambda x: (x > 0).mean()])
    sh = a[(a.side < 0)]
    out["short side slope on |fc| by h (all offsets pooled, naive t)"] = sh.assign(fc=-sh.fc, ex=-sh.ex).groupby("h").apply(slope)
    lo = a[(a.side > 0)]
    out["long side slope on fc by h (pooled)"] = lo.groupby("h").apply(slope)
    s5 = a0[(a0.h == 5) & (a0.side < 0)]
    out["h5 short by year"] = s5.groupby("yr").apply(daytstat)
    out["h5 short by coin"] = s5.groupby("coin").apply(daytstat)
    s5q = s5.copy(); s5q["q"] = pd.qcut(-s5q.fc, 3, labels=False)
    out["h5 short dirx by |fc| tercile"] = s5q.groupby("q").apply(daytstat)
    l5 = a0[(a0.h == 5) & (a0.side > 0)].copy(); l5["q"] = pd.qcut(l5.fc, 3, labels=False)
    out["h5 long dirx by fc tercile"] = l5.groupby("q").apply(daytstat)
    s10 = a0[(a0.h == 10) & (a0.side < 0)]
    out["h10 short by year"] = s10.groupby("yr").apply(daytstat)
    return out
