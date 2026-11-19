def explore(data):
    import numpy as np, pandas as pd
    out = {}
    tr = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if t is None or len(t) == 0: continue
            t = t.copy(); t["coin"] = c; t["win"] = w
            tr.append(t)
    T = pd.concat(tr)
    out["trades_summary"] = pd.DataFrame({
        "n": T.groupby("coin").size(),
        "gross_mean": T.groupby("coin")["profit_loss_percent"].mean(),
        "net_mean": T.groupby("coin")["net_profit_loss_percent"].mean(),
        "dur_h_median": T.groupby("coin")["duration_minutes"].median() / 60,
        "comm_mean": T.groupby("coin")["total_commission"].mean(),
    })
    # bar-level position gains by hour, and turnover
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            r1 = b["close"].shift(-1) / b["close"] - 1
            pos = b["postRebalance_current_allocation"].fillna(0)
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            rows.append(pd.DataFrame({"coin": c, "win": w, "hour": ts.dt.hour, "pos": pos,
                                      "gain": pos * r1, "fee": fee, "r1": r1,
                                      "fc": b["forecast"], "close": b["close"], "year": ts.dt.year,
                                      "ret24": b["close"] / b["close"].shift(24) - 1}))
    B = pd.concat(rows)
    act = B[B.pos.abs() > 0]
    out["by_hour_held"] = act.groupby("hour").agg(n=("gain", "size"), pos=("pos", "mean"),
                                                   gain=("gain", "mean"), r1=("r1", "mean"))
    out["fee_vs_gain_total"] = pd.Series({"sum_gain": B.gain.sum(), "sum_fee": B.fee.sum(),
                                          "mean_pos_active": act.pos.mean()})
    # 20:00 decision bars: 2h return by forecast bucket
    d = B[B.hour == 20].copy()
    # recompute 2h fwd return within window
    parts = []
    for (c, w), g in B.groupby(["coin", "win"]):
        g = g.copy(); g["f2"] = g["close"].shift(-2) / g["close"] - 1
        parts.append(g[g.hour == 20])
    D = pd.concat(parts)
    D["bucket"] = pd.cut(D.fc, [-0.01, 0.0001, 2, 5, 10, 21])
    out["dec_by_fc"] = D.groupby("bucket", observed=True)["f2"].agg(["size", "mean", "median"])
    out["dec_by_coin_fcpos"] = D[D.fc > 0].groupby("coin")["f2"].agg(["size", "mean"])
    out["dec_by_year"] = D.assign(p=D.fc > 0).groupby(["year", "p"])["f2"].agg(["size", "mean"])
    out["book_by_coin_year"] = act.groupby("year").agg(gain=("gain", "sum"), fee=("fee", "sum"))
    return out
