def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # trades
    tr = []
    for c, ws in data["trades"].items():
        for w, df in ws.items():
            if len(df):
                d = df.copy(); d["coin"] = c; d["win"] = w; tr.append(d)
    T = pd.concat(tr, ignore_index=True)
    T["days"] = T["duration_minutes"] / 1440
    T["fee_pct"] = T["profit_loss_percent"] - T["net_profit_loss_percent"]
    out["trades_by_coin"] = T.groupby("coin").agg(n=("side", "size"), days=("days", "mean"),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"),
        fee=("fee_pct", "mean"), win=("profit_loss_percent", lambda x: (x > 0).mean()))
    out["trades_all"] = pd.Series({"n": len(T), "days_med": T["days"].median(), "days_mean": T["days"].mean(),
        "gross_mean": T["profit_loss_percent"].mean(), "net_mean": T["net_profit_loss_percent"].mean(),
        "fee_mean": T["fee_pct"].mean(), "sides_long": (T["side"] == "LONG").mean()})
    T["dur_b"] = pd.cut(T["days"], [0, 1.5, 3.5, 7.5, 15, 1000])
    out["trades_by_duration"] = T.groupby("dur_b").agg(n=("side", "size"), gross=("profit_loss_percent", "mean"),
        net=("net_profit_loss_percent", "mean"))
    # bars: forecast buckets, forward returns non-overlapping, book return by state
    rows = []; drows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; n = len(cl)
            f = b["forecast"].values
            fwd20 = np.full(n, np.nan); fwd20[:n-20] = cl[20:] / cl[:n-20] - 1
            fwd1 = np.full(n, np.nan); fwd1[:n-1] = cl[1:] / cl[:-1] - 1
            past20 = np.full(n, np.nan); past20[20:] = cl[20:] / cl[:-20] - 1
            r = pd.Series(cl).pct_change()
            vol20 = r.rolling(20).std().values
            ma100 = pd.Series(cl).rolling(100, min_periods=60).mean().values
            alloc = b["postRebalance_current_allocation"].values
            bv = b["postRebalance_total_value"].values
            bret = np.full(n, np.nan); bret[:n-1] = bv[1:] / bv[:-1] - 1
            dfx = pd.DataFrame({"coin": c, "win": w, "i": np.arange(n), "f": f, "fwd20": fwd20, "fwd1": fwd1,
                "past20": past20, "vol20": vol20, "above_ma": cl > ma100, "alloc": alloc, "bret": bret,
                "year": pd.to_datetime(b["timestamp"]).dt.year.values})
            dfx["coinmean20"] = np.nan
            rows.append(dfx)
    B = pd.concat(rows, ignore_index=True)
    cm = B.groupby("coin")["fwd20"].mean()
    B["ex20"] = B["fwd20"] - B["coin"].map(cm)
    B["vq"] = B.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 3, labels=["calm", "mid", "vol"]))
    NO = B[B["i"] % 20 == 0]
    act = NO[NO["f"] > 0].copy()
    act["fb"] = pd.qcut(act["f"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    g = act.groupby("fb")["ex20"]
    out["fwd20_by_fbucket_nonoverlap"] = pd.DataFrame({"n": g.count(), "mean_ex": g.mean(),
        "t": g.mean() / (g.std() / np.sqrt(g.count())), "f_mean": act.groupby("fb")["f"].mean()})
    flat = NO[NO["f"] == 0]["ex20"]
    out["fwd20_flat_nonoverlap"] = pd.Series({"n": flat.count(), "mean_ex": flat.mean()})
    # gross daily pnl by state
    B["pnl"] = B["alloc"] * B["fwd1"]
    B["cost"] = B["pnl"] - B["bret"]
    out["daily_pnl_sum_by_coin"] = B.groupby("coin").agg(pnl=("pnl", "sum"), book=("bret", "sum"),
        alloc_mean=("alloc", "mean"), active=("alloc", lambda x: (x.abs() > 0.01).mean()))
    out["pnl_by_trend"] = B.groupby("above_ma").agg(pnl=("pnl", "sum"), book=("bret", "sum"), alloc=("alloc", "mean"), n=("pnl", "size"))
    out["pnl_by_vol"] = B.groupby("vq").agg(pnl=("pnl", "sum"), book=("bret", "sum"), alloc=("alloc", "mean"))
    out["pnl_by_year"] = B.groupby("year").agg(pnl=("pnl", "sum"), book=("bret", "sum"), coin=("fwd1", "mean"), alloc=("alloc", "mean"))
    out["pnl_by_window"] = B.groupby("win").agg(pnl=("pnl", "sum"), book=("bret", "sum"), coin=("fwd1", "sum")).sort_values("book").head(8)
    out["alloc_desc"] = B["alloc"].describe()
    out["alloc_change_rate"] = pd.Series({"share_bars_alloc_changes": (B.groupby(["coin","win"])["alloc"].diff().abs() > 1e-6).mean()})
    return out
