def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # trades
    tr = []
    for c, ws in data["trades"].items():
        for w, df in ws.items():
            if len(df):
                d = df.copy(); d["coin"] = c; tr.append(d)
    T = pd.concat(tr, ignore_index=True)
    T["days"] = T["duration_minutes"] / 1440
    T["gross"] = T["profit_loss_percent"]; T["net"] = T["net_profit_loss_percent"]
    out["trades_summary"] = pd.DataFrame({
        "n": [len(T)], "mean_days": [T.days.mean()], "median_days": [T.days.median()],
        "mean_gross": [T.gross.mean()], "median_gross": [T.gross.median()], "mean_net": [T.net.mean()],
        "mean_comm": [T.total_commission.mean()], "win_rate": [(T.gross > 0).mean()],
        "share_short_lt5d": [(T.days < 5).mean()]})
    T["dbin"] = pd.cut(T.days, [0, 2, 5, 10, 30, 90, 1000])
    out["trades_by_duration"] = T.groupby("dbin", observed=True).agg(n=("gross", "size"), mean_gross=("gross", "mean"), sum_gross=("gross", "sum"), mean_net=("net", "mean"), win=("gross", lambda x: (x > 0).mean()))
    out["trades_by_coin"] = T.groupby("coin").agg(n=("gross", "size"), mean_gross=("gross", "mean"), sum_net=("net", "sum"), mean_days=("days", "mean"))
    # bars: forecast buckets, forward returns, exposure
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            cl = b["close"]
            r = cl.pct_change()
            b["f10"] = cl.shift(-10) / cl - 1
            b["r1n"] = r.shift(-1)
            b["vol20"] = r.rolling(20).std()
            b["mom20"] = cl / cl.shift(20) - 1
            b["mom60"] = cl / cl.shift(60) - 1
            b["fdelta"] = b["forecast"].diff()
            b["alloc"] = b["postRebalance_current_allocation"]
            b["bookr"] = b["postRebalance_total_value"].pct_change().shift(-1)
            b["coin"] = c; b["win"] = w; b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b[["coin", "win", "year", "forecast", "f10", "r1n", "vol20", "mom20", "mom60", "fdelta", "alloc", "bookr"]])
    B = pd.concat(rows, ignore_index=True)
    B["fb"] = pd.cut(B.forecast, [-0.01, 0.0001, 5, 10, 15, 19.99, 20.01])
    out["fwd10_by_forecast"] = B.groupby("fb", observed=True).agg(n=("f10", "size"), f10=("f10", "mean"), r1n=("r1n", "mean"), pos=("f10", lambda x: (x > 0).mean()), alloc=("alloc", "mean"))
    act = B[B.forecast > 0].copy()
    act["volq"] = act.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=["calm", "mid", "volatile"]))
    out["active_by_vol"] = act.groupby("volq", observed=True).agg(n=("r1n", "size"), r1n=("r1n", "mean"), bookr=("bookr", "mean"))
    act["m20"] = np.sign(act.mom20); act["m60"] = np.sign(act.mom60)
    out["active_by_mom"] = act.groupby(["m60", "m20"]).agg(n=("r1n", "size"), r1n=("r1n", "mean"), bookr=("bookr", "mean"))
    act["fd"] = np.sign(act.fdelta.round(3))
    out["active_by_forecast_change"] = act.groupby("fd").agg(n=("r1n", "size"), r1n=("r1n", "mean"))
    out["by_year"] = B.groupby("year").agg(active=("forecast", lambda x: (x > 0).mean()), coin_r=("r1n", "mean"), bookr=("bookr", "mean"))
    out["inactive_vs_active_r1n"] = B.groupby(B.forecast > 0).agg(n=("r1n", "size"), r1n=("r1n", "mean"), sd=("r1n", "std"))
    # drawdown per window
    dd = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            v = d["book_value"]; dd.append((v / v.cummax() - 1).min())
    out["window_maxdd_mean_min"] = pd.Series({"mean": np.mean(dd), "min": np.min(dd)})
    return out
