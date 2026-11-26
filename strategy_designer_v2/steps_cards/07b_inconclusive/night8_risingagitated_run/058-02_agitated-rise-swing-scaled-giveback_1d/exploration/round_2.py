def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    h = 5
    drift = {}
    rows = []
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - h, h)
            rets += list(c[idx + h] / c[idx] - 1)
        rets = np.array(rets)
        m, s = rets.mean(), rets.std(ddof=1)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r = c.pct_change()
            sma = c.rolling(20).mean()
            sd = r.rolling(20).std()
            dist = (c - sma) / (sd * c)
            tr = c / c.shift(60) - 1
            ra = (df["regime"] == "unknown")
            idx = np.arange(0, len(c) - h, h)
            for i in idx:
                fr = c.iloc[i + h] / c.iloc[i] - 1
                rows.append(dict(coin=coin, w=w, dist=dist.iloc[i], ex=fr - m, st=(fr - m) / s,
                                 ra=ra.iloc[i], tr=tr.iloc[i], fc=df["forecast"].iloc[i],
                                 day=str(df["timestamp"].iloc[i])[:10]))
    R = pd.DataFrame(rows)
    R = R[R.dist.notna()]

    def clslope(g):
        x = g["dist"].values; y = g["ex"].values
        X = np.column_stack([np.ones(len(x)), x])
        b = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ b
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((2, 2))
        days = g["day"].values
        for d in np.unique(days):
            k = days == d
            sc = X[k].T @ e[k]
            meat += np.outer(sc, sc)
        G = len(np.unique(days))
        V = XtXi @ meat @ XtXi * G / (G - 1)
        return b[1], b[1] / np.sqrt(V[1, 1]), len(g), G

    def clmean(g):
        s = g.groupby("day")["ex"].sum()
        n = len(g); G = len(s)
        mu = g["ex"].mean()
        se = np.sqrt(((s - g.groupby("day")["ex"].count() * mu) ** 2).sum()) / n
        return mu, mu / se, n, G

    def grp(name):
        if name == "ra": return "rising agitated"
        return name
    R["trend"] = np.where(R.tr > 0.10, "rising", np.where(R.tr < -0.10, "falling", "choppy"))
    R.loc[R.tr.isna(), "trend"] = "unknown_trend"
    R["prof"] = np.where(R.ra, "rising agitated", R["trend"] + "_notRA")
    out = {}
    tab = []
    for p, g in R[R.dist > 0].groupby("prof"):
        if len(g) < 15: continue
        b, t, n, G = clslope(g)
        mu, tm, _, _ = clmean(g)
        tab.append(dict(prof=p, n=n, days=G, slope=b, slope_t=t, mean_ex=mu, mean_t=tm, strength=g.st.mean()))
    out["dist>0, h5, by profile (trend from 60d ret)"] = pd.DataFrame(tab).set_index("prof")
    tab = []
    for p, g in R.groupby("prof"):
        if len(g) < 15: continue
        b, t, n, G = clslope(g)
        tab.append(dict(prof=p, n=n, days=G, slope_all_dist=b, t=t))
    out["all dist, h5, slope by profile"] = pd.DataFrame(tab).set_index("prof")
    g = R[(R.dist > 0)]
    b, t, n, G = clslope(g)
    out["dist>0 all profiles clustered slope"] = f"slope {b:.5f} t {t:.2f} n {n} days {G}"
    g = R[(R.dist > 0) & (~R.ra)]
    b, t, n, G = clslope(g)
    out["dist>0 not RA clustered slope"] = f"slope {b:.5f} t {t:.2f} n {n} days {G}"
    g = R[(R.dist > 0) & (R.trend == "rising") & (~R.ra)].copy()
    if len(g) > 40:
        g["dq"] = pd.qcut(g.dist, 4, labels=["d1", "d2", "d3", "d4"])
        out["rising notRA dist>0 by dist quartile"] = g.groupby("dq").agg(n=("ex", "size"), mean_ex=("ex", "mean"), strength=("st", "mean"))
    g = R[(R.dist > 0) & (R.trend == "rising") & (~R.ra)]
    if len(g) > 10:
        out["rising notRA dist>0 slope by coin"] = pd.DataFrame(
            {c: dict(zip(["slope", "t", "n", "days"], clslope(gg))) for c, gg in g.groupby("coin") if len(gg) > 10}).T
    return out
