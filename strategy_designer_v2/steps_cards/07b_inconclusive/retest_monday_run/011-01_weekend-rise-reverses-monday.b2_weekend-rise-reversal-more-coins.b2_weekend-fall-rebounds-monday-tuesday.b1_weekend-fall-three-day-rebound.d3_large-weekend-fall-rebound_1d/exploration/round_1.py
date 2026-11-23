def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        # coin mean h-bar return over non-overlapping grid of all windows
        grid = {h: [] for h in (1, 2, 3, 5)}
        per = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            for h in grid:
                idx = np.arange(0, n - h, h)
                grid[h].extend(list(c[idx + h] / c[idx] - 1))
            r = pd.Series(c).pct_change()
            vol = r.rolling(20, min_periods=20).std()
            z = r / vol
            ts = pd.to_datetime(df["timestamp"])
            wd = ts.dt.weekday.values
            fc = df["forecast"].astype(float).values
            for t in range(n):
                rec = {"coin": coin, "win": w, "year": ts.iloc[t].year, "wd": wd[t],
                       "z": z.iloc[t], "fc": fc[t], "vol": vol.iloc[t]}
                for h in grid:
                    rec[f"r{h}"] = c[t + h] / c[t] - 1 if t + h < n else np.nan
                per.append(rec)
        p = pd.DataFrame(per)
        for h in grid:
            p[f"x{h}"] = p[f"r{h}"] - np.nanmean(grid[h])
        rows.append(p)
    a = pd.concat(rows, ignore_index=True)
    out = {}
    def summ(g, col="x3"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    cases = a[(a.wd == 6) & (a.fc >= 2) & a.x3.notna()].copy()
    out["n_cases"] = len(cases)
    cases["q"] = pd.qcut(cases.fc.rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["by_fc_quartile"] = cases.groupby("q").apply(lambda g: pd.concat([summ(g), pd.Series({"fc_mean": g.fc.mean(), "z_mean": g.z.mean()})]))
    out["cases_by_horizon"] = pd.DataFrame({h: summ(cases, f"x{h}") for h in (1, 2, 3, 5)}).T
    out["cases_by_year"] = cases.groupby("year").apply(summ)
    out["cases_by_coin"] = cases.groupby("coin").apply(summ)
    # all Sundays by z bins and all weekdays by z bins (falls), 3-day excess
    a["zb"] = pd.cut(a.z, [-np.inf, -3, -2, -1.5, -1, -0.5, 0, 0.5, 1, 2, np.inf])
    sun = a[a.wd == 6]
    out["sunday_by_zbin"] = sun.groupby("zb").apply(summ)
    oth = a[a.wd != 6]
    out["otherdays_by_zbin"] = oth.groupby("zb").apply(summ)
    falls = a[a.z < -1]
    out["falls_z<-1_by_weekday"] = falls.groupby("wd").apply(summ)
    falls2 = a[a.z < -2]
    out["falls_z<-2_by_weekday"] = falls2.groupby("wd").apply(summ)
    # vol regime of cases: high vs low vol relative to coin median
    a["volrel"] = a.vol / a.groupby("coin").vol.transform("median")
    cases = cases.join(a["volrel"])
    cases["vq"] = pd.qcut(cases.volrel, 3, labels=["lowvol", "midvol", "highvol"])
    out["cases_by_volregime"] = cases.groupby("vq").apply(summ)
    return out
