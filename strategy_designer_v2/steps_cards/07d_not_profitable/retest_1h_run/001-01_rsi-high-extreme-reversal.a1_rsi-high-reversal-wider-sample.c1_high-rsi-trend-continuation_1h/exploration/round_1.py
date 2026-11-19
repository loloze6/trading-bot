def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    allb = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            r = b["close"].shift(-1) / b["close"] - 1
            pos = b["postRebalance_current_allocation"]
            gross = pos * r
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            turn = (pos - b["previous_allocation"]).abs()
            raw = b.get("debug_info.components.rsi_above.last_history_value")
            b["gross"] = gross; b["fee"] = fee; b["turn"] = turn; b["coin"] = coin; b["w"] = w; b["r"] = r
            allb.append(b[["coin","w","gross","fee","turn","forecast","r","regime","postRebalance_current_allocation"]].assign(raw=raw))
    A = pd.concat(allb)
    g = A.groupby("coin").agg(gross_mean_hr=("gross","mean"), fee_mean_hr=("fee","mean"), turn_mean_hr=("turn","mean"),
                              pos_mean=("postRebalance_current_allocation","mean"), share_long=("forecast", lambda x:(x>0).mean()))
    g["gross_daily"] = g.gross_mean_hr*24; g["fee_daily"] = g.fee_mean_hr*24
    out["per_coin"] = g
    out["fee_per_turnover"] = float(A.fee.sum()/A.turn.sum())
    act = A[A.forecast>0]
    out["active_raw_below0_share"] = float((act.raw<0).mean())
    out["raw_below0_forecast_pos_share"] = float((A[A.raw<0].forecast>0).mean())
    out["forecast_desc"] = A.forecast.describe()
    out["by_regime"] = A.groupby("regime").agg(gross=("gross","mean"), fee=("fee","mean"), n=("gross","size"), pos=("postRebalance_current_allocation","mean"))
    # forecast change frequency
    out["mean_abs_fc_change_hr"] = float(A.groupby(["coin","w"]).forecast.diff().abs().mean())
    # timing vs market
    mr = A.groupby("coin").r.transform("mean")
    out["market_part_hr"] = float((A.postRebalance_current_allocation*mr).mean())
    out["timing_part_hr"] = float(A.gross.mean() - (A.postRebalance_current_allocation*mr).mean())
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    out["trades"] = tr.groupby("coin").agg(n=("side","size"), dur_h=("duration_minutes", lambda x: x.median()/60),
        pl=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"))
    return out
