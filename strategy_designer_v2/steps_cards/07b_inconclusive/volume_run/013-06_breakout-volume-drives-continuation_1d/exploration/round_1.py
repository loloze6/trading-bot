def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 30
    rows = []
    allrows = []
    coinmean = {}
    for coin, wins in bars.items():
        grid = {h: [] for h in (10, 20, 30, 60)}
        for w, df in wins.items():
            c = df["close"].values
            for h in grid:
                idx = np.arange(0, len(c) - h, h)
                grid[h] += list(c[idx + h] / c[idx] - 1)
        coinmean[coin] = {h: np.mean(v) if v else np.nan for h, v in grid.items()}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            v = df["volume"].values
            vr = pd.Series(v).rolling(90, min_periods=22).mean().values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            act = ((df["regime"] == "trending") & (df["forecast"] > 0)).values
            last = -10**9
            n = len(c)
            for t in np.where(act)[0]:
                rec = dict(coin=coin, w=w, year=yr[t], f=df["forecast"].iloc[t],
                           vr=v[t] / vr[t] if vr[t] > 0 else np.nan)
                for h in (10, 20, 30, 60):
                    rec["r%d" % h] = c[t + h] / c[t] - 1 - coinmean[coin][h] if t + h < n else np.nan
                    rec["raw%d" % h] = c[t + h] / c[t] - 1 if t + h < n else np.nan
                rec["kept"] = False
                if t + H < n and t - last >= H:
                    rec["kept"] = True
                    last = t
                allrows.append(rec)
    A = pd.DataFrame(allrows)
    K = A[A.kept].copy()
    med = K.f.median()
    K["hi"] = K.f > med
    out = {}
    def welch(d, col):
        a = d[d.hi][col].dropna(); b = d[~d.hi][col].dropna()
        if len(a) < 2 or len(b) < 2:
            return (np.nan, np.nan, len(a), len(b))
        return (a.mean() - b.mean(), stats.ttest_ind(a, b, equal_var=False).statistic, len(a), len(b))
    res = {}
    for col in ["r10", "r20", "r30", "r60", "raw30"]:
        d, t, na, nb = welch(K, col)
        rho = stats.spearmanr(K.f, K[col], nan_policy="omit").correlation
        res[col] = dict(diff=d, t=t, nhi=na, nlo=nb, spearman=rho,
                        hi_mean=K[K.hi][col].mean(), lo_mean=K[~K.hi][col].mean())
    out["main_by_horizon"] = pd.DataFrame(res).T
    out["median_forecast"] = med
    g = []
    for k, d in K.groupby("coin"):
        g.append(dict(coin=k, n=len(d), mean30=d.r30.mean(), hi=d[d.hi].r30.mean(), lo=d[~d.hi].r30.mean(),
                      nhi=d.hi.sum(), rho=stats.spearmanr(d.f, d.r30).correlation if len(d) > 3 else np.nan))
    out["by_coin"] = pd.DataFrame(g)
    g = []
    for k, d in K.groupby("year"):
        g.append(dict(year=k, n=len(d), mean30=d.r30.mean(), hi=d[d.hi].r30.mean(), lo=d[~d.hi].r30.mean(), nhi=d.hi.sum()))
    out["by_year"] = pd.DataFrame(g)
    K["q"] = pd.qcut(K.f.rank(method="first"), 4, labels=False)
    out["by_forecast_quartile"] = K.groupby("q").agg(n=("r30", "size"), fmin=("f", "min"), fmax=("f", "max"),
        vr=("vr", "median"), r30=("r30", "mean"), r30med=("r30", "median"), r10=("r10", "mean"), raw30=("raw30", "mean"),
        pos=("raw30", lambda x: (x > 0).mean()))
    out["overall_kept"] = pd.Series(dict(n=len(K), mean_r30=K.r30.mean(), t=K.r30.mean() / (K.r30.std() / np.sqrt(len(K))),
        median_r30=K.r30.median(), std_r30=K.r30.std(), max=K.r30.max(), min=K.r30.min()))
    # without top outliers
    Ks = K[K.r30 < K.r30.quantile(0.95)]
    out["main_drop_top5pct"] = pd.Series(welch(Ks, "r30"), index=["diff", "t", "nhi", "nlo"])
    K["rank_r30"] = K.r30.rank()
    out["rank_test_hi_lo"] = stats.mannwhitneyu(K[K.hi].r30, K[~K.hi].r30).pvalue
    out["all_active_bars"] = pd.Series(dict(n=len(A), kept=len(K)))
    return out
