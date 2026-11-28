def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [2, 3, 4, 5, 7, 10]
    drift = {}
    for coin, wins in bars.items():
        for h in H:
            g = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                g += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = (np.mean(g), np.std(g, ddof=1))
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            lr = np.log(pd.Series(c)).diff()
            sd30 = lr.rolling(30).std().values
            r7 = pd.Series(c).pct_change(7).values
            sc = r7 / (sd30 * np.sqrt(7))
            for h in H:
                for off in range(h):
                    for i in range(off, n - h, h):
                        if f[i] > 0:
                            rows.append(dict(coin=coin, win=w, h=h, off=off, f=f[i],
                                             ex=c[i + h] / c[i] - 1 - drift[(coin, h)][0],
                                             sd=drift[(coin, h)][1], sc=sc[i],
                                             year=ts[i].year, day=ts[i].normalize()))
    d = pd.DataFrame(rows)
    def summ(x):
        n = len(x)
        m = x["ex"].mean()
        wm = (x["ex"] * x["f"]).sum() / x["f"].sum()
        dd = x.groupby("day").apply(lambda y: (y["f"] * (y["ex"] - wm)).sum())
        G = len(dd)
        se = np.sqrt((dd ** 2).sum() * G / max(G - 1, 1)) / x["f"].sum()
        return pd.Series(dict(n=n, days=x["day"].nunique(), mean_ex=m, wmean_ex=wm,
                              t_w_clustered=wm / se if se > 0 else np.nan,
                              hit=(x["ex"] > 0).mean(), strength=(x["ex"] / x["sd"]).mean(),
                              spearman_f=stats.spearmanr(x["f"], x["ex"])[0] if n > 3 else np.nan))
    out = {}
    d0 = d[d.off == 0]
    out["grid0_by_h"] = d0.groupby("h").apply(summ)
    # average over grid offsets (each offset a valid non-overlapping grid)
    byoff = d.groupby(["h", "off"]).apply(summ).reset_index()
    out["offsets_by_h"] = byoff.groupby("h").agg(n_mean=("n", "mean"), wmean_mean=("wmean_ex", "mean"),
                                                 wmean_min=("wmean_ex", "min"), t_mean=("t_w_clustered", "mean"),
                                                 share_t_pos=("t_w_clustered", lambda s: (s > 0).mean()),
                                                 strength_mean=("strength", "mean"))
    d3 = d0[d0.h == 3]
    out["h3_by_year"] = d3.groupby("year").apply(summ)
    out["h3_by_coin"] = d3.groupby("coin").apply(summ)
    d3 = d3.copy()
    d3["fq"] = pd.qcut(d3["f"].rank(method="first"), 3, labels=["low", "mid", "high"])
    out["h3_by_fterc"] = d3.groupby("fq").apply(summ)
    d5 = d0[d0.h == 5]
    out["h5_by_year"] = d5.groupby("year").apply(summ)
    out["h5_by_coin"] = d5.groupby("coin").apply(summ)
    return out
