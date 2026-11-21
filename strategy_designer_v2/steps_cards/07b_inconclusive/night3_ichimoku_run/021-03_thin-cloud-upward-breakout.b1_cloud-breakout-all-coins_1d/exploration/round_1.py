def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 26
    bars = data["bars"]
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                rets.append(c[i + H] / c[i] - 1)
        drift[coin] = np.mean(rets) if rets else np.nan
        usual[coin] = np.std(rets) if len(rets) > 1 else np.nan
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = df["forecast"].fillna(0).values
            c = df["close"].values
            raw = df.get("debug_info.components.thin_cloud.last_history_value")
            post = df.get("debug_info.components.thin_cloud.post_pipeline_value")
            ts = pd.to_datetime(df["timestamp"])
            seen = set()
            for i in range(1, len(df)):
                if f[i - 1] == 0 and f[i] - f[i - 1] >= 2:
                    cell = i // H
                    if cell in seen:
                        continue
                    seen.add(cell)
                    r = {}
                    for h in [5, 10, 26, 52]:
                        r["r%d" % h] = c[i + h] / c[i] - 1 if i + h < len(c) else np.nan
                    # prior 26-bar return and position vs 52-bar
                    r["past26"] = c[i] / c[i - 26] - 1 if i >= 26 else np.nan
                    r["coin"] = coin
                    r["win"] = w
                    r["year"] = ts.iloc[i].year
                    r["raw"] = raw.iloc[i] if raw is not None else np.nan
                    r["post"] = post.iloc[i] if post is not None else np.nan
                    r["fc"] = f[i]
                    r["drift"] = drift[coin]
                    r["usual"] = usual[coin]
                    rows.append(r)
    d = pd.DataFrame(rows)
    d["u26"] = d["r26"] - d["drift"]
    d26 = d.dropna(subset=["u26", "raw"])
    med = d26["raw"].median()
    d26 = d26.assign(thin=d26["raw"] > med)
    out = {}
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "median": x.median(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    a = d26[d26.thin]["u26"]; b = d26[~d26.thin]["u26"]
    out["recon"] = pd.Series({"n": len(d26), "thin_mean": a.mean(), "thick_mean": b.mean(),
                              "welch_t": stats.ttest_ind(a, b, equal_var=False).statistic,
                              "thin_median": a.median(), "thick_median": b.median(),
                              "mwu_p": stats.mannwhitneyu(a, b).pvalue,
                              "spearman_raw_u26": stats.spearmanr(d26["raw"], d26["u26"]).correlation,
                              "raw_med": med, "raw_min": d26.raw.min(), "raw_max": d26.raw.max()})
    d26["q"] = pd.qcut(d26["raw"], 5, labels=False)
    out["by_quintile"] = d26.groupby("q").agg(n=("u26", "size"), mean=("u26", "mean"), median=("u26", "median"),
                                              raw=("raw", "mean"), win=("u26", lambda x: (x > 0).mean()))
    d26["yr"] = d26["year"]
    def diff(g):
        a = g[g.thin]["u26"]; b = g[~g.thin]["u26"]
        return pd.Series({"n_thin": len(a), "n_thick": len(b), "thin": a.mean(), "thick": b.mean(),
                          "all": g["u26"].mean()})
    out["by_year"] = d26.groupby("yr").apply(diff)
    out["by_coin"] = d26.groupby("coin").apply(diff)
    # horizons
    hz = {}
    for h in [5, 10, 26, 52]:
        dd = d.dropna(subset=["r%d" % h, "raw"]).copy()
        dd["u"] = dd["r%d" % h] - dd["drift"] * h / 26
        th = dd["raw"] > dd["raw"].median()
        x, y = dd[th]["u"], dd[~th]["u"]
        hz[h] = {"n": len(dd), "all": dd["u"].mean(), "t_all": tt(dd["u"])["t"], "thin": x.mean(), "thick": y.mean(),
                 "welch": stats.ttest_ind(x, y, equal_var=False).statistic,
                 "spearman": stats.spearmanr(dd["raw"], dd["u"]).correlation}
    out["by_horizon"] = pd.DataFrame(hz).T
    # past momentum split
    dp = d26.dropna(subset=["past26"]).copy()
    dp["pq"] = pd.qcut(dp["past26"], 3, labels=False)
    out["by_past26_tercile"] = dp.groupby("pq").apply(diff)
    out["trim"] = pd.Series({"thin_trim": stats.trim_mean(a, 0.05), "thick_trim": stats.trim_mean(b, 0.05),
                             "thin_std": a.std(), "thick_std": b.std(),
                             "corr_raw_usual": stats.spearmanr(d26.raw, d26.usual).correlation})
    return out
