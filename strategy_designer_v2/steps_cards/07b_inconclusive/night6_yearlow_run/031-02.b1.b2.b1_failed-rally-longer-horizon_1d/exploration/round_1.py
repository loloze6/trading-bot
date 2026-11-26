def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    def grid_cases(h):
        rows = []
        for coin, ws in bars.items():
            # drift over all windows on grid h
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
        g = d.groupby("day")[col].sum()
        n = len(d)
        m = d[col].mean()
        dev = (d[col] - m)
        gd = dev.groupby(d["day"]).sum()
        se = np.sqrt((gd ** 2).sum()) / n
        return m, m / se if se > 0 else np.nan, len(g)

    d = grid_cases(40)
    d["prod"] = d["f"] / 10 * d["ex"]
    d["bin"] = pd.cut(d["f"], [-20, -3, -2, -1, -0.5, 0, 0.5, 1, 2, 20])
    def summ(g):
        m, t, nd = tday(g, "ex")
        mp, tp, _ = tday(g, "prod")
        return pd.Series(dict(n=len(g), days=nd, mean_ex=m, t_ex=t, mean_prod=mp, t_prod=tp, mean_f=g["f"].mean()))
    out["h40 by forecast bin"] = d.groupby("bin", observed=True).apply(summ)
    out["h40 by sign"] = d.groupby(np.sign(d["f"])).apply(summ)
    out["h40 by year"] = d.groupby("year").apply(summ)
    out["h40 by coin"] = d.groupby("coin").apply(summ)
    hz = []
    for h in [10, 20, 40, 60, 90]:
        dd = grid_cases(h)
        dd["prod"] = dd["f"] / 10 * dd["ex"]
        for name, sub in [("all", dd), ("short", dd[dd.f < 0]), ("long", dd[dd.f > 0]), ("f<=-2", dd[dd.f <= -2])]:
            if len(sub) < 3: continue
            m, t, nd = tday(sub, "ex"); mp, tp, _ = tday(sub, "prod")
            hz.append(dict(h=h, part=name, n=len(sub), days=nd, mean_ex=m, t_ex=t, mean_prod=mp, t_prod=tp))
    out["by horizon"] = pd.DataFrame(hz)
    # strength among short cases: correlation f vs ex
    s = d[d.f < 0]
    out["short cases spearman f vs ex"] = float(s[["f", "ex"]].corr(method="spearman").iloc[0, 1])
    out["forecast describe"] = d["f"].describe()
    return out
