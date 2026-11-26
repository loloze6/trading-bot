def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            z = r1 / sd30
            n = len(b)
            for H in (3, 5, 10):
                fwd = c.shift(-H) / c - 1
                for i in range(0, n, H):
                    sd = sd30[i]
                    rows.append(dict(H=H, coin=coin, z=z[i],
                                     zp5=(c[i] / c[i-5] - 1) / (sd * np.sqrt(5)) if i >= 5 and sd > 0 else np.nan,
                                     zp3=(c[i] / c[i-3] - 1) / (sd * np.sqrt(3)) if i >= 3 and sd > 0 else np.nan,
                                     tr=c[i] / c[i-60] - 1 if i >= 60 else np.nan,
                                     fwd=fwd[i], calm=b["regime"].iloc[i] != "chop",
                                     day=pd.Timestamp(b["timestamp"].iloc[i]).normalize(),
                                     year=pd.Timestamp(b["timestamp"].iloc[i]).year))
    d = pd.DataFrame(rows).dropna(subset=["fwd"])
    d["ex"] = d["fwd"] - d.groupby(["H", "coin"])["fwd"].transform("mean")
    def cl_t(g, x):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 20: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        X = np.column_stack([np.ones(len(g)), g[x].values]); y = g["ex"].values
        XtX = np.linalg.inv(X.T @ X); beta = XtX @ X.T @ y; e = y - X @ beta
        meat = np.zeros((2, 2))
        for _, idx in g.groupby("day").indices.items():
            s = X[idx].T @ e[idx]; meat += np.outer(s, s)
        V = XtX @ meat @ XtX
        return pd.Series(dict(n=len(g), slope=beta[1], t=beta[1] / np.sqrt(V[1, 1])))
    out = {}
    res = []
    for H in (3, 5, 10):
        for calm in (True, False):
            for x in ("z", "zp3", "zp5"):
                g = d[(d.H == H) & (d.calm == calm)]
                s = cl_t(g, x); s["H"] = H; s["calm"] = calm; s["x"] = x
                for side, gg in (("neg", g[g[x] < 0]), ("pos", g[g[x] > 0])):
                    s2 = cl_t(gg, x); s["slope_" + side] = s2["slope"]; s["t_" + side] = s2["t"]
                res.append(s)
    out["slopes"] = pd.DataFrame(res).set_index(["H", "calm", "x"])
    g = d[(d.H == 5) & d.calm].copy()
    g["tb"] = pd.cut(g["tr"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
    out["calm5_zp5_by_trend"] = g.groupby("tb").apply(lambda x: cl_t(x, "zp5"))
    out["calm5_zp5_by_year"] = g.groupby("year").apply(lambda x: cl_t(x, "zp5"))
    out["calm5_zp5_neg_by_coin"] = g[g.zp5 < 0].groupby("coin").apply(lambda x: cl_t(x, "zp5"))
    out["calm5_zp5_neg_mean"] = g[g.zp5 < -0.5].groupby("tb")["ex"].agg(["count", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    return out
