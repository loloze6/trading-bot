def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 7, 7)
            rs += list(c[idx + 7] / c[idx] - 1)
        cm = np.mean(rs)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, n - 7, 7):
                if i < 30: continue
                r30 = c[i] / c[i - 30] - 1
                r60 = c[i] / c[i - 60] - 1 if i >= 60 else np.nan
                reg = df["regime"].iloc[i]
                rows.append(dict(coin=coin, w=w, year=ts.iloc[i].year, day=ts.iloc[i].normalize(),
                                 reg=reg, f=df["forecast"].iloc[i], r30=r30, r60=r60,
                                 x7=c[i + 7] / c[i] - 1 - cm))
    d = pd.DataFrame(rows)
    def clus(g, x="r30", y="x7"):
        g = g.dropna(subset=[x, y])
        if len(g) < 15: return pd.Series(dict(n=len(g)))
        X = np.column_stack([np.ones(len(g)), g[x].values]); Y = g[y].values
        b = np.linalg.lstsq(X, Y, rcond=None)[0]; e = Y - X @ b
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((2, 2)); days = g["day"].values
        for dd in np.unique(days):
            m = days == dd; s = X[m].T @ e[m]; meat += np.outer(s, s)
        G = len(np.unique(days)); k = 2; N = len(g)
        V = XtXi @ meat @ XtXi * G / (G - 1) * (N - 1) / (N - k)
        sig = np.sign(g[x])
        return pd.Series(dict(n=N, days=G, slope=b[1], t_cl=b[1] / np.sqrt(V[1, 1]),
                              long_mean=g.loc[sig > 0, y].mean(), short_mean=g.loc[sig < 0, y].mean()))
    cc = d[d.reg == "unknown"]
    out = {}
    out["chopcalm_raw"] = clus(cc)
    out["chopcalm_fcst"] = clus(cc, "f")
    out["chopcalm_raw_by_year"] = cc.groupby("year").apply(clus)
    big = cc[cc.r30.abs() > cc.r30.abs().median()]
    out["chopcalm_big_half"] = clus(big)
    out["chopcalm_small_half"] = clus(cc[cc.r30.abs() <= cc.r30.abs().median()])
    cc2 = cc.copy(); cc2["side"] = np.sign(cc2.r30)
    out["chopcalm_by_side"] = cc2.groupby("side").apply(clus)
    # out of calm-choppy, approximated choppy (r60 within +-10%) but vetoed => agitated choppy
    ca = d[(d.reg != "unknown") & (d.r60.abs() <= 0.10)]
    out["choppy_agitated_approx"] = clus(ca)
    out["not_choppy"] = clus(d[(d.reg != "unknown") & (d.r60.abs() > 0.10)])
    out["all_bars"] = clus(d)
    # forecast vs raw disagreement
    out["sign_disagree_share"] = float((np.sign(cc.f) != np.sign(cc.r30)).mean())
    return out
