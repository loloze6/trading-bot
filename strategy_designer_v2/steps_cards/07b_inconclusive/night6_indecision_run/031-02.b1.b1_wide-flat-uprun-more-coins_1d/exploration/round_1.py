def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    rows = []
    drift = {}
    usual = {}
    # drift and usual move per coin over grid of H
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
                if f[t] >= 2 and f[t - 1] < f[t] - 1.99:
                    cell = t // H
                    if cell in seen:
                        continue
                    seen.add(cell)
                    rec = dict(coin=coin, window=w, year=yr[t], f=f[t],
                               day=str(b["timestamp"].iloc[t])[:10])
                    for h in (1, 3, 5, 10, 20):
                        rec[f"r{h}"] = c[t + h] / c[t] - 1 if t + h < n else np.nan
                    rec["unus"] = rec["r10"] - drift[coin] if not np.isnan(rec["r10"]) else np.nan
                    rec["strength"] = rec["unus"] / usual[coin]
                    rec["r5past"] = c[t] / c[t - 5] - 1 if t >= 5 else np.nan
                    rec["r20past"] = c[t] / c[t - 20] - 1 if t >= 20 else np.nan
                    rec["r60past"] = c[t] / c[t - 60] - 1 if t >= 60 else np.nan
                    rec["widen"] = rng[t] / mrng[t] if not np.isnan(mrng[t]) else np.nan
                    rec["upclose"] = (c[t] - o[t]) / rng[t] if rng[t] > 0 else np.nan
                    rec["closepos"] = (c[t] - lo[t]) / rng[t] if rng[t] > 0 else np.nan
                    rows.append(rec)
    d = pd.DataFrame(rows)
    d10 = d.dropna(subset=["r10"])
    def summ(g):
        x = g["unus"].dropna()
        byday = g.groupby("day")["unus"].sum()
        t = byday.mean() / (byday.std(ddof=1) / np.sqrt(len(byday))) if len(byday) > 2 else np.nan
        return pd.Series(dict(n=len(x), days=len(byday), mean=x.mean(), med=x.median(),
                              hit=(x > 0).mean(), t_day=t, tot=g["r10"].mean()))
    out = {}
    out["all"] = summ(d10).to_frame().T
    out["by_year"] = d10.groupby("year").apply(summ)
    out["by_coin"] = d10.groupby("coin").apply(summ)
    d10 = d10.copy()
    d10["fq"] = pd.qcut(d10["f"], 3, labels=["low", "mid", "high"])
    out["by_forecast_tercile"] = d10.groupby("fq").apply(summ)
    d10["r20q"] = pd.qcut(d10["r20past"], 3, labels=["low", "mid", "high"])
    out["by_past20_tercile"] = d10.groupby("r20q").apply(summ)
    d10["r60s"] = np.where(d10["r60past"] > 0, "60d up", "60d down")
    out["by_past60_sign"] = d10.groupby("r60s").apply(summ)
    d10["wq"] = pd.qcut(d10["widen"], 3, labels=["low", "mid", "high"])
    out["by_width_tercile"] = d10.groupby("wq").apply(summ)
    d10["cp"] = pd.cut(d10["closepos"], [-0.01, 0.4, 0.6, 1.01], labels=["low", "mid", "high"])
    out["by_closepos"] = d10.groupby("cp").apply(summ)
    hz = {}
    for h in (1, 3, 5, 10, 20):
        x = d[f"r{h}"].dropna()
        hz[h] = dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std(ddof=1) / np.sqrt(len(x))), hit=(x > 0).mean())
    out["raw_returns_by_horizon"] = pd.DataFrame(hz).T
    out["spearman_f_unus"] = stats.spearmanr(d10["f"], d10["unus"]).correlation
    out["spearman_r20_unus"] = stats.spearmanr(d10["r20past"], d10["unus"], nan_policy="omit").correlation
    out["unus_quantiles"] = d10["unus"].quantile([0.05, 0.25, 0.5, 0.75, 0.95])
    return out
