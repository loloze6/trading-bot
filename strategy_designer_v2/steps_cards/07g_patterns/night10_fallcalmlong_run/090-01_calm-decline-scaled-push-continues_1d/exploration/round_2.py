def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if t is None or len(t) == 0: continue
            t = t.copy(); t["coin"] = coin; t["win"] = w
            T.append(t)
    T = pd.concat(T)
    T["dur_d"] = T["duration_minutes"] / 1440
    T["dbin"] = pd.cut(T["dur_d"], [0, 5, 6, 10, 20, 1000])
    g = T.groupby("dbin", observed=True)["net_profit_loss_percent"].agg(["mean", "count", "std"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["trades by duration (days)"] = g
    T["fbin"] = pd.qcut(T["entry_forecast"].rank(method="first"), 4, labels=False)
    g = T.groupby("fbin")["net_profit_loss_percent"].agg(["mean", "count", "std"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["trades by entry forecast quartile"] = g
    out["trades overall"] = pd.Series({"n": len(T), "mean_net": T.net_profit_loss_percent.mean(),
                                       "share_win": (T.net_profit_loss_percent > 0).mean(),
                                       "median_net": T.net_profit_loss_percent.median()})
    # up20 robustness and s5 in-profile by coin and by year, grid
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; r = c.pct_change()
            vol = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({"coin": coin, "win": w,
                               "inprof": (b["regime"] == "unknown").astype(int),
                               "f5": c.shift(-5) / c - 1,
                               "up20": (r > 0).rolling(20, min_periods=10).mean(),
                               "s5": (c / c.shift(5) - 1) / vol,
                               "yr": pd.to_datetime(b["timestamp"]).dt.year,
                               "pos": np.arange(len(b))})
            rows.append(df[df.pos % 5 == 0])
    D = pd.concat(rows).dropna(subset=["f5"])
    P = D[D.inprof == 1].dropna(subset=["up20", "s5"])
    res = []
    for k, s in P.groupby("coin"):
        res.append([k, len(s), s[["up20", "f5"]].corr().iloc[0, 1], s[["s5", "f5"]].corr().iloc[0, 1]])
    out["in-profile corr with f5 by coin"] = pd.DataFrame(res, columns=["coin", "n", "corr_up20", "corr_s5"])
    res = []
    for k, s in P.groupby("yr"):
        if len(s) >= 8:
            res.append([k, len(s), s[["up20", "f5"]].corr().iloc[0, 1], s[["s5", "f5"]].corr().iloc[0, 1]])
    out["in-profile corr with f5 by year"] = pd.DataFrame(res, columns=["yr", "n", "corr_up20", "corr_s5"])
    # book daily: largest gains vs losses, share of book from top days
    B = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; B.append(d)
    B = pd.concat(B).dropna(subset=["book_return"])
    act = B[B.book_return != 0]
    out["book active days"] = pd.Series({"n_active": len(act), "mean": act.book_return.mean(),
        "sum": act.book_return.sum(),
        "sum_top10": act.book_return.nlargest(10).sum(),
        "sum_bottom10": act.book_return.nsmallest(10).sum()})
    return out
