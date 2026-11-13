def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            b["ret"] = b["close"].pct_change()
            b["pos_prev"] = b["postRebalance_current_allocation"].shift(1)
            b["gross"] = b["pos_prev"] * b["ret"]
            b["fc_prev"] = b["forecast"].shift(1)
            raw = b["debug_info.components.sma_cross_down.last_history_value"]
            b["raw_prev"] = raw.shift(1)
            b["raw_chg5"] = (raw - raw.shift(5)).shift(1)
            short = (b["forecast"] < 0).astype(int)
            grp = (short != short.shift()).cumsum()
            b["age"] = short.groupby(grp).cumcount().shift(1)
            b["fwd10"] = b["close"].shift(-10) / b["close"] - 1
            b["px_vs_sma50"] = (b["close"] / b["close"].rolling(50).mean() - 1).shift(1)
            b["coin"] = coin; b["w"] = w
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    act = B[(B["pos_prev"].abs() > 1e-9)].dropna(subset=["gross"]).copy()
    act["agebin"] = pd.cut(act["age"], [-1, 10, 30, 60, 120, 1e9])
    out["by_age"] = act.groupby("agebin").agg(n=("gross", "size"), gross=("gross", "mean"),
        coinret=("ret", "mean"), t=("gross", lambda s: s.mean()/s.std()*np.sqrt(len(s))))
    act["chg"] = np.where(act["raw_chg5"] < 0, "spread_widening", "spread_narrowing")
    out["by_spread_dir"] = act.groupby("chg").agg(n=("gross", "size"), gross=("gross", "mean"),
        coinret=("ret", "mean"))
    act["pxbin"] = np.where(act["px_vs_sma50"] < 0, "price_below_sma50", "price_above_sma50")
    out["by_px_vs_sma50"] = act.groupby("pxbin").agg(n=("gross", "size"), gross=("gross", "mean"),
        coinret=("ret", "mean"))
    act["rawbin"] = pd.qcut(act["raw_prev"], 4, labels=["deepest", "q2", "q3", "shallowest"])
    out["by_raw_spread"] = act.groupby("rawbin").agg(n=("gross", "size"), raw=("raw_prev", "mean"),
        fc=("fc_prev", "mean"), gross=("gross", "mean"))
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    T["efb"] = pd.qcut(T["entry_forecast"].abs(), 3, labels=["small", "mid", "large"], duplicates="drop")
    out["trades_by_entry_fc"] = T.groupby("efb").agg(n=("side", "size"),
        gross=("profit_loss_percent", "mean"), med=("profit_loss_percent", "median"),
        win=("profit_loss_percent", lambda s: (s > 0).mean()))
    out["trade_pl_dist"] = T["profit_loss_percent"].describe()
    return out
