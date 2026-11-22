def explore(data):
    import numpy as np, pandas as pd
    coins = list(data["days"].keys())
    wins = sorted(set().union(*[set(data["days"][c].keys()) for c in coins]), key=lambda w: int(w[1:]))
    # book daily
    rows = []
    for w in wins:
        dfs = []
        for c in coins:
            if w in data["days"][c]:
                d = data["days"][c][w][["day", "book_return", "coin_return"]].copy()
                b = data["bars"][c][w].copy()
                b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
                g = b.groupby("day").agg(alloc=("postRebalance_current_allocation", "mean"))
                d["day"] = pd.to_datetime(d["day"])
                d = d.merge(g, left_on="day", right_index=True, how="left")
                d["coin"] = c
                dfs.append(d)
        dd = pd.concat(dfs)
        m = dd.groupby("day").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), alloc=("alloc", "mean")).reset_index()
        m["window"] = w
        rows.append(m)
    B = pd.concat(rows, ignore_index=True).dropna(subset=["book"])
    B["year"] = B["day"].dt.year
    eq = (1 + B["book"]).cumprod()
    dd = eq / eq.cummax() - 1
    B["dd"] = dd.values
    out = {}
    out["overall"] = pd.Series({"mean": B.book.mean(), "sd": B.book.std(), "maxdd": dd.min(),
                                "years": len(B) / 365, "yearly": eq.iloc[-1] ** (365 / len(B)) - 1,
                                "corr_book_coin": B.book.corr(B.coin), "mean_alloc": B.alloc.mean()})
    # drawdown episodes
    peak = eq.cummax()
    ep = (peak != peak.shift()).cumsum()
    E = []
    for k, g in B.assign(ep=ep.values, eq=eq.values, peak=peak.values).groupby("ep"):
        if len(g) < 2: continue
        i = g["eq"].idxmin()
        depth = g.loc[i, "eq"] / g["peak"].iloc[0] - 1
        sub = g.loc[:i]
        E.append({"depth": depth, "days_to_trough": len(sub), "windows": ",".join(sorted(set(sub.window), key=lambda w: int(w[1:]))),
                  "year": sub.year.iloc[0], "coin_ret_during": (1 + sub.coin).prod() - 1,
                  "book_ret": (1 + sub.book).prod() - 1, "mean_alloc": sub.alloc.mean(),
                  "share_days_coin_down": (sub.coin < 0).mean()})
    E = pd.DataFrame(E).sort_values("depth").head(8).reset_index(drop=True)
    out["worst_falls"] = E
    # per window
    out["by_window"] = B.groupby("window").agg(n=("book", "size"), book=("book", "sum"), coin=("coin", "sum"), alloc=("alloc", "mean")).reindex(wins)
    # book daily return by coin-day bucket
    B["coin_q"] = pd.qcut(B.coin, 5, labels=False)
    out["by_coin_day_quintile"] = B.groupby("coin_q").agg(n=("book", "size"), book=("book", "mean"), coin=("coin", "mean"), alloc=("alloc", "mean"))
    # trades
    T = []
    for c in coins:
        for w in data["trades"][c]:
            t = data["trades"][c][w].copy(); t["coin"] = c; t["window"] = w; T.append(t)
    T = pd.concat(T, ignore_index=True)
    out["trades"] = T.groupby("side").agg(n=("net_profit_loss_percent", "size"), net=("net_profit_loss_percent", "mean"),
                                          gross=("profit_loss_percent", "mean"), win=("net_profit_loss_percent", lambda x: (x > 0).mean()),
                                          dur_h=("duration_minutes", lambda x: x.mean() / 60), worst=("net_profit_loss_percent", "min"))
    return out
