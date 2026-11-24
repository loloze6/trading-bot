def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            dn = np.zeros(n)
            for i in range(1, n):
                if c[i] < c[i-1]:
                    dn[i] = dn[i-1] + 1
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            sd = pd.Series(r1).rolling(60, min_periods=20).std().shift(1).values
            f = b["forecast"].astype(float).values
            ts = pd.to_datetime(b["timestamp"])
            for h in (1, 2, 5):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, h=h, day=ts.iloc[i].normalize(), year=ts.iloc[i].year,
                                     fc=f[i], dn=dn[i], r1=r1[i], z1=r1[i] / sd[i] if sd[i] > 0 else np.nan,
                                     r=c[i+h]/c[i]-1))
    d = pd.DataFrame(rows)
    d["ex"] = d["r"] - d.groupby(["coin", "h"])["r"].transform("mean")

    def clt(x, y, day):
        x = np.asarray(x, float); y = np.asarray(y, float); day = np.asarray(day)
        m = ~(np.isnan(x) | np.isnan(y))
        x, y, day = x[m], y[m], day[m]
        X = np.c_[np.ones(len(x)), x]
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ beta
        s = pd.DataFrame(X * e[:, None]).groupby(day).sum().values
        G = len(s)
        XtXi = np.linalg.inv(X.T @ X)
        V = XtXi @ (s.T @ s) @ XtXi * G / (G - 1)
        return beta[1], beta[1] / np.sqrt(V[1, 1]), int(m.sum())

    out = {}
    res = []
    for h, g in d.groupby("h"):
        gp = g[g.fc > 0]
        s, t, k = clt(gp.fc, gp.ex, gp.day); res.append(dict(h=h, what="fc|fc>0", slope=s, t=t, n=k))
        s, t, k = clt((g.fc > 0).astype(float), g.ex, g.day); res.append(dict(h=h, what="fc>0 dummy", slope=s, t=t, n=k))
        s, t, k = clt(-g.z1, g.ex, g.day); res.append(dict(h=h, what="-z1 all", slope=s, t=t, n=k))
        gd = g[g.r1 < 0]
        s, t, k = clt(-gd.z1, gd.ex, gd.day); res.append(dict(h=h, what="-z1 down days", slope=s, t=t, n=k))
        gu = g[g.r1 > 0]
        s, t, k = clt(-gu.z1, gu.ex, gu.day); res.append(dict(h=h, what="-z1 up days", slope=s, t=t, n=k))
    out["slopes"] = pd.DataFrame(res)
    g1 = d[d.h == 1]
    rc = []
    for cn, g in g1.groupby("coin"):
        s, t, k = clt(g.fc, g.ex, g.day); s2, t2, _ = clt(-g.z1, g.ex, g.day)
        rc.append(dict(coin=cn, fc_slope=s, fc_t=t, z_slope=s2, z_t=t2, n=k))
    out["h1_by_coin"] = pd.DataFrame(rc)
    ry = []
    for y, g in g1.groupby("year"):
        s, t, k = clt(g.fc, g.ex, g.day); s2, t2, _ = clt(-g.z1, g.ex, g.day)
        ry.append(dict(year=y, fc_slope=s, fc_t=t, z_slope=s2, z_t=t2, n=k))
    out["h1_by_year"] = pd.DataFrame(ry)
    g1 = g1.dropna(subset=["z1"]).copy()
    g1["zq"] = pd.qcut(g1.z1, 10, labels=False)
    out["h1_excess_by_z1_decile"] = g1.groupby("zq").agg(z=("z1", "mean"), n=("ex", "size"), mean_ex=("ex", "mean"),
                                                         t=("ex", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    return out
