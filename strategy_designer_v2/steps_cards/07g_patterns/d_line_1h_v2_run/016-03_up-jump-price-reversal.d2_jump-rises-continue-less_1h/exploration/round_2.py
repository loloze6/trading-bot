def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 72
    rows = []
    hr = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            n = len(c)
            ts = pd.to_datetime(b["timestamp"])
            nxt = np.r_[c[1:] / c[:-1] - 1, np.nan]
            hr.append(pd.DataFrame({"coin": coin, "hour": ts.dt.hour.values, "year": ts.dt.year.values, "nxt": nxt}))
            if n < 2 * H + 2:
                continue
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            for t in range(H, n - H, H):
                past = c[t] / c[t - H] - 1
                rr = r1[t - H + 1:t + 1]
                lr = np.log1p(rr)
                eff = abs(np.log(c[t] / c[t - H])) / np.nansum(np.abs(lr))
                rv = np.nanstd(rr)
                fwd = c[t + H] / c[t] - 1
                fwd24 = c[t + 24] / c[t] - 1
                rows.append(dict(coin=coin, w=w, past=past, eff=eff, rv=rv, fwd=fwd, fwd24=fwd24, year=ts.iloc[t].year))
    df = pd.DataFrame(rows)
    df["fwd_dm"] = df["fwd"] - df.groupby("coin")["fwd"].transform("mean")
    df["fwd24_dm"] = df["fwd24"] - df.groupby("coin")["fwd24"].transform("mean")
    df["seff"] = df["eff"] * np.sign(df["past"])
    df["zpast"] = df.groupby("coin")["past"].transform(lambda x: (x - x.mean()) / x.std())
    df["zseff"] = df.groupby("coin")["seff"].transform(lambda x: (x - x.mean()) / x.std())
    df["zrv"] = df.groupby("coin")["rv"].transform(lambda x: (x - x.mean()) / x.std())
    out = {}
    # regression fwd_dm ~ zpast + zseff + zrv
    X = np.column_stack([np.ones(len(df)), df.zpast, df.zseff, df.zrv])
    y = df.fwd_dm.values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    s2 = res @ res / (len(y) - X.shape[1])
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["reg_fwd72"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["const", "zpast", "zseff", "zrv"])
    X2 = np.column_stack([np.ones(len(df)), df.zpast, df.zseff, df.zrv])
    y2 = df.fwd24_dm.values
    b2, *_ = np.linalg.lstsq(X2, y2, rcond=None)
    r2 = y2 - X2 @ b2; s22 = r2 @ r2 / (len(y2) - 4)
    out["reg_fwd24"] = pd.DataFrame({"beta": b2, "t": b2 / np.sqrt(np.diag(s22 * np.linalg.inv(X2.T @ X2)))}, index=["const", "zpast", "zseff", "zrv"])
    # up moves: eff top vs bottom quintile within past-size terciles
    up = df[df.past > 0].copy()
    up["eq"] = up.groupby("coin")["eff"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    up["pt"] = up.groupby("coin")["past"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    rr_ = []
    for p, g in up.groupby("pt"):
        a = g[g.eq == 4].fwd; z = g[g.eq == 0].fwd
        rr_.append(dict(past_tercile=p, diff=a.mean() - z.mean(), t=stats.ttest_ind(a, z, equal_var=False).statistic, na=len(a), nz=len(z)))
    out["up_eff_top_minus_bottom_by_past_tercile"] = pd.DataFrame(rr_)
    # signed eff top minus bottom quintile, by coin and by year
    df["sq"] = df.groupby("coin")["seff"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    def tb(g):
        a = g[g.sq == 4].fwd; z = g[g.sq <= 1].fwd
        return pd.Series(dict(diff=a.mean() - z.mean(), t=stats.ttest_ind(a, z, equal_var=False).statistic, n=len(g)))
    out["seff_top_minus_low2_by_coin"] = df.groupby("coin").apply(tb)
    out["seff_top_minus_low2_by_year"] = df.groupby("year").apply(tb)
    # hours 20-21 by year and coin
    h = pd.concat(hr).dropna()
    h["nxt_dm"] = h["nxt"] - h.groupby("coin")["nxt"].transform("mean")
    h["is2021"] = h.hour.isin([20, 21])
    def ht(g):
        a = g[g.is2021].nxt_dm; z = g[~g.is2021].nxt_dm
        return pd.Series(dict(diff=a.mean() - z.mean(), t=stats.ttest_ind(a, z, equal_var=False).statistic, n=len(a)))
    out["h2021_by_year"] = h.groupby("year").apply(ht)
    out["h2021_by_coin"] = h.groupby("coin").apply(ht)
    return out
