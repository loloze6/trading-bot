def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        allr = {h: [] for h in (1,3,5,10)}
        for w, df in ws.items():
            c = df["close"].values
            for h in allr:
                idx = np.arange(0, len(c)-h, h)
                allr[h].extend(list(c[idx+h]/c[idx]-1))
        drift[coin] = {h: np.mean(v) for h, v in allr.items()}
        drift[coin]["sd3"] = np.std(allr[3])
        for w, df in ws.items():
            c = df["close"].values.astype(float)
            r1 = pd.Series(c).pct_change()
            sd20 = r1.rolling(20).std()
            z = (r1/sd20).values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            for i in range(n):
                row = dict(coin=coin, w=w, i=i, year=ts.iloc[i].year,
                           inprof=(df["regime"].iloc[i]=="unknown"),
                           fc=df["forecast"].iloc[i], z=z[i], r1=r1.iloc[i], day=str(ts.iloc[i].date()))
                for h in (1,3,5,10):
                    row[f"f{h}"] = (c[i+h]/c[i]-1 - drift[coin][h]) if i+h < n else np.nan
                    row[f"g{h}"] = (i % h == 0)
                rows.append(row)
    d = pd.DataFrame(rows)
    out = {}
    out["profile share"] = d.groupby("coin")["inprof"].mean()
    p = d[d.inprof]
    def summ(g, h):
        g = g[g[f"g{h}"] & g[f"f{h}"].notna()]
        x = -g[f"f{h}"]  # fade beyond drift, positive = fade works
        ds = x.groupby(g["day"]).sum()
        t = ds.mean()/(ds.std()/np.sqrt(len(ds))) if len(ds) > 2 else np.nan
        return pd.Series({"n": len(g), "days": len(ds), "mean_fade%": 100*x.mean(), "t_day": t})
    # up days in profile by horizon
    res = {}
    up = p[p.z > 0]
    dn = p[p.z < 0]
    for h in (1,3,5,10):
        res[f"up h{h}"] = summ(up, h)
        res[f"down h{h}"] = summ(dn, h)
    out["fade by horizon, up vs down days (fade=-unusual)"] = pd.DataFrame(res).T
    # by z bins, h3 and h5
    bins = [-np.inf, -1, -0.5, 0, 0.5, 1, 1.5, 2, np.inf]
    for h in (3, 5):
        pp = p.copy(); pp["zb"] = pd.cut(pp.z, bins)
        out[f"by z bin h{h}"] = pp.groupby("zb", observed=True).apply(lambda g: summ(g, h))
    for h in (3,):
        out[f"up by coin h{h}"] = up.groupby("coin").apply(lambda g: summ(g, h))
        out[f"up by year h{h}"] = up.groupby("year").apply(lambda g: summ(g, h))
        out[f"up by window h{h}"] = up.groupby("w").apply(lambda g: summ(g, h))
    # slope of fade on z, up days, h3 grid
    g = up[up.g3 & up.f3.notna()]
    sl = stats.linregress(g.z, -g.f3)
    out["up h3 slope fade on z"] = f"slope {sl.slope:.5f} t {sl.slope/sl.stderr:.2f} n {len(g)}"
    # outside profile up days, h3, for comparison
    q = d[(~d.inprof) & (d.z > 0)]
    qq = q.copy(); qq["zb"] = pd.cut(qq.z, bins)
    out["outside profile up days by z h3"] = qq.groupby("zb", observed=True).apply(lambda g: summ(g, 3))
    return out
