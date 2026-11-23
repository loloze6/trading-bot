def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        # coin mean h-bar return on non-overlapping grid, pooled
        for h in (1, 2, 3, 5):
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rr.extend(list(c[idx + h] / c[idx] - 1))
            drift[(coin, h)] = np.mean(rr) if rr else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            c = df["close"]
            r1 = c.pct_change()
            sd = r1.rolling(60, min_periods=20).std()
            mu = r1.rolling(60, min_periods=20).mean()
            z = (r1 - mu) / sd
            vol = df["volume"]
            vrel = vol / vol.rolling(60, min_periods=20).median()
            year = ts.dt.year
            dow = ts.dt.dayofweek
            n = len(df)
            for t in range(n):
                if np.isnan(z.iloc[t]) or z.iloc[t] >= 0:
                    continue
                rec = {"coin": coin, "win": w, "year": year.iloc[t], "dow": dow.iloc[t],
                       "fz": -z.iloc[t], "r1": r1.iloc[t], "vrel": vrel.iloc[t],
                       "fc": df["forecast"].iloc[t]}
                for h in (1, 2, 3, 5):
                    if t + h < n:
                        rec[f"x{h}"] = c.iloc[t + h] / c.iloc[t] - 1 - drift[(coin, h)]
                    else:
                        rec[f"x{h}"] = np.nan
                # day-2 alone (Tuesday) return
                if t + 2 < n:
                    rec["d2"] = c.iloc[t + 2] / c.iloc[t + 1] - 1 - drift[(coin, 1)]
                else:
                    rec["d2"] = np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    def summ(g, col="x2"):
        v = g[col].dropna()
        return pd.Series({"n": len(v), "mean%": 100 * v.mean(),
                          "t": v.mean() / (v.std() / np.sqrt(len(v))) if len(v) > 2 else np.nan})
    out = {}
    out["by_dow_x2"] = d.groupby("dow").apply(summ)
    sun = d[d.dow == 6].copy()
    out["sun_horizons"] = pd.DataFrame({h: summ(sun, h) for h in ["x1", "d2", "x2", "x3", "x5"]}).T
    wk = d[d.dow < 5]
    out["wkday_horizons"] = pd.DataFrame({h: summ(wk, h) for h in ["x1", "d2", "x2", "x3", "x5"]}).T
    sun["fq"] = pd.qcut(sun.fz, 5, labels=False)
    wk = wk.copy(); wk["fq"] = pd.cut(wk.fz, bins=pd.qcut(sun.fz, 5, retbins=True)[1], labels=False, include_lowest=True)
    out["sun_by_fallquint"] = sun.groupby("fq").apply(summ).join(sun.groupby("fq").fz.mean().rename("fz"))
    out["wk_by_fallquint"] = wk.groupby("fq").apply(summ)
    out["sun_by_year"] = sun.groupby("year").apply(summ)
    out["sun_by_coin"] = sun.groupby("coin").apply(summ)
    sun["vq"] = pd.qcut(sun.vrel, 3, labels=False)
    out["sun_by_volterc"] = sun.groupby("vq").apply(summ)
    big = sun[sun.fz > sun.fz.quantile(0.6)]
    out["sun_bigfall_by_volterc"] = big.groupby("vq").apply(summ)
    out["sun_corr_fz_x2"] = float(sun[["fz", "x2"]].dropna().corr().iloc[0, 1])
    return out
