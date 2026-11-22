def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    # weekday consistency
    dd = []
    for coin in days:
        for w, t in days[coin].items():
            t = t.copy(); t["coin"] = coin; t["w"] = w; dd.append(t)
    dd = pd.concat(dd)
    dd["ts"] = pd.to_datetime(dd["day"])
    dd["wd"] = dd["ts"].dt.dayofweek; dd["yr"] = dd["ts"].dt.year
    dd["sat"] = (dd["wd"] == 5)
    def tt(s):
        s = s.dropna(); return s.mean() / (s.std() / np.sqrt(len(s)))
    g = dd.groupby(["coin", "sat"])["coin_return"].mean().unstack()
    g["t_sat"] = dd[dd.sat].groupby("coin")["coin_return"].apply(tt)
    out["sat_by_coin"] = g
    g = dd.groupby(["yr", "sat"])["coin_return"].mean().unstack()
    g["t_sat"] = dd[dd.sat].groupby("yr")["coin_return"].apply(tt)
    out["sat_by_year"] = g
    # Saturday graded by prior 5-day return?
    rows = []
    H = 10
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = pd.Series(b["close"].values.astype(float))
            n = len(c)
            hi30 = c.rolling(30, min_periods=30).max()
            lo30 = c.rolling(30, min_periods=30).min()
            hi60 = c.rolling(60, min_periods=60).max()
            dh30 = c / hi30 - 1; dh60 = c / hi60 - 1; dl30 = c / lo30 - 1
            vol = c.pct_change().rolling(20).std()
            r30 = c.pct_change(30)
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, dh30=dh30[i], dh60=dh60[i], dl30=dl30[i],
                                 dh30v=dh30[i] / vol[i] if vol[i] > 0 else np.nan, r30=r30[i],
                                 yr=pd.to_datetime(b["timestamp"].iloc[i]).year,
                                 f10=c[i + H] / c[i] - 1))
    d = pd.DataFrame(rows)
    d["f10x"] = d["f10"] - d.groupby("coin")["f10"].transform("mean")
    def tab(col, q=6):
        x = d.dropna(subset=[col]).copy()
        x["b"] = pd.qcut(x[col].rank(method="first"), q, labels=False)
        gg = x.groupby("b")
        t = gg.agg(lo=(col, "min"), hi=(col, "max"), n=("f10x", "size"), f10x=("f10x", "mean"))
        t["t"] = gg["f10x"].apply(tt)
        return t
    out["by_dist_high30"] = tab("dh30")
    out["by_dist_high60"] = tab("dh60")
    out["by_dist_high30_volunits"] = tab("dh30v")
    out["by_dist_low30"] = tab("dl30")
    res = {}
    x = d.dropna(subset=["dh60"])
    for k, gq in x.groupby("coin"):
        s = stats.linregress(gq["dh60"], gq["f10x"]); res[k] = dict(slope=s.slope, t=s.slope / s.stderr, n=len(gq))
    out["dh60_slope_by_coin"] = pd.DataFrame(res).T
    res = {}
    for k, gq in x.groupby("yr"):
        s = stats.linregress(gq["dh60"], gq["f10x"]); res[k] = dict(slope=s.slope, t=s.slope / s.stderr, n=len(gq))
    out["dh60_slope_by_year"] = pd.DataFrame(res).T
    s = stats.linregress(x["dh60"], x["f10x"]); out["dh60_pooled"] = pd.Series(dict(slope=s.slope, t=s.slope / s.stderr, n=len(x)))
    return out
