def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    dist = []
    rows = []
    for coin, wins in bars.items():
        r48 = []; r24 = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 48, 48); r48 += list(c[idx + 48] / c[idx] - 1)
            idx = np.arange(0, len(c) - 24, 24); r24 += list(c[idx + 24] / c[idx] - 1)
        d48 = np.mean(r48); d24 = np.mean(r24)
        for w, df in wins.items():
            ts = pd.to_datetime(df["timestamp"])
            c = df["close"].values; f = df["forecast"].values; n = len(c)
            wd = ts.dt.weekday.values; hr = ts.dt.hour.values; yr = ts.dt.year.values
            reg = df["regime"].astype(str).values
            for i in np.where(reg == "mean_reversion")[0]:
                dist.append(dict(wd=wd[i], hr=hr[i], pos=f[i] > 0))
            for i in np.where(f >= 2)[0]:
                if i + 48 < n and i >= 24:
                    rows.append(dict(coin=coin, year=yr[i], wd=wd[i], hr=hr[i], f=f[i],
                                     s24=c[i]/c[i-24]-1,
                                     x48=c[i+48]/c[i]-1-d48, x24=c[i+24]/c[i]-1-d24,
                                     x24b=c[i+48]/c[i+24]-1-d24))
    dd = pd.DataFrame(dist)
    out["regime_bars_by_wd_hr"] = dd.groupby(["wd", "hr"]).agg(n=("pos", "size"), share_pos=("pos", "mean")).head(10)
    d = pd.DataFrame(rows)
    def summ(g, col="x48"):
        v = g[col].dropna()
        return pd.Series(dict(n=len(v), mean=v.mean(), t=v.mean()/(v.std()/np.sqrt(len(v))) if len(v) > 2 else np.nan))
    out["f_ge2_by_wd_hr"] = d.groupby(["wd", "hr"]).apply(summ).head(10)
    out["f_ge2_overall"] = pd.DataFrame({k: summ(d, k) for k in ["x48", "x24", "x24b"]})
    out["f_ge2_by_year"] = d.groupby("year").apply(summ)
    out["f_ge2_by_coin"] = d.groupby("coin").apply(summ)
    out["corr_f_x48"] = pd.Series(dict(r=stats.pearsonr(d.f, d.x48)[0], r24=stats.pearsonr(d.f, d.x24)[0], s24_mean=d.s24.mean()))
    return out
