def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [3, 6, 12]
    drift, usual = {}, {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = np.mean(rs); usual[(coin, h)] = np.std(rs)
    out = {}
    def summ(x):
        x = pd.Series(x).dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    allrows = {}
    for h in H:
        rows = []
        for coin, wins in bars.items():
            for w, df in wins.items():
                c = df["close"].values
                f = df["forecast"].fillna(0).values
                raw = df["debug_info.components.panic.last_history_value"].values
                yr = pd.to_datetime(df["timestamp"]).dt.year.values
                n = len(c)
                for s in range(0, n, h):
                    e = min(s + h, n)
                    idx = np.where(f[s:e] >= 2)[0]
                    if len(idx) == 0: continue
                    t = s + idx[0]
                    if t + h >= n: continue
                    u = c[t + h] / c[t] - 1 - drift[(coin, h)]
                    tot = c[t + h] / c[t] - 1
                    rows.append({"coin": coin, "year": yr[t], "fc": f[t], "raw": raw[t], "u": u, "tot": tot, "z": u / usual[(coin, h)]})
        d = pd.DataFrame(rows)
        allrows[h] = d
        out["h%d_all" % h] = pd.concat([summ(d["u"]), pd.Series({"strength": d["z"].mean(), "total": d["tot"].mean()})])
    d = allrows[6]
    out["h6_by_coin"] = d.groupby("coin")["u"].apply(summ).unstack()
    out["h6_by_year"] = d.groupby("year")["u"].apply(summ).unstack()
    d["rq"] = pd.qcut(d["raw"].rank(method="first"), 5, labels=False)
    out["h6_by_raw_quintile"] = d.groupby("rq")["u"].apply(summ).unstack()
    out["h6_raw_quintile_mean_raw"] = d.groupby("rq")["raw"].mean()
    med = d["fc"].median()
    up = d.loc[d["fc"] > med, "u"]; lo = d.loc[d["fc"] <= med, "u"]
    out["h6_upper_minus_lower_fc"] = pd.Series({"diff": up.mean() - lo.mean(), "welch_t": stats.ttest_ind(up, lo, equal_var=False).statistic, "n_up": len(up), "n_lo": len(lo)})
    out["h6_spearman_raw_u"] = stats.spearmanr(d["raw"], d["u"], nan_policy="omit").correlation
    return out
