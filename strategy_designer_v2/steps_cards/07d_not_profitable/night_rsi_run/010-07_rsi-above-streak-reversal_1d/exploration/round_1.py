def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    col = "debug_info.components.rsi_above_age.last_history_value"
    # coin mean daily return over all windows, per coin
    rows = []
    grid = []
    win = []
    for coin in data["days"]:
        dd = pd.concat([d.assign(window=w) for w, d in data["days"][coin].items()])
        mu = dd["coin_return"].mean()
        b = data["bars"][coin]
        allb = []
        for w, df in b.items():
            df = df.reset_index(drop=True).copy()
            df["ret1"] = df["close"].shift(-1) / df["close"] - 1
            df["fwd14"] = df["close"].shift(-14) / df["close"] - 1
            df["fwd7"] = df["close"].shift(-7) / df["close"] - 1
            df["past14"] = df["close"] / df["close"].shift(14) - 1
            df["window"] = w
            df["coin"] = coin
            df["pos"] = np.arange(len(df))
            allb.append(df)
        ab = pd.concat(allb)
        m14 = ab.loc[ab["pos"] % 14 == 0, "fwd14"].mean()
        ab["gain"] = ab["postRebalance_current_allocation"] * ab["ret1"]
        ab["timing"] = ab["postRebalance_current_allocation"] * (ab["ret1"] - mu)
        ab["mkt"] = ab["postRebalance_current_allocation"] * mu
        ab["age"] = ab[col]
        ab["fee"] = (ab["total_portfolio_value"] - ab["postRebalance_total_value"]) / ab["total_portfolio_value"]
        rows.append(ab)
        g = ab[(ab["pos"] % 14 == 0) & ab["fwd14"].notna()].copy()
        g["ex14"] = g["fwd14"] - m14
        grid.append(g)
        wd = dd.groupby("window").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "count"))
        wd["coin_sym"] = coin
        win.append(wd)
    A = pd.concat(rows)
    G = pd.concat(grid)
    out["per coin bar-level"] = A.groupby("coin").agg(gain=("gain", "mean"), timing=("timing", "mean"), mkt=("mkt", "mean"), fee=("fee", "mean"), alloc=("postRebalance_current_allocation", "mean"), short_share=("postRebalance_current_allocation", lambda s: (s < 0).mean()))
    # excess fwd14 by age bin on grid
    G["agebin"] = pd.cut(G["age"], [-61, -20, -5, 0, 5, 10, 20, 40, 61])
    out["ex14 by age bin (grid)"] = G.groupby("agebin").agg(n=("ex14", "count"), mean=("ex14", "mean"), sd=("ex14", "std"))
    # gain by age bin, bar level
    A["agebin"] = pd.cut(A["age"], [-61, -20, -5, 0, 5, 10, 20, 40, 61])
    out["daily gain/timing by age bin"] = A.groupby("agebin").agg(n=("gain", "count"), gain=("gain", "mean"), timing=("timing", "mean"), ret1=("ret1", "mean"), alloc=("postRebalance_current_allocation", "mean"))
    # past 14d return bins among active short bars
    act = A[A["postRebalance_current_allocation"] < 0].copy()
    act["p14q"] = pd.qcut(act["past14"], 5)
    out["active: next-day ret by past14 quintile"] = act.groupby("p14q").agg(n=("ret1", "count"), ret1=("ret1", "mean"), gain=("gain", "mean"))
    Gp = G.copy()
    Gp["p14q"] = pd.qcut(Gp["past14"], 5)
    out["grid: ex14 by past14 quintile (all bars)"] = Gp.groupby("p14q").agg(n=("ex14", "count"), mean=("ex14", "mean"))
    W = pd.concat(win)
    W["yr_win"] = W.index
    out["window book vs coin"] = W.groupby(W.index).agg(book=("book", "mean"), coin=("coin", "mean"))
    t = A.groupby("coin")["gain"].apply(lambda s: s.mean() / (s.std() / np.sqrt(s.count())))
    out["t of gain per coin"] = t
    return out
