def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = []
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            r1 = c.pct_change()
            H.append(pd.DataFrame({"coin": coin, "w": w, "ts": ts, "hour": ts.dt.hour, "wd": ts.dt.weekday,
                                   "year": ts.dt.year, "r": r1}))
            past = c / c.shift(72) - 1
            gain = r1.clip(lower=0)
            sg = gain.rolling(72).sum()
            top3g = gain.rolling(72).apply(lambda x: np.sort(x)[-3:].sum(), raw=True)
            vol = r1.rolling(72).std(); vol720 = r1.rolling(720).std()
            fwd = c.shift(-72) / c - 1
            idx = np.arange(0, len(b), 72)
            rows.append(pd.DataFrame({"coin": coin, "w": w, "year": ts.dt.year.iloc[idx].values,
                                      "past": past.iloc[idx].values, "fwd": fwd.iloc[idx].values,
                                      "grindG": (1 - top3g / sg).iloc[idx].values,
                                      "volratio": (vol / vol720).iloc[idx].values,
                                      "zp": (past / (vol * np.sqrt(72))).iloc[idx].values}))
    h = pd.concat(H).dropna(subset=["r"])
    # cross-coin average per timestamp to remove correlation
    m = h.groupby(["ts"]).agg(r=("r", "mean"), hour=("hour", "first"), wd=("wd", "first"), year=("year", "first"))
    def tt(x):
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    out["coin-avg 1h return by hour (per timestamp)"] = m.groupby("hour")["r"].apply(tt).unstack()
    out["coin-avg 1h return by weekday"] = m.groupby("wd")["r"].apply(tt).unstack()
    m["h2122"] = m["hour"].isin([21, 22])
    out["hours 21-22 coin-avg by year"] = m[m.h2122].groupby("year")["r"].apply(tt).unstack()
    out["hours 21-22 by coin"] = h[h.hour.isin([21, 22])].groupby("coin")["r"].apply(tt).unstack()
    out["hour 14 by year (coin-avg)"] = m[m.hour == 14].groupby("year")["r"].apply(tt).unstack()
    out["hours 21-22 by weekday (coin-avg)"] = m[m.h2122].groupby("wd")["r"].apply(tt).unstack()
    g = pd.concat(rows).dropna(subset=["past", "fwd"])
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    up = g[g.past > 0].dropna(subset=["grindG"]).copy()
    med = up["grindG"].median()
    a = up[up.grindG > med]["ex"]; bb = up[up.grindG < med]["ex"]
    out["up: high grind minus low grind"] = pd.Series({"diff": a.mean() - bb.mean(), "welch_t": stats.ttest_ind(a, bb, equal_var=False).statistic, "n": len(up)})
    # regression ex ~ zp + grindG on up moves
    X = np.column_stack([np.ones(len(up)), up["zp"], up["grindG"] - up["grindG"].mean()])
    beta, *_ = np.linalg.lstsq(X, up["ex"].values, rcond=None)
    res = up["ex"].values - X @ beta
    s2 = res @ res / (len(up) - 3); cov = s2 * np.linalg.inv(X.T @ X)
    out["up: ex ~ zpast + grind (beta, t)"] = pd.DataFrame({"beta": beta, "t": beta / np.sqrt(np.diag(cov))}, index=["const", "zpast", "grind"])
    up["hi"] = up.grindG > med
    out["up: hi-lo grind by coin"] = up.groupby("coin").apply(lambda x: pd.Series({"n": len(x), "diff": x[x.hi]["ex"].mean() - x[~x.hi]["ex"].mean()}))
    out["up: hi-lo grind by year"] = up.groupby("year").apply(lambda x: pd.Series({"n": len(x), "diff": x[x.hi]["ex"].mean() - x[~x.hi]["ex"].mean()}))
    gg = g.dropna(subset=["volratio"]).copy()
    gg["vq"] = gg.groupby("coin")["volratio"].transform(lambda x: pd.qcut(x, 4, labels=False))
    top = gg[gg.vq == 3]
    out["top volratio quartile: ex by past sign"] = top.groupby(top.past > 0)["ex"].apply(tt).unstack()
    out["top volratio by year"] = top.groupby("year")["ex"].apply(tt).unstack()
    out["volratio vs ex spearman"] = pd.Series({"rho": stats.spearmanr(gg["volratio"], gg["ex"]).correlation, "n": len(gg)})
    return out
