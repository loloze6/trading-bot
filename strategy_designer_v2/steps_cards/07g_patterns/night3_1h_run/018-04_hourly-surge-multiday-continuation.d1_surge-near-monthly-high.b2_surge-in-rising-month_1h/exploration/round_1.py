def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            c = df["close"].astype(float).reset_index(drop=True)
            n = len(c)
            r24 = c / c.shift(24) - 1
            mabs = r24.abs().rolling(720, min_periods=360).mean()
            surge = r24 / mabs
            r720 = c / c.shift(720) - 1
            r168 = c / c.shift(168) - 1
            hi720 = c.rolling(720, min_periods=360).max()
            near = c / hi720 - 1
            vol = c.pct_change().rolling(720, min_periods=360).std()
            f240 = c.shift(-240) / c - 1
            f72 = c.shift(-72) / c - 1
            fc = df["forecast"].astype(float).reset_index(drop=True)
            idx = np.arange(0, n, 240)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            for i in idx:
                rows.append(dict(coin=coin, w=w, surge=surge[i], r720=r720[i], r168=r168[i],
                                 near=near[i], vol=vol[i], f240=f240[i], f72=f72[i], fc=fc[i],
                                 year=ts[i].year, wd=ts[i].dayofweek))
    g = pd.DataFrame(rows)
    g["drift"] = g.groupby("coin")["f240"].transform("mean")
    g["ex"] = g["f240"] - g["drift"]
    g["volq"] = g.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 4, labels=False, duplicates="drop"))
    out = {}
    def summ(gr, col="ex"):
        def f(s):
            s = s.dropna()
            return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s) > 2 else np.nan})
        return gr[col].apply(f).unstack()
    h = g.dropna(subset=["surge", "r720", "ex"]).copy()
    h["sq"] = pd.qcut(h["surge"], 5, labels=False)
    h["up30"] = (h["r720"] > 0).astype(int)
    out["ex240_by_surge_q_and_30d_sign"] = summ(h.groupby(["up30", "sq"]))
    h["rq"] = h.groupby("coin")["r720"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["ex240_by_30d_return_q"] = summ(h.groupby("rq"))
    h["r7q"] = h.groupby("coin")["r168"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["ex240_by_7d_return_q"] = summ(h.groupby("r7q"))
    h["nq"] = h.groupby("coin")["near"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["ex240_by_near_high_q"] = summ(h.groupby("nq"))
    out["ex240_by_volq"] = summ(h.groupby("volq"))
    out["ex240_by_year"] = summ(h.groupby("year"))
    out["ex240_by_coin_30dup"] = summ(h.groupby(["coin", "up30"]))
    # book
    d = []
    for coin, ws in days.items():
        for w, df in ws.items():
            x = df[["book_return", "coin_return"]].copy(); x["w"] = w; x["coin"] = coin
            x["year"] = pd.to_datetime(df["day"]).dt.year
            d.append(x)
    d = pd.concat(d)
    bd = d.groupby(["w", "year"])[["book_return", "coin_return"]].mean()
    bw = d.groupby(["w"]).apply(lambda x: x.groupby(level=0).size().shape[0] if False else None)
    by = d.groupby("year")[["book_return", "coin_return"]].agg(["mean", "std", "count"])
    out["book_by_year"] = by
    # per window: book chain and drawdown
    dd = {}
    for w, x in d.groupby("w"):
        m = x.groupby(x.index)["book_return"].mean() if False else None
    daily = d.reset_index().groupby(["w", "index"])[["book_return", "coin_return"]].mean()
    ws_stats = daily.groupby(level=0).agg(lambda s: (1 + s.fillna(0)).prod() - 1)
    out["window_total_return"] = ws_stats
    return out
