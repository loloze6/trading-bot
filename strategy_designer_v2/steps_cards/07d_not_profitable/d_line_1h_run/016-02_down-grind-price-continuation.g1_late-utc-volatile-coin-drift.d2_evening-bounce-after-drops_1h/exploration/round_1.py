def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    trows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            b["ts"] = pd.to_datetime(b["timestamp"], utc=True)
            b["hr"] = b["ts"].dt.hour
            b["r1"] = b["close"].shift(-1) / b["close"] - 1
            b["gain"] = b["postRebalance_current_allocation"] * b["r1"]
            b["fee"] = b["total_portfolio_value"].shift(-1)  # placeholder
            b["feecost"] = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            b["coin"] = coin; b["w"] = w
            rows.append(b[["coin","w","hr","gain","feecost","postRebalance_current_allocation","forecast","r1"]])
        for w, t in data["trades"][coin].items():
            t = t.copy(); t["coin"] = coin; t["w"] = w
            trows.append(t)
    B = pd.concat(rows)
    T = pd.concat(trows)
    g = B.groupby("hr").agg(gain_mean=("gain","mean"), fee_mean=("feecost","mean"),
                            alloc_mean=("postRebalance_current_allocation","mean"),
                            r1_mean=("r1","mean"), n=("gain","count"))
    g["net"] = g["gain_mean"] - g["fee_mean"]
    out["by_hour"] = g
    out["total_gross_per_bar"] = B["gain"].mean()
    out["total_fee_per_bar"] = B["feecost"].mean()
    out["trades"] = pd.Series({
        "n": len(T), "mean_pl_pct": T["profit_loss_percent"].mean(),
        "mean_net_pl_pct": T["net_profit_loss_percent"].mean(),
        "median_dur_min": T["duration_minutes"].median(),
        "mean_dur_min": T["duration_minutes"].mean(),
        "share_long": (T["side"]=="LONG").mean()})
    T["fq"] = pd.qcut(T["entry_forecast"].rank(method="first"), 5, labels=False)
    out["trades_by_forecast_q"] = T.groupby("fq").agg(fc=("entry_forecast","mean"), pl=("profit_loss_percent","mean"),
        net=("net_profit_loss_percent","mean"), n=("side","count"))
    out["trades_by_coin"] = T.groupby("coin").agg(pl=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"),
        comm=("total_commission","mean"), n=("side","count"))
    T["dur_bin"] = pd.cut(T["duration_minutes"], [0,60,120,180,600,1e9])
    out["trades_by_dur"] = T.groupby("dur_bin").agg(pl=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"), n=("side","count"))
    return out
