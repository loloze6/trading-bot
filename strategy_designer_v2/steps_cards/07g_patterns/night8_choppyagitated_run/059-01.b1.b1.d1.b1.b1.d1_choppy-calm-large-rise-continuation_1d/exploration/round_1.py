def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r7 = c / c.shift(7) - 1
            s = r7 / r7.abs().rolling(30, min_periods=20).mean()
            r1 = c / c.shift(1) - 1
            vol30 = r1.rolling(30, min_periods=20).std()
            r60 = c / c.shift(60) - 1
            f14 = c.shift(-14) / c - 1
            f3 = c.shift(-3) / c - 1
            rng = (df["high"] - df["low"]) / c
            clv = (c - df["low"]) / (df["high"] - df["low"]).replace(0, np.nan)
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, len(df), 14):
                if np.isnan(f14.iloc[i]): continue
                rows.append(dict(coin=coin, w=w, i=i, day=ts.iloc[i].normalize(),
                                 wd=ts.iloc[i].dayofweek, year=ts.iloc[i].year,
                                 reg=df["regime"].iloc[i], s=s.iloc[i], r7=r7.iloc[i],
                                 r1s=r1.iloc[i] / vol30.iloc[i] if vol30.iloc[i] else np.nan,
                                 r60=r60.iloc[i], f14=f14.iloc[i], f3=f3.iloc[i],
                                 fc=df["forecast"].iloc[i], rng=rng.iloc[i], clv=clv.iloc[i]))
    g = pd.DataFrame(rows)
    g["ex"] = g["f14"] - g.groupby("coin")["f14"].transform("mean")
    g["inprof"] = g["reg"] == "unknown"
    out = {}
    def summ(x, col="ex"):
        x = x.dropna(subset=[col])
        d = x.groupby("day")[col].sum()
        n = len(x); m = x[col].mean()
        se = np.sqrt((d ** 2).sum()) / n if n else np.nan
        return pd.Series(dict(n=n, days=x["day"].nunique(), mean=m, t=m / se if se else np.nan))
    out["by_profile"] = g.groupby("inprof").apply(summ)
    g["sbin"] = pd.cut(g["s"], [-np.inf, -1.5, -0.75, -0.25, 0.25, 0.75, 1.5, np.inf])
    out["in_prof_by_s"] = g[g.inprof].groupby("sbin").apply(summ)
    out["out_prof_by_s"] = g[~g.inprof].groupby("sbin").apply(summ)
    g["r60bin"] = pd.cut(g["r60"], [-np.inf, -0.3, -0.1, 0.1, 0.3, np.inf])
    out["out_prof_by_r60"] = g[~g.inprof].groupby("r60bin").apply(summ)
    g["r1bin"] = pd.cut(g["r1s"], [-np.inf, -2, -1, 0, 1, 2, np.inf])
    out["all_by_1day_scaled"] = g.groupby("r1bin").apply(summ)
    out["all_by_year"] = g.groupby("year").apply(summ)
    out["all_by_window"] = g.groupby("w").apply(summ)
    # in-profile: slope of ex on s for falls and rises
    for name, sub in [("in_rise", g[g.inprof & (g.s > 0)]), ("in_fall", g[g.inprof & (g.s < 0)]),
                      ("out_rise", g[~g.inprof & (g.s > 0)]), ("out_fall", g[~g.inprof & (g.s < 0)])]:
        sub = sub.dropna(subset=["s", "ex"])
        if len(sub) > 10:
            lr = stats.linregress(sub["s"], sub["ex"])
            out["slope_" + name] = f"n={len(sub)} slope={lr.slope:.4f} t={lr.slope/lr.stderr:.2f}"
    # book daily
    dd = []
    for coin, wins in days.items():
        for w, df in wins.items():
            x = df.copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    D = pd.concat(dd)
    D["day"] = pd.to_datetime(D["day"])
    book = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    book["wd"] = book.index.get_level_values("day").dayofweek
    out["book_by_weekday"] = book.groupby("wd")[["book_return", "coin_return"]].agg(["mean", "count"])
    q = book["book_return"].quantile([0.02, 0.98])
    out["coin_ret_around_book_extremes"] = pd.Series(dict(
        coin_on_worst=book.loc[book.book_return <= q.iloc[0], "coin_return"].mean(),
        coin_on_best=book.loc[book.book_return >= q.iloc[1], "coin_return"].mean(),
        n_each=int((book.book_return <= q.iloc[0]).sum())))
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tt = t.copy(); tt["coin"] = coin; tr.append(tt)
    T = pd.concat(tr)
    T["fcbin"] = pd.qcut(T["entry_forecast"].rank(method="first"), 3, labels=["low", "mid", "high"])
    out["trades_by_entry_fc"] = T.groupby("fcbin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"])
    return out
