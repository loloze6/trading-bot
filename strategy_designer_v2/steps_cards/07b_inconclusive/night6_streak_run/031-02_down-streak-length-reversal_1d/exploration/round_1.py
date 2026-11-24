def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        # coin mean returns per horizon over all windows (grid)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            ret1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            # streak counts
            dn = np.zeros(n); up = np.zeros(n)
            for i in range(1, n):
                if c[i] < c[i-1]:
                    dn[i] = dn[i-1] + 1
                elif c[i] > c[i-1]:
                    up[i] = up[i-1] + 1
            # 30-day past return
            p30 = pd.Series(c).pct_change(30).values
            p5 = pd.Series(c).pct_change(5).values
            f = b["forecast"].astype(float).values
            ts = pd.to_datetime(b["timestamp"])
            for h in (1, 2, 3, 5, 10):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, day=ts.iloc[i].normalize(),
                                     year=ts.iloc[i].year, fc=f[i], dn=dn[i], up=up[i],
                                     p30=p30[i], p5=p5[i], r=c[i+h]/c[i]-1))
    d = pd.DataFrame(rows)
    d["ex"] = d["r"] - d.groupby(["coin", "h"])["r"].transform("mean")

    def clt(x, y, day):
        m = ~(np.isnan(x) | np.isnan(y))
        x, y, day = x[m], y[m], day[m]
        X = np.c_[np.ones(len(x)), x]
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ beta
        s = pd.DataFrame(X * e[:, None]).groupby(day.values).sum().values
        G = len(s)
        XtXi = np.linalg.inv(X.T @ X)
        V = XtXi @ (s.T @ s) @ XtXi * G / (G - 1)
        return beta[1], beta[1] / np.sqrt(V[1, 1]), int(m.sum())

    out = {}
    # by horizon, slope on forecast
    rh = []
    for h, g in d.groupby("h"):
        s, t, k = clt(g.fc.values, g.ex.values, g.day)
        rh.append(dict(h=h, slope=s, t=t, n=k))
    out["slope_by_horizon"] = pd.DataFrame(rh)
    g5 = d[d.h == 5]
    # by coin
    rc = []
    for cn, g in g5.groupby("coin"):
        s, t, k = clt(g.fc.values, g.ex.values, g.day)
        rc.append(dict(coin=cn, slope=s, t=t, n=k))
    out["slope_by_coin_h5"] = pd.DataFrame(rc)
    ry = []
    for y, g in g5.groupby("year"):
        s, t, k = clt(g.fc.values, g.ex.values, g.day)
        ry.append(dict(year=y, slope=s, t=t, n=k))
    out["slope_by_year_h5"] = pd.DataFrame(ry)
    # mean excess by raw down-streak length and up-streak length, by horizon
    tab = []
    for h, g in d.groupby("h"):
        for lab, col in (("dn", "dn"), ("up", "up")):
            gg = g.copy(); gg["L"] = gg[col].clip(upper=5)
            for L, x in gg.groupby("L"):
                tab.append(dict(h=h, side=lab, L=L, n=len(x), mean_ex=x.ex.mean(),
                                t=x.ex.mean() / (x.ex.std() / np.sqrt(len(x)))))
    out["excess_by_streak"] = pd.DataFrame(tab).query("h in (1,5,10)")
    # regime split: past 30d return sign, h5, forecast slope
    rr = []
    for lab, g in g5.groupby(np.sign(g5.p30)):
        s, t, k = clt(g.fc.values, g.ex.values, g.day)
        rr.append(dict(p30sign=lab, slope=s, t=t, n=k))
    out["slope_by_30d_trend_h5"] = pd.DataFrame(rr)
    return out
