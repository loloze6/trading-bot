def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol20 = r1.rolling(20, min_periods=10).std()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "fwd5": c.shift(-5) / c - 1,
                "fwd1": c.shift(-1) / c - 1,
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "r1z": r1 / vol20,
                "r5": c / c.shift(5) - 1,
                "r20": c / c.shift(20) - 1,
                "vol20": vol20,
                "near30": c / c.rolling(30, min_periods=20).max() - 1,
                "range_z": ((b["high"] - b["low"]) / c) / ((b["high"] - b["low"]) / c).rolling(20, min_periods=10).mean(),
                "volz": b["volume"] / b["volume"].rolling(20, min_periods=10).mean(),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "pos": np.arange(len(b)),
            })
            rows.append(d)
    df = pd.concat(rows, ignore_index=True)
    g = df[df["pos"] % 5 == 0].dropna(subset=["fwd5"]).copy()
    drift = g.groupby("coin")["fwd5"].mean()
    sd = g.groupby("coin")["fwd5"].std()
    g["ex5"] = g["fwd5"] - g["coin"].map(drift)
    g["s5"] = g["ex5"] / g["coin"].map(sd)
    out = {}
    feats = ["fc", "r1z", "r5", "r20", "vol20", "near30", "range_z", "volz"]
    res = []
    for f in feats:
        x = g[[f, "s5", "coin"]].dropna()
        x["fz"] = x.groupby("coin")[f].transform(lambda s: (s - s.mean()) / s.std())
        x = x.dropna()
        sl = stats.linregress(x["fz"], x["s5"])
        q = pd.qcut(x["fz"].rank(method="first"), 5, labels=False)
        qm = x.groupby(q)["s5"].mean()
        res.append({"feat": f, "n": len(x), "slope": sl.slope, "t": sl.slope / sl.stderr,
                    **{f"q{i+1}": qm.iloc[i] for i in range(5)}})
    out["feature slopes on strength (5d excess / usual move)"] = pd.DataFrame(res)
    # forecast zero vs positive
    out["fc>0 vs 0"] = g.assign(on=g["fc"] > 0).groupby("on")["s5"].agg(["count", "mean"])
    # weekday on 1d returns, all bars
    a = df.dropna(subset=["fwd1"]).copy()
    a["ex1"] = a["fwd1"] - a["coin"].map(a.groupby("coin")["fwd1"].mean())
    a["s1"] = a["ex1"] / a["coin"].map(a.groupby("coin")["fwd1"].std())
    wd = a.groupby("wd")["s1"].agg(["count", "mean", "std"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["weekday next-day strength"] = wd
    # vol regime x r20 interaction
    x = g.dropna(subset=["vol20", "r20"]).copy()
    x["volq"] = x.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    x["r20q"] = x.groupby("coin")["r20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["vol tercile x r20 tercile mean strength"] = x.pivot_table(index="volq", columns="r20q", values="s5", aggfunc="mean")
    out["vol x r20 counts"] = x.pivot_table(index="volq", columns="r20q", values="s5", aggfunc="count")
    # book: daily returns, by year and by window
    days = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            days.append(d)
    D = pd.concat(days)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    bk = D.groupby(["win", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean"), year=("year", "first")).dropna()
    yr = bk.groupby("year").agg(n=("br", "count"), book=("br", "mean"), hold=("cr", "mean"))
    yr["book_sharpe"] = bk.groupby("year")["br"].mean() / bk.groupby("year")["br"].std() * np.sqrt(365)
    out["book by year"] = yr
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values() if len(t)])
    T["days"] = T["duration_minutes"] / 1440
    T["dq"] = pd.qcut(T["days"].rank(method="first"), 4, labels=False)
    out["trades by duration quartile"] = T.groupby("dq").agg(n=("days", "count"), days=("days", "mean"),
                                                             pl=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    return out
