def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H_list = [1, 3, 5, 7, 10]
    out = {}
    # coin mean h-day return over all windows (non-overlapping)
    drift = {}
    for c, wd in bars.items():
        for h in H_list:
            rs = []
            for w, b in wd.items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs) if rs else np.nan
    rows = []
    for c, wd in bars.items():
        for w, b in wd.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            fc = b["forecast"].values
            reg = b["regime"].values
            ts = pd.to_datetime(b["timestamp"])
            hi, lo = b["high"].values, b["low"].values
            rng = pd.Series((hi - lo) / cl).rolling(30).mean().values
            r7 = pd.Series(cl).pct_change(7).values
            r60 = pd.Series(cl).pct_change(60).values
            for h in H_list:
                for i in range(0, len(cl) - h, h):
                    if reg[i] == "unknown" and fc[i] > 0:
                        rows.append(dict(coin=c, win=w, h=h, f=fc[i], day=ts[i].normalize(),
                                         year=ts[i].year, ex=cl[i + h] / cl[i] - 1 - drift[(c, h)],
                                         sc=r7[i] / rng[i] if rng[i] > 0 else np.nan,
                                         r60=r60[i], r7=r7[i]))
    df = pd.DataFrame(rows)

    def tclust(d, weighted=True):
        if len(d) < 5:
            return pd.Series(dict(n=len(d), mean=np.nan, t=np.nan))
        wgt = d["f"] if weighted else pd.Series(1.0, index=d.index)
        m = (d["ex"] * wgt).sum() / wgt.sum()
        dev = (wgt * (d["ex"] - m)).groupby(d["day"]).sum()
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / max(G - 1, 1)) / wgt.sum()
        return pd.Series(dict(n=len(d), days=G, mean=m, t=m / se if se > 0 else np.nan))

    out["by_horizon_weighted"] = df.groupby("h").apply(tclust)
    out["by_horizon_unweighted"] = df.groupby("h").apply(lambda d: tclust(d, False))
    d3 = df[df.h == 3].copy()
    out["h3_by_coin"] = d3.groupby("coin").apply(tclust)
    out["h3_by_year"] = d3.groupby("year").apply(lambda d: tclust(d, False))
    out["h3_by_window"] = d3.groupby("win").apply(lambda d: tclust(d, False))
    d3["fq"] = pd.qcut(d3["f"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["h3_by_forecast_quartile"] = d3.groupby("fq").apply(lambda d: tclust(d, False))
    d3["scq"] = pd.qcut(d3["sc"].rank(method="first"), 4, labels=["s1", "s2", "s3", "s4"])
    out["h3_by_rawscaled_quartile"] = d3.groupby("scq").apply(lambda d: tclust(d, False))
    d3["r60q"] = pd.qcut(d3["r60"].rank(method="first"), 3, labels=["deep", "mid", "mild"])
    out["h3_by_60d_fall_tercile"] = d3.groupby("r60q").apply(lambda d: tclust(d, False))
    out["h3_spearman_f_ex"] = stats.spearmanr(d3["f"], d3["ex"]).correlation
    out["h3_spearman_sc_ex"] = stats.spearmanr(d3["sc"], d3["ex"], nan_policy="omit").correlation
    d7 = df[df.h == 7].copy()
    d7["fq"] = pd.qcut(d7["f"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["h7_by_forecast_quartile"] = d7.groupby("fq").apply(lambda d: tclust(d, False))
    out["h7_by_coin"] = d7.groupby("coin").apply(tclust)
    return out
