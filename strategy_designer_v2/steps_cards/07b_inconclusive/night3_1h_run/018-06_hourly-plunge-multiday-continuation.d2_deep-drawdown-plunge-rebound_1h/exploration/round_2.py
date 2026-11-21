def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}; usual = {}
    H = (12, 24, 48, 72, 168)
    for coin, wins in bars.items():
        allr = {h: [] for h in H}
        for w, df in wins.items():
            c = df["close"].values
            for h in H:
                idx = np.arange(0, len(c) - h, h)
                allr[h] += list(c[idx + h] / c[idx] - 1)
        for h in H:
            drift[(coin, h)] = np.mean(allr[h]); usual[(coin, h)] = np.std(allr[h])
        for w, df in wins.items():
            c = df["close"].values; f = df["forecast"].fillna(0).values
            n = len(c)
            hi = pd.Series(c).rolling(720, min_periods=720).max().values
            depth = (c - hi) / hi * 100
            r24 = np.full(n, np.nan); r24[24:] = c[24:] / c[:-24] - 1
            ts = pd.to_datetime(df["timestamp"])
            lowest = 0.0; lastcell = -1
            for t in range(n):
                lowest = min(lowest, f[t])
                if f[t] - lowest >= 2:
                    cell = t // 72
                    if cell != lastcell:
                        lastcell = cell
                        rec = {"coin": coin, "win": w, "f": f[t], "depth": depth[t], "r24": r24[t],
                               "year": ts.iloc[t].year}
                        for h in H:
                            if t + h < n:
                                rec["u%d" % h] = c[t + h] / c[t] - 1 - drift[(coin, h)]
                        rows.append(rec)
                    lowest = f[t]
    d = pd.DataFrame(rows)
    def tt(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["horizons_all"] = pd.DataFrame({h: tt(d["u%d" % h]) for h in H}).T
    deep = d[d["depth"] < -33.33]
    out["horizons_deep"] = pd.DataFrame({h: tt(deep["u%d" % h]) for h in H}).T
    out["deep_by_year"] = deep.groupby("year")["u72"].apply(tt).unstack()
    out["deep_by_coin"] = deep.groupby("coin")["u72"].apply(tt).unstack()
    d["dq"] = pd.qcut(d["depth"], 4, labels=False)
    d["fq"] = pd.qcut(d["f"].rank(method="first"), 2, labels=False)
    out["depthq_x_forecasthalf_u72"] = d.groupby(["dq", "fq"])["u72"].apply(tt).unstack()
    out["spearman_depth_u72"] = stats.spearmanr(d["depth"], d["u72"], nan_policy="omit")[0]
    out["spearman_f_u72_deep"] = stats.spearmanr(deep["f"], deep["u72"], nan_policy="omit")[0]
    out["spearman_f_u24_all"] = stats.spearmanr(d["f"], d["u24"], nan_policy="omit")[0]
    out["by_year_u24"] = d.groupby("year")["u24"].apply(tt).unstack()
    return out
