def explore(data):
    import numpy as np, pandas as pd
    H = 18
    rows = []; hourrows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            v = b["volume"].astype(float).values
            n = len(c)
            if n < 200: continue
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            mabs = pd.Series(np.abs(r1)).rolling(180, min_periods=90).mean().values
            sl = np.zeros(n); sstart = np.zeros(n, dtype=int)
            for i in range(1, n):
                s = np.sign(r1[i])
                if i > 1 and np.sign(r1[i-1]) == s and s != 0:
                    sl[i] = sl[i-1] + s; sstart[i] = sstart[i-1]
                else:
                    sl[i] = s; sstart[i] = i - 1
            sgain = c / c[sstart] - 1
            r6 = np.r_[[np.nan]*6, c[6:]/c[:-6]-1]
            vrel = pd.Series(v).rolling(6).sum().values / pd.Series(v).rolling(180, min_periods=90).mean().values / 6
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, fwd=c[i+H]/c[i]-1, sl=sl[i],
                    sg=sgain[i]/mabs[i] if mabs[i] > 0 else np.nan,
                    m6=r6[i]/mabs[i] if mabs[i] > 0 else np.nan, vrel=vrel[i], yr=ts.iloc[i].year))
            for i in range(1, n - 1):
                hourrows.append((coin, ts.iloc[i].hour, ts.iloc[i].year, c[i+1]/c[i]-1))
    df = pd.DataFrame(rows).dropna()
    df["adj"] = df["fwd"] - df.groupby("coin")["fwd"].transform("mean")
    def st(g):
        return pd.Series(dict(count=len(g), mean=g.mean(), t=g.mean()/(g.std()/np.sqrt(len(g))) if len(g) > 2 else np.nan))
    res = {}
    df["vq"] = pd.qcut(df["vrel"].rank(method="first"), 5, labels=False)
    df["mside"] = np.where(df["m6"] > 0, "past1d up", "past1d down")
    res["volume quintile x past 1d sign"] = df.groupby(["mside", "vq"])["adj"].apply(st).unstack().round(5)
    res["volume quintile by year (top minus bottom)"] = df.groupby("yr").apply(lambda d: pd.Series(dict(
        n=len(d), top=d.loc[d.vq == 4, "adj"].mean(), bottom=d.loc[d.vq == 0, "adj"].mean()))).round(5)
    cm = df.groupby(["coin"]).apply(lambda d: d.loc[d.vq == 4, "adj"].mean() - d.loc[d.vq == 0, "adj"].mean())
    res["coins with top-bottom volume >0 share"] = float((cm > 0).mean())
    dn = df[df.sl < 0].copy()
    dn["q"] = pd.qcut(dn["sg"].rank(method="first"), 5, labels=False)
    res["largest down streak quintile by year"] = dn[dn.q == 0].groupby("yr")["adj"].apply(st).unstack().round(5)
    cm2 = dn[dn.q == 0].groupby("coin")["adj"].mean()
    res["coins with positive adj after largest down streaks share"] = float((cm2 > 0).mean())
    # regression: adj ~ m6 + vrel(log) for joint
    X = np.c_[np.ones(len(df)), df["m6"].clip(-15, 15), np.log(df["vrel"].clip(1e-3)), (df["sl"] < 0) * df["sg"].clip(-15, 0)]
    y = df["adj"].values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ beta; s2 = e @ e / (len(y) - X.shape[1])
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    res["joint OLS adj ~ m6 + log vrel + down streak loss"] = pd.DataFrame(dict(coef=beta, t=beta/se), index=["const", "m6", "logvrel", "dnloss"]).round(5)
    h = pd.DataFrame(hourrows, columns=["coin", "hour", "yr", "r"])
    h["a"] = h["r"] - h.groupby("coin")["r"].transform("mean")
    res["hour 16 bar by year"] = h[h.hour == 16].groupby("yr")["a"].apply(st).unstack().round(6)
    return res
