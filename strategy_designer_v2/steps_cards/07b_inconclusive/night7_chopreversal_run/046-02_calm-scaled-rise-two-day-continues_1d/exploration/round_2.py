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
            d3 = c.shift(-3) / c.shift(-2) - 1
            calm = d["regime"].astype(str) != "chop"
            n = len(d)
            rows.append(pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(n), "z": z, "calm": calm,
                                      "f1": f1, "d2": d2, "d3": d3, "sd": sd}))
    A = pd.concat(rows, ignore_index=True)
    m1 = A[A.pos % 1 == 0].groupby("coin")["f1"].mean()
    A["ex1"] = A.f1 - A.coin.map(m1)
    A["exd2"] = A.d2 - A.coin.map(m1)
    A["exd3"] = A.d3 - A.coin.map(m1)
    A["sexd2"] = A.exd2 / A.sd
    out = {}
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x)))})
    def sl(x, y="exd2"):
        x = x.dropna(subset=["z", y])
        if len(x) < 10: return pd.Series({"n": len(x), "slope": np.nan, "t": np.nan})
        res = stats.linregress(x.z, x[y])
        return pd.Series({"n": len(x), "slope": res.slope, "t": res.slope/res.stderr})
    # day2 return as 1-bar horizon from close of day after rise: every bar is non-overlapping at h=1
    S = A[(A.z > 0) & A.calm].dropna(subset=["z", "exd2"]).copy()
    S["zq"] = pd.qcut(S.z, 5, labels=False)
    out["all bars calm up: exd2 by z quint"] = S.groupby("zq")["exd2"].apply(tt).unstack()
    out["all bars calm up: ex1 by z quint"] = S.groupby("zq")["ex1"].apply(tt).unstack()
    out["all bars calm up: exd3 by z quint"] = S.groupby("zq")["exd3"].apply(tt).unstack()
    out["slope exd2 on z, all calm up"] = sl(S)
    out["slope exd2 on z, z>1"] = sl(S[S.z > 1])
    out["slope ex1 on z, all calm up"] = sl(S, "ex1")
    T = S[S.zq == 4]
    out["top quint exd2 by coin"] = T.groupby("coin")["exd2"].apply(tt).unstack()
    out["top quint exd2 by window"] = T.groupby("win")["exd2"].apply(tt).unstack()
    # day-clustered t for top quint
    # conditional on day1 sign
    T = T.copy(); T["d1neg"] = T.f1 < 0
    out["top quint exd2 by day1 sign (neg?)"] = T.groupby("d1neg")["exd2"].apply(tt).unstack()
    # agitated comparison for day2
    Ag = A[(A.z > 0) & (~A.calm)].dropna(subset=["z", "exd2"]).copy()
    Ag["zq"] = pd.qcut(Ag.z, 5, labels=False)
    out["agitated up: exd2 by z quint"] = Ag.groupby("zq")["exd2"].apply(tt).unstack()
    return out
