def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    # book daily returns, per coin/window and pooled per day
    rows = []
    for c in days:
        for w, d in days[c].items():
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            alloc = b.groupby("day")["postRebalance_current_allocation"].last().shift(1)
            dd = d.copy(); dd["day"] = pd.to_datetime(dd["day"]).dt.floor("D")
            dd = dd.set_index("day"); dd["alloc_prev"] = alloc.reindex(dd.index)
            dd["coin"] = c; dd["window"] = w
            rows.append(dd.reset_index())
    D = pd.concat(rows, ignore_index=True)
    D = D.dropna(subset=["book_return", "coin_return"])
    # coin mean daily return over all windows
    mu = D.groupby("coin")["coin_return"].mean()
    D["mkt_gain"] = D["alloc_prev"].fillna(0) * D["coin"].map(mu)
    D["side"] = np.sign(D["alloc_prev"].fillna(0))
    pooled = D.groupby("day")[["book_return", "mkt_gain"]].mean()
    out["book_mean_daily_vs_mkt"] = pd.Series({"book_mean": pooled.book_return.mean(), "mkt_gain": pooled.mkt_gain.mean(),
        "timing": pooled.book_return.mean() - pooled.mkt_gain.mean(), "days": len(pooled),
        "t_book": pooled.book_return.mean() / pooled.book_return.std() * np.sqrt(len(pooled))})
    # per coin
    pc = D.groupby("coin").agg(mean=("book_return", "mean"), n=("book_return", "size"), sum=("book_return", "sum"),
                               long_share=("side", lambda s: (s > 0).mean()), short_share=("side", lambda s: (s < 0).mean()))
    out["per_coin"] = pc
    # per window
    out["per_window"] = D.groupby("window").agg(mean=("book_return", "mean"), sum=("book_return", "sum"), n=("book_return", "size"),
                                              coin_mean=("coin_return", "mean"))
    # by side: contribution
    out["by_side"] = D.groupby("side").agg(sum=("book_return", "sum"), mean=("book_return", "mean"), n=("book_return", "size"),
                                         coin_mean=("coin_return", "mean"))
    # forward returns grid with trend, horizons
    recs = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; n = len(b)
            hi = b["high"].rolling(20).max(); lo = b["low"].rolling(20).min()
            pos = ((b["close"] - lo) / (hi - lo) * 2 - 1).values
            tr = (b["close"] / b["close"].shift(60) - 1).values
            r5 = b["close"].pct_change(5).values
            for h in [1, 3, 5, 10, 20]:
                for i in range(0, n - h, h):
                    recs.append((c, w, h, i, b["regime"].iloc[i], b["forecast"].iloc[i], pos[i], tr[i], r5[i], cl[i + h] / cl[i] - 1))
    G = pd.DataFrame(recs, columns=["coin", "window", "h", "i", "regime", "fc", "pos", "trend", "r5", "fwd"])
    dr = G.groupby(["coin", "h"])["fwd"].mean().rename("drift")
    G = G.join(dr, on=["coin", "h"]); G["ex"] = G["fwd"] - G["drift"]
    G["inprof"] = G["regime"] == "unknown"
    res = []
    for h in [1, 3, 5, 10, 20]:
        for ip in [True, False]:
            g = G[(G.h == h) & (G.inprof == ip)].dropna(subset=["pos", "ex"])
            if len(g) > 30:
                s = stats.linregress(g["pos"], g["ex"])
                res.append((h, ip, len(g), s.slope, s.slope / s.stderr))
    out["slope_pos_by_h"] = pd.DataFrame(res, columns=["h", "inprof", "n", "slope", "t"])
    g = G[(G.h == 5) & G.inprof].dropna(subset=["pos", "ex"]).copy()
    g["trendp"] = pd.cut(g["trend"], [-9, -0.1, 0.1, 9], labels=["falling", "choppy", "rising"])
    g["trendp"] = g["trendp"].cat.add_categories("na").fillna("na")
    res = []
    for k, gg in g.groupby("trendp"):
        if len(gg) > 30:
            s = stats.linregress(gg["pos"], gg["ex"])
            res.append((k, len(gg), s.slope, s.slope / s.stderr, gg["fwd"].mean()))
    out["h5_inprof_by_trend"] = pd.DataFrame(res, columns=["trend", "n", "slope", "t", "fwd_mean"])
    g["q"] = pd.qcut(g["pos"], 5, labels=False)
    out["h5_inprof_pos_quintile"] = g.groupby("q").agg(pos=("pos", "mean"), ex=("ex", "mean"), n=("ex", "size"),
                                                      tstat=("ex", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    out["h5_inprof_by_window_slope"] = g.groupby("window").apply(lambda x: pd.Series({"n": len(x),
        "t": stats.linregress(x["pos"], x["ex"]).slope / stats.linregress(x["pos"], x["ex"]).stderr if len(x) > 10 else np.nan}))
    return out
