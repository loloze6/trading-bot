def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 3
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            b["fwd"] = c.shift(-H) / c - 1
            b["fwd1"] = c.shift(-1) / c - 1
            b["r1"] = c.pct_change()
            b["r5"] = c / c.shift(5) - 1
            b["r20"] = c / c.shift(20) - 1
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            b["clv"] = (c - b["low"]) / rng
            b["relvol"] = b["volume"] / b["volume"].rolling(20, min_periods=10).mean().shift(1)
            b["vol20"] = b["r1"].rolling(20, min_periods=10).std()
            b["vol20rel"] = b["vol20"] / b["r1"].rolling(120, min_periods=40).std()
            b["rangerel"] = (rng / c) / (rng / c).rolling(20, min_periods=10).mean().shift(1)
            b["fc"] = b["forecast"]
            b["alloc"] = b["postRebalance_current_allocation"]
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["pos"] = np.arange(len(b))
            b["coin"] = coin; b["win"] = w
            rows.append(b)
    df = pd.concat(rows, ignore_index=True)
    g = df[(df["pos"] % H == 0) & df["fwd"].notna()].copy()
    drift = g.groupby("coin")["fwd"].mean()
    usual = g.groupby("coin")["fwd"].std()
    g["ex"] = g["fwd"] - g["coin"].map(drift)
    g["z"] = g["ex"] / g["coin"].map(usual)
    def summ(grp):
        x = grp["ex"]
        return pd.Series({"n": len(x), "mean_ex%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan, "meanz": grp["z"].mean()})
    out = {}
    g["fcb"] = pd.cut(g["fc"], [-0.01, 0.0001, 3, 6, 10, 21])
    out["fwd3 by forecast bucket"] = g.groupby("fcb").apply(summ)
    # scaled 5-day return incl. negative side
    g["r5z"] = g["r5"] / g.groupby("coin")["r5"].transform(lambda s: s.abs().mean())
    g["r5q"] = pd.qcut(g["r5z"], 6)
    out["fwd3 by r5 sextile (both sides)"] = g.groupby("r5q").apply(summ)
    g["r1q"] = pd.qcut(g["r1"] / g["vol20"], 5)
    out["fwd3 by 1d move in vol units"] = g.groupby("r1q").apply(summ)
    hv = g[g["relvol"] > g["relvol"].quantile(0.8)]
    flat = hv[(hv["r1"].abs() / hv["vol20"]) < 0.5]
    out["heavy flat days by clv tercile"] = flat.groupby(pd.cut(flat["clv"], [0, 1/3, 2/3, 1.0001])).apply(summ)
    out["all days by clv tercile"] = g.groupby(pd.cut(g["clv"], [0, 1/3, 2/3, 1.0001])).apply(summ)
    out["fwd3 by volatility regime (vol20/vol120 quintile)"] = g.groupby(pd.qcut(g["vol20rel"], 5)).apply(summ)
    out["fwd3 by 20d return quintile"] = g.groupby(pd.qcut(g["r20"] / g["vol20"], 5)).apply(summ)
    out["fwd3 by relvol quintile"] = g.groupby(pd.qcut(g["relvol"], 5)).apply(summ)
    out["fwd3 by weekday"] = g.groupby("wd").apply(summ)
    # forecast>0 split by vol regime: interaction
    p = g[g["fc"] > 0]
    out["forecast>0: by vol regime tercile"] = p.groupby(pd.qcut(p["vol20rel"], 3)).apply(summ)
    out["forecast>0: by relvol tercile"] = p.groupby(pd.qcut(p["relvol"], 3)).apply(summ)
    out["forecast>0: by clv tercile"] = p.groupby(pd.cut(p["clv"], [0, 1/3, 2/3, 1.0001])).apply(summ)
    # book days
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; dl.append(d)
    D = pd.concat(dl, ignore_index=True)
    bk = D.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book: share of total from top/bottom 5% days"] = pd.Series({
        "n_days": len(bk), "sum_all%": 100*bk.sum(),
        "sum_top5%": 100*bk[bk >= bk.quantile(0.95)].sum(),
        "sum_bot5%": 100*bk[bk <= bk.quantile(0.05)].sum(),
        "skew": stats.skew(bk), "kurt": stats.kurtosis(bk)})
    # trades
    tl = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; tl.append(t)
    T = pd.concat(tl, ignore_index=True)
    T["days"] = T["duration_minutes"] / 1440
    T["db"] = pd.cut(T["days"], [0, 3.5, 6.5, 12.5, 30, 1000])
    out["trades by duration"] = T.groupby("db").agg(n=("net_profit_loss_percent", "size"), mean_net=("net_profit_loss_percent", "mean"), win=("net_profit_loss_percent", lambda s: (s > 0).mean()))
    T["efb"] = pd.qcut(T["entry_forecast"], 4, duplicates="drop")
    out["trades by entry forecast"] = T.groupby("efb").agg(n=("net_profit_loss_percent", "size"), mean_net=("net_profit_loss_percent", "mean"))
    return out
