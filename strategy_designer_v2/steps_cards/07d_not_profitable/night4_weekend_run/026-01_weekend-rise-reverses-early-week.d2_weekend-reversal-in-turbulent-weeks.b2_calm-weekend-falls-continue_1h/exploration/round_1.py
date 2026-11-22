def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    tr_rows = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if t is None or len(t) == 0: continue
            d = t.copy(); d["coin"] = c; d["window"] = w
            tr_rows.append(d)
    T = pd.concat(tr_rows, ignore_index=True)
    T["entry_time"] = pd.to_datetime(T["entry_time"]); T["exit_time"] = pd.to_datetime(T["exit_time"])
    T["ewd"] = T["entry_time"].dt.dayofweek; T["ehr"] = T["entry_time"].dt.hour
    T["dur_h"] = T["duration_minutes"] / 60
    out["trades_by_coin"] = T.groupby("coin").agg(n=("side", "size"), short=("side", lambda s: (s == "SHORT").mean()),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"), dur_h=("dur_h", "median"))
    out["trades_by_entry_weekday"] = T.groupby("ewd").agg(n=("side", "size"), gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"), dur=("dur_h", "median"))
    out["trades_duration_quantiles"] = T["dur_h"].describe()
    out["trades_by_window"] = T.groupby("window").agg(n=("side", "size"), gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    # bars: positions
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"])
            al = b["postRebalance_current_allocation"].fillna(0)
            r1 = b["close"].shift(-1) / b["close"] - 1
            g = al * r1
            rows.append(pd.DataFrame({"coin": c, "window": w, "wd": ts.dt.dayofweek, "hr": ts.dt.hour, "al": al, "g": g, "r1": r1,
                                      "fc": b["forecast"], "regime": b["regime"]}))
    B = pd.concat(rows, ignore_index=True)
    B["in"] = B["al"] != 0
    out["share_bars_in"] = float(B["in"].mean())
    out["alloc_when_in"] = B.loc[B["in"], "al"].describe()
    out["gain_by_weekday_in"] = B[B["in"]].groupby("wd").agg(n=("g", "size"), meanal=("al", "mean"), g_bp=("g", lambda x: x.mean() * 1e4), r1_bp=("r1", lambda x: x.mean() * 1e4))
    out["regime_counts"] = B["regime"].value_counts()
    out["fc_nonzero_by_wd_hr"] = B[B["fc"] != 0].groupby(["wd"]).size()
    return out
