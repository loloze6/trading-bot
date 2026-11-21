def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(240, min_periods=200).std()
            vrank = vol.rolling(720, min_periods=300).apply(lambda x: (x[:-1] < x[-1]).mean(), raw=True)
            d = pd.DataFrame({"coin": coin, "w": w, "yr": ts.dt.year.values,
                              "hc": ((ts + pd.Timedelta(hours=1)).dt.hour).values,
                              "wd": (ts + pd.Timedelta(hours=1)).dt.weekday.values,
                              "f1": (c.shift(-1)/c - 1).values,
                              "f24": (c.shift(-24)/c - 1).values,
                              "p24": (c/c.shift(24) - 1).values,
                              "vol": vol.values, "vr": vrank.values})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["f24x"] = D["f24"] - D.groupby("coin")["f24"].transform("mean")
    D["f1x"] = D["f1"] - D.groupby("coin")["f1"].transform("mean")
    S = D[D.hc == 20].dropna(subset=["f24x", "p24", "vr"]).copy()
    S["z"] = -S["p24"]/S.groupby("coin")["p24"].transform("std")
    S["vb"] = pd.cut(S["vr"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01], labels=["v1", "v2", "v3", "v4", "v5"])
    def reg(g):
        sl = stats.linregress(g["z"], g["f24x"])
        return pd.Series({"n": len(g), "slope_bp": sl.slope*1e4, "t": sl.slope/sl.stderr})
    out["slope_by_volbin_hc20"] = S.groupby("vb").apply(reg).round(2)
    out["slope_hi_by_coin"] = S[S.vr >= 0.5].groupby("coin").apply(reg).round(2)
    out["slope_hi_by_year"] = S[S.vr >= 0.5].groupby("yr").apply(reg).round(2)
    out["slope_lo_by_year"] = S[S.vr < 0.5].groupby("yr").apply(reg).round(2)
    out["slope_lo_by_coin"] = S[S.vr < 0.5].groupby("coin").apply(reg).round(2)
    E = D.dropna(subset=["f1x"])
    def tt(g):
        return pd.Series({"n": len(g), "mean_bp": g.f1x.mean()*1e4, "t": g.f1x.mean()/(g.f1x.std()/np.sqrt(len(g)))})
    out["bar21_22_by_year"] = E[E.hc.isin([21, 22])].groupby("yr").apply(tt).round(2)
    out["bar21_22_by_coin"] = E[E.hc.isin([21, 22])].groupby("coin").apply(tt).round(2)
    out["bar21_22_by_weekday"] = E[E.hc.isin([21, 22])].groupby("wd").apply(tt).round(2)
    return out
