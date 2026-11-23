def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        g = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 48, 48)
            g.extend(c[idx + 48] / c[idx] - 1)
        g = np.array(g); m48, s48 = g.mean(), g.std(ddof=1)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            c = df["close"]
            r24 = c / c.shift(24) - 1
            z24 = r24 / r24.abs().rolling(720, min_periods=360).mean()
            r48 = c / c.shift(48) - 1
            z48 = r48 / r48.abs().rolling(720, min_periods=360).mean()
            for i in np.where((ts.dt.hour == 23).values)[0]:
                if i + 48 >= len(c) or np.isnan(z24.iloc[i]):
                    continue
                f = c.iloc[i + 48] / c.iloc[i] - 1
                rows.append({"coin": coin, "year": ts.iloc[i].year, "dow": ts.iloc[i].dayofweek,
                             "z24": z24.iloc[i], "z48": z48.iloc[i],
                             "fx": f - m48, "fs": (f - m48) / s48})
    d = pd.DataFrame(rows)
    def summ(g, col="z24"):
        x = -np.sign(g[col]) * g["fx"]
        return pd.Series({"n": len(x), "rev_mean%": 100 * x.mean(),
                          "t": x.mean() / (x.std(ddof=1) / np.sqrt(len(x))),
                          "strength": (-np.sign(g[col]) * g["fs"]).mean()})
    def slope(g, col):
        zz = g[col].clip(-4, 4); y = g["fx"]
        b = np.polyfit(zz, y, 1)[0]
        res = y - np.polyval(np.polyfit(zz, y, 1), zz)
        se = np.sqrt((res**2).sum() / (len(y) - 2) / ((zz - zz.mean())**2).sum())
        return pd.Series({"n": len(y), "slope%perz": 100 * b, "t": b / se})
    out = {}
    sun = d[d.dow == 6].copy()
    sun["q"] = pd.qcut(sun.z24.abs(), 5, labels=False)
    out["sun24_rev_by_quintile"] = sun.groupby("q").apply(summ)
    out["sun24_rev_by_coin"] = sun.groupby("coin").apply(summ)
    out["sun24_rev_by_year"] = sun.groupby("year").apply(summ)
    sun["side"] = np.where(sun.z24 > 0, "up", "down")
    out["sun24_rev_by_side"] = sun.groupby("side").apply(summ)
    out["slope_z24_by_dow"] = d.groupby("dow").apply(lambda g: slope(g, "z24"))
    out["slope_z48_by_dow"] = d.groupby("dow").apply(lambda g: slope(g, "z48"))
    sun["q2"] = pd.qcut(sun.z48.abs(), 5, labels=False)
    out["weekend48_rev_by_quintile"] = sun.groupby("q2").apply(lambda g: summ(g, "z48"))
    out["weekend48_rev_all"] = summ(sun, "z48")
    return out
