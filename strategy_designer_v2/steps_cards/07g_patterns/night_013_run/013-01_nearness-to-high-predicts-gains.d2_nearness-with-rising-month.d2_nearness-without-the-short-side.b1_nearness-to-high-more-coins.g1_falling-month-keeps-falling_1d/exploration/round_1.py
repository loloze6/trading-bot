def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 7
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            v = b["volume"].astype(float)
            r1 = c.pct_change()
            ret30 = c / c.shift(30) - 1
            hi60 = c.rolling(60, min_periods=30).max()
            depth = c / hi60 - 1
            ret7p = c / c.shift(7) - 1
            vol20 = r1.rolling(20, min_periods=15).std()
            vrel = v / v.rolling(20, min_periods=15).mean()
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            idx = np.arange(0, len(b), H)
            for i in idx:
                rows.append(dict(coin=coin, w=w, ret30=ret30[i], depth=depth[i], ret7p=ret7p[i],
                                 vol20=vol20[i], vrel=vrel[i], fwd=fwd[i], reg=b["regime"][i],
                                 fc=b["forecast"][i], year=ts[i].year))
            dd = pd.DataFrame(dict(coin=coin, w=w, wd=ts.dt.weekday, r1=r1, fwd1=fwd1, ret7p=ret7p,
                                   alloc=b["postRebalance_current_allocation"]))
            daily.append(dd)
    g = pd.DataFrame(rows).dropna(subset=["fwd"])
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    out = {}
    def bucket(df, col, q=5):
        d = df.dropna(subset=[col, "ex"]).copy()
        d["b"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        t = d.groupby("b")["ex"].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        sl = stats.linregress(d[col], d["ex"])
        t.loc["slope_t", "mean"] = sl.slope / sl.stderr
        return t.round(4)
    out["depth_fallingmonth"] = bucket(g[g.ret30 < 0], "depth")
    out["depth_risingmonth"] = bucket(g[g.ret30 >= 0], "depth")
    out["ret30_all"] = bucket(g, "ret30")
    out["ret7p_all"] = bucket(g, "ret7p")
    out["vol20_all"] = bucket(g, "vol20")
    out["vrel_all"] = bucket(g, "vrel")
    out["vrel_fallingmonth"] = bucket(g[g.ret30 < 0], "vrel")
    # by year in falling month: depth slope
    yr = {}
    for y, d in g[(g.ret30 < 0)].dropna(subset=["depth"]).groupby("year"):
        if len(d) > 30:
            sl = stats.linregress(d["depth"], d["ex"]); yr[y] = (round(sl.slope, 4), round(sl.slope / sl.stderr, 2), len(d))
    out["depth_slope_by_year_falling"] = pd.DataFrame(yr, index=["slope", "t", "n"]).T
    D = pd.concat(daily).dropna(subset=["fwd1"])
    D["ex1"] = D["fwd1"] - D.groupby("coin")["fwd1"].transform("mean")
    wdt = D.groupby("wd")["ex1"].agg(["mean", "count", "std"])
    wdt["t"] = wdt["mean"] / (wdt["std"] / np.sqrt(wdt["count"]))
    out["weekday_next_day_excess"] = wdt.round(5)
    # book daily
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bk.append(d.assign(coin=coin, w=w)[["coin", "w", "book_return", "coin_return"]])
    B = pd.concat(bk).dropna()
    B["absb"] = B["book_return"].abs()
    big = B.sort_values("book_return")
    n = max(1, int(len(B) * 0.01))
    out["book_worst1pct"] = pd.Series(dict(mean_book=big.head(n)["book_return"].mean(), mean_coin=big.head(n)["coin_return"].mean(), n=n))
    out["book_best1pct"] = pd.Series(dict(mean_book=big.tail(n)["book_return"].mean(), mean_coin=big.tail(n)["coin_return"].mean(), n=n))
    out["book_by_coin"] = B.groupby("coin")["book_return"].agg(["mean", "count"]).assign(sh=B.groupby("coin")["book_return"].apply(lambda s: s.mean() / s.std() * np.sqrt(365))).round(4)
    return out
