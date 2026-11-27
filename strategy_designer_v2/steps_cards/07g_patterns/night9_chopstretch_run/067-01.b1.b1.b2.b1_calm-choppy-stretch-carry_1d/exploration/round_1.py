def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd20 = r.rolling(20).std()
            sma = c.rolling(20).mean()
            stretch = (c / sma - 1) / sd20
            lr = np.log(c)
            ret60 = c / c.shift(60) - 1
            for h in (1, 3, 10):
                fwd = c.shift(-h) / c - 1
                df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "h": h,
                                   "fwd": fwd, "stretch": stretch, "r1": r / sd20,
                                   "inprof": (b["regime"] == "unknown").astype(int),
                                   "fc": b["forecast"], "sd20": sd20,
                                   "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                                   "ret20": c / c.shift(20) - 1})
                df = df[df["pos"] % h == 0]
                rows.append(df)
    A = pd.concat(rows)
    A["drift"] = A.groupby(["coin", "h"])["fwd"].transform("mean")
    A["ex"] = A["fwd"] - A["drift"]
    A = A.dropna(subset=["fwd", "stretch"])

    def summ(g):
        x = g["ex"]
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    # 1. stretch quintiles, in profile vs out, h=10 and 3
    for h in (3, 10):
        S = A[A.h == h].copy()
        S["q"] = pd.qcut(S["stretch"], 5, labels=False)
        out[f"stretch_q_h{h}_by_prof"] = S.groupby(["inprof", "q"]).apply(summ).round(3)
    # 2. large one-day moves (in sd units) -> next days
    for h in (1, 3, 10):
        S = A[A.h == h].copy()
        S["q"] = pd.qcut(S["r1"], 5, labels=False)
        out[f"r1_q_h{h}"] = S.groupby("q").apply(summ).round(3)
    # 3. 20-day return quintile -> 10 days
    S = A[A.h == 10].dropna(subset=["ret20"]).copy()
    S["q"] = pd.qcut(S["ret20"], 5, labels=False)
    out["ret20_q_h10"] = S.groupby("q").apply(summ).round(3)
    # 4. vol level (sd20 rank within coin) -> h=10 signed by stretch
    S = A[A.h == 10].copy()
    S["vq"] = S.groupby("coin")["sd20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    S["sx"] = np.sign(S["stretch"]) * S["ex"]
    out["vol_tercile_signed_carry_h10"] = S.groupby("vq")["sx"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))]).round(4)
    # 5. weekday daily
    S = A[A.h == 1]
    out["weekday_h1"] = S.groupby("wd").apply(summ).round(3)
    # 6. book: day returns, largest gains/losses context
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; D.append(d)
    D = pd.concat(D)
    D["pos"] = D["book_return"].abs() > 1e-9
    out["book_by_window"] = D.groupby("w").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), act=("pos", "mean")).round(5)
    # 7. trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): T.append(t)
    T = pd.concat(T)
    out["trades_by_side"] = T.groupby("side")[["net_profit_loss_percent", "profit_loss_percent"]].agg(["count", "mean", "median"]).round(3)
    T["fq"] = pd.qcut(T["entry_forecast"].abs(), 4, labels=False, duplicates="drop")
    out["trades_by_absfc"] = T.groupby(["side", "fq"])["net_profit_loss_percent"].agg(["count", "mean"]).round(3)
    return out
