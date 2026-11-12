def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    trows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            b["alloc"] = b["postRebalance_current_allocation"].astype(float)
            b["ret1"] = b["close"].pct_change().shift(-1)
            b["fwd20"] = b["close"].shift(-20) / b["close"] - 1
            v = b["postRebalance_total_value"].astype(float)
            b["bookret1"] = v.shift(-1) / v - 1
            b["past20"] = b["close"] / b["close"].shift(20) - 1
            b["vol20"] = b["close"].pct_change().rolling(20).std()
            b["coin"] = coin; b["win"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b[["coin","win","year","forecast","alloc","ret1","fwd20","bookret1","past20","vol20"]])
            t = data["trades"][coin][w].copy()
            t["coin"] = coin
            trows.append(t)
    B = pd.concat(rows, ignore_index=True)
    T = pd.concat(trows, ignore_index=True)
    B["gross1"] = B["alloc"] * B["ret1"]
    B["fee1"] = B["gross1"] - B["bookret1"]
    out["alloc_summary"] = B["alloc"].describe()
    out["alloc_vs_forecast_ratio"] = (B["alloc"] / B["forecast"].replace(0, np.nan)).describe()
    out["share_active"] = (B["alloc"].abs() > 1e-9).mean()
    # forecast buckets
    fb = pd.cut(B["forecast"], [-0.01, 0.0001, 5, 10, 15, 20.01], labels=["0","0-5","5-10","10-15","15-20"])
    g = B.groupby(fb).agg(n=("fwd20","size"), fwd20=("fwd20","mean"), ret1=("ret1","mean"),
                          hit=("fwd20", lambda s: (s > 0).mean()), alloc=("alloc","mean"))
    out["by_forecast_bucket"] = g
    # gross vs net totals
    out["gross_vs_book_mean_daily"] = pd.Series({"gross": B["gross1"].mean(), "book": B["bookret1"].mean(),
                                                 "fee_drag": B["fee1"].mean(), "coin": B["ret1"].mean()})
    # trades
    T["dur_days"] = T["duration_minutes"] / 1440
    out["trades"] = pd.Series({"n": len(T), "share_long": (T["side"] == "LONG").mean(),
                               "dur_mean": T["dur_days"].mean(), "dur_median": T["dur_days"].median(),
                               "gross_mean": T["profit_loss_percent"].mean(), "net_mean": T["net_profit_loss_percent"].mean(),
                               "gross_median": T["profit_loss_percent"].median(),
                               "win_rate_gross": (T["profit_loss_percent"] > 0).mean(),
                               "comm_sum": T["total_commission"].sum()})
    T["durb"] = pd.cut(T["dur_days"], [0, 1.5, 5, 20, 60, 10000])
    out["trades_by_duration"] = T.groupby("durb").agg(n=("dur_days","size"), gross=("profit_loss_percent","mean"),
                                                      net=("net_profit_loss_percent","mean"), comm=("total_commission","mean"))
    # regimes
    B["trend"] = np.where(B["past20"] > 0, "up20", "down20")
    B["volt"] = pd.qcut(B["vol20"], 3, labels=["calm","mid","volatile"])
    act = B[B["alloc"].abs() > 1e-9]
    out["active_by_trend"] = act.groupby("trend").agg(n=("gross1","size"), gross=("gross1","mean"), book=("bookret1","mean"), coin=("ret1","mean"))
    out["active_by_vol"] = act.groupby("volt").agg(n=("gross1","size"), gross=("gross1","mean"), book=("bookret1","mean"), coin=("ret1","mean"))
    out["by_coin"] = B.groupby("coin").agg(gross=("gross1","mean"), book=("bookret1","mean"), coin=("ret1","mean"), active=("alloc", lambda s: (s.abs()>1e-9).mean()))
    out["by_year"] = B.groupby("year").agg(gross=("gross1","mean"), book=("bookret1","mean"), coin=("ret1","mean"), active=("alloc", lambda s: (s.abs()>1e-9).mean()))
    flat = B[B["alloc"].abs() <= 1e-9]
    out["flat_vs_active_coin_ret"] = pd.Series({"coin_ret_flat": flat["ret1"].mean(), "coin_ret_active": act["ret1"].mean(),
                                                "coin_sd_flat": flat["ret1"].std(), "coin_sd_active": act["ret1"].std()})
    return out
