def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 48, 48)
            rs.append(c[idx + 48] / c[idx] - 1)
        dr = np.nanmean(np.concatenate(rs))
        for w, df in wins.items():
            ts = pd.to_datetime(df["timestamp"])
            c = df["close"].values.astype(float)
            s = pd.Series(c)
            vs = pd.Series(df["volume"].values.astype(float))
            r48 = s / s.shift(48) - 1
            usual = r48.abs().rolling(720, min_periods=360).mean()
            thin = vs.shift(48).rolling(120).mean() / vs.rolling(48).mean()
            fc = df["forecast"].values
            raw = df["debug_info.components.thin_weekend_move.last_history_value"].values if "debug_info.components.thin_weekend_move.last_history_value" in df else np.full(len(c), np.nan)
            hr = ts.dt.hour.values; wd = ts.dt.weekday.values
            n = len(c)
            for i in np.where(hr == 23)[0]:
                if i + 48 >= n:
                    continue
                rows.append(dict(coin=coin, win=w, year=ts.iloc[i].year, wd=wd[i],
                                 mz=r48.iloc[i] / usual.iloc[i] if usual.iloc[i] else np.nan,
                                 thin=thin.iloc[i], f48=c[i + 48] / c[i] - 1 - dr,
                                 fc=fc[i], raw=raw[i]))
    D = pd.DataFrame(rows).dropna(subset=["mz", "thin", "f48"])
    D = D[D.thin > 0]
    D["rev"] = -np.sign(D["mz"]) * D["f48"]
    D["lthin"] = np.log(D["thin"])
    out = {}

    def reg(x, y):
        m = ~(np.isnan(x) | np.isnan(y))
        if m.sum() < 20:
            return np.nan, np.nan, int(m.sum())
        r = stats.linregress(x[m], y[m])
        return r.slope, r.slope / r.stderr, int(m.sum())

    # weekday comparison: reversal share graded by thinness (log of far/near volume)
    t = []
    for day in range(7):
        d = D[D.wd == day]
        a = reg(d["lthin"].values, d["rev"].values)
        q = pd.qcut(d["thin"], 5, labels=False)
        g = d.groupby(q)["rev"].mean()
        t.append(dict(day=day, slope=a[0], t=a[1], n=a[2], q0=g.iloc[0], q2=g.iloc[2], q4=g.iloc[4],
                      top_minus_bottom_t=stats.ttest_ind(d.rev[q == 4], d.rev[q == 0], equal_var=False).statistic))
    out["rev_on_logthin_by_day (6=Sun)"] = pd.DataFrame(t)

    S = D[D.wd == 6].copy()
    S["q"] = pd.qcut(S["thin"], 5, labels=False)
    out["sun_thin_q_by_side"] = S.groupby(["q", S.mz > 0])["rev"].agg(["size", "mean"]).unstack()
    out["sun_logthin_by_coin"] = pd.DataFrame([dict(coin=k, slope=reg(g.lthin.values, g.rev.values)[0],
        t=reg(g.lthin.values, g.rev.values)[1], n=len(g)) for k, g in S.groupby("coin")])
    S["era"] = np.where(S.year <= 2021, "2018-2021", "2022-2025")
    out["sun_logthin_by_era"] = pd.DataFrame([dict(era=k, slope=reg(g.lthin.values, g.rev.values)[0],
        t=reg(g.lthin.values, g.rev.values)[1], n=len(g)) for k, g in S.groupby("era")])
    # does the move size matter inside the thin weekends?
    S["absmz_q"] = pd.qcut(S["mz"].abs(), 3, labels=False)
    out["sun_rev_thinq_x_moveterc"] = S.groupby(["q", "absmz_q"])["rev"].mean().unstack()
    # recorded forecast vs cube
    m = S["fc"].fillna(0) != 0
    out["sun_recorded_forecast"] = pd.Series(dict(
        n_nonzero=int(m.sum()),
        t_fc=reg(S.loc[m, "fc"].values, S.loc[m, "f48"].values)[1],
        t_cuberoot_fc=reg(np.cbrt(S.loc[m, "fc"].values), S.loc[m, "f48"].values)[1],
        t_neg_raw=reg(-S.loc[m, "raw"].values.astype(float), S.loc[m, "f48"].values)[1],
        spearman=stats.spearmanr(S.loc[m, "fc"], S.loc[m, "f48"]).correlation))
    return out
