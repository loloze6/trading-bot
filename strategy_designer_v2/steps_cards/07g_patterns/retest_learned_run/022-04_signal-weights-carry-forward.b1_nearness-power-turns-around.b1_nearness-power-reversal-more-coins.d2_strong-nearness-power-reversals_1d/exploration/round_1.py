def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            if n < 40: continue
            r1 = pd.Series(c).pct_change().values
            vol20 = pd.Series(r1).rolling(20).std().values
            mom20 = pd.Series(c).pct_change(20).values
            mom5 = pd.Series(c).pct_change(5).values
            hi = pd.Series(c).rolling(60, min_periods=20).max().values
            near = c / hi - 1
            ts = pd.to_datetime(b["timestamp"])
            fc = b["forecast"].astype(float).values
            alloc = b["postRebalance_current_allocation"].astype(float).values
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, year=ts.iloc[i].year, wd=ts.iloc[i].dayofweek,
                                 fwd=c[i+H]/c[i]-1, r1=r1[i], vol=vol20[i], mom20=mom20[i],
                                 mom5=mom5[i], near=near[i], fc=fc[i], alloc=alloc[i]))
    g = pd.DataFrame(rows)
    g["drift"] = g.groupby("coin")["fwd"].transform("mean")
    g["ex"] = g["fwd"] - g["drift"]
    g["volz"] = g.groupby("coin")["vol"].transform(lambda s: (s - s.mean())/s.std())
    def tab(col, q=5):
        d = g.dropna(subset=[col, "ex"]).copy()
        d["b"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        out = d.groupby("b")["ex"].agg(["mean", "count", "std"])
        out["t"] = out["mean"]/(out["std"]/np.sqrt(out["count"]))
        sl = stats.linregress(d[col].rank(pct=True), d["ex"])
        out["rank_slope_t"] = sl.slope/sl.stderr
        return out.round(5)
    res = {}
    res["fc_quintile"] = tab("fc")
    res["r1_quintile"] = tab("r1")
    res["mom5_quintile"] = tab("mom5")
    res["mom20_quintile"] = tab("mom20")
    res["near60_quintile"] = tab("near")
    res["vol_quintile"] = tab("vol")
    # mom20 slope within vol terciles
    d = g.dropna(subset=["mom20", "volz", "ex"]).copy()
    d["vt"] = pd.qcut(d["volz"], 3, labels=False)
    out = {}
    for k, s in d.groupby("vt"):
        z = s.groupby("coin")["mom20"].transform(lambda x: (x - x.mean())/x.std())
        sl = stats.linregress(z.fillna(0), s["ex"])
        out[k] = dict(slope=sl.slope, t=sl.slope/sl.stderr, n=len(s))
    res["mom20_slope_by_vol_tercile"] = pd.DataFrame(out).T.round(5)
    wd = g.groupby("wd")["ex"].agg(["mean", "count", "std"]); wd["t"] = wd["mean"]/(wd["std"]/np.sqrt(wd["count"]))
    res["start_weekday"] = wd.round(5)
    # book daily by year, gain vs coin
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    D = pd.concat(dd).dropna(subset=["book_return"])
    D["year"] = pd.to_datetime(D["day"]).dt.year
    daily = D.groupby(["day", "year"])[["book_return", "coin_return"]].mean().reset_index()
    yr = daily.groupby("year")[["book_return", "coin_return"]].agg(["mean", "count"])
    res["book_by_year"] = yr.round(5)
    # book returns by daily-day weekday
    daily["wd"] = pd.to_datetime(daily["day"]).dt.dayofweek
    res["book_by_weekday"] = daily.groupby("wd")["book_return"].agg(["mean", "std", "count"]).round(5)
    # per coin forecast slope t
    pc = {}
    for coin, s in g.dropna(subset=["fc"]).groupby("coin"):
        sl = stats.linregress(s["fc"], s["ex"]); pc[coin] = dict(slope=sl.slope, t=sl.slope/sl.stderr, n=len(s))
    res["fc_slope_by_coin"] = pd.DataFrame(pc).T.round(5)
    res["n_grid"] = len(g)
    return res
