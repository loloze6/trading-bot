def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    H = [3, 5, 10]
    drift = {}; usual = {}
    for coin, wins in data["bars"].items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(list(c[idx + h] / c[idx] - 1))
            drift[(coin, h)] = np.mean(rs); usual[(coin, h)] = np.std(rs)
        for w, df in wins.items():
            c = df["close"].values
            f = df["forecast"].values
            raw = df["debug_info.components.support_break.last_history_value"].values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            for i in range(0, n, 5):
                if not (f[i] > 0):
                    continue
                r = {"coin": coin, "win": w, "year": ts.iloc[i].year, "f": f[i], "raw": raw[i]}
                for h in H:
                    ok = i + h < n
                    r["u%d" % h] = (c[i + h] / c[i] - 1 - drift[(coin, h)]) if ok else np.nan
                    r["t%d" % h] = (c[i + h] / c[i] - 1) if ok else np.nan
                    r["s%d" % h] = r["u%d" % h] / usual[(coin, h)] if ok else np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    d["rawq10"] = pd.qcut(d["raw"].rank(method="first"), 10, labels=False)

    def summ(g, col="u5"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "total": g[col.replace("u", "t")].mean(),
                          "strength": g[col.replace("u", "s")].mean()})
    out = {}
    out["by_raw_decile_u5"] = d.groupby("rawq10").apply(summ)
    top = d[d["rawq10"] >= 8]
    out["rawtop20_by_horizon"] = pd.DataFrame({h: summ(top, "u%d" % h) for h in H}).T
    out["rawtop20_by_coin"] = top.groupby("coin").apply(summ)
    out["rawtop20_by_year"] = top.groupby("year").apply(summ)
    out["rawtop20_share_f20"] = float((top["f"] >= 19.999).mean())
    f20 = d[d["f"] >= 19.999]
    out["f20_raw_quantiles"] = f20["raw"].quantile([0.1, 0.5, 0.9])
    out["spearman_raw_u5_within_f20"] = stats.spearmanr(f20["raw"], f20["u5"], nan_policy="omit").correlation
    out["spearman_raw_u5_by_coin"] = d.groupby("coin").apply(lambda g: stats.spearmanr(g["raw"], g["u5"], nan_policy="omit").correlation)
    return out
