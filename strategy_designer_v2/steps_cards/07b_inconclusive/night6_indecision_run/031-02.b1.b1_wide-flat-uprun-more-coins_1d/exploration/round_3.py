def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    Hs = (1, 2, 3, 5, 10)
    drift, usual = {}, {}
    for coin, wins in data["bars"].items():
        for H in Hs:
            rs = []
            for w, b in wins.items():
                c = b["close"].values
                for i in range(0, len(c) - H, H):
                    rs.append(c[i + H] / c[i] - 1)
            drift[(coin, H)] = np.mean(rs) if rs else np.nan
            usual[(coin, H)] = np.std(rs, ddof=1) if len(rs) > 1 else np.nan
    out = {}
    res = {}
    allrows = {}
    for H in Hs:
        rows = []
        for coin, wins in data["bars"].items():
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                f = b["forecast"].fillna(0).values
                c = b["close"].values
                n = len(b)
                yr = pd.to_datetime(b["timestamp"]).dt.year.values
                seen = set()
                for t in range(1, n):
                    if f[t] >= 2 and f[t] - f[t - 1] >= 2:
                        cell = t // H
                        if cell in seen:
                            continue
                        seen.add(cell)
                        if t + H >= n:
                            continue
                        r = c[t + H] / c[t] - 1
                        u = r - drift[(coin, H)]
                        rows.append(dict(coin=coin, year=yr[t], f=f[t], day=str(b["timestamp"].iloc[t])[:10],
                                         u=u, s=u / usual[(coin, H)], r=r,
                                         r5=c[t] / c[t - 5] - 1 if t >= 5 else np.nan))
        d = pd.DataFrame(rows)
        allrows[H] = d
        byday = d.groupby("day")["u"].sum()
        t = byday.mean() / (byday.std(ddof=1) / np.sqrt(len(byday)))
        res[H] = dict(n=len(d), days=len(byday), unus=d["u"].mean(), med=d["u"].median(),
                      hit=(d["u"] > 0).mean(), t_day=t, strength=d["s"].mean(), total=d["r"].mean(),
                      spearman=stats.spearmanr(d["f"], d["u"]).correlation)
    out["unusual_by_horizon"] = pd.DataFrame(res).T
    d = allrows[3]
    def summ(g):
        byday = g.groupby("day")["u"].sum()
        t = byday.mean() / (byday.std(ddof=1) / np.sqrt(len(byday))) if len(byday) > 2 else np.nan
        return pd.Series(dict(n=len(g), days=len(byday), mean=g["u"].mean(), hit=(g["u"] > 0).mean(), t_day=t))
    out["h3_by_year"] = d.groupby("year").apply(summ)
    d = d.copy()
    d["fq"] = pd.qcut(d["f"].rank(method="first"), 3, labels=["low", "mid", "high"])
    out["h3_by_forecast_tercile"] = d.groupby("fq").apply(summ)
    d["big"] = np.where(d["coin"].isin(["BTCUSD", "ETHUSD", "LTCUSD", "XMRUSD", "XRPUSD", "ZECUSD"]), "default6", "others")
    out["h3_by_coingroup"] = d.groupby("big").apply(summ)
    top = d["u"].nlargest(5).sum()
    out["h3_mean_without_top5"] = float((d["u"].sum() - top) / (len(d) - 5))
    return out
