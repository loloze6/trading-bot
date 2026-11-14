def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            b = data["bars"][coin][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            al = b.groupby("day")["postRebalance_current_allocation"].last()
            cl = b.groupby("day")["close"].last()
            reg = b.groupby("day")["regime"].last()
            fc = b.groupby("day")["forecast"].last()
            df = pd.DataFrame({"alloc": al, "close": cl, "regime": reg, "fc": fc})
            df["r60"] = df["close"] / df["close"].shift(60) - 1
            df["r20"] = df["close"] / df["close"].shift(20) - 1
            df["vol20"] = df["close"].pct_change().rolling(20).std()
            df["coin_next"] = df["close"].shift(-1) / df["close"] - 1
            df["gain"] = df["alloc"] * df["coin_next"]
            dd = d.copy()
            dd["day"] = pd.to_datetime(dd["day"]).dt.floor("D")
            dd = dd.set_index("day")
            df["book_next"] = dd["book_return"].reindex(df.index).shift(-1)
            df["coin"] = coin; df["w"] = w
            df["year"] = df.index.year
            rows.append(df.reset_index())
    A = pd.concat(rows, ignore_index=True)
    A = A.dropna(subset=["book_next", "coin_next"])
    # book per day = mean across coins
    bk = A.groupby(["w", "day"])[["book_next", "coin_next", "gain"]].mean()
    out["book overall"] = pd.Series({"mean book": bk.book_next.mean(), "sharpe book": bk.book_next.mean()/bk.book_next.std()*np.sqrt(365),
                                     "mean hold": bk.coin_next.mean(), "sharpe hold": bk.coin_next.mean()/bk.coin_next.std()*np.sqrt(365),
                                     "mean gain prefee": bk.gain.mean(), "n days": len(bk)})
    # per coin
    g = A.groupby("coin").agg(book=("book_next", "mean"), coin_ret=("coin_next", "mean"), alloc=("alloc", "mean"),
                              inmkt=("alloc", lambda x: (x > 0).mean()))
    g["drift_x_alloc"] = g["coin_ret"] * g["alloc"]
    g["book_sum_share"] = A.groupby("coin")["book_next"].sum() / A["book_next"].sum()
    out["per coin"] = g
    # per window
    bw = bk.reset_index().groupby("w").agg(book=("book_next", "mean"), hold=("coin_next", "mean"), n=("book_next", "size"))
    bw["share_of_sum"] = bk.reset_index().groupby("w")["book_next"].sum() / bk.book_next.sum()
    out["per window"] = bw
    by = bk.reset_index(); by["year"] = pd.to_datetime(by["day"]).dt.year
    out["per year"] = by.groupby("year").agg(book=("book_next", "mean"), hold=("coin_next", "mean"), n=("book_next", "size"))
    # in vs out of market
    A["inm"] = A["alloc"] > 0
    out["in vs out"] = A.groupby("inm").agg(n=("coin_next", "size"), coin_next=("coin_next", "mean"), book=("book_next", "mean"), alloc=("alloc", "mean"))
    inm = A[A.inm]["coin_next"]; allr = A["coin_next"]
    out["t coin in mkt minus all"] = stats.ttest_ind(inm, A[~A.inm]["coin_next"], equal_var=False).statistic
    # timing vs drift decomposition per coin-window
    A["alloc_mean_cw"] = A.groupby(["coin", "w"])["alloc"].transform("mean")
    A["coin_mean_all"] = A.groupby("coin")["coin_next"].transform("mean")
    A["drift_part"] = A["alloc"] * A["coin_mean_all"]
    A["timing_part"] = A["alloc"] * (A["coin_next"] - A["coin_mean_all"])
    out["decomp"] = pd.Series({"gain": A.gain.mean(), "drift part": A.drift_part.mean(), "timing part": A.timing_part.mean(),
                               "t timing": A.timing_part.mean()/(A.timing_part.std()/np.sqrt(len(A)))})
    # market states
    A["r60q"] = pd.qcut(A["r60"], 5, labels=False, duplicates="drop")
    out["by r60 quintile"] = A.groupby("r60q").agg(n=("gain", "size"), gain=("gain", "mean"), coin=("coin_next", "mean"), alloc=("alloc", "mean"), r60=("r60", "mean"))
    A["volq"] = pd.qcut(A["vol20"], 3, labels=False)
    out["by vol tercile"] = A.groupby("volq").agg(n=("gain", "size"), gain=("gain", "mean"), coin=("coin_next", "mean"), alloc=("alloc", "mean"))
    # trades concentration
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    p = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(T), "sum": p.sum(), "top10 sum": p.head(10).sum(), "top5% sum": p.head(int(len(p)*0.05)).sum(),
                               "win rate": (p > 0).mean(), "median": p.median()})
    return out
