def explore(data):
    import pandas as pd, numpy as np
    out = {}
    coins = list(data["days"].keys())
    wins = list(data["days"][coins[0]].keys())
    # book daily per window
    book = {}
    for w in wins:
        frames = []
        for c in coins:
            d = data["days"][c].get(w)
            if d is None: continue
            frames.append(d.set_index("day")["book_return"].rename(c))
        df = pd.concat(frames, axis=1)
        book[w] = df.mean(axis=1)
    rows = []
    for w in wins:
        r = book[w].fillna(0)
        eq = (1 + r).cumprod()
        dd = eq / eq.cummax() - 1
        rows.append({"win": w, "ret": eq.iloc[-1] - 1, "maxdd": dd.min(), "n": len(r),
                     "std": r.std()})
    out["per_window"] = pd.DataFrame(rows).set_index("win")
    # overall drawdown episodes chained across windows (book equity)
    allr = pd.concat([book[w].fillna(0) for w in wins], ignore_index=True)
    eq = (1 + allr).cumprod(); dd = eq / eq.cummax() - 1
    out["overall_maxdd"] = float(dd.min())
    out["ann_ret"] = float(allr.mean() * 365)
    # worst book days: what coins did
    allc = []
    for w in wins:
        for c in coins:
            d = data["days"][c][w].copy(); d["coin"] = c; d["win"] = w
            b = data["bars"][c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            d["day2"] = pd.to_datetime(d["day"])
            cl = b["close"]
            b["r1"] = cl.pct_change(); b["r20"] = cl.pct_change(20); b["r60"] = cl.pct_change(60)
            b["vol20"] = b["r1"].rolling(20).std()
            b["alloc"] = b["postRebalance_current_allocation"]
            b = b[["day", "r1", "r20", "r60", "vol20", "alloc", "forecast", "regime"]].shift(1)  # state at prior close
            b["day"] = pd.to_datetime(data["bars"][c][w]["timestamp"]).dt.floor("D")
            m = d.merge(b, left_on="day2", right_on="day", how="left", suffixes=("", "_b"))
            allc.append(m)
    A = pd.concat(allc, ignore_index=True)
    A["held"] = A["alloc"].abs() > 1e-6
    out["share_days_held"] = float(A["held"].mean())
    H = A[A["held"]]
    out["held_coinret_by_prior_r1_bucket"] = H.groupby(pd.qcut(H["r1"], 5, duplicates="drop"))["coin_return"].agg(["mean", "count", "std"])
    out["held_by_r20_bucket"] = H.groupby(pd.qcut(H["r20"], 5, duplicates="drop"))["book_return"].agg(["mean", "count", "std"])
    out["held_by_vol20_bucket"] = H.groupby(pd.qcut(H["vol20"], 5, duplicates="drop"))["book_return"].agg(["mean", "count", "std"])
    out["held_by_coin"] = H.groupby("coin")["book_return"].agg(["mean", "count", "std", "min"])
    # trades
    T = []
    for c in coins:
        for w in wins:
            t = data["trades"][c][w].copy(); t["coin"] = c; T.append(t)
    T = pd.concat(T, ignore_index=True)
    T["dur_d"] = T["duration_minutes"] / 1440
    out["trades_summary"] = T["net_profit_loss_percent"].describe()
    out["trades_by_dur"] = T.groupby(pd.cut(T["dur_d"], [0, 1.5, 3.5, 7.5, 15, 1000]))["net_profit_loss_percent"].agg(["mean", "count", "sum", "min"])
    out["trades_by_entry_fc"] = T.groupby(pd.qcut(T["entry_forecast"], 4, duplicates="drop"))["net_profit_loss_percent"].agg(["mean", "count", "sum", "min"])
    out["mean_commission"] = float(T["total_commission"].mean())
    out["fee_vs_gross"] = pd.Series({"gross": T["profit_loss_percent"].mean(), "net": T["net_profit_loss_percent"].mean()})
    return out
