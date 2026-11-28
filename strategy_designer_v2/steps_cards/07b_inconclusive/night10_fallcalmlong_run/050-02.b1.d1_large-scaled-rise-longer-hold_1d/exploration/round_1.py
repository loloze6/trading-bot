def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [3, 5, 10, 15, 20]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for h in H:
            g = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                g += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = (np.mean(g), np.std(g, ddof=1))
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            r7 = pd.Series(c).pct_change(7).values
            for h in H:
                for i in range(0, n - h, h):
                    if f[i] > 0:
                        rows.append(dict(coin=coin, win=w, h=h, f=f[i], ret=c[i + h] / c[i] - 1,
                                         ex=c[i + h] / c[i] - 1 - drift[(coin, h)][0],
                                         sd=drift[(coin, h)][1], r7=r7[i],
                                         year=ts[i].year, day=ts[i].normalize()))
    d = pd.DataFrame(rows)
    out = {}
    def summ(x):
        n = len(x)
        m = x["ex"].mean()
        wm = (x["ex"] * x["f"]).sum() / x["f"].sum()
        dd = x.groupby("day")["ex"].sum()
        t = m / (x["ex"].std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series(dict(n=n, days=x["day"].nunique(), mean_ex=m, wmean_ex=wm, t=t,
                              mean_tot=x["ret"].mean(), hit=(x["ex"] > 0).mean(),
                              strength=(x["ex"] / x["sd"]).mean()))
    out["by_horizon"] = d.groupby("h").apply(summ)
    d10 = d[d.h == 10].copy()
    out["h10_by_coin"] = d10.groupby("coin").apply(summ)
    out["h10_by_year"] = d10.groupby("year").apply(summ)
    out["h10_by_window"] = d10.groupby("win").apply(summ)
    d10["fq"] = pd.qcut(d10["f"].rank(method="first"), 3, labels=["low", "mid", "high"])
    out["h10_by_fterc"] = d10.groupby("fq").apply(summ)
    for h in [5, 20]:
        dh = d[d.h == h].copy()
        dh["fq"] = pd.qcut(dh["f"].rank(method="first"), 3, labels=["low", "mid", "high"])
        out[f"h{h}_by_fterc"] = dh.groupby("fq").apply(summ)
    out["h10_median_trim"] = pd.Series(dict(median_ex=d10["ex"].median(),
                                            mean_ex_drop_top5=d10.sort_values("ex").iloc[:-5]["ex"].mean(),
                                            max_ex=d10["ex"].max(), min_ex=d10["ex"].min(),
                                            share_f_eq_20=(d10["f"] >= 19.9).mean(),
                                            spearman_f_ex=stats.spearmanr(d10["f"], d10["ex"])[0]))
    return out
