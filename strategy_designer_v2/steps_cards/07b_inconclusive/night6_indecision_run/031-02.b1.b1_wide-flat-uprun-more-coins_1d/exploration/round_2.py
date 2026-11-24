def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    rows = []
    drift, usual = {}, {}
    for coin, wins in data["bars"].items():
        rs = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - H, H):
                rs.append(c[i + H] / c[i] - 1)
        drift[coin] = np.mean(rs) if rs else np.nan
        usual[coin] = np.std(rs, ddof=1) if len(rs) > 1 else np.nan
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            f = b["forecast"].fillna(0).values
            c = b["close"].values; o = b["open"].values; hi = b["high"].values; lo = b["low"].values
            n = len(b)
            rng = hi - lo
            mrng = pd.Series(rng).rolling(20, min_periods=20).mean().values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            seen = set()
            for t in range(1, n):
                if f[t] >= 2 and f[t] - f[t - 1] >= 2:
                    cell = t // H
                    if cell in seen:
                        continue
                    seen.add(cell)
                    rec = dict(coin=coin, window=w, year=yr[t], f=f[t],
                               day=str(b["timestamp"].iloc[t])[:10])
                    for h in (1, 3, 5, 10, 20):
                        rec[f"r{h}"] = c[t + h] / c[t] - 1 if t + h < n else np.nan
                    rec["unus"] = rec["r10"] - drift[coin] if not np.isnan(rec["r10"]) else np.nan
                    rec["r5past"] = c[t] / c[t - 5] - 1 if t >= 5 else np.nan
                    rec["r20past"] = c[t] / c[t - 20] - 1 if t >= 20 else np.nan
                    rec["r60past"] = c[t] / c[t - 60] - 1 if t >= 60 else np.nan
                    rec["widen"] = rng[t] / mrng[t] if not np.isnan(mrng[t]) else np.nan
                    rec["closepos"] = (c[t] - lo[t]) / rng[t] if rng[t] > 0 else np.nan
                    rows.append(rec)
    d = pd.DataFrame(rows)
    d10 = d.dropna(subset=["r10"]).copy()
    def summ(g):
        x = g["unus"].dropna()
        byday = g.groupby("day")["unus"].sum()
        t = byday.mean() / (byday.std(ddof=1) / np.sqrt(len(byday))) if len(byday) > 2 else np.nan
        return pd.Series(dict(n=len(x), days=len(byday), mean=x.mean(), med=x.median(),
                              hit=(x > 0).mean(), t_day=t, tot=g["r10"].mean()))
    def terc(s):
        return pd.qcut(s.rank(method="first"), 3, labels=["low", "mid", "high"])
    out = {}
    out["all"] = summ(d10).to_frame().T
    out["by_year"] = d10.groupby("year").apply(summ)
    out["by_coin"] = d10.groupby("coin").apply(summ)
    d10["fq"] = terc(d10["f"])
    out["by_forecast_tercile"] = d10.groupby("fq").apply(summ)
    out["forecast_counts"] = pd.Series(dict(n_at_20=(d10["f"] >= 19.99).sum(), n=len(d10)))
    s = d10.dropna(subset=["r20past"]).copy(); s["q"] = terc(s["r20past"])
    out["by_past20_tercile"] = s.groupby("q").apply(summ)
    s = d10.dropna(subset=["r60past"]).copy(); s["q"] = np.where(s["r60past"] > 0, "60d up", "60d down")
    out["by_past60_sign"] = s.groupby("q").apply(summ)
    s = d10.dropna(subset=["widen"]).copy(); s["q"] = terc(s["widen"])
    out["by_width_tercile"] = s.groupby("q").apply(summ)
    s = d10.dropna(subset=["closepos"]).copy()
    s["q"] = pd.cut(s["closepos"], [-0.01, 0.4, 0.6, 1.01], labels=["low", "mid", "high"])
    out["by_closepos"] = s.groupby("q").apply(summ)
    hz = {}
    for h in (1, 3, 5, 10, 20):
        x = d[f"r{h}"].dropna()
        hz[h] = dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std(ddof=1) / np.sqrt(len(x))), hit=(x > 0).mean())
    out["raw_returns_by_horizon"] = pd.DataFrame(hz).T
    out["spearman_f_unus"] = float(stats.spearmanr(d10["f"], d10["unus"]).correlation)
    out["spearman_r20_unus"] = float(stats.spearmanr(d10["r20past"], d10["unus"], nan_policy="omit").correlation)
    out["unus_quantiles"] = d10["unus"].quantile([0.05, 0.25, 0.5, 0.75, 0.95])
    top = d10["unus"].nlargest(5).sum()
    out["mean_without_top5"] = float((d10["unus"].sum() - top) / (len(d10) - 5))
    return out
