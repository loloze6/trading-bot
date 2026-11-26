def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            hh = h.rolling(20, min_periods=20).max(); ll = l.rolling(20, min_periods=20).min()
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "rangepos": (c - ll) / (hh - ll),
                "r1": c.pct_change(), "r3back": c / c.shift(3) - 1,
                "r20back": c / c.shift(20) - 1,
                "r60back": c / c.shift(60) - 1,
                "fwd3": c.shift(-3) / c - 1, "fwd1": c.shift(-1) / c - 1,
                "calm": (b["regime"] != "chop").astype(int),
                "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek,
                "vol20": c.pct_change().rolling(20).std(),
                "bodyz": (c - b["open"]) / (h - l).replace(0, np.nan),
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    # z of 1d return vs coin vol
    A["r1z"] = A["r1"] / A["vol20"]
    A["r3z"] = A["r3back"] / (A["vol20"] * np.sqrt(3))
    G = A[A["pos"] % 3 == 0].copy()
    G["drift"] = G.groupby("coin")["fwd3"].transform("mean")
    G["ex3"] = G["fwd3"] - G["drift"]
    G = G.dropna(subset=["ex3"])
    out = {}
    def tab(df, key, q=5):
        d = df.dropna(subset=[key]).copy()
        d["bin"] = pd.qcut(d[key], q, labels=False, duplicates="drop")
        g = d.groupby("bin")["ex3"].agg(["mean", "std", "count"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        g["keymean"] = d.groupby("bin")[key].mean()
        return g.round(4)
    for prof, sub in [("calm", G[G.calm == 1]), ("agit", G[G.calm == 0])]:
        out[f"rangepos_{prof}"] = tab(sub, "rangepos")
        out[f"r1z_{prof}"] = tab(sub, "r1z")
        out[f"r3z_{prof}"] = tab(sub, "r3z")
        out[f"bodyz_{prof}"] = tab(sub, "bodyz")
    # trend splits for rangepos
    def trend(x):
        return np.where(x > 0.10, "rising", np.where(x < -0.10, "falling", "choppy"))
    T = G.dropna(subset=["r60back", "rangepos"]).copy()
    T["tr"] = trend(T["r60back"])
    T["top"] = pd.cut(T["rangepos"], [-0.01, 0.2, 0.8, 1.01], labels=["low", "mid", "high"])
    g = T.groupby(["tr", "calm", "top"], observed=True)["ex3"].agg(["mean", "count"])
    g["t"] = T.groupby(["tr", "calm", "top"], observed=True)["ex3"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x))))
    out["trend_calm_rangepos"] = g.round(4)
    # weekday 1d returns
    D = A.dropna(subset=["fwd1"]).copy()
    D["drift1"] = D.groupby("coin")["fwd1"].transform("mean")
    D["ex1"] = D["fwd1"] - D["drift1"]
    g = D.groupby("wd")["ex1"].agg(["mean", "std", "count"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["weekday_next1d_ex"] = g.round(5)
    # vol level
    out["vol20_all"] = tab(G, "vol20")
    # book: daily returns, largest
    bd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bd.append(d.assign(coin=coin, win=w))
    BD = pd.concat(bd, ignore_index=True)
    br = BD.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book_by_win"] = BD.groupby("win")["book_return"].agg(["mean", "std", "count"]).round(5)
    out["book_quant"] = br.quantile([0.01, 0.05, 0.5, 0.95, 0.99]).round(4)
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            tr.append(t.assign(coin=coin, win=w))
    TR = pd.concat(tr, ignore_index=True)
    TR["dur_d"] = TR["duration_minutes"] / 1440
    TR["db"] = pd.qcut(TR["dur_d"], 4, duplicates="drop")
    out["trades_by_dur"] = TR.groupby("db", observed=True)["net_profit_loss_percent"].agg(["mean", "median", "count"]).round(3)
    out["trades_by_entryfc"] = TR.assign(fb=pd.qcut(TR["entry_forecast"], 4, duplicates="drop")).groupby("fb", observed=True)["net_profit_loss_percent"].agg(["mean", "count"]).round(3)
    return out
