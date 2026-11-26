def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for h in (7, 14, 28):
        for coin, wins in bars.items():
            recs = []
            for w, df in wins.items():
                df = df.reset_index(drop=True)
                c = df["close"].values; v = df["volume"].values; f = df["forecast"].values
                n = len(df)
                yr = pd.to_datetime(df["timestamp"]).dt.year.values
                for i in range(0, n - h, h):
                    r = c[i + h] / c[i] - 1
                    p14 = c[i] / c[i - 14] - 1 if i >= 14 else np.nan
                    p60 = c[i] / c[i - 60] - 1 if i >= 60 else np.nan
                    recs.append(dict(coin=coin, win=w, h=h, f=f[i], r=r, p14=p14, p60=p60,
                                     year=yr[i], day=str(df["timestamp"].iloc[i])[:10]))
            d = pd.DataFrame(recs)
            if len(d) == 0: continue
            d["x"] = d["r"] - d["r"].mean()
            d["sd"] = d["r"].std()
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)

    def stat(g):
        g = g[g.f > 0]
        if len(g) < 5: return pd.Series(dict(n=len(g)))
        wm = (g.f * g.x).sum() / g.f.sum()
        dd = g.assign(dev=g.f * (g.x - wm)).groupby("day")["dev"].sum()
        Dn = len(dd)
        se = np.sqrt((dd ** 2).sum() * Dn / max(Dn - 1, 1)) / g.f.sum()
        um = g.x.mean()
        du = g.groupby("day")["x"].sum()
        return pd.Series(dict(n=len(g), days=Dn, wmean=wm, t=wm / se, unusual=um,
                              strength=(g.x / g.sd).mean()))
    out = {}
    out["by_horizon"] = D.groupby("h").apply(stat)
    D14 = D[D.h == 14].copy()
    out["by_year"] = D14.groupby("year").apply(stat)
    out["by_coin"] = D14.groupby("coin").apply(stat)
    pos = D14[D14.f > 0].copy()
    pos["fq"] = pd.qcut(pos.f, 4, labels=False, duplicates="drop")
    out["by_forecast_quartile"] = pos.groupby("fq").apply(stat)
    pos["p14s"] = np.sign(pos.p14)
    out["by_past14_sign"] = pos.groupby("p14s").apply(stat)
    pos["p60q"] = pd.qcut(pos.p60, 3, labels=False, duplicates="drop")
    out["by_past60_tercile"] = pos.groupby("p60q").apply(stat)
    out["flat_cases_f0"] = D14[D14.f == 0].assign(f=1.0).pipe(stat)
    return out
