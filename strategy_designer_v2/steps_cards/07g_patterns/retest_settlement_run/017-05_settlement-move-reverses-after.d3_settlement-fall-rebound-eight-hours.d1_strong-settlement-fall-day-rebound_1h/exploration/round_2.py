def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allg = {h: [] for h in (24, 72)}
        for w, df in wins.items():
            c = df["close"].values
            for h in (24, 72):
                idx = np.arange(0, len(c) - h, h)
                allg[h].append(c[idx + h] / c[idx] - 1)
        drift = {h: np.concatenate(allg[h]).mean() for h in allg}
        sd24 = np.concatenate(allg[24]).std()
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            c = d["close"].astype(float)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            r1 = c.pct_change()
            r24 = c / c.shift(24) - 1
            z24 = r24 / r24.abs().rolling(720, min_periods=200).mean()
            r72 = c / c.shift(72) - 1
            z72 = r72 / r72.abs().rolling(720, min_periods=200).mean()
            vrel = r1.rolling(168).std() / r1.rolling(720).std()
            rows.append(pd.DataFrame({"coin": coin, "w": w, "wnum": int(w[1:]),
                "hour": ts.dt.hour.values, "wd": ts.dt.weekday.values, "year": ts.dt.year.values,
                "z24": z24, "z72": z72, "vrel": vrel,
                "f24": c.shift(-24) / c - 1 - drift[24], "f72": c.shift(-72) / c - 1 - drift[72],
                "nxt1": c.shift(-1) / c - 1, "sd24": sd24, "pos": np.arange(len(d))}))
    A = pd.concat(rows, ignore_index=True)
    out = {}

    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean_bp": x.mean() * 1e4,
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    G = A[A.pos % 24 == 0].dropna(subset=["f24", "z24"]).copy()
    G["dec"] = pd.qcut(G.z24, 10, labels=False)
    out["grid24: f24 by z24 decile"] = G.groupby("dec")["f24"].apply(tt).unstack().round(3)
    lo = G[G.dec <= 1].copy()
    lo["str"] = lo.f24 / lo.sd24
    out["bottom 2 deciles z24: by coin"] = lo.groupby("coin")["f24"].apply(tt).unstack().round(3)
    out["bottom 2 deciles z24: by window third"] = lo.groupby(pd.cut(lo.wnum, [0, 8, 16, 24]))["f24"].apply(tt).unstack().round(3)
    out["bottom 2 deciles z24: strength mean"] = float(lo.str.mean())
    out["bottom 2 deciles z24: by vol-ratio half"] = lo.dropna(subset=["vrel"]).groupby(
        lo.vrel > lo.vrel.median())["f24"].apply(tt).unstack().round(3)
    out["spearman z24 vs f24 (grid), negative z24 only"] = float(stats.spearmanr(G[G.z24 < 0].z24, G[G.z24 < 0].f24).correlation)
    out["spearman z24 vs f24 (grid), positive z24 only"] = float(stats.spearmanr(G[G.z24 > 0].z24, G[G.z24 > 0].f24).correlation)

    G3 = A[A.pos % 72 == 0].dropna(subset=["f72", "z72"]).copy()
    out["grid72: f72 by z72 quintile"] = G3.groupby(pd.qcut(G3.z72, 5, labels=False))["f72"].apply(tt).unstack().round(3)

    H = A[A.hour.isin([21, 22])]
    out["hour21-22 bar next1 by coin"] = H.groupby("coin")["nxt1"].apply(tt).unstack().round(3)
    out["hour21-22 bar next1 by year"] = H.groupby("year")["nxt1"].apply(tt).unstack().round(3)
    out["hour21-22 bar next1 by weekday"] = H.groupby("wd")["nxt1"].apply(tt).unstack().round(3)
    # 2-hour block 21:00-23:00 as one return, per day
    A["r2blk"] = np.nan
    blk = A[A.hour == 21].index
    nx = blk + 1
    ok = (nx < len(A))
    blk = blk[ok]; nx = nx[ok]
    same = (A.loc[nx, "coin"].values == A.loc[blk, "coin"].values) & (A.loc[nx, "w"].values == A.loc[blk, "w"].values) & (A.loc[nx, "hour"].values == 22)
    two = (1 + A.loc[blk, "nxt1"].values) * (1 + A.loc[nx, "nxt1"].values) - 1
    two = pd.Series(two[same])
    out["21-23 UTC two-hour return per day"] = tt(two).round(3)
    out["21-23 share positive"] = float((two > 0).mean())

    Fr = G.groupby(["wd"])["f24"].apply(tt).unstack()
    out["grid24 by weekday x year: friday mean bp by year"] = G[G.wd == 4].groupby("year")["f24"].apply(tt).unstack().round(3)
    return out
