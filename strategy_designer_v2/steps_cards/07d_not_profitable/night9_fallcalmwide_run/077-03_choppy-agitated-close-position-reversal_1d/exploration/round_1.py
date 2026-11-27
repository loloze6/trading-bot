def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = coin; dd["window"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["window"].str[1:].astype(int)
    book = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().dropna().sort_index()
    # chain and drawdown
    v = (1 + book["book_return"]).cumprod()
    dd = v / v.cummax() - 1
    out["book_maxdd"] = float(dd.min())
    yrs = len(book) / 365
    out["book_yearly"] = float(v.iloc[-1] ** (1 / yrs) - 1)
    out["book_sharpe"] = float(book["book_return"].mean() / book["book_return"].std() * np.sqrt(365))
    # per window
    pw = book.groupby(level=0).agg(mean=("book_return", "mean"), sd=("book_return", "std"), n=("book_return", "size"))
    pw["sum"] = book.groupby(level=0)["book_return"].sum()
    pw["mindd"] = dd.groupby(level=0).min()
    out["per_window"] = pw
    # worst 15 book days: window, return
    worst = book.nsmallest(15, "book_return").reset_index()[["wn", "book_return", "coin_return"]]
    out["worst_days"] = worst
    # bar-level: position, next-day return, features
    B = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            b["coin"] = coin; b["wn"] = int(w[1:])
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            r = b["close"].pct_change()
            b["sd30"] = r.rolling(30).std()
            b["width"] = (b["high"] - b["low"]) / b["close"] / b["sd30"]
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            b["cpos"] = (b["close"] - b["low"]) / rng  # 0 low, 1 high
            b["r1"] = r
            b["r5"] = b["close"] / b["close"].shift(5) - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * b["ret1"]
            b["fee"] = (b["postRebalance_total_value"] - b["total_portfolio_value"]) / b["total_portfolio_value"]
            B.append(b)
    B = pd.concat(B)
    P = B[(B["pos"].abs() > 1e-9) & B["ret1"].notna()].copy()
    P["side"] = np.sign(P["pos"])
    P["dret"] = P["side"] * P["ret1"]
    g = P.groupby("side").agg(n=("gain", "size"), gain_mean=("gain", "mean"), dret=("dret", "mean"),
                              dret_sd=("dret", "std"), absPos=("pos", lambda x: x.abs().mean()))
    g["t"] = g["dret"] / (g["dret_sd"] / np.sqrt(g["n"]))
    g["gain_sum"] = P.groupby("side")["gain"].sum()
    out["by_side"] = g
    out["fee_sum_total"] = float(B["fee"].sum())
    out["gain_sum_total"] = float(P["gain"].sum())
    # by width tercile within position
    P["wq"] = pd.qcut(P["width"], 3, labels=["narrow", "mid", "wide"])
    out["by_width_side"] = P.groupby(["wq", "side"]).agg(n=("dret", "size"), dret=("dret", "mean"),
                                                          sd=("dret", "std"), gain=("gain", "mean"))
    # by prior 1-day return magnitude in direction (did the day fall)
    P["r1dir"] = P["side"] * P["r1"]  # negative = contrarian to the day's move
    P["r1q"] = pd.qcut(P["r1dir"], 3, labels=["strong_against", "mid", "weak"])
    out["by_dayret_dir"] = P.groupby(["r1q", "side"]).agg(n=("dret", "size"), dret=("dret", "mean"), sd=("dret", "std"))
    # tails: largest losing gains
    out["loss_tail_share"] = float(P["gain"].nsmallest(20).sum() / P["gain"][P["gain"] < 0].sum())
    out["dret_quantiles"] = P["dret"].quantile([0.01, 0.05, 0.5, 0.95, 0.99])
    out["per_window_side"] = P.groupby(["wn", "side"])["gain"].sum().unstack()
    return out
