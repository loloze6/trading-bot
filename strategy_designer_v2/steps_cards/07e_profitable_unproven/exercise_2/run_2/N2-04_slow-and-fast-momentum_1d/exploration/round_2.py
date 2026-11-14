def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
    def todays(s):
        return pd.to_datetime(s, utc=True).dt.floor("D")
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            b = data["bars"][coin][w].copy()
            b["day"] = todays(b["timestamp"])
            alloc = b.groupby("day")["postRebalance_current_allocation"].last()
            fc = b.groupby("day")["forecast"].last()
            cl = b.groupby("day")["close"].last()
            dd = d.copy()
            dd["day"] = todays(dd["day"])
            dd = dd.set_index("day")
            dd["alloc_prev"] = alloc.reindex(dd.index).shift(1)
            dd["fc_prev"] = fc.reindex(dd.index).shift(1)
            c = cl.reindex(dd.index)
            dd["r60"] = (c / c.shift(60) - 1).shift(1)
            dd["r20"] = (c / c.shift(20) - 1).shift(1)
            dd["vol20"] = dd["coin_return"].rolling(20).std().shift(1)
            dd["coin"] = coin; dd["window"] = w
            dd["year"] = dd.index.year
            rows.append(dd.reset_index())
    D = pd.concat(rows, ignore_index=True)
    D = D.dropna(subset=["book_return", "coin_return"])
    def sh(x):
        return x.mean() / x.std() * np.sqrt(365) if x.std() > 0 else np.nan
    out["by_coin"] = D.groupby("coin").agg(book_mean=("book_return", "mean"), book_sh=("book_return", sh),
        coin_mean=("coin_return", "mean"), coin_sh=("coin_return", sh), mean_alloc=("alloc_prev", "mean"),
        share_in=("alloc_prev", lambda x: (x > 0).mean()), sum_book=("book_return", "sum"))
    out["by_window"] = D.groupby("window").agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"),
        sum_book=("book_return", "sum"), share_in=("alloc_prev", lambda x: (x > 0).mean()))
    out["by_year"] = D.groupby("year").agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"),
        sum_book=("book_return", "sum"), share_in=("alloc_prev", lambda x: (x > 0).mean()), n=("book_return", "size"))
    D["inmkt"] = D["alloc_prev"] > 0
    out["in_vs_out"] = D.groupby("inmkt").agg(n=("coin_return", "size"), coin_mean=("coin_return", "mean"),
        coin_sd=("coin_return", "std"), book_mean=("book_return", "mean"),
        coin_t=("coin_return", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    a = D.loc[D.inmkt, "coin_return"]; bb = D.loc[~D.inmkt, "coin_return"]
    out["coin_ret_in_minus_out_welch_t"] = float(stats.ttest_ind(a, bb, equal_var=False).statistic)
    D["alloc_x_drift"] = D["alloc_prev"] * D.groupby("coin")["coin_return"].transform("mean")
    D["alloc_x_coin"] = D["alloc_prev"] * D["coin_return"]
    tim = D.alloc_x_coin - D.alloc_x_drift
    out["decomp"] = pd.Series({"book_mean": D.book_return.mean(), "alloc_x_coin": D.alloc_x_coin.mean(),
        "exposure_drift": D.alloc_x_drift.mean(), "timing": tim.mean(),
        "timing_t": tim.mean() / tim.std() * np.sqrt(tim.notna().sum()), "mean_alloc": D.alloc_prev.mean()})
    D["state"] = np.sign(D["r60"]).astype(str) + "/" + np.sign(D["r20"]).astype(str)
    out["by_state"] = D.groupby("state").agg(n=("book_return", "size"), book_mean=("book_return", "mean"),
        coin_mean=("coin_return", "mean"), mean_alloc=("alloc_prev", "mean"), sum_book=("book_return", "sum"))
    D["volq"] = D.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 4, labels=False, duplicates="drop"))
    out["by_volq"] = D.groupby("volq").agg(n=("book_return", "size"), book_mean=("book_return", "mean"),
        coin_mean=("coin_return", "mean"), mean_alloc=("alloc_prev", "mean"), sum_book=("book_return", "sum"))
    act = D[D.inmkt].copy()
    act["fcq"] = pd.qcut(act["fc_prev"].rank(method="first"), 4, labels=False)
    out["active_by_fcq"] = act.groupby("fcq").agg(n=("coin_return", "size"), fc=("fc_prev", "mean"),
        coin_mean=("coin_return", "mean"), book_mean=("book_return", "mean"), alloc=("alloc_prev", "mean"))
    loo = {}
    for c in D.coin.unique():
        loo[c] = sh(D.loc[D.coin != c, "book_return"])
    out["sharpe_without_coin"] = pd.Series(loo)
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    pl = T["net_profit_loss_percent"].dropna().sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(pl), "win_rate": (pl > 0).mean(), "sum": pl.sum(),
        "top10_sum": pl.head(10).sum(), "top5pct_sum": pl.head(max(1, len(pl) // 20)).sum(),
        "median": pl.median(), "mean_duration_days": T["duration_minutes"].mean() / 1440})
    # book's best days share
    br = D["book_return"].sort_values(ascending=False)
    out["book_top_days"] = pd.Series({"n_days": len(br), "sum_all": br.sum(), "sum_top1pct": br.head(len(br)//100).sum(),
        "sum_top5pct": br.head(len(br)//20).sum()})
    return out
