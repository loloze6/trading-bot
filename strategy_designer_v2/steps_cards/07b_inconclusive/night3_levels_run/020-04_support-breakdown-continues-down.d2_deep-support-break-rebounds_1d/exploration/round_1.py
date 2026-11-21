def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    H = [1, 3, 5, 10, 20]
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
            past30 = pd.Series(c).pct_change(30).values
            for i in range(0, n, 5):
                if not (f[i] > 0):
                    continue
                r = {"coin": coin, "win": w, "year": ts.iloc[i].year, "f": f[i], "raw": raw[i], "past30": past30[i]}
                for h in H:
                    r["u%d" % h] = (c[i + h] / c[i] - 1 - drift[(coin, h)]) if i + h < n else np.nan
                    r["t%d" % h] = (c[i + h] / c[i] - 1) if i + h < n else np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    thr = d["f"].quantile(0.8)
    d["top"] = d["f"] >= thr
    d["fq"] = pd.qcut(d["f"].rank(method="first"), 5, labels=False)

    def summ(g, col="u5"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    out = {}
    out["by_fq_u5"] = d.groupby("fq").apply(summ)
    hz = []
    for h in H:
        for lab, g in [("top", d[d.top]), ("all", d)]:
            s = summ(g, "u%d" % h); s["h"] = h; s["grp"] = lab
            st = summ(g, "t%d" % h); s["total_mean"] = st["mean"]
            hz.append(s)
    out["by_horizon"] = pd.DataFrame(hz)
    out["top_by_coin"] = d[d.top].groupby("coin").apply(summ)
    out["top_by_year"] = d[d.top].groupby("year").apply(summ)
    d["p30q"] = pd.qcut(d["past30"], 4, labels=False)
    out["all_by_past30_quartile"] = d.groupby("p30q").apply(summ)
    out["all_by_past30_quartile_u10"] = d.groupby("p30q").apply(lambda g: summ(g, "u10"))
    out["p30_bounds"] = d["past30"].quantile([0.25, 0.5, 0.75])
    out["spearman_f_u5"] = stats.spearmanr(d["f"], d["u5"], nan_policy="omit").correlation
    out["spearman_raw_u5"] = stats.spearmanr(d["raw"], d["u5"], nan_policy="omit").correlation
    out["thr"] = thr
    return out
