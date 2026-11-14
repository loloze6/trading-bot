def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    # trades
    tr = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t):
                t = t.copy(); t["coin"] = c; t["win"] = w; tr.append(t)
    T = pd.concat(tr)
    T["hold_d"] = T["duration_minutes"] / 1440
    T["fee"] = T["profit_loss_percent"] - T["net_profit_loss_percent"]
    T["fbin"] = pd.cut(T["entry_forecast"], [-0.01, 1, 5, 10, 19.9, 20.1])
    out["trades_overall"] = pd.DataFrame({
        "n": [len(T)], "mean_gross": [T.profit_loss_percent.mean()],
        "mean_net": [T.net_profit_loss_percent.mean()], "mean_fee": [T.fee.mean()],
        "median_hold_d": [T.hold_d.median()], "mean_hold_d": [T.hold_d.mean()],
        "win_rate_net": [(T.net_profit_loss_percent > 0).mean()],
        "side_long_share": [(T.side == "LONG").mean()]})
    out["trades_by_entry_fc"] = T.groupby("fbin", observed=True).agg(
        n=("profit_loss_percent", "size"), gross=("profit_loss_percent", "mean"),
        net=("net_profit_loss_percent", "mean"), hold=("hold_d", "mean"))
    T["hbin"] = pd.cut(T["hold_d"], [0, 1.5, 2.5, 4.5, 10, 1000])
    out["trades_by_hold"] = T.groupby("hbin", observed=True).agg(
        n=("profit_loss_percent", "size"), gross=("profit_loss_percent", "mean"),
        net=("net_profit_loss_percent", "mean"),
        worst=("net_profit_loss_percent", "min"))
    out["trades_by_coin"] = T.groupby("coin").agg(
        n=("profit_loss_percent", "size"), gross=("profit_loss_percent", "mean"),
        net=("net_profit_loss_percent", "mean"), worst=("net_profit_loss_percent", "min"))
    # days: book vs coin, by window, drawdown
    rows = []; dd = []
    D = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = c; d["win"] = w
            b = data["bars"][c][w]
            # position at day's close (approx from bars)
            pos = b["postRebalance_current_allocation"].values
            d["pos"] = pd.Series(pos[:len(d)] if len(pos) >= len(d) else np.r_[pos, [np.nan]*(len(d)-len(pos))]).values
            d["pos_prev"] = d["pos"].shift(1)
            D.append(d)
            bv = d["book_value"]
            rows.append({"coin": c, "win": w, "book_ret": bv.iloc[-1]/bv.iloc[0]-1,
                         "coin_ret": d["close"].iloc[-1]/d["close"].iloc[0]-1,
                         "maxdd": (bv/bv.cummax()-1).min()})
    R = pd.DataFrame(rows)
    out["by_window"] = R.groupby("win").agg(book=("book_ret", "mean"), coin=("coin_ret", "mean"), dd=("maxdd", "mean"), worst_dd=("maxdd", "min")).reindex([f"w{i}" for i in range(1, 25)])
    D = pd.concat(D)
    D["active"] = D["pos_prev"].abs() > 0.01
    out["active_share"] = float(D["active"].mean())
    A = D[D.active].copy()
    # vol state: coin 20d realized vol rank
    D["vol20"] = D.groupby(["coin", "win"])["coin_return"].transform(lambda s: s.rolling(20, min_periods=10).std())
    D["volq"] = D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=["calm", "mid", "wild"]))
    A = D[D.active]
    out["active_days_by_vol"] = A.groupby("volq", observed=True).agg(n=("book_return", "size"), mean=("book_return", "mean"), sd=("book_return", "std"), worst=("book_return", "min"))
    A2 = A.copy(); A2["mkt"] = np.where(A2.coin_return > 0, "up", "down")
    out["active_days_by_coin_dir"] = A2.groupby("mkt").agg(n=("book_return", "size"), mean=("book_return", "mean"))
    out["pos_size_dist"] = A["pos_prev"].describe()
    return out
