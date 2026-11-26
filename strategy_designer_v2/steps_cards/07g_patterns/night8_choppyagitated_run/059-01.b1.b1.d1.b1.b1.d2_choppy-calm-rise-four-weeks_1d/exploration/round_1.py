def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            r1 = c.pct_change()
            r7 = c / c.shift(7) - 1
            sc = r7.abs().rolling(30, min_periods=20).mean()
            s7 = r7 / sc
            z1 = r1 / r1.rolling(30, min_periods=20).std()
            vol30 = r1.rolling(30, min_periods=20).std()
            r28p = c / c.shift(28) - 1
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                               "inprof": (b["regime"] == "unknown").values,
                               "s7": s7, "z1": z1, "vol30": vol30, "r28p": r28p,
                               "wd": ts.dt.weekday, "alloc": b["postRebalance_current_allocation"].astype(float),
                               "fc": b["forecast"].astype(float)})
            for h in (1, 7, 28):
                df["f%d" % h] = c.shift(-h) / c - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    out = {}
    def grid(h):
        g = D[(D["pos"] % h == 0)].dropna(subset=["f%d" % h]).copy()
        g["ex"] = g["f%d" % h] - g.groupby("coin")["f%d" % h].transform("mean")
        return g
    def summ(g, key, col="ex"):
        r = g.groupby(key)[col].agg(["count", "mean", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r.round(4)
    # 1. scaled 7-day return quintile -> next 7 and 28 days, in/out of profile
    for h in (7, 28):
        g = grid(h).dropna(subset=["s7"])
        g["q"] = pd.qcut(g["s7"], 5, labels=False)
        out["s7 quintile -> excess %dd, by inprof" % h] = summ(g, ["inprof", "q"])
    # 2. daily scaled move -> next day and next 7 days
    g = grid(1).dropna(subset=["z1"])
    g["q"] = pd.qcut(g["z1"], 5, labels=False)
    out["z1 quintile -> next day excess, by inprof"] = summ(g, ["inprof", "q"])
    g = grid(7).dropna(subset=["z1"])
    g["q"] = pd.qcut(g["z1"], 5, labels=False)
    out["z1 quintile -> next 7d excess"] = summ(g, "q")
    # 3. vol level -> next 7d
    g = grid(7).dropna(subset=["vol30"])
    g["q"] = g.groupby("coin")["vol30"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["vol30 tercile (per coin) -> next 7d excess"] = summ(g, "q")
    # 4. 28-day past return quintile -> next 28d
    g = grid(28).dropna(subset=["r28p"])
    g["q"] = pd.qcut(g["r28p"], 5, labels=False)
    out["past 28d ret quintile -> next 28d excess, by inprof"] = summ(g, ["inprof", "q"])
    # 5. weekday of next day
    g = grid(1).copy()
    g["wdn"] = (g["wd"] + 1) % 7
    out["next-day excess by weekday of that day"] = summ(g, "wdn")
    # 6. profile share and positions
    out["share in profile"] = float(D["inprof"].mean())
    # 7. book daily returns: top/bottom days
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    DD = pd.concat(dd, ignore_index=True)
    bk = DD.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book by window: mean, sd, n"] = bk.groupby(level=0)["book_return"].agg(["mean", "std", "count"]).round(5)
    q = bk["book_return"].quantile([0.02, 0.98])
    out["coin ret on book's worst 2% / best 2% days"] = pd.Series({
        "worst_book": bk.loc[bk.book_return <= q.iloc[0], "book_return"].mean(),
        "worst_coin": bk.loc[bk.book_return <= q.iloc[0], "coin_return"].mean(),
        "best_book": bk.loc[bk.book_return >= q.iloc[1], "book_return"].mean(),
        "best_coin": bk.loc[bk.book_return >= q.iloc[1], "coin_return"].mean(),
        "corr_book_coin": bk["book_return"].corr(bk["coin_return"])}).round(4)
    # 8. trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tt = t.copy(); tt["coin"] = coin; tr.append(tt)
    T = pd.concat(tr, ignore_index=True)
    T["dur_d"] = T["duration_minutes"] / 1440
    T["fq"] = pd.qcut(T["entry_forecast"].rank(method="first"), 3, labels=False)
    out["trades by entry forecast tercile"] = T.groupby("fq").agg(n=("net_profit_loss_percent", "size"),
        mean_net=("net_profit_loss_percent", "mean"), win=("net_profit_loss_percent", lambda x: (x > 0).mean()),
        dur=("dur_d", "mean")).round(3)
    return out
