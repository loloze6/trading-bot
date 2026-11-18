def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    H = [3, 5, 10, 20]
    rows = []
    gridmean = {}
    for coin in bars:
        for h in H:
            rs = []
            for w, df in bars[coin].items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            gridmean[(coin, h)] = np.mean(rs)
        for w, df in bars[coin].items():
            c = df["close"].values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            last = -10**9
            for i in range(1, n):
                prior = c[max(0, i - 30):i]
                if not (c[i] < prior.min()):
                    continue
                if i - last < 10 or i + 10 >= n:
                    continue
                last = i
                mx = c[max(0, i - 29):i + 1].max()
                D = (mx - c[i]) / mx
                r60 = c[i] / c[max(0, i - 60)] - 1
                rec = dict(coin=coin, win=w, year=ts.iloc[i].year, D=D, r60=r60,
                           wnum=int(w[1:]))
                for h in H:
                    if i + h < n:
                        rec[f"x{h}"] = c[i + h] / c[i] - 1 - gridmean[(coin, h)]
                rows.append(rec)
    d = pd.DataFrame(rows)
    med = d["D"].median()
    d["mild"] = d["D"] <= med

    def welch(sub, col):
        a = sub.loc[sub.mild, col].dropna(); b = sub.loc[~sub.mild, col].dropna()
        if len(a) < 3 or len(b) < 3:
            return (len(a), len(b), np.nan, np.nan, np.nan)
        return (len(a), len(b), a.mean(), b.mean(), stats.ttest_ind(a, b, equal_var=False).statistic)

    out["n_cases_medianD"] = f"{len(d)} cases, median D {med:.4f}"
    out["by_horizon"] = pd.DataFrame({f"h{h}": welch(d, f"x{h}") for h in H},
                                     index=["n_mild", "n_deep", "mean_mild", "mean_deep", "t"]).T
    out["by_coin"] = pd.DataFrame({c: welch(d[d.coin == c], "x10") for c in d.coin.unique()},
                                  index=["n_mild", "n_deep", "mean_mild", "mean_deep", "t"]).T
    out["by_year"] = pd.DataFrame({y: welch(d[d.year == y], "x10") for y in sorted(d.year.unique())},
                                  index=["n_mild", "n_deep", "mean_mild", "mean_deep", "t"]).T
    d["Dq"] = pd.qcut(d["D"], 5, labels=False)
    out["by_D_quintile"] = d.groupby("Dq").agg(D_mean=("D", "mean"), n=("x10", "count"),
                                                x10=("x10", "mean"), x5=("x5", "mean"), x20=("x20", "mean"),
                                                sd10=("x10", "std"))
    d["bull"] = d["r60"] > 0
    out["by_r60_sign"] = pd.DataFrame({f"r60>0={b}": welch(d[d.bull == b], "x10") for b in [True, False]},
                                      index=["n_mild", "n_deep", "mean_mild", "mean_deep", "t"]).T
    d["r60q"] = pd.qcut(d["r60"], 3, labels=False)
    out["by_r60_tercile_mean"] = d.groupby("r60q").agg(r60=("r60", "mean"), n=("x10", "count"),
                                                         x10=("x10", "mean"),
                                                         t=("x10", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))))
    out["all_cases_mean_x10"] = (d.x10.mean(), d.x10.std(), d.x10.mean() / (d.x10.std() / np.sqrt(len(d))))
    out["spearman_D_x10"] = stats.spearmanr(d["D"], d["x10"], nan_policy="omit")[0]
    out["spearman_D_x20"] = stats.spearmanr(d["D"], d["x20"], nan_policy="omit")[0]
    return out
