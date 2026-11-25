def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; out = {}
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float); n = len(df)
            r1 = c.pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            prevlow = c.shift(1).rolling(30, min_periods=30).min()
            prevhigh = c.shift(1).rolling(30, min_periods=30).max()
            ret5 = c / c.shift(5) - 1
            ret10 = c / c.shift(10) - 1
            ts = pd.to_datetime(df["timestamp"], utc=True)
            wn = int(w[1:])
            for h in (1, 3):
                fwd = c.shift(-h) / c - 1
                for i in range(0, n - h, h):
                    v = vol30[i]
                    rows.append(dict(coin=coin, w=w, half="early" if wn <= 12 else "late", h=h, fwd=fwd[i],
                                     day=ts[i].floor("D"), r1z=r1[i] / v if v > 0 else np.nan,
                                     newlow=bool(c[i] < prevlow[i]) if prevlow[i] == prevlow[i] else np.nan,
                                     newhigh=bool(c[i] > prevhigh[i]) if prevhigh[i] == prevhigh[i] else np.nan,
                                     ret5z=ret5[i] / (v * np.sqrt(5)) if v > 0 else np.nan,
                                     ret10z=ret10[i] / (v * np.sqrt(10)) if v > 0 else np.nan,
                                     prof="outside" if df["regime"].iloc[i] == "chop" else "fallagit",
                                     wd=ts[i].dayofweek))
    S = pd.DataFrame(rows).dropna(subset=["fwd"])
    drift = {h: S[S.h == h].groupby("coin").fwd.mean() for h in (1, 3)}
    S["u"] = S.fwd - S.apply(lambda r: drift[r.h][r.coin], axis=1)
    def ct(g):
        g = g.dropna(subset=["u"])
        if len(g) < 3: return pd.Series({"n": len(g), "days": np.nan, "mean%": np.nan, "t_day": np.nan})
        m = g.u.mean(); d = (g.u - m).groupby(g.day).sum(); D = len(d)
        se = np.sqrt((d ** 2).sum() * D / max(D - 1, 1)) / len(g)
        return pd.Series({"n": len(g), "days": D, "mean%": 100 * m, "t_day": m / se if se > 0 else np.nan})
    S3 = S[S.h == 3].copy(); S1 = S[S.h == 1].copy()
    S3["r5q"] = pd.qcut(S3.ret5z, 5, labels=False)
    out["A 3d unusual by 5d-ret z quintile (day-clustered)"] = S3.groupby("r5q").apply(ct)
    out["B 5dz quintile x half"] = S3.groupby(["half", "r5q"]).apply(ct)
    out["C 5dz quintile x prof"] = S3.groupby(["prof", "r5q"]).apply(ct)
    top = S3[S3.r5q == 4]
    out["D top 5dz quintile by coin"] = top.groupby("coin").apply(ct)
    S3["r10q"] = pd.qcut(S3.ret10z, 5, labels=False)
    out["E 3d by 10d-ret z quintile"] = S3.groupby("r10q").apply(ct)
    fa = S3[S3.prof == "fallagit"].copy()
    fa["r1zq"] = pd.qcut(fa.r1z, 4, labels=False)
    out["F fallagit 1d-move z quartile x newlow"] = fa.groupby(["newlow", "r1zq"]).apply(ct)
    out["G fallagit newlow x half"] = fa.groupby(["half", "newlow"]).apply(ct)
    out["H outside newhigh x half"] = S3[S3.prof == "outside"].groupby(["half", "newhigh"]).apply(ct)
    out["I 1d unusual by weekday"] = S1.groupby("wd").apply(ct)
    out["J weekday Thu+Fri x half"] = S1.assign(tf=S1.wd.isin([3, 4])).groupby(["half", "tf"]).apply(ct)
    # graded slope: corr of ret5z with u, by coin
    out["K corr ret5z vs 3d unusual by coin"] = S3.dropna(subset=["ret5z", "u"]).groupby("coin").apply(lambda g: pd.Series({"n": len(g), "corr": g.ret5z.corr(g.u)}))
    return out
