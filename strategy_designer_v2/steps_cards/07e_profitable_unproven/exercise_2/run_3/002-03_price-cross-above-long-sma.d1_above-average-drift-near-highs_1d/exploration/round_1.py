def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin in data["days"]:
        for w, d in data["days"][coin].items():
            d = d.copy()
            b = data["bars"][coin][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            al = b.groupby("day")["postRebalance_current_allocation"].last()
            fc = b.groupby("day")["forecast"].last()
            dist = None
            d["dayk"] = pd.to_datetime(d["day"]).dt.floor("D")
            d["alloc_prev"] = d["dayk"].map(al).shift(1)
            d["fc_prev"] = d["dayk"].map(fc).shift(1)
            cl = d["close"]
            d["ret20_prev"] = (cl / cl.shift(20) - 1).shift(1)
            d["above200"] = np.nan
            d["coin"] = coin; d["w"] = w
            d["year"] = pd.to_datetime(d["day"]).dt.year
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D = D.dropna(subset=["book_return", "coin_return"])
    mu = D.groupby("coin")["coin_return"].mean()
    D["mu"] = D["coin"].map(mu)
    D["drift_part"] = D["alloc_prev"] * D["mu"]
    book = D.groupby(["w", "day"])["book_return"].mean()
    hold = D.groupby(["w", "day"])["coin_return"].mean()
    drift = D.groupby(["w", "day"])["drift_part"].mean()
    out["book_mean_vs_drift"] = pd.Series({"book_mean": book.mean(), "drift_part": drift.mean(),
        "timing": book.mean() - drift.mean(), "hold_mean": hold.mean(), "mean_alloc": D["alloc_prev"].mean(),
        "n_days": len(book)})
    g = D.groupby("coin")
    out["per_coin"] = pd.DataFrame({"book_mean": g["book_return"].mean(), "drift": g["drift_part"].mean(),
        "hold": g["coin_return"].mean(), "alloc": g["alloc_prev"].mean(),
        "share_in": g["alloc_prev"].apply(lambda s: (s > 0).mean())})
    gw = D.groupby("w")
    out["per_window"] = pd.DataFrame({"book": gw["book_return"].mean(), "drift": gw["drift_part"].mean(),
        "hold": gw["coin_return"].mean(), "alloc": gw["alloc_prev"].mean()})
    gy = D.groupby("year")
    out["per_year"] = pd.DataFrame({"book": gy["book_return"].mean(), "drift": gy["drift_part"].mean(),
        "hold": gy["coin_return"].mean(), "n": gy.size()})
    # in vs out: coin return next day when in vs out
    D["in"] = D["alloc_prev"] > 0
    gi = D.groupby("in")["coin_return"]
    out["coin_ret_in_vs_out"] = pd.DataFrame({"mean": gi.mean(), "n": gi.size(), "std": gi.std()})
    # forecast strength buckets among in
    I = D[D["fc_prev"] > 0].copy()
    I["q"] = pd.qcut(I["fc_prev"], 4, labels=False, duplicates="drop")
    gq = I.groupby("q")
    out["fc_quartile_next_day"] = pd.DataFrame({"fc_mean": gq["fc_prev"].mean(), "coin_ret": gq["coin_return"].mean(),
        "excess": gq["coin_return"].mean() - gq["mu"].mean(), "n": gq.size()})
    # trades
    T = pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values()], ignore_index=True)
    pl = T["profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(T), "sum_pl": pl.sum(), "top10_sum": pl.head(10).sum(),
        "top5pct_sum": pl.head(int(len(pl) * 0.05)).sum(), "median": pl.median(), "win": (pl > 0).mean(),
        "mean_dur_days": T["duration_minutes"].mean() / 1440})
    # forward returns at horizons on grid, conditioned on forecast>0 vs ==0
    res = []
    for h in [1, 5, 10, 20, 40, 60]:
        a = []
        for coin in data["bars"]:
            for w, b in data["bars"][coin].items():
                c = b["close"].values; f = b["forecast"].values
                idx = np.arange(0, len(c) - h, h)
                for i in idx:
                    a.append((coin, f[i], c[i + h] / c[i] - 1))
        A = pd.DataFrame(a, columns=["coin", "f", "r"])
        A["r_ex"] = A["r"] - A["coin"].map(A.groupby("coin")["r"].mean())
        on = A[A["f"] > 0]["r_ex"]; off = A[A["f"] <= 0]["r_ex"]
        t = stats.ttest_ind(on, off, equal_var=False).statistic
        rho = stats.spearmanr(A.loc[A.f > 0, "f"], A.loc[A.f > 0, "r_ex"]).correlation
        res.append((h, on.mean(), len(on), off.mean(), len(off), t, rho))
    out["horizons_on_minus_off"] = pd.DataFrame(res, columns=["h", "on_ex", "n_on", "off_ex", "n_off", "t_welch", "spearman_f_in_on"])
    return out
