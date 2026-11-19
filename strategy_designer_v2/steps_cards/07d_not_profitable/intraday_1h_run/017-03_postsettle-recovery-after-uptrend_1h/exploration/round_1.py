def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    # trades: gross vs net
    tr = []
    for c in trades:
        for w in trades[c]:
            t = trades[c][w].copy(); t["coin"] = c; tr.append(t)
    T = pd.concat(tr, ignore_index=True)
    T["et"] = pd.to_datetime(T["entry_time"], utc=True)
    T["hour"] = T["et"].dt.hour
    out["trades_summary"] = pd.Series({
        "n": len(T),
        "mean_gross_pct": T["profit_loss_percent"].mean(),
        "mean_net_pct": T["net_profit_loss_percent"].mean(),
        "median_dur_min": T["duration_minutes"].median(),
        "share_gross_pos": (T["profit_loss_percent"] > 0).mean(),
        "t_gross": T["profit_loss_percent"].mean() / (T["profit_loss_percent"].std() / np.sqrt(len(T))),
    })
    out["trades_by_coin"] = T.groupby("coin").agg(n=("profit_loss_percent","size"),
        gross=("profit_loss_percent","mean"), net=("profit_loss_percent", lambda s: np.nan),
    ).assign(net=T.groupby("coin")["net_profit_loss_percent"].mean())
    out["trades_by_entry_hour"] = T.groupby("hour").agg(n=("profit_loss_percent","size"),
        gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"),
        dur=("duration_minutes","median"))
    # bar-level gross gain and fees
    rows = []
    for c in bars:
        for w in bars[c]:
            b = bars[c][w].copy()
            b["ts"] = pd.to_datetime(b["timestamp"], utc=True)
            b["r1"] = b["close"].shift(-1) / b["close"] - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gross"] = b["pos"] * b["r1"]
            b["fee"] = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            b["turn"] = (b["postRebalance_current_allocation"] - b["previous_allocation"]).abs()
            b["coin"] = c; b["w"] = w
            b["r72"] = b["close"] / b["close"].shift(72) - 1
            rows.append(b[["ts","coin","w","r1","pos","gross","fee","turn","forecast","r72"]])
    B = pd.concat(rows, ignore_index=True)
    B["hour"] = B["ts"].dt.hour
    ndays = sum(len(days[c][w]) for c in days for w in days[c])
    out["per_coinday"] = pd.Series({
        "gross_per_coinday": B["gross"].sum() / ndays,
        "fee_per_coinday": B["fee"].sum() / ndays,
        "turn_per_coinday": B["turn"].sum() / ndays,
        "fee_per_unit_turn": B["fee"].sum() / B["turn"].sum(),
        "mean_pos_when_in": B.loc[B["pos"].abs() > 1e-9, "pos"].mean(),
        "share_bars_in": (B["pos"].abs() > 1e-9).mean(),
    })
    g = B.groupby("hour").agg(pos=("pos","mean"), gross_sum=("gross","sum"), fee_sum=("fee","sum"),
                              mean_r1=("r1","mean"))
    g["gross_sum"] /= ndays; g["fee_sum"] /= ndays
    out["by_hour"] = g
    # unconditional hourly return by hour (coin avg) and with r72>0
    up = B[B["r72"] > 0]
    out["r1_by_hour_uptrend_vs_all_bp"] = pd.DataFrame({
        "all": B.groupby("hour")["r1"].mean() * 1e4,
        "up72": up.groupby("hour")["r1"].mean() * 1e4,
    })
    # daily book
    D = pd.concat([days[c][w].assign(coin=c, w=w) for c in days for w in days[c]])
    out["daily"] = pd.Series({"book_mean": D["book_return"].mean(), "coin_mean": D["coin_return"].mean()})
    return out
