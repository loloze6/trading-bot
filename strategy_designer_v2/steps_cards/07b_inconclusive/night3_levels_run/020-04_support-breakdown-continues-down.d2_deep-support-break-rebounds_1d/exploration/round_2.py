def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    H = [5, 10]
    drift = {}
    for coin, wins in data["bars"].items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(list(c[idx + h] / c[idx] - 1))
            drift[(coin, h)] = np.mean(rs)
        for w, df in wins.items():
            c = df["close"].values
            f = df["forecast"].values
            raw = df["debug_info.components.support_break.last_history_value"].values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            s = pd.Series(c)
            past90 = s.pct_change(90).values
            past5 = s.pct_change(5).values
            ma90 = s.rolling(90, min_periods=60).mean().values
            for i in range(0, n, 5):
                if not (f[i] > 0):
                    continue
                r = {"coin": coin, "f": f[i], "raw": raw[i], "past90": past90[i], "past5": past5[i],
                     "above_ma90": (c[i] > ma90[i]) if not np.isnan(ma90[i]) else np.nan}
                for h in H:
                    r["u%d" % h] = (c[i + h] / c[i] - 1 - drift[(coin, h)]) if i + h < n else np.nan
                rows.append(r)
    d = pd.DataFrame(rows)

    def summ(g, col="u5"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "sd": x.std(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    out = {}
    out["share_f_at_20"] = float((d["f"] >= 19.999).mean())
    out["f_quantiles"] = d["f"].quantile([0.1, 0.25, 0.5, 0.6, 0.7, 0.8, 0.9])
    d["rawq"] = pd.qcut(d["raw"].rank(method="first"), 5, labels=False)
    out["by_raw_quintile_u5"] = d.groupby("rawq").apply(summ)
    out["by_raw_quintile_u10"] = d.groupby("rawq").apply(lambda g: summ(g, "u10"))
    out["raw_quintile_bounds"] = d.groupby("rawq")["raw"].agg(["min", "median", "max"])
    top = d[d["f"] >= 20]
    out["top_by_above_ma90"] = top.groupby("above_ma90").apply(summ)
    top = top.copy()
    top["p90q"] = pd.qcut(top["past90"], 3, labels=False)
    out["top_by_past90_tercile"] = top.groupby("p90q").apply(summ)
    top["p5q"] = pd.qcut(top["past5"], 3, labels=False)
    out["top_by_past5_tercile"] = top.groupby("p5q").apply(summ)
    out["top_p5_bounds"] = top["past5"].quantile([0.333, 0.667])
    out["spearman_raw_u10"] = stats.spearmanr(d["raw"], d["u10"], nan_policy="omit").correlation
    out["spearman_past5_u5_top"] = stats.spearmanr(top["past5"], top["u5"], nan_policy="omit").correlation
    return out
