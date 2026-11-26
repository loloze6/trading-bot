def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        # coin normal drift per horizon over all windows, non-overlapping
        for h in (1, 2, 3, 5):
            vals = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    vals.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = (np.mean(vals), np.std(vals, ddof=1))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r = c.pct_change()
            vol = r.rolling(20).std().shift(1)
            z = r / vol
            r20 = c / c.shift(20) - 1
            vol20_rel = r.rolling(20).std() / r.rolling(60).std()
            n = len(c)
            for i in range(n):
                if pd.isna(z.iloc[i]):
                    continue
                if abs(z.iloc[i]) < 2:
                    continue
                rec = {"coin": coin, "win": w, "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                       "z": z.iloc[i], "r20": r20.iloc[i], "volrel": vol20_rel.iloc[i],
                       "day": pd.Timestamp(df["timestamp"].iloc[i]).floor("D")}
                for h in (1, 2, 3, 5):
                    if i + h < n:
                        m, s = drift[(coin, h)]
                        rec[f"u{h}"] = c.iloc[i + h] / c.iloc[i] - 1 - m
                        rec[f"s{h}"] = (c.iloc[i + h] / c.iloc[i] - 1 - m) / s
                rows.append(rec)
    ev = pd.DataFrame(rows)

    def summ(g, col):
        g = g.dropna(subset=[col])
        if len(g) < 3:
            return pd.Series({"n": len(g), "days": g["day"].nunique() if len(g) else 0, "mean%": np.nan, "t": np.nan})
        d = g.groupby("day")[col].sum()
        nd = len(d)
        mean = g[col].mean()
        se = d.std(ddof=1) * np.sqrt(nd) / len(g) if nd > 1 else np.nan
        return pd.Series({"n": len(g), "days": nd, "mean%": 100 * mean, "t": mean / se if se else np.nan})

    out = {}
    fall = ev[ev.z <= -2].copy()
    rise = ev[ev.z >= 2].copy()
    hz = {}
    for h in (1, 2, 3, 5):
        hz[f"fall_h{h}"] = summ(fall, f"u{h}")
        hz[f"rise_h{h}"] = summ(rise, f"u{h}")
    out["by horizon, side (unusual move, long view)"] = pd.DataFrame(hz).T
    fall["zb"] = pd.cut(fall.z, [-np.inf, -4, -3, -2.5, -2])
    out["fall by z bucket h2"] = fall.groupby("zb", observed=True).apply(lambda g: summ(g, "u2"))
    out["fall by coin h2"] = fall.groupby("coin").apply(lambda g: summ(g, "u2"))
    out["fall by window h2"] = fall.groupby("win").apply(lambda g: summ(g, "u2"))
    out["fall by year h2"] = fall.groupby("year").apply(lambda g: summ(g, "u2"))
    fall["trend"] = np.where(fall.r20 < 0, "20d down", "20d up")
    out["fall by 20d trend h2"] = fall.groupby("trend").apply(lambda g: summ(g, "u2"))
    out["fall by 20d trend h5"] = fall.groupby("trend").apply(lambda g: summ(g, "u5"))
    fall["r20q"] = pd.qcut(fall.r20, 4)
    out["fall by r20 quartile h2"] = fall.groupby("r20q", observed=True).apply(lambda g: summ(g, "u2"))
    fall["vq"] = pd.qcut(fall.volrel, 3)
    out["fall by vol rel (20/60) h2"] = fall.groupby("vq", observed=True).apply(lambda g: summ(g, "u2"))
    sl = fall.dropna(subset=["u2"])
    res = stats.linregress(-sl.z, sl.u2)
    out["slope u2 on -z"] = f"slope {res.slope:.5f} t {res.slope/res.stderr:.2f} n {len(sl)}"
    sl = fall.dropna(subset=["u1"])
    res = stats.linregress(-sl.z, sl.u1)
    out["slope u1 on -z"] = f"slope {res.slope:.5f} t {res.slope/res.stderr:.2f} n {len(sl)}"
    out["fall share of cases by day breadth"] = fall.groupby("day").size().value_counts().sort_index()
    return out
