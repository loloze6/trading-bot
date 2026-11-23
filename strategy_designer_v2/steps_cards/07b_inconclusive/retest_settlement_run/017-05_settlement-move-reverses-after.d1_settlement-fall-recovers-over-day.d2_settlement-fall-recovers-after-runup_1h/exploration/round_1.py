def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    ctrl = []
    coin_mean = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            c = df["close"].values
            n = len(c)
            idx = np.arange(0, n - 24, 24)
            allr.extend(list(c[idx + 24] / c[idx] - 1))
        coin_mean[coin] = np.nanmean(allr)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            hr = ((ts + pd.Timedelta(hours=1)).dt.hour).values
            yr = ts.dt.year.values
            r2 = pd.Series(c).pct_change(2)
            fall = (-r2).clip(lower=0)
            scale = r2.abs().rolling(720).mean()
            sf = (fall / scale).values
            rise = pd.Series(c).pct_change(168).values
            fc = df["forecast"].values
            fwd = np.full(n, np.nan)
            fwd[:n - 24] = c[24:] / c[:n - 24] - 1
            vol = df["volume"].values
            volrel = (pd.Series(vol) / pd.Series(vol).rolling(720).median()).values
            cell = np.arange(n) // 24
            seen = set()
            for i in range(n):
                if np.isnan(fwd[i]):
                    continue
                if hr[i] in (0, 16) and fc[i] >= 2 and cell[i] not in seen:
                    seen.add(cell[i])
                    rows.append(dict(coin=coin, w=w, year=yr[i], hour=hr[i], fc=fc[i],
                                     ex=fwd[i] - coin_mean[coin], sf=sf[i], rise=rise[i]))
            # control: every hour, one per cell per hour, situation fall>0 & rise>0
            for h in range(24):
                m = (hr == h) & (sf > 0) & (rise > 0) & ~np.isnan(fwd)
                ii = np.where(m)[0]
                _, first = np.unique(cell[ii], return_index=True)
                ii = ii[first]
                for i in ii:
                    ctrl.append(dict(coin=coin, hour=h, ex=fwd[i] - coin_mean[coin],
                                     x=sf[i] * rise[i] * 100))
    d = pd.DataFrame(rows)
    out = {}
    med = d.fc.median()
    out["n, median fc, share at 20"] = pd.Series({"n": len(d), "median": med,
                                                  "share_fc>=19.99": (d.fc >= 19.99).mean(),
                                                  "share_fc<=med": (d.fc <= med).mean()})
    d["q"] = pd.qcut(d.fc.rank(method="first"), 5, labels=False)
    def summ(g):
        return pd.Series({"n": len(g), "mean_ex%": 100 * g.ex.mean(),
                          "t": g.ex.mean() / (g.ex.std() / np.sqrt(len(g))),
                          "mean_fc": g.fc.mean()})
    out["by fc quintile"] = d.groupby("q").apply(summ)
    out["by hour"] = d.groupby("hour").apply(summ)
    out["by coin"] = d.groupby("coin").apply(summ)
    out["by year"] = d.groupby("year").apply(summ)
    d["sfq"] = pd.qcut(d.sf.rank(method="first"), 4, labels=False)
    d["rq"] = pd.qcut(d.rise.rank(method="first"), 4, labels=False)
    out["by scaled-fall quartile"] = d.groupby("sfq").apply(summ)
    out["by 7d-rise quartile"] = d.groupby("rq").apply(summ)
    cd = pd.DataFrame(ctrl)
    def summ2(g):
        x = g.x / g.x.std()
        p = g.ex * x
        return pd.Series({"n": len(g), "mean_ex%": 100 * g.ex.mean(),
                          "t_ex": g.ex.mean() / (g.ex.std() / np.sqrt(len(g))),
                          "t_prod": p.mean() / (p.std() / np.sqrt(len(g))),
                          "corr": np.corrcoef(g.x, g.ex)[0, 1]})
    out["control all hours (fall>0 & rise>0)"] = cd.groupby("hour").apply(summ2)
    return out
