def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            f = df["forecast"].values
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            vol60 = pd.Series(r1).rolling(60, min_periods=20).std().values
            for i in range(n):
                d = {"coin": coin, "i": i, "year": ts.iloc[i].year, "day": ts.iloc[i].normalize(),
                     "f": f[i], "r1": r1[i], "z": r1[i]/vol60[i] if vol60[i] > 0 else np.nan}
                d["fr1"] = c[i+1]/c[i]-1 if i+1 < n else np.nan
                d["fr2"] = c[i+2]/c[i]-1 if i+2 < n else np.nan
                d["d2only"] = c[i+2]/c[i+1]-1 if i+2 < n else np.nan
                rows.append(d)
    D = pd.DataFrame(rows)
    m1 = D.groupby("coin")["fr1"].mean(); D["ex1"] = D["fr1"] - D["coin"].map(m1)
    D["exd2"] = D["d2only"] - D["coin"].map(m1)
    m2 = D[D["i"] % 2 == 0].groupby("coin")["fr2"].mean(); D["ex2"] = D["fr2"] - D["coin"].map(m2)

    def clt(sub, y, x="f"):
        sub = sub[[y, x, "day"]].dropna()
        if len(sub) < 30: return (np.nan, np.nan, len(sub), np.nan)
        X = np.c_[np.ones(len(sub)), sub[x].values]; Y = sub[y].values
        b = np.linalg.lstsq(X, Y, rcond=None)[0]; e = Y - X @ b
        XtXi = np.linalg.inv(X.T @ X); meat = np.zeros((2, 2))
        for _, idx in sub.groupby("day").indices.items():
            s = X[idx].T @ e[idx]; meat += np.outer(s, s)
        G = sub["day"].nunique(); N = len(sub)
        V = XtXi @ meat @ XtXi * G/(G-1)*(N-1)/(N-2)
        return (b[1], b[1]/np.sqrt(V[1, 1]), N, G)

    def daymean_t(sub, y):
        s = sub[[y, "day"]].dropna().groupby("day")[y].sum()
        cnt = sub[[y, "day"]].dropna().groupby("day")[y].size()
        mean = s.sum()/cnt.sum()
        dev = sub[[y, "day"]].dropna().assign(dv=lambda x: x[y]-mean).groupby("day")["dv"].sum()
        se = np.sqrt((dev**2).sum())/cnt.sum()
        return mean, mean/se, cnt.sum(), len(s)

    out = {}
    s1 = D[D["f"] > 0]
    out["h1_all"] = pd.Series(clt(s1, "ex1"), index=["slope", "t", "n", "days"])
    out["day2_only_on_2grid"] = pd.Series(clt(D[(D["i"] % 2 == 0) & (D["f"] > 0)], "exd2"), index=["slope", "t", "n", "days"])
    out["h1_by_year"] = pd.DataFrame({y: clt(g, "ex1") for y, g in s1.groupby("year")}, index=["slope", "t", "n", "days"]).T
    bc = pd.DataFrame({c: clt(g, "ex1") for c, g in s1.groupby("coin")}, index=["slope", "t", "n", "days"]).T
    out["h1_by_coin"] = bc
    out["h1_coins_positive_slope"] = int((bc["slope"] > 0).sum())
    s1 = s1.copy(); s1["q"] = pd.qcut(s1["f"], 5, labels=False, duplicates="drop")
    qq = []
    for q, g in s1.groupby("q"):
        m, t, n, G = daymean_t(g, "ex1"); qq.append({"q": q, "f": g["f"].mean(), "z": g["z"].mean(), "ex1": m, "t": t, "n": n, "days": G})
    out["h1_quintiles"] = pd.DataFrame(qq)
    s2 = D[(D["i"] % 2 == 0) & (D["f"] > 0)].copy(); s2["q"] = pd.qcut(s2["f"], 5, labels=False, duplicates="drop")
    qq = []
    for q, g in s2.groupby("q"):
        m, t, n, G = daymean_t(g, "ex2"); qq.append({"q": q, "ex2": m, "t": t, "n": n, "days": G})
    out["h2_quintiles_t"] = pd.DataFrame(qq)
    # all bars incl. up days: graded over full z
    a1 = D.dropna(subset=["z"]).copy(); a1["negz"] = -a1["z"]
    out["h1_raw_negz_all_days"] = pd.Series(clt(a1, "ex1", "negz"), index=["slope", "t", "n", "days"])
    return out
