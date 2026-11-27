def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        allr = {h: [] for h in (1,2,3)}
        for w, df in ws.items():
            c = df["close"].values
            for h in allr:
                idx = np.arange(0, len(c)-h, h)
                allr[h].extend(list(c[idx+h]/c[idx]-1))
        dr = {h: np.mean(v) for h, v in allr.items()}
        for w, df in ws.items():
            c = df["close"].values.astype(float)
            r1 = pd.Series(c).pct_change()
            z = (r1/r1.rolling(20).std()).values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            for i in range(n):
                row = dict(coin=coin, w=w, year=ts.iloc[i].year, inprof=(df["regime"].iloc[i]=="unknown"),
                           z=z[i], fc=df["forecast"].iloc[i], day=str(ts.iloc[i].date()))
                for h in (1,2,3):
                    row[f"f{h}"] = (c[i+h]/c[i]-1 - dr[h]) if i+h < n else np.nan
                    row[f"g{h}"] = (i % h == 0)
                rows.append(row)
    d = pd.DataFrame(rows)
    p = d[d.inprof]
    def summ(g, h):
        g = g[g[f"g{h}"] & g[f"f{h}"].notna()]
        x = -g[f"f{h}"]
        ds = x.groupby(g["day"]).sum()
        t = ds.mean()/(ds.std()/np.sqrt(len(ds))) if len(ds) > 2 else np.nan
        return pd.Series({"n": len(g), "days": len(ds), "mean_fade%": 100*x.mean(), "t_day": t})
    out = {}
    big = p[p.z > 1]
    res = {}
    for h in (1,2,3):
        res[f"z>1 h{h}"] = summ(big, h)
        res[f"0<z<=1 h{h}"] = summ(p[(p.z > 0) & (p.z <= 1)], h)
    out["big vs small rises by horizon"] = pd.DataFrame(res).T
    out["z>1 h3 by year"] = big.groupby("year").apply(lambda g: summ(g, 3))
    out["z>1 h3 by coin"] = big.groupby("coin").apply(lambda g: summ(g, 3))
    out["forecast<0 h3 by year"] = p[p.fc < 0].groupby("year").apply(lambda g: summ(g, 3))
    dn = p[p.z < 0]
    out["down days h3 by year (positive = further fall)"] = dn.groupby("year").apply(lambda g: summ(g, 3))
    g = p[(p.z > 0) & p.g1 & p.f1.notna()]
    sl = stats.linregress(g.z, -g.f1)
    out["up h1 slope"] = f"slope {sl.slope:.5f} t {sl.slope/sl.stderr:.2f} n {len(g)}"
    return out
