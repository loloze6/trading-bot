def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    H = [2, 3, 4, 5, 7]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            rng = ((h - l) / c).rolling(30, min_periods=20).mean()
            s3 = (c / c.shift(3) - 1) / rng
            r60 = c / c.shift(60) - 1
            ret = c.pct_change()
            v30 = ret.rolling(30, min_periods=20).std()
            vpct = v30.rolling(365, min_periods=60).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            yr = pd.to_datetime(b["timestamp"]).dt.year
            day = pd.to_datetime(b["timestamp"]).dt.floor("D")
            for hh in H:
                fwd = c.shift(-hh) / c - 1
                for i in range(0, len(b), hh):
                    if i + hh >= len(b): continue
                    rows.append(dict(coin=coin, w=w, year=int(yr.iloc[i]), h=hh, day=day.iloc[i],
                                     s3=s3.iloc[i], fwd=fwd.iloc[i], r60=r60.iloc[i], vp=vpct.iloc[i]))
    df = pd.DataFrame(rows).dropna(subset=["fwd", "s3"])
    df["drift"] = df.groupby(["coin", "h"])["fwd"].transform("mean")
    df["ex"] = df["fwd"] - df["drift"]
    df["trend"] = np.where(df.r60 > 0.1, "rising", np.where(df.r60 < -0.1, "falling", "choppy"))
    df["agit"] = np.where(df.vp.isna(), "na", np.where(df.vp > 0.5, "agitated", "calm"))
    out = {}
    def summ(x):
        x = x.dropna(subset=["ex"])
        n = len(x)
        if n < 10:
            return pd.Series({"n": n})
        ds = x.groupby("day")["ex"].sum()
        tday = ds.mean() / (ds.std() / np.sqrt(len(ds)))
        sl = stats.linregress(x["s3"], x["ex"])
        return pd.Series({"n": n, "days": len(ds), "mean%": 100 * x["ex"].mean(), "t_day": tday,
                          "slope_t": sl.slope / sl.stderr})
    up = df[df.s3 > 0]
    out["up cells by horizon"] = up.groupby("h").apply(summ)
    u3 = up[up.h == 3]
    out["h3 up by year"] = u3.groupby("year").apply(summ)
    out["h3 up by trend"] = u3.groupby("trend").apply(summ)
    out["h3 up by agitation"] = u3.groupby("agit").apply(summ)
    out["h3 up by coin"] = u3.groupby("coin").apply(summ)
    u7 = up[up.h == 7]
    out["h7 up by agitation"] = u7.groupby("agit").apply(summ)
    out["h7 up by trend x agit"] = u7.groupby(["trend", "agit"]).apply(summ)
    out["h3 up by trend x agit"] = u3.groupby(["trend", "agit"]).apply(summ)
    return out
