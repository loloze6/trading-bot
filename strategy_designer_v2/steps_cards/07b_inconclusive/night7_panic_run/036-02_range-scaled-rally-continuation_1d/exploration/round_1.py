def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    H = [1, 3, 7, 14]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            rng = ((h - l) / c).rolling(30, min_periods=20).mean()
            s3 = (c / c.shift(3) - 1) / rng
            r60 = c / c.shift(60) - 1
            vol30 = c.pct_change().rolling(30, min_periods=20).std()
            fc = b["forecast"].astype(float)
            yr = pd.to_datetime(b["timestamp"]).dt.year
            for hh in H:
                fwd = c.shift(-hh) / c - 1
                idx = np.arange(0, len(b), hh)
                for i in idx:
                    if i + hh >= len(b): continue
                    rows.append(dict(coin=coin, w=w, year=int(yr.iloc[i]), h=hh, i=i,
                                     s3=s3.iloc[i], fc=fc.iloc[i], fwd=fwd.iloc[i], r60=r60.iloc[i],
                                     ts=b["timestamp"].iloc[i]))
    df = pd.DataFrame(rows).dropna(subset=["fwd"])
    df["drift"] = df.groupby(["coin", "h"])["fwd"].transform("mean")
    df["ex"] = df["fwd"] - df["drift"]
    out = {}
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    d = df.dropna(subset=["s3"]).copy()
    d["q"] = d.groupby("h")["s3"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["excess by s3 quintile x horizon"] = d.groupby(["h", "q"])["ex"].apply(tt).unstack()
    corr = []
    for hh in H:
        x = d[d.h == hh]
        r, p = stats.spearmanr(x["s3"], x["ex"])
        sl = stats.linregress(x["s3"], x["ex"])
        corr.append(dict(h=hh, n=len(x), spearman=r, slope_t=sl.slope / sl.stderr))
    out["s3 vs excess, all cells"] = pd.DataFrame(corr)
    p7 = d[(d.h == 7) & (d.fc > 0)]
    out["fc>0 h7 by coin"] = p7.groupby("coin")["ex"].apply(tt).unstack()
    out["fc>0 h7 by year"] = p7.groupby("year")["ex"].apply(tt).unstack()
    p7 = p7.copy()
    p7["trend"] = np.where(p7.r60 > 0.1, "rising", np.where(p7.r60 < -0.1, "falling", "choppy"))
    out["fc>0 h7 by trend"] = p7.groupby("trend")["ex"].apply(tt).unstack()
    p7["fq"] = pd.qcut(p7["fc"].rank(method="first"), 4, labels=False)
    out["fc>0 h7 by fc quartile"] = p7.groupby("fq")["ex"].apply(tt).unstack()
    a7 = d[d.h == 7].copy()
    a7["trend"] = np.where(a7.r60 > 0.1, "rising", np.where(a7.r60 < -0.1, "falling", "choppy"))
    a7["side"] = np.where(a7.s3 > 0, "up", "down")
    out["all h7 by trend x side"] = a7.groupby(["trend", "side"])["ex"].apply(tt).unstack()
    return out
