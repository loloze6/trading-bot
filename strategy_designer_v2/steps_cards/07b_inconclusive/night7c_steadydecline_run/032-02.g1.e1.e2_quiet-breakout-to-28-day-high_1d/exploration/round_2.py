def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    drift = {}
    for coin, wins in bars.items():
        for H in (5, 10, 20):
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - H, H):
                    rs.append(c[i + H] / c[i] - 1)
            drift[(coin, H)] = (np.mean(rs), np.std(rs, ddof=1))
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            for H in (5, 10, 20):
                m, s = drift[(coin, H)]
                for off in range(H):
                    for i in range(off, n - H, H):
                        f = df["forecast"].iloc[i]
                        rows.append(dict(coin=coin, w=w, H=H, off=off, day=ts.iloc[i].normalize(),
                                         trend=df["regime"].iloc[i] == "trending",
                                         f=f, ex=c[i + H] / c[i] - 1 - m, exs=(c[i + H] / c[i] - 1 - m) / s))
    d = pd.DataFrame(rows)
    out = {}
    res = []
    for H in (5, 10, 20):
        for off in range(H):
            g = d[(d.H == H) & (d.off == off) & d.trend].dropna(subset=["f"])
            if len(g) < 8:
                continue
            r = stats.linregress(g["f"], g["ex"])
            gc = g[g.f > 0]
            rc = stats.linregress(gc["f"], gc["ex"]) if len(gc) > 8 else None
            ntr = d[(d.H == H) & (d.off == off) & (~d.trend)]
            res.append(dict(H=H, off=off, n=len(g), slope_t=r.slope / r.stderr,
                            mean_ex_trend=g["ex"].mean(), t_mean_trend=stats.ttest_1samp(g["ex"], 0).statistic,
                            mean_ex_nontrend=ntr["ex"].mean(),
                            mean_ex_pos_f=g.loc[g.f > 0, "ex"].mean(), mean_ex_neg_f=g.loc[g.f <= 0, "ex"].mean(),
                            slope_t_within_pos=(rc.slope / rc.stderr) if rc else np.nan))
    r = pd.DataFrame(res)
    out["by_H_offset_summary"] = r.groupby("H").agg(['mean', 'min', 'max'])[["slope_t", "mean_ex_trend", "t_mean_trend",
                                                                               "mean_ex_nontrend", "mean_ex_pos_f",
                                                                               "mean_ex_neg_f", "slope_t_within_pos"]].T
    # day-clustered t of mean excess, positive vs negative forecast, H=5 offset 0
    g = d[(d.H == 5) & (d.off == 0) & d.trend].dropna(subset=["f"])
    for name, sub in (("pos_f", g[g.f > 0]), ("neg_f", g[g.f <= 0])):
        dd = sub.groupby("day")["ex"].sum()
        out["h5_dayclustered_" + name] = f"n_cases {len(sub)} days {len(dd)} mean {sub['ex'].mean():.4f} t {dd.mean()/dd.std(ddof=1)*np.sqrt(len(dd))*1:.2f}"
    return out
