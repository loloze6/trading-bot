def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 26
    rows = []
    drift = {}
    sdv = {}
    for coin, wins in bars.items():
        rets = {h: [] for h in (5, 10, 26, 52)}
        for w, df in wins.items():
            c = df["close"].values
            n = len(c)
            for h in rets:
                idx = np.arange(0, n - h, h)
                rets[h] += list(c[idx + h] / c[idx] - 1)
        drift[coin] = {h: np.mean(v) for h, v in rets.items()}
        sdv[coin] = np.std(rets[26])
        for w, df in wins.items():
            c = df["close"].values
            n = len(c)
            reg = (df["regime"] == "trending").values
            tc = df["debug_info.components.thin_cloud.post_pipeline_value"].values if "debug_info.components.thin_cloud.post_pipeline_value" in df else np.full(n, np.nan)
            tcr = df["debug_info.components.thin_cloud.last_history_value"].values if "debug_info.components.thin_cloud.last_history_value" in df else np.full(n, np.nan)
            seen = set()
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for i in np.where(reg)[0]:
                if i + H >= n:
                    continue
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                r = {"coin": coin, "win": w, "year": yr[i], "tc": tc[i], "tcraw": tcr[i]}
                for h in (5, 10, 26, 52):
                    r["u%d" % h] = (c[i + h] / c[i] - 1 - drift[coin][h]) if i + h < n else np.nan
                r["past26"] = c[i] / c[i - 26] - 1 if i >= 26 else np.nan
                r["past52"] = c[i] / c[i - 52] - 1 if i >= 52 else np.nan
                r["usd"] = sdv[coin]
                rows.append(r)
    d = pd.DataFrame(rows)
    def summ(g):
        x = g["u26"].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "median": x.median(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan, "share_pos": (x > 0).mean()})
    out = {}
    out["all"] = summ(d)
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    hz = {}
    for h in (5, 10, 26, 52):
        x = d["u%d" % h].dropna()
        hz[h] = {"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))}
    out["by_horizon"] = pd.DataFrame(hz).T
    d["tcq"] = pd.qcut(d["tc"], 4, labels=False, duplicates="drop")
    out["by_tc_quartile"] = d.groupby("tcq").apply(summ)
    d["rawq"] = pd.qcut(d["tcraw"], 4, labels=False, duplicates="drop")
    out["by_raw_quartile"] = d.groupby("rawq").apply(summ)
    d["p26q"] = pd.qcut(d["past26"], 4, labels=False, duplicates="drop")
    out["by_past26_quartile"] = d.groupby("p26q").apply(summ)
    d["p52q"] = pd.qcut(d["past52"], 4, labels=False, duplicates="drop")
    out["by_past52_quartile"] = d.groupby("p52q").apply(summ)
    x = d["u26"]
    out["trim"] = pd.Series({"mean_excl_top5": x[x < x.quantile(0.95)].mean(), "t_excl_top5": stats.ttest_1samp(x[x < x.quantile(0.95)], 0).statistic, "skew": stats.skew(x.dropna()), "sd": x.std(), "spearman_raw_u26": stats.spearmanr(d["tcraw"], d["u26"], nan_policy="omit").correlation, "spearman_tc_u26": stats.spearmanr(d["tc"], d["u26"], nan_policy="omit").correlation})
    return out
