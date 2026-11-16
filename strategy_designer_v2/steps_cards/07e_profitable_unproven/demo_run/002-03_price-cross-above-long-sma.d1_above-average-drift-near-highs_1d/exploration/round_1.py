def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    # daily book decomposition
    rows = []
    for c in days:
        for w, d in days[c].items():
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            pos = b.groupby("day")["postRebalance_current_allocation"].last()
            dd = d.copy()
            dd["day"] = pd.to_datetime(dd["day"]).dt.floor("D")
            dd = dd.set_index("day")
            dd["pos_prev"] = pos.reindex(dd.index).shift(1)
            dd["coin"] = c; dd["window"] = w
            dd["year"] = dd.index.year
            reg = b.groupby("day")["regime"].last().reindex(dd.index).shift(1)
            dd["reg_prev"] = reg
            rows.append(dd.reset_index())
    D = pd.concat(rows, ignore_index=True)
    D = D.dropna(subset=["book_return", "coin_return"])
    mu = D.groupby("coin")["coin_return"].mean()
    D["mkt_gain"] = D["pos_prev"].fillna(0) * D["coin"].map(mu)
    # per-coin
    pc = D.groupby("coin").agg(book_mean=("book_return", "mean"), mkt_gain=("mkt_gain", "mean"),
                               coin_mean=("coin_return", "mean"), avg_pos=("pos_prev", "mean"),
                               n=("book_return", "size"))
    pc["timing"] = pc["book_mean"] - pc["mkt_gain"]
    pc["sum_book"] = D.groupby("coin")["book_return"].sum()
    out["by_coin"] = pc
    # per window: book averaged across coins per day
    daily = D.groupby(["window", "day"]).agg(book=("book_return", "mean"), mkt=("mkt_gain", "mean"),
                                            coin=("coin_return", "mean")).reset_index()
    pw = daily.groupby("window").agg(book_mean=("book", "mean"), mkt=("mkt", "mean"), coin=("coin", "mean"),
                                     book_sum=("book", "sum"), n=("book", "size"))
    pw["timing"] = pw["book_mean"] - pw["mkt"]
    pw["year"] = daily.groupby("window")["day"].first().dt.year
    out["by_window"] = pw
    out["total"] = pd.Series({"book_mean": daily["book"].mean(), "mkt": daily["mkt"].mean(),
                              "timing": daily["book"].mean() - daily["mkt"].mean(),
                              "coin_mean": daily["coin"].mean()})
    # book share of gain by top windows
    s = pw["book_sum"].sort_values(ascending=False)
    out["top3_window_share_of_sum"] = float(s.head(3).sum() / s.sum())
    # grades: forward returns at horizons on non-overlapping grid vs forecast, in-regime only
    res = []
    for h in [1, 3, 5, 10, 20, 40]:
        xs, ys = [], []
        for c in bars:
            allr = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                allr.append(cl[idx + h] / cl[idx] - 1)
            m = np.concatenate(allr).mean() if allr else 0
            for w, b in bars[c].items():
                cl = b["close"].values; f = b["forecast"].values
                idx = np.arange(0, len(cl) - h, h)
                xs.append(f[idx]); ys.append(cl[idx + h] / cl[idx] - 1 - m)
        x = np.concatenate(xs); y = np.concatenate(ys)
        ok = ~np.isnan(x) & ~np.isnan(y)
        x, y = x[ok], y[ok]
        lr = stats.linregress(x, y)
        on = x > 0
        t2 = stats.ttest_ind(y[on], y[~on], equal_var=False)
        xo, yo = x[on], y[on]
        lr2 = stats.linregress(xo, yo) if on.sum() > 3 else None
        res.append({"h": h, "n": len(x), "slope_t": lr.slope / lr.stderr, "n_on": int(on.sum()),
                    "on_mean": y[on].mean(), "off_mean": y[~on].mean(), "on_minus_off_t": t2.statistic,
                    "slope_t_within_on": lr2.slope / lr2.stderr if lr2 else np.nan})
    out["horizon_grades"] = pd.DataFrame(res)
    # trades concentration
    T = pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values()], ignore_index=True)
    pl = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(T), "sum": pl.sum(), "top10_sum": pl.head(10).sum(),
                               "win_share": (pl > 0).mean(), "median": pl.median()})
    # in-regime vs out: book by regime of prev day
    D["inpos"] = D["pos_prev"].fillna(0) > 0.01
    out["in_vs_out"] = D.groupby("inpos").agg(n=("coin_return", "size"), coin_mean=("coin_return", "mean"),
                                              book_mean=("book_return", "mean"))
    return out
