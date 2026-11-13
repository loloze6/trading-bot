def explore(data):
    import pandas as pd, numpy as np
    days = data["days"]; trades = data["trades"]; bars = data["bars"]
    rows = []
    for c in days:
        for w, d in days[c].items():
            x = d[["day", "book_return", "coin_return"]].copy()
            x["coin"] = c; x["window"] = w
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            reg = b.groupby("day")["regime"].last()
            alloc = b.groupby("day")["postRebalance_current_allocation"].last()
            x["day"] = pd.to_datetime(x["day"])
            x = x.merge(reg.rename("regime"), left_on="day", right_index=True, how="left")
            x = x.merge(alloc.rename("alloc"), left_on="day", right_index=True, how="left")
            x = x.sort_values("day")
            x["mom20"] = x["coin_return"].rolling(20).sum().shift(1)
            x["vol20"] = x["coin_return"].rolling(20).std().shift(1)
            rows.append(x)
    A = pd.concat(rows)
    A = A.dropna(subset=["book_return"])
    book = A.groupby(["window", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean"),
                                            mom=("mom20", "mean"), vol=("vol20", "mean")).reset_index()
    book["year"] = book["day"].dt.year
    def sh(s): return s.mean() / s.std() * np.sqrt(365) if s.std() > 0 else np.nan
    out = {}
    tot = book["br"].sum()
    bw = book.groupby("window")["br"].agg(["mean", "count", "sum"])
    bw["share_of_total"] = bw["sum"] / tot
    bw["sharpe"] = book.groupby("window")["br"].apply(sh)
    bw["hold_mean"] = book.groupby("window")["cr"].mean()
    out["by_window"] = bw.round(4)
    by = book.groupby("year")["br"].agg(["mean", "count", "sum"])
    by["sharpe"] = book.groupby("year")["br"].apply(sh)
    by["hold_sharpe"] = book.groupby("year")["cr"].apply(sh)
    out["by_year"] = by.round(4)
    # coin contribution to book: mean over days of book_return/6
    cc = A.groupby("coin")["book_return"].agg(["mean", "sum"])
    cc["share"] = cc["sum"] / cc["sum"].sum()
    cc["sharpe"] = A.groupby("coin")["book_return"].apply(sh)
    cc["hold_sharpe"] = A.groupby("coin")["coin_return"].apply(sh)
    cc["time_in_mkt"] = A.groupby("coin")["alloc"].apply(lambda s: (s.abs() > 1e-9).mean())
    out["by_coin"] = cc.round(4)
    # top days concentration
    s = book["br"].sort_values(ascending=False)
    n = len(s)
    out["top_days"] = pd.Series({"n_days": n, "total_sum": tot,
        "top1pct_share": s.iloc[:max(1, n // 100)].sum() / tot,
        "top5pct_share": s.iloc[:n // 20].sum() / tot,
        "sum_without_top1pct": s.iloc[n // 100:].sum()}).round(4)
    # market states
    b2 = book.dropna(subset=["mom", "vol"]).copy()
    b2["trend"] = np.where(b2["mom"] > 0, "up20", "down20")
    b2["volq"] = pd.qcut(b2["vol"], 3, labels=["calm", "mid", "volatile"])
    g = b2.groupby(["trend", "volq"])["br"].agg(["mean", "count", "sum"])
    g["t"] = b2.groupby(["trend", "volq"])["br"].apply(lambda x: x.mean() / x.std() * np.sqrt(len(x)))
    g["share"] = g["sum"] / b2["br"].sum()
    out["by_state"] = g.round(4)
    # regime labels (per coin)
    rg = A.groupby("regime")["book_return"].agg(["mean", "count"])
    out["by_regime"] = rg.round(5)
    # fees
    T = pd.concat([t.assign(coin=c, window=w) for c in trades for w, t in trades[c].items()])
    f = T.groupby("coin").agg(n=("net_profit_loss_percent", "size"),
                               gross=("profit_loss_percent", "mean"),
                               net=("net_profit_loss_percent", "mean"),
                               dur_days=("duration_minutes", lambda x: x.mean() / 1440),
                               win=("net_profit_loss_percent", lambda x: (x > 0).mean()))
    f["fee_share_of_gross"] = 1 - f["net"] / f["gross"]
    out["fees_by_coin"] = f.round(4)
    out["fees_all"] = pd.Series({"n": len(T), "gross_mean": T["profit_loss_percent"].mean(),
        "net_mean": T["net_profit_loss_percent"].mean(),
        "median_net": T["net_profit_loss_percent"].median(),
        "sides": str(T["side"].value_counts().to_dict())}).astype(str)
    return out
