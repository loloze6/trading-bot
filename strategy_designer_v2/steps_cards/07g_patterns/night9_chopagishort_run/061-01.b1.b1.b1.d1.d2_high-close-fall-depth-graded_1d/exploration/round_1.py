def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float); op = b["open"].astype(float)
            rng = (hi - lo).replace(0, np.nan)
            cl = (c - lo) / rng
            r1 = c.pct_change()
            r5 = c / c.shift(5) - 1
            r20 = c / c.shift(20) - 1
            r60 = c / c.shift(60) - 1
            vol30 = r1.rolling(30).std()
            vol10 = r1.rolling(10).std()
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            wr = rng / c
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "cl": cl, "r1": r1, "r5": r5, "r20": r20,
                               "r60": r60, "vol30": vol30, "volratio": vol10 / vol30, "fwd": fwd, "fwd1": fwd1,
                               "wr": wr, "wr_rel": wr / wr.rolling(30).mean(), "wd": ts.dt.weekday, "yr": ts.dt.year,
                               "alloc": b["postRebalance_current_allocation"].astype(float), "fc": b["forecast"].astype(float),
                               "usd": fwd / (vol30 * np.sqrt(H))})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin").apply(lambda g: g.loc[g.pos % H == 0, "fwd"].mean())
    D["ufwd"] = D["fwd"] - D["coin"].map(drift)
    G = D[(D.pos % H == 0)].dropna(subset=["ufwd"])
    out = {}
    def tab(g, key):
        r = g.groupby(key, observed=True)["ufwd"].agg(["count", "mean", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r.round(4)
    G = G.copy()
    G["clq"] = pd.cut(G.cl, [-0.01, 0.25, 0.5, 0.75, 1.01])
    G["r5s"] = np.where(G.r5 < 0, "r5neg", "r5pos")
    G["trend"] = pd.cut(G.r60, [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])
    out["cl x r5 sign"] = tab(G, ["clq", "r5s"])
    out["trend x cl"] = tab(G.dropna(subset=["trend"]), ["trend", "clq"])
    G["r5q"] = pd.qcut(G.r5, 5)
    out["r5 quintile"] = tab(G, "r5q")
    G["r1q"] = pd.qcut(G.r1, 5)
    out["r1 quintile"] = tab(G, "r1q")
    G["wrq"] = pd.qcut(G.wr_rel, 4)
    out["range rel quartile x clq"] = tab(G.dropna(subset=["wrq"]), ["wrq", "clq"])
    G["vrq"] = pd.qcut(G.volratio, 4)
    out["vol10/30 quartile"] = tab(G.dropna(subset=["vrq"]), "vrq")
    out["weekday"] = tab(G, "wd")
    G["r20q"] = pd.qcut(G.r20, 5)
    out["r20 quintile"] = tab(G.dropna(subset=["r20q"]), "r20q")
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, w=w))
    DD = pd.concat(dd)
    out["book days active share"] = float((DD.book_return.abs() > 0).mean())
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            T.append(t.assign(coin=coin, w=w))
    T = pd.concat(T)
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "sum"]).round(3)
    out["trades n"] = len(T)
    return out
