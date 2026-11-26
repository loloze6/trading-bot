def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            c = d["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            f1 = c.shift(-1) / c - 1
            d2 = c.shift(-2) / c.shift(-1) - 1
            calm = d["regime"].astype(str) != "chop"
            ts = pd.to_datetime(d["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(d)), "z": z, "calm": calm,
                                      "f1": f1, "d2": d2, "sd": sd, "day": ts.dt.floor("D"),
                                      "year": ts.dt.year, "wd": ts.dt.weekday}))
    A = pd.concat(rows, ignore_index=True)
    m1 = A.groupby("coin")["f1"].mean()
    A["exd2"] = A.d2 - A.coin.map(m1)
    A["sexd2"] = A.exd2 / A.sd
    S = A[(A.z > 0) & A.calm].dropna(subset=["z", "exd2"]).copy()
    S["zq"] = pd.qcut(S.z, 5, labels=False)
    out = {}
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x)))})
    def sl(x, y="exd2"):
        x = x.dropna(subset=["z", y])
        if len(x) < 10: return pd.Series({"n": len(x), "slope": np.nan, "t": np.nan})
        res = stats.linregress(x.z, x[y])
        return pd.Series({"n": len(x), "slope": res.slope, "t": res.slope/res.stderr})
    T = S[S.zq == 4]
    # day-clustered t for top quintile
    dsum = T.groupby("day")["exd2"].sum()
    out["top quint exd2 day-clustered: n days, t"] = pd.Series({"days": len(dsum), "mean%": 100*T.exd2.mean(),
        "t": dsum.mean()/(dsum.std()/np.sqrt(len(dsum))) * 1.0})
    # slope day-clustered via per-day aggregation of z-weighted deviations
    Sc = S.copy(); zc = Sc.z - Sc.z.mean(); Sc["xy"] = zc * (Sc.exd2 - Sc.exd2.mean())
    dd = Sc.groupby("day")["xy"].sum()
    out["slope day-clustered t"] = dd.mean()/(dd.std()/np.sqrt(len(dd)))
    out["slope exd2 without w10"] = sl(S[S.win != "w10"])
    out["top quint exd2 without w10"] = tt(T[T.win != "w10"].exd2)
    out["slope sexd2 (in usual swings) all calm up"] = sl(S, "sexd2")
    out["slope exd2 by coin"] = S.groupby("coin").apply(sl)
    out["slope exd2 by year"] = S.groupby("year").apply(sl)
    out["top quint exd2 by year"] = T.groupby("year")["exd2"].apply(tt).unstack()
    out["top quint exd2 by weekday"] = T.groupby("wd")["exd2"].apply(tt).unstack()
    return out
