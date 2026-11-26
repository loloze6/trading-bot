def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            z5 = (c / c.shift(5) - 1) / (sd30 * np.sqrt(5))
            tr60 = 100 * (c / c.shift(60) - 1)
            f5 = c.shift(-5) / c - 1
            clpos = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "day": ts.dt.floor("D"),
                "yr": ts.dt.year, "z5": z5, "tr60": tr60, "f5": f5, "clpos": clpos,
                "cc": (b["regime"] == "unknown").astype(int)}))
    d = pd.concat(rows, ignore_index=True)
    g = d[d["pos"] % 5 == 0].dropna(subset=["f5"]).copy()
    g["ex"] = g["f5"] - g.groupby("coin")["f5"].transform("mean")
    g["trend"] = np.where(g.tr60 > 10, "rising", np.where(g.tr60 < -10, "falling", "choppy"))
    g.loc[g.tr60.isna(), "trend"] = "na"
    def slope(s, x):
        s = s.dropna(subset=[x, "ex"])
        if len(s) < 20: return pd.Series({"n": len(s)})
        xs = s[x] - s[x].mean()
        b = (xs * s["ex"]).sum() / (xs ** 2).sum()
        res = s["ex"] - s["ex"].mean() - b * xs
        sc = pd.Series((xs * res).values).groupby(s["day"].values).sum()
        se = np.sqrt((sc ** 2).sum()) / (xs ** 2).sum()
        return pd.Series({"n": len(s), "days": s["day"].nunique(), "slope_%_per_unit": 100 * b, "t_day": b / se})
    out = {}
    out["slope ex on z5, all"] = slope(g, "z5")
    out["slope ex on z5 by trend"] = g.groupby("trend").apply(lambda s: slope(s, "z5"))
    out["slope ex on z5 by year"] = g.groupby("yr").apply(lambda s: slope(s, "z5"))
    out["slope ex on z5 by coin"] = g.groupby("coin").apply(lambda s: slope(s, "z5"))
    out["slope ex on z5, choppy calm"] = slope(g[g.cc == 1], "z5")
    out["slope ex on z5, falls only, all"] = slope(g[g.z5 < 0], "z5")
    out["slope ex on z5, rises only, all"] = slope(g[g.z5 > 0], "z5")
    out["slope ex on clpos by trend"] = g.groupby("trend").apply(lambda s: slope(s, "clpos"))
    return out
