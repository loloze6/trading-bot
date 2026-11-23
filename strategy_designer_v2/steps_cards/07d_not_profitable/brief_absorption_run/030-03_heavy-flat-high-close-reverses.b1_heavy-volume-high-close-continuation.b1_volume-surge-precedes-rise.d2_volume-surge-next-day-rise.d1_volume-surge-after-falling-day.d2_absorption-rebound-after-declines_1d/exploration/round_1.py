def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for c, wd in data["bars"].items():
        for w, b in wd.items():
            b = b.copy().reset_index(drop=True)
            b["coin"] = c; b["win"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            cl = b["close"]
            for h in [1, 2, 3, 5, 10]:
                b[f"r{h}"] = cl.shift(-h) / cl - 1
            b["ret1"] = cl.pct_change()
            b["ret20"] = cl / cl.shift(20) - 1
            b["pos"] = np.arange(len(b))
            b["pnl"] = b["postRebalance_current_allocation"] * b["r1"]
            b["vr"] = b["volume"] / b["volume"].shift(1).rolling(20).mean()
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    mu = {h: B.groupby("coin")[f"r{h}"].mean() for h in [1, 2, 3, 5, 10]}
    for h in [1, 2, 3, 5, 10]:
        B[f"x{h}"] = B[f"r{h}"] - B["coin"].map(mu[h])
    S = B[B["forecast"] > 0].copy()
    S["q"] = pd.qcut(S["forecast"].rank(method="first"), 5, labels=False)
    g = S.groupby("q")
    out["by forecast quintile"] = pd.DataFrame({
        "n": g.size(), "fc": g["forecast"].mean(),
        "x1": g["x1"].mean(), "x2": g["x2"].mean(), "x3": g["x3"].mean(),
        "x5": g["x5"].mean(), "x10": g["x10"].mean(),
        "alloc": g["postRebalance_current_allocation"].mean()})
    def tt(s):
        s = s.dropna(); return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean() / s.std() * np.sqrt(len(s))})
    out["signal x by horizon (overlapping)"] = pd.DataFrame({f"x{h}": tt(S[f"x{h}"]) for h in [1, 2, 3, 5, 10]}).T
    out["signal by year x1"] = S.groupby("year")["x1"].agg(["count", "mean"])
    out["signal by coin x1"] = S.groupby("coin")["x1"].agg(["count", "mean"])
    # ret20 buckets: signal vs no signal (down day, no signal) 
    down = B[B["ret1"] < 0].copy()
    down["sig"] = down["forecast"] > 0
    down["r20b"] = pd.cut(down["ret20"], [-1, -0.3, -0.15, -0.05, 0, 0.1, 10])
    out["down days by ret20 & signal x1"] = down.groupby(["r20b", "sig"])["x1"].agg(["count", "mean"]).unstack()
    down["vb"] = pd.cut(down["vr"], [0, 0.8, 1.2, 2, 3, 100])
    out["down days by volratio & signal x1"] = down.groupby(["vb", "sig"])["x1"].agg(["count", "mean"]).unstack()
    # held days: pnl by state of allocation
    H = B[B["postRebalance_current_allocation"].abs() > 0]
    out["held bars"] = pd.Series({"n": len(H), "held with fc>0": (H["forecast"] > 0).mean(),
                                  "mean pnl": H["pnl"].mean(), "mean alloc": H["postRebalance_current_allocation"].mean()})
    H2 = H.copy(); H2["fcpos"] = H2["forecast"] > 0
    out["held pnl by fc>0"] = H2.groupby("fcpos")["pnl"].agg(["count", "mean", "sum"])
    # book daily drawdown
    D = []
    for c, wd in data["days"].items():
        for w, d in wd.items():
            d = d.copy(); d["coin"] = c; d["win"] = w; D.append(d)
    D = pd.concat(D)
    bk = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().reset_index()
    bk["wn"] = bk["win"].str[1:].astype(int)
    bk = bk.sort_values(["wn", "day"]).dropna()
    v = (1 + bk["book_return"]).cumprod(); dd = v / v.cummax() - 1
    bk["dd"] = dd.values
    out["book by window"] = bk.groupby("wn").agg(book=("book_return", "sum"), coin=("coin_return", "sum"),
                                                 mindd=("dd", "min"))
    # trades
    T = pd.concat([t.assign(coin=c) for c, wd in data["trades"].items() for w, t in wd.items()])
    out["trades"] = pd.Series({"n": len(T), "gross mean %": T["profit_loss_percent"].mean(),
                               "net mean %": T["net_profit_loss_percent"].mean(),
                               "dur days": T["duration_minutes"].mean() / 1440,
                               "win share": (T["net_profit_loss_percent"] > 0).mean()})
    return out
