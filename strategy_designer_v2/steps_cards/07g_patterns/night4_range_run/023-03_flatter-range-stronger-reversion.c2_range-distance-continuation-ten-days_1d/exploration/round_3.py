def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    def tt(s):
        s = s.dropna(); return s.mean() / (s.std() / np.sqrt(len(s)))
    H = 10
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = pd.Series(b["close"].values.astype(float)); n = len(c)
            hi30 = c.rolling(30, min_periods=30).max()
            lo30 = c.rolling(30, min_periods=30).min()
            pos = 2 * (c - lo30) / (hi30 - lo30) - 1
            # days since 30-day high
            dsh = c.rolling(30, min_periods=30).apply(lambda a: len(a) - 1 - np.argmax(a), raw=True)
            r60 = c.pct_change(60); r30 = c.pct_change(30)
            r1 = c.pct_change()
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, pos=pos[i], dsh=dsh[i], r60=r60[i], r30=r30[i],
                                 newhi=float(c[i] >= hi30[i]) if not np.isnan(hi30[i]) else np.nan,
                                 r1=r1[i], f10=c[i + H] / c[i] - 1))
    d = pd.DataFrame(rows)
    d["f10x"] = d["f10"] - d.groupby("coin")["f10"].transform("mean")
    x = d.dropna(subset=["dsh"])
    x["dshb"] = pd.cut(x["dsh"], [-1, 0, 2, 5, 10, 20, 30])
    g = x.groupby("dshb")
    out["by_days_since_high30"] = pd.DataFrame({"n": g["f10x"].size(), "f10x": g["f10x"].mean(), "t": g["f10x"].apply(tt)})
    nh = x[x.dsh == 0]
    out["newhigh_by_coin"] = pd.DataFrame({"n": nh.groupby("coin")["f10x"].size(), "f10x": nh.groupby("coin")["f10x"].mean(),
                                           "t": nh.groupby("coin")["f10x"].apply(tt)})
    # pos slope split by own 60-day return sign
    y = d.dropna(subset=["pos", "r60"]).copy()
    y["reg"] = np.where(y["r60"] > 0, "r60_up", "r60_down")
    res = {}
    for k, gq in y.groupby("reg"):
        s = stats.linregress(gq["pos"], gq["f10x"]); res[k] = dict(slope=s.slope, t=s.slope / s.stderr, n=len(gq))
    out["pos_slope_by_r60_sign"] = pd.DataFrame(res).T
    # Saturday graded by prior 7-day return
    dd = []
    for coin in days:
        for w, t in days[coin].items():
            t = t.copy().reset_index(drop=True)
            t["r7"] = t["close"].pct_change(7)
            t["coin"] = coin; dd.append(t)
    dd = pd.concat(dd)
    dd["wd"] = pd.to_datetime(dd["day"]).dt.dayofweek
    s = dd[dd.wd == 5].dropna(subset=["r7", "coin_return"]).copy()
    s["q"] = pd.qcut(s["r7"], 5, labels=False)
    g = s.groupby("q")
    out["sat_by_prior7d"] = pd.DataFrame({"n": g["coin_return"].size(), "mean": g["coin_return"].mean(), "t": g["coin_return"].apply(tt)})
    # weekend vs weekdays pooled: Fri+Sat vs rest
    dd["fs"] = dd.wd.isin([4, 5])
    out["fri_sat_vs_rest"] = pd.DataFrame({"mean": dd.groupby("fs")["coin_return"].mean(), "n": dd.groupby("fs")["coin_return"].count()})
    out["sat_minus_rest_welch_t"] = float(stats.ttest_ind(dd.loc[dd.wd == 5, "coin_return"].dropna(), dd.loc[dd.wd != 5, "coin_return"].dropna(), equal_var=False).statistic)
    return out
