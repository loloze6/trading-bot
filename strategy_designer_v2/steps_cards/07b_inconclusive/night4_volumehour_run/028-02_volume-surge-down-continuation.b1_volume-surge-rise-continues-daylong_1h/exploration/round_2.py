def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    H = [2, 6, 12, 24]
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
            # causal case definitions: first qualifying bar in each 24-bar cell
            defs = {
                "fc>=2 long": (fc >= 2, 1),
                "z>=2 long": (z >= 2, 1),
                "z<=-2 short": (z <= -2, -1),
            }
            for name, (cond, side) in defs.items():
                cond = np.nan_to_num(cond.astype(float)) > 0
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
                        rows.append(dict(case=name, coin=coin, year=yr[t], h=h, side=side,
                                         z=abs(z[t]), v=v[t], fc=fc[t],
                                         unusual=side * (fr - d), strength=side * (fr - d) / s))
    R = pd.DataFrame(rows)
    def summ(g):
        x = g["unusual"]
        return pd.Series(dict(n=len(x), mean_pct=100 * x.mean(),
                              t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                              strength=g["strength"].mean()))
    out["by case and h"] = R.groupby(["case", "h"]).apply(summ)
    F = R[R.case == "fc>=2 long"].copy()
    F["fq"] = F.groupby("h")["fc"].transform(lambda s: pd.qcut(s.rank(method="first"), 4, labels=False))
    out["fc cases by h, forecast quartile"] = F.groupby(["h", "fq"]).apply(summ)
    F["vbin"] = pd.cut(F["v"], [0, 1, 2, 4, 1e6], labels=["v<1", "1-2", "2-4", ">4"])
    out["fc cases h24/h6 by vol bin"] = F[F.h.isin([6, 24])].groupby(["h", "vbin"]).apply(summ)
    out["fc cases h24 by coin"] = F[F.h == 24].groupby("coin").apply(summ)
    out["fc cases h24 by year"] = F[F.h == 24].groupby("year").apply(summ)
    Z = R[R.case != "fc>=2 long"].copy()
    Z["vbin"] = pd.cut(Z["v"], [0, 1, 2, 4, 1e6], labels=["v<1", "1-2", "2-4", ">4"])
    out["z cases by case,h(6,24),vol bin"] = Z[Z.h.isin([6, 24])].groupby(["case", "h", "vbin"]).apply(summ)
    return out
