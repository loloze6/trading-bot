def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            if len(b) < 3: continue
            v = b["postRebalance_total_value"].astype(float)
            c = b["close"].astype(float)
            d = pd.DataFrame({
                "coin": coin, "w": w,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "regime": b["regime"].astype(str),
            })
            d["next_book"] = v.shift(-1) / v - 1
            d["next_coin"] = c.shift(-1) / c - 1
            r = c.pct_change()
            d["vol20"] = r.rolling(20, min_periods=10).std()
            d["ret20"] = c / c.shift(20) - 1
            d["ret1"] = r
            rows.append(d)
    D = pd.concat(rows, ignore_index=True).dropna(subset=["next_book", "next_coin"])
    out = {}

    # forecast buckets
    D["fb"] = pd.cut(D["fc"], [-0.01, 0.0001, 3, 8, 14, 19.99, 20.01],
                     labels=["0", "0-3", "3-8", "8-14", "14-20", "20"])
    g = D.groupby("fb", observed=True)
    out["by_forecast"] = pd.DataFrame({
        "n": g.size(),
        "alloc": g["alloc"].mean(),
        "next_coin": g["next_coin"].mean(),
        "next_book": g["next_book"].mean(),
        "t_coin": g["next_coin"].mean() / (g["next_coin"].std() / np.sqrt(g.size())),
    })

    # book return by year and coin; pnl split on volatility
    out["by_year"] = D.groupby("year").agg(n=("next_book", "size"),
                                           book=("next_book", "mean"),
                                           coin=("next_coin", "mean"),
                                           alloc=("alloc", "mean"))
    out["by_coin"] = D.groupby("coin").agg(book=("next_book", "mean"),
                                           coin=("next_coin", "mean"),
                                           alloc=("alloc", "mean"),
                                           bookstd=("next_book", "std"))

    A = D[D["alloc"] > 0.01].copy()
    A["volq"] = pd.qcut(A["vol20"], 3, labels=["calm", "mid", "volatile"])
    A["r20q"] = pd.qcut(A["ret20"], 3, labels=["weak", "mid", "strong"])
    g = A.groupby("volq", observed=True)
    out["active_by_vol"] = pd.DataFrame({
        "n": g.size(), "book": g["next_book"].mean(),
        "coin": g["next_coin"].mean(), "worst": g["next_book"].min(),
        "t": g["next_book"].mean() / (g["next_book"].std() / np.sqrt(g.size())),
    })
    g = A.groupby("r20q", observed=True)
    out["active_by_ret20"] = pd.DataFrame({
        "n": g.size(), "book": g["next_book"].mean(),
        "t": g["next_book"].mean() / (g["next_book"].std() / np.sqrt(g.size())),
    })

    # share of losses from the worst days
    lb = A["next_book"]
    out["active_tail"] = pd.Series({
        "n_active": len(A),
        "sum_book": lb.sum(),
        "sum_worst5pct": lb[lb <= lb.quantile(0.05)].sum(),
        "sum_best5pct": lb[lb >= lb.quantile(0.95)].sum(),
        "mean_alloc_active": A["alloc"].mean(),
    })

    # trades
    T = pd.concat([t.assign(coin=c, w=w) for c, ws in data["trades"].items()
                   for w, t in ws.items() if len(t)], ignore_index=True)
    out["trades"] = pd.Series({
        "n": len(T),
        "share_long": (T["side"] == "LONG").mean(),
        "dur_days_med": T["duration_minutes"].median() / 1440,
        "dur_days_mean": T["duration_minutes"].mean() / 1440,
        "gross_mean": T["profit_loss_percent"].mean(),
        "net_mean": T["net_profit_loss_percent"].mean(),
        "gross_win": (T["profit_loss_percent"] > 0).mean(),
        "gross_t": T["profit_loss_percent"].mean() / (T["profit_loss_percent"].std() / np.sqrt(len(T))),
    })
    T["durb"] = pd.cut(T["duration_minutes"] / 1440, [0, 1.5, 3.5, 7.5, 1000])
    out["trades_by_dur"] = T.groupby("durb", observed=True).agg(
        n=("profit_loss_percent", "size"),
        gross=("profit_loss_percent", "mean"),
        net=("net_profit_loss_percent", "mean"))

    # max drawdown per coin over the window-chained book (within-window daily returns compounded)
    dd = {}
    for coin, ws in data["days"].items():
        r = pd.concat([x["book_return"].dropna() for x in ws.values()])
        eq = (1 + r).cumprod()
        dd[coin] = (eq / eq.cummax() - 1).min()
    out["maxdd_by_coin"] = pd.Series(dd)
    return out
