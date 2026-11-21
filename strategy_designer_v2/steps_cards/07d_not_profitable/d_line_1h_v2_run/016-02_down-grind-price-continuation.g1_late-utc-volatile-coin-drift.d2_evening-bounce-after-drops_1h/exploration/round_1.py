def explore(data):
    import pandas as pd, numpy as np
    out = {}
    tr = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if t is None or len(t) == 0: continue
            d = t.copy(); d["coin"] = c; d["win"] = w
            tr.append(d)
    T = pd.concat(tr, ignore_index=True)
    T["entry_time"] = pd.to_datetime(T["entry_time"])
    T["hour"] = T["entry_time"].dt.hour
    T["fee"] = T["profit_loss_percent"] - T["net_profit_loss_percent"]
    out["trades summary"] = pd.DataFrame({
        "n": [len(T)],
        "gross_mean": [T.profit_loss_percent.mean()],
        "net_mean": [T.net_profit_loss_percent.mean()],
        "fee_mean": [T.fee.mean()],
        "dur_min_mean": [T.duration_minutes.mean()],
        "dur_min_median": [T.duration_minutes.median()],
        "gross_t": [T.profit_loss_percent.mean()/T.profit_loss_percent.std()*np.sqrt(len(T))],
        "win_gross": [(T.profit_loss_percent>0).mean()],
    })
    out["by coin"] = T.groupby("coin").agg(n=("fee","size"), gross=("profit_loss_percent","mean"),
                                          net=("net_profit_loss_percent","mean"), fee=("fee","mean"),
                                          dur=("duration_minutes","mean"))
    out["entry hour"] = T.groupby("hour").agg(n=("fee","size"), gross=("profit_loss_percent","mean"))
    T["fq"] = pd.qcut(T["entry_forecast"].rank(method="first"), 5, labels=False)
    out["by entry forecast quintile"] = T.groupby("fq").agg(n=("fee","size"), fc=("entry_forecast","mean"),
        gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"), fee=("fee","mean"),
        dur=("duration_minutes","mean"))
    # bar-level: position gain by hour of bar
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"])
            r = b["close"].shift(-1)/b["close"]-1
            pos = b["postRebalance_current_allocation"]
            g = pos*r
            v = b["postRebalance_total_value"]; tv = b["total_portfolio_value"]
            fee = (tv - v)/tv
            rows.append(pd.DataFrame({"hour": ts.dt.hour, "g": g, "pos": pos, "fee": fee, "win": w, "coin": c,
                                      "fc": b["forecast"], "r": r}))
    B = pd.concat(rows, ignore_index=True)
    out["bar gain by hour (pos held)"] = B.groupby("hour").agg(pos=("pos","mean"), gain=("g","mean"),
                                                              fee=("fee","mean"), nonzero=("pos", lambda x:(x.abs()>1e-9).mean()))
    out["totals per bar"] = pd.Series({"gross_sum_per_bar": B.g.mean(), "fee_per_bar": B.fee.mean(),
                                       "share_bars_in_pos": (B.pos.abs()>1e-9).mean(),
                                       "mean_pos_when_in": B.pos[B.pos.abs()>1e-9].mean()})
    out["by window gross/fee"] = B.groupby("win").agg(gain=("g","sum"), fee=("fee","sum"))
    return out
