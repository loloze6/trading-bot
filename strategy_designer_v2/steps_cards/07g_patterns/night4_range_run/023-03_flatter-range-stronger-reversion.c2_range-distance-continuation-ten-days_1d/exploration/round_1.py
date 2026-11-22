def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    H = 10
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            n = len(c)
            hi = pd.Series(c).rolling(30, min_periods=30).max().values
            lo = pd.Series(c).rolling(30, min_periods=30).min().values
            pos = np.where(hi > lo, 2 * (c - lo) / (hi - lo) - 1, np.nan)
            r30 = pd.Series(c).pct_change(30).values
            r1 = pd.Series(c).pct_change(1).values
            r5 = pd.Series(c).pct_change(5).values
            vol20 = pd.Series(r1).rolling(20).std().values
            width = (hi - lo) / c
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, fc=b["forecast"].iloc[i], pos=pos[i], r30=r30[i],
                                 r1=r1[i], r5=r5[i], vol=vol20[i], width=width[i],
                                 wd=ts.iloc[i].dayofweek, yr=ts.iloc[i].year,
                                 f10=c[i + H] / c[i] - 1, f1=c[i + 1] / c[i] - 1, f5=c[i + 5] / c[i] - 1))
    d = pd.DataFrame(rows)
    for k in ["f10", "f1", "f5"]:
        d[k + "x"] = d[k] - d.groupby("coin")[k].transform("mean")
    out = {}
    def tab(col, q=5):
        x = d.dropna(subset=[col]).copy()
        x["b"] = pd.qcut(x[col], q, labels=False, duplicates="drop")
        g = x.groupby("b")
        t = g.agg(lo=(col, "min"), hi=(col, "max"), n=("f10x", "size"),
                  f1x=("f1x", "mean"), f5x=("f5x", "mean"), f10x=("f10x", "mean"))
        t["t10"] = g["f10x"].apply(lambda s: s.mean() / (s.std() / np.sqrt(len(s))))
        return t
    out["by_forecast"] = tab("fc")
    out["by_pos"] = tab("pos")
    out["by_r30"] = tab("r30")
    out["by_r1"] = tab("r1")
    out["by_r5"] = tab("r5")
    out["by_vol"] = tab("vol")
    out["by_width"] = tab("width")
    # pos slope inside trend terciles of |r30|
    x = d.dropna(subset=["pos", "r30"]).copy()
    x["tr"] = pd.qcut(x["r30"].abs(), 3, labels=["flat", "mid", "trend"])
    res = {}
    for k, g in x.groupby("tr"):
        s = stats.linregress(g["pos"], g["f10x"])
        res[k] = dict(slope=s.slope, t=s.slope / s.stderr, n=len(g))
    out["pos_slope_by_trend"] = pd.DataFrame(res).T
    res = {}
    for k, g in x.assign(wq=pd.qcut(x["width"], 3, labels=["narrow", "mid", "wide"])).groupby("wq"):
        s = stats.linregress(g["pos"], g["f10x"])
        res[k] = dict(slope=s.slope, t=s.slope / s.stderr, n=len(g))
    out["pos_slope_by_width"] = pd.DataFrame(res).T
    res = {}
    for k, g in x.groupby("coin"):
        s = stats.linregress(g["pos"], g["f10x"])
        res[k] = dict(slope=s.slope, t=s.slope / s.stderr, n=len(g))
    out["pos_slope_by_coin"] = pd.DataFrame(res).T
    res = {}
    for k, g in x.groupby("yr"):
        s = stats.linregress(g["pos"], g["f10x"])
        res[k] = dict(slope=s.slope, t=s.slope / s.stderr, n=len(g))
    out["pos_slope_by_year"] = pd.DataFrame(res).T
    # daily weekday on days table
    dd = []
    for coin in days:
        for w, t in days[coin].items():
            t = t.copy(); t["coin"] = coin; t["w"] = w; dd.append(t)
    dd = pd.concat(dd)
    dd["wd"] = pd.to_datetime(dd["day"]).dt.dayofweek
    g = dd.groupby("wd")
    out["weekday"] = pd.DataFrame({"coin_mean": g["coin_return"].mean(), "book_mean": g["book_return"].mean(),
                                   "coin_t": g["coin_return"].apply(lambda s: s.mean() / (s.std() / np.sqrt(s.count()))),
                                   "n": g["coin_return"].count()})
    # book: daily book across coins
    bk = dd.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    q = bk["book_return"].quantile([0.05, 0.95])
    out["book_extremes"] = pd.DataFrame({
        "worst5pct_book": [bk.loc[bk.book_return <= q.iloc[0], "book_return"].mean(), bk.loc[bk.book_return <= q.iloc[0], "coin_return"].mean()],
        "best5pct_book": [bk.loc[bk.book_return >= q.iloc[1], "book_return"].mean(), bk.loc[bk.book_return >= q.iloc[1], "coin_return"].mean()]},
        index=["book", "coin"])
    out["book_coin_corr"] = float(bk.corr().iloc[0, 1])
    return out
