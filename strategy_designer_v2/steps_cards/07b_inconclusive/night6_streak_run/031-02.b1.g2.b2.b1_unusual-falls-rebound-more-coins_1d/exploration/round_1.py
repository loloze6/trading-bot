def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            f = df["forecast"].values
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            r1s = pd.Series(r1)
            vol60 = r1s.rolling(60, min_periods=20).std().values
            ret30 = pd.Series(c).pct_change(30).values
            for i in range(n):
                d = {"coin": coin, "win": w, "i": i, "year": ts.iloc[i].year,
                     "day": ts.iloc[i].normalize(), "f": f[i], "r1": r1[i],
                     "z": r1[i]/vol60[i] if vol60[i] > 0 else np.nan, "ret30": ret30[i]}
                for h in (1, 2, 3, 5, 10):
                    d["fr%d" % h] = c[i+h]/c[i]-1 if i+h < n else np.nan
                rows.append(d)
    D = pd.DataFrame(rows)
    for h in (1, 2, 3, 5, 10):
        D["drift%d" % h] = np.nan
        g = D[D["i"] % h == 0]
        m = g.groupby("coin")["fr%d" % h].mean()
        D["drift%d" % h] = D["coin"].map(m)
        D["ex%d" % h] = D["fr%d" % h] - D["drift%d" % h]

    def clt(sub, y, x="f"):
        sub = sub[[y, x, "day"]].dropna()
        if len(sub) < 30: return (np.nan, np.nan, len(sub))
        X = np.c_[np.ones(len(sub)), sub[x].values]; Y = sub[y].values
        b = np.linalg.lstsq(X, Y, rcond=None)[0]; e = Y - X @ b
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((2, 2))
        for _, idx in sub.groupby("day").indices.items():
            s = X[idx].T @ e[idx]; meat += np.outer(s, s)
        G = sub["day"].nunique(); k = 2; N = len(sub)
        V = XtXi @ meat @ XtXi * G/(G-1)*(N-1)/(N-k)
        return (b[1], b[1]/np.sqrt(V[1, 1]), N)

    out = {}
    hz = []
    for h in (1, 2, 3, 5, 10):
        s = D[(D["i"] % h == 0) & (D["f"] > 0)]
        b, t, N = clt(s, "ex%d" % h)
        hz.append({"h": h, "slope": b, "t": t, "n": N, "mean_ex": s["ex%d" % h].mean()})
    out["horizons"] = pd.DataFrame(hz)
    s2 = D[(D["i"] % 2 == 0) & (D["f"] > 0)].copy()
    s2["q"] = pd.qcut(s2["f"], 5, labels=False, duplicates="drop")
    out["by_forecast_quintile"] = s2.groupby("q").agg(n=("ex2", "size"), f=("f", "mean"), z=("z", "mean"), ex2=("ex2", "mean"), ex5=("ex5", "mean"))
    out["by_coin"] = pd.DataFrame({c: clt(g, "ex2") for c, g in s2.groupby("coin")}, index=["slope", "t", "n"]).T
    out["by_year"] = pd.DataFrame({y: clt(g, "ex2") for y, g in s2.groupby("year")}, index=["slope", "t", "n"]).T
    s2["trend"] = np.where(s2["ret30"] > 0, "up30", "down30")
    out["by_trend"] = pd.DataFrame({y: clt(g, "ex2") for y, g in s2.groupby("trend")}, index=["slope", "t", "n"]).T
    # raw z instead of standardised forecast
    s2n = D[(D["i"] % 2 == 0) & (D["r1"] < 0)].copy(); s2n["negz"] = -s2n["z"]
    out["raw_z_on_down_days"] = pd.Series(clt(s2n, "ex2", "negz"), index=["slope", "t", "n"])
    s2n["zq"] = pd.qcut(s2n["negz"], 5, labels=False, duplicates="drop")
    out["raw_z_quintile"] = s2n.groupby("zq").agg(n=("ex2", "size"), negz=("negz", "mean"), ex2=("ex2", "mean"), ex5=("ex5", "mean"))
    return out
