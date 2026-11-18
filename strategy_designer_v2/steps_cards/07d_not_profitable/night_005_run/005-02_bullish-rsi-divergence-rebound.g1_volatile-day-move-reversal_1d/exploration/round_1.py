def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    days = data["days"]; bars = data["bars"]
    # coin mean daily return over all windows
    rows = []
    dec = []
    for c in days:
        allc = pd.concat([days[c][w]["coin_return"] for w in days[c]]).dropna()
        mu = allc.mean()
        for w in days[c]:
            d = days[c][w].copy()
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            pos = b.groupby("day")["postRebalance_current_allocation"].last().shift(1)
            d["dayk"] = pd.to_datetime(d["day"]).dt.floor("D")
            d["pos"] = d["dayk"].map(pos)
            d["coin"] = c; d["w"] = w; d["mu"] = mu
            d["year"] = pd.to_datetime(d["day"]).dt.year
            rows.append(d)
    D = pd.concat(rows).dropna(subset=["book_return", "coin_return"])
    D["mkt"] = D["pos"] * D["mu"]
    g = D.groupby("coin").agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"),
                              book_sd=("book_return", "std"), coin_sd=("coin_return", "std"),
                              mkt_gain=("mkt", "mean"), mean_pos=("pos", "mean"), absmean_pos=("pos", lambda x: x.abs().mean()))
    g["book_sharpe"] = g.book_mean / g.book_sd * np.sqrt(365)
    g["coin_sharpe"] = g.coin_mean / g.coin_sd * np.sqrt(365)
    out["by_coin"] = g
    # by window
    out["by_window"] = D.groupby("w").agg(book=("book_return", "sum"), coin=("coin_return", "sum"), n=("book_return", "size"))
    out["by_year"] = D.groupby("year").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "size"))
    # position sign gain
    D["side"] = np.sign(D["pos"]).fillna(0)
    out["by_side"] = D.groupby("side").agg(n=("book_return", "size"), book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"))
    # bar-level: gain by forecast quintile, regime, fees
    B = []
    for c in bars:
        for w in bars[c]:
            b = bars[c][w].copy()
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            b["gain"] = b["postRebalance_current_allocation"] * b["ret1"]
            b["fee"] = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            b["r1"] = b["close"] / b["close"].shift(1) - 1
            b["r20"] = b["close"] / b["close"].shift(20) - 1
            b["coin"] = c
            B.append(b)
    B = pd.concat(B)
    out["gain_vs_fee"] = pd.Series({"mean_gain_per_bar": B["gain"].mean(), "mean_fee_per_bar": B["fee"].mean(),
                                    "share_active": (B["forecast"] != 0).mean(), "mean_abs_alloc": B["postRebalance_current_allocation"].abs().mean()})
    A = B[B["forecast"] != 0].copy()
    A["fq"] = pd.qcut(A["forecast"].abs().rank(method="first"), 5, labels=False)
    A["dir"] = np.sign(A["forecast"])
    out["by_absfc_quint_dir"] = A.groupby(["fq", "dir"]).agg(n=("gain", "size"), gain=("gain", "mean"), fee=("fee", "mean"), alloc=("postRebalance_current_allocation", lambda x: x.abs().mean()))
    # by 20-day trend
    A["trend_sign"] = np.sign(A["r20"])
    A["agree"] = np.sign(A["dir"] * A["trend_sign"])
    out["by_trend_agree"] = A.groupby(["dir", "trend_sign"]).agg(n=("gain", "size"), gain=("gain", "mean"), gain_t=("gain", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    # drawdown of chained book
    ch = []
    for c in days:
        r = pd.concat([days[c][w]["book_return"].dropna() for w in days[c]])
        v = (1 + r).cumprod()
        dd = v / v.cummax() - 1
        ch.append(pd.Series({"coin": c, "maxdd": dd.min(), "ann": v.iloc[-1] ** (365 / len(r)) - 1}))
    out["dd"] = pd.DataFrame(ch)
    return out
