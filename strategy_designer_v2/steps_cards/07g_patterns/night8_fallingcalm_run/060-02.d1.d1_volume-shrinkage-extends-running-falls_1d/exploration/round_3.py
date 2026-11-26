def explore(data):
    import numpy as np, pandas as pd
    out = {}
    H = 5
    drift = {}
    for coin, wins in data["bars"].items():
        rs = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            rs += list(c[idx + H] / c[idx] - 1)
        drift[coin] = np.mean(rs)
    drows = []; rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; v = b["volume"]
            r1 = c.pct_change()
            ret60 = c / c.shift(60) - 1
            ret20 = c / c.shift(20) - 1
            ret7 = c / c.shift(7) - 1
            sd30 = r1.rolling(30).std()
            vr = np.log(v.rolling(30).mean() / v.shift(30).rolling(30).mean())
            vd = np.log(v / v.rolling(30).mean().shift(1))
            ts = pd.to_datetime(b["timestamp"])
            fwd = c.shift(-H) / c - 1
            for i in range(len(b) - 1):
                drows.append(dict(coin=coin, w=w, yr=ts.iloc[i].year, wd=ts.iloc[i].weekday(), ret60=ret60.iloc[i],
                                  ret7=ret7.iloc[i], z1=r1.iloc[i]/sd30.iloc[i-1] if i > 0 and sd30.iloc[i-1] else np.nan,
                                  vd=vd.iloc[i], r=c.iloc[i+1]/c.iloc[i]-1))
            for i in range(0, len(b) - H, H):
                rows.append(dict(coin=coin, w=w, yr=ts.iloc[i].year, ret60=ret60.iloc[i], ret20=ret20.iloc[i], vr=vr.iloc[i],
                                 un=fwd.iloc[i]-drift[coin]))
    D = pd.DataFrame(drows).dropna(subset=["r"]); g = pd.DataFrame(rows)
    def summ(df, key, col):
        a = df.dropna(subset=[col]).groupby(key)[col]
        r = a.agg(["count", "mean"]); r["t"] = a.mean() / (a.std() / np.sqrt(a.count()))
        return r.round(4)
    F = D[D.ret60 < -0.10].copy()
    sat = F[F.wd == 5].copy()
    out["falling, Sat bar -> Sun return, by year"] = summ(sat, "yr", "r")
    out["falling, Sat bar -> Sun return, by coin"] = summ(sat, "coin", "r")
    sat["r60q"] = pd.qcut(sat.ret60, 3, labels=False)
    out["falling Sat bar: by ret60 tercile (0 deepest)"] = summ(sat, "r60q", "r")
    sat["r7q"] = pd.qcut(sat.ret7, 3, labels=False)
    out["falling Sat bar: by ret7 tercile"] = summ(sat, "r7q", "r")
    sat["vdq"] = pd.qcut(sat.vd, 3, labels=False)
    out["falling Sat bar: by day volume vs 30d tercile"] = summ(sat, "vdq", "r")
    nf = D[D.ret60 >= -0.10]
    out["not falling, Sat bar -> Sun return, by year"] = summ(nf[nf.wd == 5], "yr", "r")
    f = g[(g.ret60 < -0.1) & (g.ret20 < 0)].dropna(subset=["vr"]).copy()
    f["vrq"] = pd.qcut(f.vr, 3, labels=False)
    out["running fall lowest vr tercile by coin"] = summ(f[f.vrq == 0], "coin", "un")
    f["r20q"] = pd.qcut(f.ret20, 2, labels=False)
    out["running fall: ret20 half x vr tercile"] = summ(f, ["r20q", "vrq"], "un")
    return out
