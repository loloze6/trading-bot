def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            b["fwd"] = c.shift(-H) / c - 1
            b["ret1"] = c.pct_change()
            b["ret5"] = c / c.shift(5) - 1
            hi20 = c.rolling(20).max(); lo20 = c.rolling(20).min()
            b["rpos"] = (c - lo20) / (hi20 - lo20) - 0.5
            b["tr60"] = c / c.shift(60) - 1
            b["vol30"] = b["ret1"].rolling(30).std()
            b["vol10"] = b["ret1"].rolling(10).std()
            ts = pd.to_datetime(b["timestamp"])
            b["wd"] = ts.dt.weekday; b["yr"] = ts.dt.year
            b["coin"] = coin; b["win"] = w
            b["day"] = ts.dt.floor("D")
            b["alloc"] = b["postRebalance_current_allocation"]
            b["ah"] = b.get("debug_info.components.above_high.last_history_value")
            g = b.iloc[::H]
            rows.append(g)
    G = pd.concat(rows, ignore_index=True)
    G = G.dropna(subset=["fwd"])
    drift = G.groupby("coin")["fwd"].transform("mean")
    G["ex"] = G["fwd"] - drift
    volmed = G.groupby("coin")["vol30"].transform("median")
    G["agit"] = np.where(G["vol30"] > volmed, "agit", "calm")
    G["trend"] = pd.cut(G["tr60"], [-np.inf, -0.1, 0.1, np.inf], labels=["fall", "chop", "rise"])
    out = {}
    def summ(df, key):
        r = df.groupby(key, observed=True)["ex"].agg(["count", "mean", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r.round(4)
    G["fq"] = pd.qcut(G["forecast"], 5, labels=False, duplicates="drop")
    out["forecast quintile"] = summ(G, "fq")
    G["rq"] = pd.qcut(G["rpos"], 5, labels=False, duplicates="drop")
    out["rangepos quintile"] = summ(G, "rq")
    G["r5q"] = pd.qcut(G["ret5"], 5, labels=False, duplicates="drop")
    out["5d return quintile"] = summ(G, "r5q")
    G["r1q"] = pd.qcut(G["ret1"], 5, labels=False, duplicates="drop")
    out["1d return quintile"] = summ(G, "r1q")
    G["vq"] = pd.qcut(G["vol10"], 4, labels=False, duplicates="drop")
    out["vol10 quartile"] = summ(G, "vq")
    out["trend x rpos sign"] = G.assign(up=G["rpos"] > 0).pipe(lambda d: summ(d, ["trend", "up"]))
    out["agit x rpos sign"] = G.assign(up=G["rpos"] > 0).pipe(lambda d: summ(d, ["agit", "up"]))
    # slope of ex on rpos by trend
    sl = {}
    for k, d in G.dropna(subset=["rpos", "trend"]).groupby("trend", observed=True):
        r = stats.linregress(d["rpos"], d["ex"]); sl[k] = (len(d), round(r.slope, 4), round(r.slope / r.stderr, 2))
    out["slope rpos by trend (n,slope,t)"] = pd.DataFrame(sl, index=["n", "slope", "t"]).T
    sl = {}
    for k, d in G.dropna(subset=["rpos"]).groupby("agit"):
        r = stats.linregress(d["rpos"], d["ex"]); sl[k] = (len(d), round(r.slope, 4), round(r.slope / r.stderr, 2))
    out["slope rpos by agit"] = pd.DataFrame(sl, index=["n", "slope", "t"]).T
    sl = {}
    for k, d in G.dropna(subset=["rpos"]).groupby("coin"):
        r = stats.linregress(d["rpos"], d["ex"]); sl[k] = (len(d), round(r.slope, 4), round(r.slope / r.stderr, 2))
    out["slope rpos by coin"] = pd.DataFrame(sl, index=["n", "slope", "t"]).T
    sl = {}
    for k, d in G.dropna(subset=["rpos"]).groupby("win"):
        r = stats.linregress(d["rpos"], d["ex"]); sl[k] = (len(d), round(r.slope, 4), round(r.slope / r.stderr, 2))
    out["slope rpos by window"] = pd.DataFrame(sl, index=["n", "slope", "t"]).T
    # book daily
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D)
    book = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna().reset_index()
    out["book by window"] = book.groupby("win")[["book_return", "coin_return"]].agg(["mean", "std"]).round(4)
    book["wd"] = pd.to_datetime(book["day"]).dt.weekday
    out["book by weekday"] = book.groupby("wd")["book_return"].agg(["count", "mean"]).round(5)
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    T["dur_d"] = T["duration_minutes"] / 1440
    out["trades by side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median"]).round(3)
    T["absf"] = pd.qcut(T["entry_forecast"].abs(), 4, labels=False, duplicates="drop")
    out["trades by |entry fc| quartile, side"] = T.groupby(["side", "absf"])["net_profit_loss_percent"].agg(["count", "mean"]).round(3)
    return out
