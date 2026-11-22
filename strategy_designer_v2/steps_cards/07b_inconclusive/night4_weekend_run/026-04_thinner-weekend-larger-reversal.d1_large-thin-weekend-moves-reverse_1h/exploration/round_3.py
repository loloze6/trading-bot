def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    sd = {}
    for coin, wins in bars.items():
        dr = {}
        for h in (24, 48, 96):
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.append(c[idx + h] / c[idx] - 1)
            rs = np.concatenate(rs)
            dr[h] = (np.nanmean(rs), np.nanstd(rs))
        sd[coin] = dr
        for w, df in wins.items():
            ts = pd.to_datetime(df["timestamp"])
            c = df["close"].values.astype(float)
            s = pd.Series(c)
            vs = pd.Series(df["volume"].values.astype(float))
            r48 = s / s.shift(48) - 1
            usual = r48.abs().rolling(720, min_periods=360).mean()
            thin = vs.shift(48).rolling(120).mean() / vs.rolling(48).mean()
            hr = ts.dt.hour.values; wd = ts.dt.weekday.values
            n = len(c)
            for i in np.where((hr == 23) & (wd == 6))[0]:
                rec = dict(coin=coin, year=ts.iloc[i].year, mz=r48.iloc[i] / usual.iloc[i] if usual.iloc[i] else np.nan,
                           thin=thin.iloc[i])
                for h in (24, 48, 96):
                    rec[f"f{h}"] = (c[i + h] / c[i] - 1 - dr[h][0]) if i + h < n else np.nan
                    rec[f"z{h}"] = rec[f"f{h}"] / dr[h][1]
                rows.append(rec)
    S = pd.DataFrame(rows).dropna(subset=["mz", "thin"])
    S = S[S.thin > 0]
    S["lthin"] = np.log(S.thin)
    out = {}
    t = []
    for h in (24, 48, 96):
        for side, g in [("all", S), ("up", S[S.mz > 0]), ("down", S[S.mz < 0])]:
            g = g.dropna(subset=[f"f{h}"])
            rev = -np.sign(g.mz) * g[f"f{h}"]
            r = stats.linregress(g.lthin, rev)
            q = pd.qcut(g.thin, 5, labels=False)
            top = rev[q == 4]
            t.append(dict(h=h, side=side, n=len(g), slope=r.slope, t=r.slope / r.stderr,
                          top_q_rev=top.mean(), top_q_t=stats.ttest_1samp(top, 0).statistic,
                          top_q_strength=(-np.sign(g.mz) * g[f"z{h}"])[q == 4].mean()))
    out["sun_rev_on_logthin_h_side"] = pd.DataFrame(t)
    g = S.dropna(subset=["f48"])
    rev = -np.sign(g.mz) * g.f48
    # thinness times move size vs thinness alone
    out["sun_48_compare"] = pd.Series(dict(
        t_lthin=stats.linregress(g.lthin, rev).rvalue * np.sqrt(len(g) - 2) / np.sqrt(1 - stats.linregress(g.lthin, rev).rvalue ** 2),
        t_lthin_x_absmz=(lambda r: r.slope / r.stderr)(stats.linregress(g.lthin * g.mz.abs().clip(upper=3), rev)),
        corr_thin_absmz=np.corrcoef(g.lthin, g.mz.abs())[0, 1]))
    return out
