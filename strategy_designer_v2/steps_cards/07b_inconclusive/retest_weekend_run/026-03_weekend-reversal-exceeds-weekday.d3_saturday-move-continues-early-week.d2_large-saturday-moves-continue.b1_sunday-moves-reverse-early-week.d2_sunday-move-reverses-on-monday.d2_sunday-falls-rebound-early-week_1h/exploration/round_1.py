def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift48 = {}; drift24 = {}; sd48 = {}
    for coin, wins in bars.items():
        r48 = []; r24 = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 48, 48)
            r48 += list(c[idx + 48] / c[idx] - 1)
            idx = np.arange(0, len(c) - 24, 24)
            r24 += list(c[idx + 24] / c[idx] - 1)
        drift48[coin] = np.mean(r48); drift24[coin] = np.mean(r24); sd48[coin] = np.std(r48)
        for w, df in wins.items():
            ts = pd.to_datetime(df["timestamp"])
            c = df["close"].values
            lr = np.log(c[1:] / c[:-1])
            hv = pd.Series(np.r_[np.nan, lr]).rolling(720, min_periods=500).std().values
            past24 = pd.Series(c).pct_change(24).abs()
            mabs = past24.rolling(720, min_periods=500).mean().values
            n = len(c)
            wd = ts.dt.weekday.values; hr = ts.dt.hour.values
            fc = df["forecast"].values
            year = ts.dt.year.values
            for i in range(24, n - 48):
                if hr[i] == 23 and wd[i] in (6, 2):
                    s24 = c[i] / c[i - 24] - 1
                    rows.append(dict(coin=coin, win=w, year=year[i], day="Sun" if wd[i] == 6 else "Wed",
                                     s24=s24, sc=s24 / mabs[i] if mabs[i] > 0 else np.nan, hv=hv[i],
                                     f=fc[i], x48=c[i + 48] / c[i] - 1 - drift48[coin],
                                     x24=c[i + 24] / c[i] - 1 - drift24[coin],
                                     x24b=c[i + 48] / c[i + 24] - 1 - drift24[coin]))
    d = pd.DataFrame(rows).dropna(subset=["sc"])
    def summ(g, col="x48"):
        v = g[col].dropna()
        return pd.Series(dict(n=len(v), mean=v.mean(), t=v.mean() / (v.std() / np.sqrt(len(v))) if len(v) > 2 else np.nan))
    out = {}
    sun = d[d.day == "Sun"]; wed = d[d.day == "Wed"]
    cases = sun[sun.f >= 2]
    out["cases_overall"] = pd.DataFrame({k: summ(cases, k) for k in ["x48", "x24", "x24b"]})
    out["cases_by_coin"] = cases.groupby("coin").apply(summ)
    out["cases_by_year"] = cases.groupby("year").apply(summ)
    cases = cases.assign(fq=pd.qcut(cases.f, 4, labels=False, duplicates="drop"))
    out["cases_by_forecast_q"] = cases.groupby("fq").apply(summ)
    # all Sundays and all Wednesdays: by scaled move quintile, signed reversal x48
    for nm, g in [("sun", sun), ("wed", wed)]:
        g = g.assign(q=pd.qcut(g.sc, 5, labels=False))
        out[f"{nm}_by_scaled_q"] = g.groupby("q").apply(lambda h: pd.concat([summ(h), pd.Series(dict(sc=h.sc.mean()))]))
        out[f"{nm}_corr_sc_x48"] = pd.Series(dict(r=stats.pearsonr(g.sc, g.x48)[0], n=len(g),
                                                  r24=stats.pearsonr(g.sc, g.x24)[0]))
    # falls by vol tercile within each coin
    sf = sun[sun.s24 < 0].copy()
    sf["vq"] = sf.groupby("coin").hv.transform(lambda v: pd.qcut(v, 3, labels=False))
    out["sun_falls_by_vol_tercile"] = sf.groupby("vq").apply(summ)
    sr = sun[sun.s24 > 0].copy()
    out["sun_rises_x48"] = summ(sr)
    out["sd48"] = pd.Series(sd48)
    return out
