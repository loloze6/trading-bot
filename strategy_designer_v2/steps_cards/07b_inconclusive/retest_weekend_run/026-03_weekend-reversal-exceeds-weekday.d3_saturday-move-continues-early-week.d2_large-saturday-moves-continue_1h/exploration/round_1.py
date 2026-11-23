def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    drifts = {}
    for coin, wins in data["bars"].items():
        # drift and usual move per horizon, pooled non-overlapping grid
        for h in (24, 48, 72):
            g = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                g.extend(c[idx + h] / c[idx] - 1)
            g = np.array(g)
            drifts[(coin, h)] = (g.mean(), g.std(ddof=1))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            c = df["close"]
            r24 = c / c.shift(24) - 1
            scale = r24.abs().rolling(720, min_periods=360).mean()
            z = r24 / scale
            sel = (ts.dt.hour == 23)
            for i in np.where(sel.values)[0]:
                if np.isnan(z.iloc[i]) or i - 24 < 0:
                    continue
                # day of week whose 24h ends at close (next day 00:00)
                rec = {"coin": coin, "win": w, "year": ts.iloc[i].year,
                       "dow": ts.iloc[i].dayofweek, "z": z.iloc[i],
                       "fc": df["forecast"].iloc[i]}
                for h in (24, 48, 72):
                    if i + h < len(c):
                        m, s = drifts[(coin, h)]
                        f = c.iloc[i + h] / c.iloc[i] - 1
                        rec[f"ex{h}"] = np.sign(z.iloc[i]) * (f - m)
                        rec[f"st{h}"] = rec[f"ex{h}"] / s
                rows.append(rec)
    d = pd.DataFrame(rows)
    out = {}
    def summ(g, col="ex48"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(),
                          "t": x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    # by day of week (dow=5 is Saturday's 24h), horizons
    t = []
    for dw, g in d.groupby("dow"):
        r = {"dow": dw}
        for h in (24, 48, 72):
            s = summ(g, f"ex{h}")
            r[f"n{h}"] = s["n"]; r[f"mean{h}%"] = s["mean%"]; r[f"t{h}"] = s["t"]
        t.append(r)
    out["by_dow_sign_continuation"] = pd.DataFrame(t)
    sat = d[d.dow == 5].copy()
    sat["q"] = pd.qcut(sat["z"].abs(), 5, labels=False)
    out["sat_by_absz_quintile_48"] = sat.groupby("q").apply(summ)
    out["sat_by_absz_quintile_24"] = sat.groupby("q").apply(lambda g: summ(g, "ex24"))
    out["sat_by_coin_48"] = sat.groupby("coin").apply(summ)
    out["sat_by_year_48"] = sat.groupby("year").apply(summ)
    sat["side"] = np.where(sat.z > 0, "up", "down")
    out["sat_by_side_48"] = sat.groupby("side").apply(summ)
    out["sat_by_side_24"] = sat.groupby("side").apply(lambda g: summ(g, "ex24"))
    out["sat_strength_mean"] = pd.Series({h: sat[f"st{h}"].mean() for h in (24, 48, 72)})
    # all weekdays: quintile of |z|, 48h, for comparison
    d["q"] = d.groupby("dow")["z"].transform(lambda s: pd.qcut(s.abs(), 5, labels=False))
    out["top_quintile_by_dow_48"] = d[d.q == 4].groupby("dow").apply(summ)
    return out
