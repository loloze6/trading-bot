def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    rows = []
    hr_rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            r1 = np.full(n, np.nan); r1[:-1] = c[1:]/c[:-1]-1
            lr = np.log(c)
            ret24p = np.full(n, np.nan); ret24p[24:] = c[24:]/c[:-24]-1
            ret6p = np.full(n, np.nan); ret6p[6:] = c[6:]/c[:-6]-1
            vol168 = pd.Series(np.r_[np.nan, np.diff(lr)]).rolling(168, min_periods=84).std().values
            f24 = np.full(n, np.nan); f24[:-24] = c[24:]/c[:-24]-1
            f6 = np.full(n, np.nan); f6[:-6] = c[6:]/c[:-6]-1
            gain = df["postRebalance_current_allocation"].values * r1
            for i in range(0, n, 24):
                rows.append(dict(coin=coin, w=w, fc=df["forecast"].iloc[i], z24=ret24p[i]/(vol168[i]*np.sqrt(24)) if vol168[i]>0 else np.nan,
                                 z6=ret6p[i]/(vol168[i]*np.sqrt(6)) if vol168[i]>0 else np.nan,
                                 vol=vol168[i], f24=f24[i], hour=ts.iloc[i].hour, wd=ts.iloc[i].weekday(), year=ts.iloc[i].year))
            hr_rows.append(pd.DataFrame(dict(coin=coin, hour=ts.dt.hour.values, wd=ts.dt.weekday.values, r1=r1, gain=gain,
                                             vol=df["volume"].values.astype(float), turn=np.abs(df["postRebalance_current_allocation"].values-df["previous_allocation"].values),
                                             z6=ret6p/(vol168*np.sqrt(6)), f6=f6)))
    g = pd.DataFrame(rows).dropna(subset=["f24"])
    g["ex"] = g["f24"] - g.groupby("coin")["f24"].transform("mean")
    g["fq"] = pd.qcut(g["fc"], 5, labels=False, duplicates="drop")
    out["fc_quintile_next24"] = g.groupby("fq").agg(n=("ex","size"), fc=("fc","mean"), ex_bp=("ex", lambda x: x.mean()*1e4), t=("ex", lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    g["vq"] = g.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    res = []
    for (vq), s in g.dropna(subset=["z24","vq"]).groupby("vq"):
        sl = stats.linregress(-s["z24"], s["ex"]); res.append(dict(vq=vq, n=len(s), slope_bp=sl.slope*1e4, t=sl.slope/sl.stderr))
    out["revslope_by_volterc"] = pd.DataFrame(res)
    res = []
    for c_, s in g.dropna(subset=["z24"]).groupby("coin"):
        sl = stats.linregress(-s["z24"], s["ex"]); res.append(dict(coin=c_, n=len(s), slope_bp=sl.slope*1e4, t=sl.slope/sl.stderr))
    out["revslope_by_coin"] = pd.DataFrame(res)
    res = []
    for y, s in g.dropna(subset=["z24"]).groupby("year"):
        sl = stats.linregress(-s["z24"], s["ex"]); res.append(dict(year=y, n=len(s), slope_bp=sl.slope*1e4, t=sl.slope/sl.stderr))
    out["revslope_by_year"] = pd.DataFrame(res)
    H = pd.concat(hr_rows)
    H["vrel"] = H["vol"]/H.groupby("coin")["vol"].transform("mean")
    out["by_hour"] = H.groupby("hour").agg(r1_bp=("r1", lambda x: x.mean()*1e4), t=("r1", lambda x: x.mean()/x.std()*np.sqrt(x.count())),
                                           gain_bp=("gain", lambda x: x.mean()*1e4), vrel=("vrel","mean"), turn=("turn","mean"))
    out["by_weekday"] = H.groupby("wd").agg(r1_bp=("r1", lambda x: x.mean()*1e4), t=("r1", lambda x: x.mean()/x.std()*np.sqrt(x.count())), gain_bp=("gain", lambda x: x.mean()*1e4))
    # book
    D = pd.concat([d.assign(coin=c) for c in days for d in days[c].values()])
    out["book_daily"] = pd.Series(dict(mean_book=D["book_return"].mean(), mean_coin=D["coin_return"].mean(), turn_per_bar=H["turn"].mean()))
    return out
