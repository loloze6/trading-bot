def explore(data):
    import pandas as pd, numpy as np
    out = {}
    tr = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t):
                t = t.copy(); t["coin"] = c; t["win"] = w; tr.append(t)
    T = pd.concat(tr, ignore_index=True)
    T["dur_d"] = T["duration_minutes"] / 1440
    T["fee_pct"] = T["profit_loss_percent"] - T["net_profit_loss_percent"]
    out["trades_summary"] = pd.DataFrame({
        "n": [len(T)], "mean_dur_d": [T.dur_d.mean()], "median_dur_d": [T.dur_d.median()],
        "mean_gross": [T.profit_loss_percent.mean()], "mean_net": [T.net_profit_loss_percent.mean()],
        "mean_fee": [T.fee_pct.mean()], "win_gross": [(T.profit_loss_percent > 0).mean()],
        "t_gross": [T.profit_loss_percent.mean() / T.profit_loss_percent.std() * np.sqrt(len(T))],
        "share_long": [(T.side == "LONG").mean()]})
    T["fbin"] = pd.cut(T.entry_forecast, [-0.01, 2, 5, 10, 15, 19.99, 20.01])
    out["by_entry_forecast"] = T.groupby("fbin").agg(n=("profit_loss_percent", "size"),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"),
        dur=("dur_d", "mean"))
    T["dbin"] = pd.cut(T.dur_d, [0, 1.5, 2.5, 4.5, 9.5, 1000])
    out["by_duration"] = T.groupby("dbin").agg(n=("profit_loss_percent", "size"),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    out["by_coin_trades"] = T.groupby("coin").agg(n=("profit_loss_percent", "size"),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"),
        dur=("dur_d", "mean"))
    # days
    D = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = c; d["win"] = w
            b = data["bars"][c][w]
            d["year"] = pd.to_datetime(d["day"]).dt.year
            d["vol20"] = d["coin_return"].rolling(20, min_periods=10).std().shift(1)
            d["mom20"] = d["close"].pct_change(20).shift(1)
            D.append(d)
    D = pd.concat(D, ignore_index=True).dropna(subset=["book_return", "coin_return"])
    D["invested"] = D.book_return.abs() > 1e-9
    out["days_overall"] = pd.DataFrame({"mean_book": [D.book_return.mean()],
        "mean_coin": [D.coin_return.mean()], "share_invested": [D.invested.mean()],
        "book_sh": [D.book_return.mean() / D.book_return.std() * np.sqrt(365)],
        "coin_sh": [D.coin_return.mean() / D.coin_return.std() * np.sqrt(365)]})
    D["volq"] = D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=["low", "mid", "high"]))
    out["by_vol"] = D.groupby("volq").agg(book=("book_return", "mean"), coin=("coin_return", "mean"),
        inv=("invested", "mean"))
    D["momq"] = pd.cut(D.mom20, [-10, -0.1, 0, 0.1, 0.3, 100])
    out["by_mom20"] = D.groupby("momq").agg(book=("book_return", "mean"), coin=("coin_return", "mean"),
        inv=("invested", "mean"), n=("book_return", "size"))
    out["by_year"] = D.groupby("year").agg(book=("book_return", "mean"), coin=("coin_return", "mean"),
        inv=("invested", "mean"))
    out["by_coin_days"] = D.groupby("coin").agg(book=("book_return", "mean"), coin=("coin_return", "mean"),
        inv=("invested", "mean"))
    # invested days: return when invested vs coin
    I = D[D.invested]
    out["invested_days"] = pd.DataFrame({"n": [len(I)], "book_mean": [I.book_return.mean()],
        "coin_mean": [I.coin_return.mean()], "coin_mean_not_inv": [D[~D.invested].coin_return.mean()]})
    # forward returns after signal at h=1,3,5,10,20 non-overlap per case
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            cl = b["close"].values; f = b["forecast"].values
            n = len(cl); last = -100
            for i in range(n):
                if f[i] > 0 and i - last > 20:
                    last = i
                    r = {"fc": f[i]}
                    for h in [1, 3, 5, 10, 20]:
                        r[f"r{h}"] = cl[i + h] / cl[i] - 1 if i + h < n else np.nan
                    rows.append(r)
    R = pd.DataFrame(rows)
    res = {}
    for h in [1, 3, 5, 10, 20]:
        x = R[f"r{h}"].dropna()
        res[h] = {"n": len(x), "mean": x.mean(), "t": x.mean() / x.std() * np.sqrt(len(x))}
    out["fwd_after_signal_sep20"] = pd.DataFrame(res).T
    return out
