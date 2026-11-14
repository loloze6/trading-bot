def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []; trows = []; drows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            b["ret"] = b["close"].pct_change()
            b["pos_prev"] = b["postRebalance_current_allocation"].shift(1)
            b["gross"] = b["pos_prev"] * b["ret"]
            b["bv"] = b["postRebalance_total_value"].pct_change()
            b["fc_prev"] = b["forecast"].shift(1)
            b["fwd10"] = b["close"].shift(-10) / b["close"] - 1
            b["vol20"] = b["ret"].rolling(20).std()
            b["mom20"] = b["close"] / b["close"].shift(20) - 1
            b["coin"] = coin; b["w"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b)
        for w, t in data["trades"][coin].items():
            t = t.copy(); t["coin"] = coin; t["w"] = w; trows.append(t)
    B = pd.concat(rows, ignore_index=True)
    T = pd.concat(trows, ignore_index=True) if trows else pd.DataFrame()
    a = B.dropna(subset=["gross", "bv"])
    act = a[a["pos_prev"].abs() > 1e-9]
    out["overall"] = pd.Series({
        "bars": len(a), "active_share": len(act)/len(a),
        "mean_book_ret": a["bv"].mean(), "mean_gross": a["gross"].mean(),
        "fee_drag_per_bar": (a["gross"] - a["bv"]).mean(),
        "mean_pos_active": act["pos_prev"].mean(),
        "coin_ret_when_short": act["ret"].mean(), "coin_ret_all": a["ret"].mean(),
    })
    out["by_coin"] = a.groupby("coin").agg(gross=("gross", "sum"), net=("bv", "sum"),
        active=("pos_prev", lambda s: (s.abs() > 1e-9).mean()))
    act = act.copy()
    act["fbin"] = pd.qcut(act["fc_prev"].abs(), 4, labels=False, duplicates="drop")
    out["by_fc_quartile"] = act.groupby("fbin").agg(n=("gross", "size"), fc=("fc_prev", "mean"),
        gross=("gross", "mean"), coinret=("ret", "mean"), net=("bv", "mean"))
    out["by_year"] = a.groupby("year").agg(active=("pos_prev", lambda s: (s.abs() > 1e-9).mean()),
        gross=("gross", "sum"), net=("bv", "sum"), coin=("ret", "mean"))
    act["vbin"] = pd.qcut(act["vol20"], 3, labels=["calm", "mid", "volatile"])
    out["by_vol"] = act.groupby("vbin").agg(n=("gross", "size"), gross=("gross", "mean"), net=("bv", "mean"))
    act["mbin"] = pd.qcut(act["mom20"], 3, labels=["falling", "flat", "rising"])
    out["by_mom20"] = act.groupby("mbin").agg(n=("gross", "size"), gross=("gross", "mean"), net=("bv", "mean"))
    # time since start of short spell
    if len(T):
        T["days"] = T["duration_minutes"] / 1440
        out["trades"] = pd.Series({
            "n": len(T), "short_share": (T["side"] == "SHORT").mean(),
            "median_days": T["days"].median(), "mean_days": T["days"].mean(),
            "mean_pl_gross": T["profit_loss_percent"].mean(),
            "mean_pl_net": T["net_profit_loss_percent"].mean(),
            "mean_comm": T["total_commission"].mean(),
            "win_rate_gross": (T["profit_loss_percent"] > 0).mean(),
            "sum_pl_gross": T["profit_loss_percent"].sum(),
            "sum_pl_net": T["net_profit_loss_percent"].sum()})
        T["dbin"] = pd.cut(T["days"], [-1, 1, 3, 10, 30, 1e9])
        out["trades_by_dur"] = T.groupby("dbin").agg(n=("days", "size"),
            gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    # forward 10 return in short state vs all
    out["fwd10"] = pd.Series({"all": B["fwd10"].mean(),
        "short_state": B.loc[B["forecast"] < 0, "fwd10"].mean(),
        "flat_state": B.loc[B["forecast"] == 0, "fwd10"].mean()})
    # allocation changes per bar
    out["alloc_change_share"] = float((B["allocation_change"].abs() > 1e-9).mean()) if "allocation_change" in B else np.nan
    return out
