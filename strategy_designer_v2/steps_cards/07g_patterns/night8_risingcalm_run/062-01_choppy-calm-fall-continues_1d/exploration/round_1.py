def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            r5p = c / c.shift(5) - 1
            z5 = r5p / (sd30 * np.sqrt(5))
            r3p = c / c.shift(3) - 1
            z1 = r1 / sd30
            r10p = c / c.shift(10) - 1
            z10 = r10p / (sd30 * np.sqrt(10))
            f5 = c.shift(-5) / c - 1
            f1 = c.shift(-1) / c - 1
            rng = (b["high"] - b["low"]) / c / sd30
            clpos = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            idx = np.arange(len(b))
            df = pd.DataFrame({"coin": coin, "w": w, "pos": idx, "day": ts.dt.floor("D"),
                               "wd": ts.dt.weekday, "z5": z5, "z1": z1, "z10": z10, "f5": f5, "f1": f1,
                               "rng": rng, "clpos": clpos, "sd30": sd30,
                               "cc": (b["regime"] == "unknown").astype(int),
                               "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"]})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    g = d[d["pos"] % 5 == 0].dropna(subset=["f5"]).copy()
    g["drift"] = g.groupby("coin")["f5"].transform("mean")
    g["ex"] = g["f5"] - g["drift"]
    def tday(s, days):
        x = pd.Series(s.values).groupby(days.values).sum()
        n = len(x); 
        if n < 3: return np.nan
        return s.mean() / (x.std(ddof=1) * np.sqrt(n) / len(s)) if x.std() > 0 else np.nan
    def tab(sub, col, q=5):
        s = sub.dropna(subset=[col]).copy()
        s["b"] = pd.qcut(s[col], q, labels=False, duplicates="drop")
        out = s.groupby("b").apply(lambda x: pd.Series({"lo": x[col].min(), "hi": x[col].max(), "n": len(x),
                         "mean_ex_%": 100 * x["ex"].mean(), "t_day": tday(x["ex"], x["day"])}))
        return out
    res = {}
    res["z5 quintiles, all bars, ex 5d"] = tab(g, "z5")
    res["z5 quintiles, choppy calm"] = tab(g[g.cc == 1], "z5")
    res["z5 quintiles, outside cc"] = tab(g[g.cc == 0], "z5")
    res["z10 quintiles, all"] = tab(g, "z10")
    res["z1 quintiles, all"] = tab(g, "z1")
    res["range/sd30 quintiles, all"] = tab(g, "rng")
    res["close position quintiles, all"] = tab(g, "clpos")
    res["sd30 quintiles, all"] = tab(g, "sd30")
    # weekday on 1-day returns
    d1 = d.dropna(subset=["f1"]).copy()
    d1["ex1"] = d1["f1"] - d1.groupby("coin")["f1"].transform("mean")
    res["weekday next-day ex %"] = d1.groupby("wd").apply(lambda x: pd.Series({"n": len(x), "mean_%": 100*x["ex1"].mean(),
                     "t_day": tday(x["ex1"], x["day"])}))
    res["by window, cc share and ex in cc short cases"] = g[(g.cc==1)&(g.z5<0)].groupby("w").apply(
        lambda x: pd.Series({"n": len(x), "short_ex_%": -100*x["ex"].mean()}))
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    dd = pd.concat(dd)
    bk = dd.groupby("day")["book_return"].mean().dropna()
    res["book daily: mean, sd, n"] = pd.Series({"mean_%": 100*bk.mean(), "sd_%": 100*bk.std(), "n": len(bk)})
    res["choppy calm share of bars"] = float(d["cc"].mean())
    return res
