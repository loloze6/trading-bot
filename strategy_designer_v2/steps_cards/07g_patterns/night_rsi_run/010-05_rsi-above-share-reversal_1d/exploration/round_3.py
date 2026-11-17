import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    L = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change(); vol20 = r1.rolling(20).std()
            vol60 = r1.rolling(60).std()
            yr = pd.to_datetime(b["timestamp"]).dt.year
            n = len(b)
            for i in range(0, n - 1):
                L.append(dict(coin=coin, win=w, yr=yr.iloc[i], r0=r1.iloc[i], vol=vol20.iloc[i],
                              vrel=vol20.iloc[i]/vol60.iloc[i] if vol60.iloc[i] > 0 else np.nan,
                              fwd=c.iloc[i+1]/c.iloc[i]-1,
                              fwd2=(c.iloc[i+2]/c.iloc[i+1]-1) if i+2 < n else np.nan))
    g = pd.DataFrame(L).dropna(subset=["r0", "vol", "fwd"])
    g["z"] = g.r0 / g.vol
    g["d"] = g.fwd - g.groupby("coin")["fwd"].transform("mean")
    g["vq"] = g.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False))
    hi = g[g.vq == 2]
    def tz(dd, y="d", x="z"):
        dd = dd.dropna(subset=[x, y])
        s = stats.linregress(dd[x], dd[y]); return pd.Series(dict(slope=s.slope, t=s.slope/s.stderr, n=len(dd)))
    out["hi_by_coin"] = hi.groupby("coin").apply(tz)
    out["hi_by_year"] = hi.groupby("yr").apply(tz)
    out["lo_by_coin"] = g[g.vq == 0].groupby("coin").apply(tz)
    # graded within high vol: by |z| sign quintiles
    hh = hi.copy(); hh["zq"] = pd.qcut(hh.z, 5, labels=False)
    t = hh.groupby("zq").agg(n=("d","size"), z=("z","mean"), m=("d","mean"), sd=("d","std"))
    t["t"] = t.m/(t.sd/np.sqrt(t.n)); out["hi_by_zq"] = t.drop(columns="sd")
    # raw return instead of z in high vol
    out["hi_raw_r0"] = tz(hi, x="r0")
    # second day after
    g["d2"] = g.fwd2 - g.groupby("coin")["fwd2"].transform("mean")
    out["hi_day2"] = tz(g[g.vq == 2], y="d2")
    # interaction with relative vol
    gg = g.dropna(subset=["vrel"]).copy()
    gg["rq"] = pd.qcut(gg.vrel, 3, labels=False)
    out["by_relvol_terc"] = gg.groupby("rq").apply(tz)
    return out
