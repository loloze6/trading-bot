def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    drift = {}
    for coin, wins in data["bars"].items():
        rets = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - H, H)
            rets += list(c[idx + H] / c[idx] - 1)
        drift[coin] = np.mean(rets)
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r1 = c.pct_change()
            vol30 = r1.rolling(30).std()
            r30 = c / c.shift(30) - 1
            r14 = c / c.shift(14) - 1
            r60 = c / c.shift(60) - 1
            ts = pd.to_datetime(df["timestamp"])
            for i in np.arange(0, len(c) - H, H):
                f = c.iloc[i + H] / c.iloc[i] - 1
                v = vol30.iloc[i]
                rows.append(dict(coin=coin, w=w, ts=ts.iloc[i], ex=f - drift[coin],
                                 fc=df["forecast"].iloc[i],
                                 r30=r30.iloc[i], r30z=r30.iloc[i] / (v * np.sqrt(30)) if v > 0 else np.nan,
                                 r14z=r14.iloc[i] / (v * np.sqrt(14)) if v > 0 else np.nan,
                                 r60z=r60.iloc[i] / (v * np.sqrt(60)) if v > 0 else np.nan,
                                 year=ts.iloc[i].year))
    g = pd.DataFrame(rows)
    res = {}
    def clustered(sub, col, q=5):
        d = sub.dropna(subset=[col, "ex"]).copy()
        d["b"] = pd.qcut(d[col], q, labels=False, duplicates="drop")
        out = []
        for b, x in d.groupby("b"):
            m = x.groupby("ts")["ex"].mean()
            out.append(dict(b=b, n=len(x), dates=len(m), lo=x[col].min(), hi=x[col].max(),
                            mean_ex=x["ex"].mean(), t_dates=m.mean() / (m.std() / np.sqrt(len(m)))))
        out = pd.DataFrame(out).set_index("b")
        # date-demeaned graded slope: rank within the whole sample, cluster by date
        d["rk"] = d[col].rank(pct=True) - 0.5
        cov = d.groupby("ts").apply(lambda x: (x["rk"] * x["ex"]).sum())
        out["slope_clustered_t"] = cov.mean() / (cov.std() / np.sqrt(len(cov)))
        return out.round(4)
    res["r30z_all_clustered"] = clustered(g, "r30z")
    res["r30z_positive_only"] = clustered(g[g.r30 > 0], "r30z", 4)
    res["r14z_all"] = clustered(g, "r14z")
    res["r60z_all"] = clustered(g, "r60z")
    tr = g[g.r30 > 0]
    res["trending_fc_on_vs_off"] = tr.assign(on=tr.fc > 0).groupby("on")["ex"].agg(["size", "mean", "std"]).assign(t=lambda x: x["mean"] / (x["std"] / np.sqrt(x["size"]))).round(4)
    # r30z top vs bottom by year
    g["top"] = g.groupby("year")["r30z"].transform(lambda s: s > s.quantile(0.8))
    g["bot"] = g.groupby("year")["r30z"].transform(lambda s: s < s.quantile(0.2))
    res["r30z_top_minus_bottom_by_year"] = g.groupby("year").apply(lambda x: pd.Series({"top": x.loc[x.top, "ex"].mean(), "bot": x.loc[x.bot, "ex"].mean(), "n": len(x)})).round(4)
    # weekday, cross-coin mean per day then t over days, and by coin consistency
    dd = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            d = df.copy(); d["coin"] = coin; dd.append(d)
    D = pd.concat(dd).dropna(subset=["coin_return"])
    D["day"] = pd.to_datetime(D["day"])
    daym = D.groupby("day")["coin_return"].mean()
    wdf = pd.DataFrame({"r": daym, "wd": daym.index.dayofweek, "yr": daym.index.year})
    res["weekday_day_clustered"] = wdf.groupby("wd")["r"].agg(["size", "mean", "std"]).assign(t=lambda x: x["mean"] / (x["std"] / np.sqrt(x["size"]))).round(5)
    res["weekday_by_year_mean"] = wdf.groupby(["yr", "wd"])["r"].mean().unstack().round(4)
    D["wd"] = D["day"].dt.dayofweek
    pc = D.groupby(["coin", "wd"])["coin_return"].mean().unstack()
    res["share_coins_wd_positive"] = (pc > 0).mean().round(3)
    # book on weekday
    D["bk"] = D["book_return"]
    bm = D.groupby("day")["bk"].mean()
    res["book_by_weekday"] = bm.groupby(bm.index.dayofweek).agg(["size", "mean"]).round(5)
    return res
