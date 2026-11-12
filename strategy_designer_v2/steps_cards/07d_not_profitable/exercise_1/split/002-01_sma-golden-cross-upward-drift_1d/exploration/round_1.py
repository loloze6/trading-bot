def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # trades
    tr = []
    for c, ws in data["trades"].items():
        for w, df in ws.items():
            if len(df):
                d = df.copy(); d["coin"] = c; d["win"] = w; tr.append(d)
    T = pd.concat(tr, ignore_index=True)
    T["days"] = T["duration_minutes"] / 1440
    out["trades_summary"] = pd.Series({
        "n": len(T), "mean_days": T["days"].mean(), "median_days": T["days"].median(),
        "gross_mean": T["profit_loss_percent"].mean(), "net_mean": T["net_profit_loss_percent"].mean(),
        "fee_mean": (T["profit_loss_percent"] - T["net_profit_loss_percent"]).mean(),
        "gross_sum": T["profit_loss_percent"].sum(), "net_sum": T["net_profit_loss_percent"].sum(),
        "win_share": (T["profit_loss_percent"] > 0).mean(),
        "long_share": (T["side"] == "LONG").mean()})
    T["dur_bin"] = pd.cut(T["days"], [0, 2, 5, 15, 50, 1000])
    out["by_duration"] = T.groupby("dur_bin", observed=True).agg(n=("days", "size"), gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    T["fbin"] = pd.cut(T["entry_forecast"], [-0.01, 5, 10, 15, 20.1])
    out["by_entry_forecast"] = T.groupby("fbin", observed=True).agg(n=("days", "size"), gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    out["by_coin_trades"] = T.groupby("coin").agg(n=("days", "size"), gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"), days=("days", "mean"))
    # days
    rows = []
    for c, ws in data["days"].items():
        b = data["bars"][c]
        for w, df in ws.items():
            d = df.copy(); d["coin"] = c; d["win"] = w
            bb = b[w][["timestamp", "postRebalance_current_allocation", "forecast"]].copy()
            bb["day"] = pd.to_datetime(bb["timestamp"]).dt.floor("D")
            bb = bb.groupby("day").last()
            d["day"] = pd.to_datetime(d["day"])
            if d["day"].dt.tz is None and bb.index.tz is not None:
                bb.index = bb.index.tz_localize(None)
            d = d.merge(bb, left_on="day", right_index=True, how="left")
            d["pos_prev"] = d["postRebalance_current_allocation"].shift(1)
            d["fc_prev"] = d["forecast"].shift(1)
            d["vol20"] = d["coin_return"].rolling(20).std()
            d["mom20"] = d["close"].pct_change(20)
            d["year"] = d["day"].dt.year
            rows.append(d)
    D = pd.concat(rows, ignore_index=True).dropna(subset=["book_return", "coin_return"])
    D["inpos"] = D["pos_prev"].abs() > 0.01
    out["in_vs_out"] = D.groupby("inpos").agg(n=("book_return", "size"), book=("book_return", "mean"), coin=("coin_return", "mean"), coin_sd=("coin_return", "std"))
    out["pos_stats"] = D["pos_prev"].describe()
    D["fcb"] = pd.cut(D["fc_prev"], [-0.01, 0.001, 5, 10, 15, 20.1])
    out["daily_by_forecast"] = D.groupby("fcb", observed=True).agg(n=("book_return", "size"), book=("book_return", "mean"), coin=("coin_return", "mean"), coin_sd=("coin_return", "std"))
    out["by_year"] = D.groupby("year").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), inpos=("inpos", "mean"))
    out["by_coin"] = D.groupby("coin").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), inpos=("inpos", "mean"))
    Din = D[D["inpos"]].copy()
    Din["volq"] = pd.qcut(Din["vol20"], 3, labels=["calm", "mid", "volatile"])
    out["inpos_by_vol"] = Din.groupby("volq", observed=True).agg(n=("book_return", "size"), book=("book_return", "mean"), coin=("coin_return", "mean"))
    Din["mkt"] = np.where(Din["mom20"] > 0, "rising20", "falling20")
    out["inpos_by_mom"] = Din.groupby("mkt").agg(n=("book_return", "size"), book=("book_return", "mean"), coin=("coin_return", "mean"))
    # drawdown per window
    dd = []
    for (c, w), g in D.groupby(["coin", "win"]):
        v = (1 + g["book_return"]).cumprod(); dd.append((v / v.cummax() - 1).min())
    out["window_maxdd"] = pd.Series(dd).describe()
    return out
