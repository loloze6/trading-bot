def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    recs = []; daily = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            n = len(c)
            if n < 40: continue
            r1 = c.pct_change()
            vol = r1.rolling(30).std()
            r1z = r1 / vol.shift(1)
            r30 = c / c.shift(30) - 1
            prevhi = c.shift(1).rolling(89, min_periods=29).max()
            ab = c / prevhi - 1
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            yr = ts.dt.year
            for H in (5, 10, 20):
                fwd = c.shift(-H) / c - 1
                for i in range(0, n - H, H):
                    recs.append(dict(coin=coin, w=w, H=H, yr=yr[i], fwd=fwd[i], r1=r1[i], r1z=r1z[i],
                                     r30=r30[i], ab=ab[i]))
            daily.append(pd.DataFrame({"coin": coin, "w": w, "day": ts.dt.floor("D"), "wd": ts.dt.weekday,
                                       "yr": yr, "nxt": c.shift(-1) / c - 1}))
    D = pd.DataFrame(recs)
    g = D.groupby(["coin", "H"])["fwd"]
    D["ex"] = D["fwd"] - g.transform("mean"); D["st"] = D["ex"] / g.transform("std")
    def summ(x):
        s = x["st"].dropna()
        wm = x.groupby("w")["st"].mean()
        return pd.Series({"n": len(s), "mean_ex": x["ex"].mean(), "strength": s.mean(),
                          "t": s.mean() / (s.std() / np.sqrt(len(s))),
                          "n_win": len(wm), "share_win_pos": (wm > 0).mean(),
                          "t_win": wm.mean() / (wm.std() / np.sqrt(len(wm))) if len(wm) > 2 else np.nan})
    for H in (5, 10, 20):
        d = D[D.H == H].copy()
        d["q"] = d.groupby("coin")["r1z"].transform(lambda x: pd.qcut(x.rank(method="first"), 10, labels=False))
        out[f"r1z_dec_H{H}"] = d.dropna(subset=["q"]).groupby("q").apply(summ)
        d["abq"] = pd.cut(d["ab"], [-1, -0.2, -0.1, -0.03, 0, 0.03, 0.08, 0.2, 10])
        out[f"above_prev90hi_H{H}"] = d.dropna(subset=["abq"]).groupby("abq").apply(summ)
    d = D[D.H == 10].copy()
    d["q"] = d.groupby("coin")["r1z"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["r1z_low_by_year"] = d[d.q == 0].groupby("yr").apply(summ)
    out["break_by_year"] = d[d.ab > 0].groupby("yr").apply(summ)
    out["spearman_r1z_H10"] = pd.Series(stats.spearmanr(d["r1z"], d["st"], nan_policy="omit"), index=["rho", "p"])
    Y = pd.concat(daily, ignore_index=True).dropna(subset=["nxt"])
    Y["ex"] = Y["nxt"] - Y.groupby("coin")["nxt"].transform("mean")
    dd = Y.groupby(["day", "wd", "yr"])["ex"].mean().reset_index()
    out["weekday_dayclustered"] = dd.groupby("wd")["ex"].agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    wed = dd[dd.wd == 2].groupby("yr")["ex"].agg(["count", "mean"])
    out["wednesday_by_year"] = wed
    # book: biggest losses context
    days = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            days.append(x.assign(coin=coin, w=w))
    B = pd.concat(days)
    out["book_return_by_window"] = B.groupby("w")["book_return"].agg(["count", "mean", "sum"]).sort_values("sum").head(8)
    return out
