def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    def grid_cases(h):
        rows = []
        for coin, ws in bars.items():
            allr = []
            for w, df in ws.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    allr.append(c[i + h] / c[i] - 1)
            drift = np.mean(allr) if allr else np.nan
            sd = np.std(allr, ddof=1) if len(allr) > 1 else np.nan
            for w, df in ws.items():
                c = df["close"].values
                f = df["forecast"].values
                ts = pd.to_datetime(df["timestamp"]).values
                for i in range(0, len(c) - h, h):
                    if f[i] == 0 or np.isnan(f[i]):
                        continue
                    r = c[i + h] / c[i] - 1
                    rows.append(dict(coin=coin, window=w, day=str(ts[i])[:10],
                                     year=str(ts[i])[:4], f=f[i], r=r,
                                     ex=r - drift, usual=sd))
        return pd.DataFrame(rows)

    def tday(d, col):
        n = len(d)
        if n < 2: return d[col].mean(), np.nan, d["day"].nunique()
        m = d[col].mean()
        gd = (d[col] - m).groupby(d["day"]).sum()
        se = np.sqrt((gd ** 2).sum()) / n
        return m, (m / se if se > 0 else np.nan), d["day"].nunique()

    def summ(g):
        m, t, nd = tday(g, "ex")
        g = g.assign(prod=g["f"] / 10 * g["ex"])
        mp, tp, _ = tday(g, "prod")
        return pd.Series(dict(n=len(g), days=nd, mean_ex=m, t_ex=t, mean_r=g["r"].mean(),
                              mean_prod=mp, t_prod=tp, share_down=(g["ex"] < 0).mean(),
                              strength=(g["ex"] / g["usual"]).mean()))
    d = grid_cases(40)
    s = d[d.f < 0]
    out["h40 short by year"] = s.groupby("year").apply(summ)
    out["h40 short by window"] = s.groupby("window").apply(summ)
    out["h40 short by coin"] = s.groupby("coin").apply(summ)
    out["h40 short by tercile of f"] = s.groupby(pd.qcut(s["f"], 3, duplicates="drop"), observed=True).apply(summ)
    hz = []
    for h in [15, 30, 40, 50, 70]:
        dd = grid_cases(h)
        sub = dd[dd.f < 0]
        r = summ(sub); r["h"] = h; hz.append(r)
        sub2 = dd[dd.f <= -2]
        if len(sub2) > 2:
            r2 = summ(sub2); r2["h"] = -h; hz.append(r2)
    out["short across horizons (neg h = f<=-2)"] = pd.DataFrame(hz)
    # all bars (daily, overlapping not used for t) of short: share of windows
    out["share of active nonzero bars short"] = float(np.mean([ (df["forecast"] < 0).sum() for ws in bars.values() for df in ws.values()]) /
                                                     np.mean([ (df["forecast"] != 0).sum() for ws in bars.values() for df in ws.values()]))
    return out
