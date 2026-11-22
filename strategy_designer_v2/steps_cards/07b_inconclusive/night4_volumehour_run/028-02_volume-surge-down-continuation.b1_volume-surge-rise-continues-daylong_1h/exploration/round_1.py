def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    rows = []
    drift = {}
    for coin in bars:
        for h in [2, 6, 24]:
            rs = []
            for w, df in bars[coin].items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.append(c[idx + h] / c[idx] - 1)
            rs = np.concatenate(rs)
            drift[(coin, h)] = (rs.mean(), rs.std())
    for coin in bars:
        for w, df in bars[coin].items():
            c = df["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(720, min_periods=240).std().shift(1)
            mv = df["volume"].astype(float).rolling(720, min_periods=240).mean().shift(1)
            z = (r / sd).values
            v = (df["volume"].astype(float) / mv).values
            fc = df["forecast"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            hr = pd.to_datetime(df["timestamp"]).dt.hour.values
            cv = c.values
            n = len(cv)
            for h in [2, 6, 24]:
                d, s = drift[(coin, h)]
                for start in range(0, n - h, h):
                    seg = slice(start, start + h)
                    zz = z[seg]; vv = v[seg]
                    if np.all(np.isnan(zz)) or np.all(np.isnan(vv)):
                        continue
                    p = zz * vv
                    if np.all(np.isnan(p)):
                        continue
                    for side in [1, -1]:
                        ps = side * p
                        j = np.nanargmax(np.where(side * zz > 0, ps, -np.inf)) if np.any(side * zz > 0) else None
                        if j is None:
                            continue
                        t = start + j
                        if t + h >= n:
                            continue
                        fr = cv[t + h] / cv[t] - 1
                        rows.append(dict(coin=coin, w=w, year=yr[t], hour=hr[t], h=h, side=side,
                                         z=abs(z[t]), v=v[t], prod=ps[j], fc=fc[t],
                                         unusual=side * (fr - d), total=side * fr, strength=side * (fr - d) / s))
    R = pd.DataFrame(rows)
    def summ(g):
        x = g["unusual"]
        return pd.Series(dict(n=len(x), mean_pct=100 * x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                              strength=g["strength"].mean()))
    R["zbin"] = pd.cut(R["z"], [0, 1, 2, 3, 5, 100], labels=["z<1", "1-2", "2-3", "3-5", ">5"])
    R["vbin"] = pd.cut(R["v"], [0, 1, 2, 4, 1000], labels=["v<1", "1-2", "2-4", ">4"])
    big = R[R["z"] >= 2]
    out["big moves (|z|>=2) by h, side, vol bin"] = big.groupby(["h", "side", "vbin"]).apply(summ)
    out["all cell-max by h,side,zbin"] = R.groupby(["h", "side", "zbin"]).apply(summ)
    surge = R[(R["z"] >= 2) & (R["v"] >= 2)]
    out["surge (z>=2,v>=2) by h,side,coin"] = surge.groupby(["h", "side", "coin"]).apply(summ)
    out["surge by h,side,year"] = surge[surge.h.isin([6, 24])].groupby(["h", "side", "year"]).apply(summ)
    # recorded cases approx: forecast>=2 first per 24-cell
    c24 = R[(R.h == 24) & (R.side == 1) & (R.fc >= 2)]
    c24 = c24.copy(); c24["fq"] = pd.qcut(c24["fc"], 4, labels=False, duplicates="drop")
    out["h24 long, forecast>=2 by forecast quartile"] = c24.groupby("fq").apply(summ)
    out["h24 long, forecast>=2 by coin"] = c24.groupby("coin").apply(summ)
    return out
