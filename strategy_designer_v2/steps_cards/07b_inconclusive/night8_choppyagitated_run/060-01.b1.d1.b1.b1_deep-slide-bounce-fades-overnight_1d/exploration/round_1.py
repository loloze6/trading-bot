def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        # coin mean daily return over all visible windows
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            allr.append(c[1:] / c[:-1] - 1)
        mu = np.nanmean(np.concatenate(allr)) if allr else np.nan
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            r = np.r_[np.nan, c[1:] / c[:-1] - 1]
            sd30 = pd.Series(r).rolling(30, min_periods=20).std().values
            f = b["forecast"].astype(float).values
            ts = pd.to_datetime(b["timestamp"])
            n = len(c)
            for i in range(n):
                if f[i] < 0:
                    d = {}
                    for h in (1, 2, 3, 5):
                        d[f"r{h}"] = c[i + h] / c[i] - 1 - h * mu if i + h < n else np.nan
                    up = r[i]
                    fall5 = c[i - 1] / c[i - 6] - 1 if i >= 6 else np.nan
                    rows.append(dict(coin=coin, win=w, year=ts.iloc[i].year, day=ts.iloc[i].normalize(),
                                     f=f[i], up=up, upz=up / sd30[i] if sd30[i] > 0 else np.nan,
                                     fallz=fall5 / sd30[i - 1] if i >= 6 and sd30[i - 1] > 0 else np.nan,
                                     sd=sd30[i], **d))
    df = pd.DataFrame(rows)
    out = {}
    def summ(g):
        res = {}
        for h in (1, 2, 3, 5):
            x = -g[f"r{h}"].dropna()
            res[f"mean_gain_h{h}"] = x.mean()
            res[f"t_h{h}"] = x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan
        res["n"] = len(g)
        return pd.Series(res)
    out["all"] = summ(df)
    out["by_coin"] = df.groupby("coin").apply(summ)
    out["by_window"] = df.groupby("win").apply(summ)
    out["by_year"] = df.groupby("year").apply(summ)
    df["fq"] = pd.qcut(df["f"].rank(method="first"), 5, labels=["q1_deepest", "q2", "q3", "q4", "q5_shallow"])
    out["by_forecast_quintile"] = df.groupby("fq").apply(summ)
    d2 = df.dropna(subset=["fallz"])
    d2["fzq"] = pd.qcut(d2["fallz"].rank(method="first"), 5, labels=["q1_deepest", "q2", "q3", "q4", "q5_shallow"])
    out["by_rawfallz_quintile"] = d2.groupby("fzq").apply(summ)
    d3 = df.dropna(subset=["upz"])
    d3["uq"] = pd.qcut(d3["upz"].rank(method="first"), 5, labels=["q1_small", "q2", "q3", "q4", "q5_large"])
    out["by_upz_quintile"] = d3.groupby("uq").apply(summ)
    d4 = df.dropna(subset=["sd"])
    d4["sq"] = pd.qcut(d4["sd"].rank(method="first"), 3, labels=["low_vol", "mid", "high_vol"])
    out["by_vol_tercile"] = d4.groupby("sq").apply(summ)
    # daily-summed t for h1 weighted by forecast/10
    df["wg"] = df["f"] / 10 * df["r1"]
    ds = df.dropna(subset=["wg"]).groupby("day")["wg"].sum()
    out["weighted_h1_daysum"] = pd.Series({"mean": ds.mean(), "t": ds.mean() / (ds.std(ddof=1) / np.sqrt(len(ds))), "days": len(ds)})
    # per-day summed t for unweighted gains at each h
    tt = {}
    for h in (1, 2, 3, 5):
        s = (-df[f"r{h}"]).dropna().groupby(df["day"]).mean()
        tt[f"h{h}"] = pd.Series({"mean": s.mean(), "t": s.mean() / (s.std(ddof=1) / np.sqrt(len(s))), "days": len(s)})
    out["unweighted_daymean_by_h"] = pd.DataFrame(tt)
    return out
