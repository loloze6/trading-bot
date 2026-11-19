def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        g = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 2, 2)
            g.append(c[idx + 2] / c[idx] - 1)
        mu2 = np.concatenate(g).mean()
        for w, df in wins.items():
            d = df[["timestamp", "close"]].copy().reset_index(drop=True)
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            c = d["close"]
            d["r72"] = c / c.shift(72) - 1
            d["f2"] = c.shift(-2) / c - 1 - mu2
            d["hour"] = d["ts"].dt.hour
            d["year"] = d["ts"].dt.year
            d["wd"] = d["ts"].dt.weekday
            d["coin"] = coin
            rows.append(d)
    A = pd.concat(rows, ignore_index=True).dropna(subset=["r72", "f2"])
    def sl(x):
        if len(x) < 30: return pd.Series({"n": len(x), "slope_t": np.nan, "rho": np.nan, "mean_up_bp": np.nan})
        s = stats.linregress(x.r72, x.f2)
        rho = stats.spearmanr(x.r72, x.f2).correlation
        up = x[x.r72 > 0]
        return pd.Series({"n": len(x), "slope_t": s.slope / s.stderr, "rho": rho,
                          "mean_up_bp": up.f2.mean() * 1e4})
    out = {}
    H = A[A.hour == 12]
    out["h12_by_coin"] = H.groupby("coin").apply(sl)
    out["h12_by_year"] = H.groupby("year").apply(sl)
    out["h12_weekend_vs_weekday"] = H.groupby(H.wd >= 5).apply(sl)
    H13 = A[A.hour == 13]
    out["h13_by_coin"] = H13.groupby("coin").apply(sl)
    out["h13_by_year"] = H13.groupby("year").apply(sl)
    H15 = A[A.hour == 15]
    out["h15_by_year"] = H15.groupby("year").apply(sl)
    S = A[A.hour.isin([21, 5, 13])]
    out["settle_pooled_spearman_by_hour"] = S.groupby("hour").apply(sl)
    return out
