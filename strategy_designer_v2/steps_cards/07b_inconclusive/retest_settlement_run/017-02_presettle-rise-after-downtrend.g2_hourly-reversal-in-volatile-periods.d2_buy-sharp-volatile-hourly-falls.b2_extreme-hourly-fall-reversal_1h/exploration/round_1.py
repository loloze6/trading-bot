def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = [1, 4, 12, 24, 48]
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        acc = {h: [] for h in H}
        for w, df in wins.items():
            c = df["close"].astype(float).values
            for h in H:
                idx = np.arange(0, len(c) - h, h)
                acc[h].extend(list(c[idx + h] / c[idx] - 1))
        drift[coin] = {h: np.mean(acc[h]) for h in H}
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            c = d["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(20).std()
            z = r / vol
            ret24 = c / c.shift(24) - 1
            volreg = vol / vol.rolling(720, min_periods=200).median()
            ts = pd.to_datetime(d["timestamp"])
            cell = np.arange(len(d)) // 24
            tmp = pd.DataFrame({"z": z, "cell": cell})
            tmp = tmp.dropna()
            if tmp.empty:
                continue
            imin = tmp.groupby("cell")["z"].idxmin()
            for i in imin.values:
                rec = {"coin": coin, "w": w, "z": z[i], "fc": d["forecast"].iloc[i],
                       "hour": ts.iloc[i].hour, "year": ts.iloc[i].year,
                       "ret24": ret24[i], "volreg": volreg[i]}
                for h in H:
                    if i + h < len(c):
                        rec["u%d" % h] = c[i + h] / c[i] - 1 - drift[coin][h]
                    else:
                        rec["u%d" % h] = np.nan
                rows.append(rec)
    ev = pd.DataFrame(rows)
    ev["zb"] = pd.cut(ev["z"], [-np.inf, -5, -4, -3, -2.5, -2, -1, 0, np.inf])
    def summ(g, col="u24"):
        x = g[col].dropna()
        n = len(x)
        m = x.mean()
        t = m / (x.std() / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series({"n": n, "mean": m, "t": t})
    out = {}
    out["by_zbucket_h"] = pd.concat({("u%d" % h): ev.groupby("zb").apply(lambda g: summ(g, "u%d" % h)) for h in H}, axis=1)
    sh = ev[ev["z"] <= -2.5].copy()
    out["sharp_by_coin_u24"] = sh.groupby("coin").apply(summ)
    out["sharp_by_year_u24"] = sh.groupby("year").apply(summ)
    sh["settle"] = sh["hour"].isin([23, 0, 7, 8, 15, 16])
    out["sharp_by_settlehour_u24"] = sh.groupby("settle").apply(summ)
    sh["trend"] = pd.cut(sh["ret24"], [-np.inf, -0.05, -0.02, 0, 0.02, np.inf])
    out["sharp_by_prior24_u24"] = sh.groupby("trend").apply(summ)
    out["sharp_by_prior24_u4"] = sh.groupby("trend").apply(lambda g: summ(g, "u4"))
    sh["vr"] = pd.qcut(sh["volreg"], 4)
    out["sharp_by_volregime_u24"] = sh.groupby("vr").apply(summ)
    out["sharp_by_volregime_u4"] = sh.groupby("vr").apply(lambda g: summ(g, "u4"))
    out["corr_z_u24_sharp"] = float(sh[["z", "u24"]].dropna().corr().iloc[0, 1])
    return out
