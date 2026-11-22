def explore(data):
    import pandas as pd, numpy as np
    out = {}
    tr = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if t is None or len(t) == 0: continue
            d = t.copy(); d["coin"] = c; d["window"] = w
            tr.append(d)
    T = pd.concat(tr, ignore_index=True)
    T["absf"] = T["entry_forecast"].abs()
    T["fbin"] = pd.cut(T["absf"], [0, 1, 2, 4, 8, 21])
    T["hours"] = T["duration_minutes"] / 60
    T["year"] = pd.to_datetime(T["entry_time"]).dt.year
    T["wd"] = pd.to_datetime(T["entry_time"]).dt.weekday
    T["hr"] = pd.to_datetime(T["entry_time"]).dt.hour
    agg = lambda g: pd.Series({"n": len(g), "gross_mean": g["profit_loss_percent"].mean(),
                               "net_mean": g["net_profit_loss_percent"].mean(),
                               "t_net": g["net_profit_loss_percent"].mean() / (g["net_profit_loss_percent"].std() / np.sqrt(len(g))) if len(g) > 1 else np.nan,
                               "hours_med": g["hours"].median(), "win": (g["net_profit_loss_percent"] > 0).mean()})
    out["all_trades"] = agg(T).to_frame().T
    out["by_side"] = T.groupby("side").apply(agg)
    out["by_forecast_bin"] = T.groupby("fbin").apply(agg)
    out["by_year"] = T.groupby("year").apply(agg)
    out["by_window"] = T.groupby("window").apply(agg)
    out["by_coin"] = T.groupby("coin").apply(agg)
    out["hours_dist"] = T["hours"].describe()
    out["entry_wd_hr"] = T.groupby(["wd", "hr"]).size().sort_values(ascending=False).head(10)
    # book daily: exposure share and daily return by window
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            a = b["postRebalance_current_allocation"].fillna(0)
            r = b["close"].pct_change().shift(-1)
            g = (a * r)
            rows.append({"coin": c, "window": w, "share_in": (a != 0).mean(), "mean_abs_alloc_when_in": a[a != 0].abs().mean(),
                         "gain_sum": g.sum(), "n": len(b)})
    B = pd.DataFrame(rows)
    out["exposure"] = B[["share_in", "mean_abs_alloc_when_in"]].describe()
    out["book_gain_by_window"] = B.groupby("window")["gain_sum"].sum()
    return out
