def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    H = [6, 12, 24, 48]
    drift = {}
    for coin in bars:
        for h in H:
            rs = []
            for w, df in bars[coin].items():
                c = df["close"].values.astype(float)
                idx = np.arange(0, len(c) - h, h)
                rs.append(c[idx + h] / c[idx] - 1)
            rs = np.concatenate(rs)
            drift[(coin, h)] = (rs.mean(), rs.std())
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            c = df["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(720, min_periods=240).std().shift(1)
            mv = df["volume"].astype(float).rolling(720, min_periods=240).mean().shift(1)
            z = (r / sd).values
            v = (df["volume"].astype(float) / mv).values
            fc = df["forecast"].values.astype(float)
            ts = pd.to_datetime(df["timestamp"])
            yr = ts.dt.year.values
            cv = c.values
            n = len(cv)
            cond = np.nan_to_num((z >= 2).astype(float)) > 0
            for start in range(0, n, 24):
                hits = np.where(cond[start:start + 24])[0]
                if len(hits) == 0:
                    continue
                t = start + hits[0]
                for h in H:
                    if t + h >= n:
                        continue
                    d, s = drift[(coin, h)]
                    fr = cv[t + h] / cv[t] - 1
                    rows.append(dict(coin=coin, w=w, year=yr[t], h=h, z=z[t], v=v[t], prod=z[t] * v[t],
                                     fc=fc[t], unusual=fr - d, total=fr, strength=(fr - d) / s))
    R = pd.DataFrame(rows)
    def summ(g):
        x = g["unusual"]
        return pd.Series(dict(n=len(x), mean_pct=100 * x.mean(),
                              t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                              total_pct=100 * g["total"].mean(), strength=g["strength"].mean()))
    out["z>=2 long by h"] = R.groupby("h").apply(summ)
    R24 = R[R.h == 24].copy()
    R24["pq"] = pd.qcut(R24["prod"].rank(method="first"), 4, labels=False)
    out["h24 by product quartile"] = R24.groupby("pq").apply(summ)
    R24["zb"] = pd.cut(R24["z"], [2, 3, 5, 100], labels=["2-3", "3-5", ">5"])
    out["h24 by z bin"] = R24.groupby("zb").apply(summ)
    out["h24 by coin"] = R24.groupby("coin").apply(summ)
    out["h24 by year"] = R24.groupby("year").apply(summ)
    R24["fpos"] = np.where(R24["fc"] >= 2, "fc>=2", "fc<2")
    out["h24 by forecast on bar"] = R24.groupby("fpos").apply(summ)
    hi = R24[R24.pq >= 2]["unusual"]; lo = R24[R24.pq < 2]["unusual"]
    from scipy import stats
    out["h24 top half minus bottom half product (pct, welch t)"] = pd.Series(
        dict(diff_pct=100 * (hi.mean() - lo.mean()), t=stats.ttest_ind(hi, lo, equal_var=False).statistic))
    return out
