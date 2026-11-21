def explore(data):
    import pandas as pd, numpy as np
    days = data["days"]; bars = data["bars"]
    rows = []
    for c in days:
        for w, d in days[c].items():
            d = d.copy(); d["coin"] = c; d["window"] = w
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            g = b.groupby("day").agg(alloc=("postRebalance_current_allocation", "last"),
                                     fc=("forecast", "last"))
            d["dayk"] = pd.to_datetime(d["day"]).dt.floor("D")
            d = d.merge(g, left_on="dayk", right_index=True, how="left")
            d["prev_alloc"] = d["alloc"].shift(1)
            d["ret20"] = d["close"] / d["close"].shift(20) - 1
            d["vol20"] = d["coin_return"].rolling(20).std()
            d["hi90"] = d["close"] / d["close"].rolling(90, min_periods=20).max() - 1
            rows.append(d)
    a = pd.concat(rows)
    a["wn"] = a["window"].str[1:].astype(int)
    port = a.groupby(["wn", "dayk"])["book_return"].mean().dropna().reset_index().sort_values(["wn", "dayk"])
    port["eq"] = (1 + port["book_return"]).cumprod()
    port["dd"] = port["eq"] / port["eq"].cummax() - 1
    port["i"] = range(len(port))
    out = {}
    out["maxdd"] = port["dd"].min()
    out["years"] = len(port) / 365
    out["cagr"] = port["eq"].iloc[-1] ** (365 / len(port)) - 1
    # drawdown episodes
    peaks = port["eq"].cummax()
    ep = (port["dd"] == 0).cumsum()
    port["ep"] = ep
    e = port.groupby("ep").agg(depth=("dd", "min"), n=("dd", "size"), w0=("wn", "first"), w1=("wn", "last"))
    out["episodes"] = e.sort_values("depth").head(8)
    # by window
    pw = port.groupby("wn").agg(mean=("book_return", "mean"), sd=("book_return", "std"),
                                 n=("book_return", "size"), wdd=("dd", "min"))
    hold = a.groupby(["wn", "dayk"])["coin_return"].mean().groupby("wn").mean()
    pw["hold_mean"] = hold
    out["by_window"] = pw
    # position-level: book_return by side, market state
    a["side"] = np.sign(a["prev_alloc"]).map({1: "long", -1: "short", 0: "flat"})
    a["absal"] = a["prev_alloc"].abs()
    out["by_side"] = a.groupby("side")["book_return"].agg(["mean", "std", "count"])
    a["volq"] = a.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["by_volq_side"] = a.groupby(["volq", "side"])["book_return"].agg(["mean", "std", "count"]).unstack()
    a["r20q"] = a.groupby("coin")["ret20"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["by_r20q_side"] = a.groupby(["r20q", "side"])["book_return"].agg(["mean", "count"]).unstack()
    a["hiq"] = a.groupby("coin")["hi90"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["by_hiq_side"] = a.groupby(["hiq", "side"])["book_return"].agg(["mean", "count"]).unstack()
    out["by_coin"] = a.groupby("coin")["book_return"].agg(["mean", "std", "count"])
    out["absalloc_by_volq"] = a.groupby("volq")["absal"].mean()
    out["worst_days_share_short"] = a.nsmallest(100, "book_return")["side"].value_counts()
    out["worst_days_coinret"] = a.nsmallest(100, "book_return")["coin_return"].describe()
    return out
