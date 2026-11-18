def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # Book daily returns: mean across coins per (window, day)
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = c; d["w"] = w
            rows.append(d)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    port = D.groupby(["wn", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).dropna().sort_index()
    eq = (1 + port["br"]).cumprod()
    dd = eq / eq.cummax() - 1
    out["port_mean_sd_n"] = pd.Series({"mean": port.br.mean(), "sd": port.br.std(), "n": len(port), "maxdd": dd.min(), "hold_mean": port.cr.mean()})
    out["port_by_window"] = port.groupby(level=0).agg(book=("br", "sum"), hold=("cr", "sum"))
    # Per bar: position, gain, context
    recs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            b["r1"] = b.close.shift(-1) / b.close - 1
            b["gain"] = b.postRebalance_current_allocation * b.r1
            b["ret20"] = b.close / b.close.shift(20) - 1
            b["ret60"] = b.close / b.close.shift(60) - 1
            b["ma50dist"] = b.close / b.close.rolling(50).mean() - 1
            b["fee"] = (b.total_portfolio_value - b.postRebalance_total_value) / b.total_portfolio_value
            b["coin"] = c; b["w"] = w
            recs.append(b)
    B = pd.concat(recs)
    B["inpos"] = B.postRebalance_current_allocation.abs() > 1e-9
    out["share_bars_in_pos"] = B.inpos.mean()
    out["mean_alloc_when_in"] = B.loc[B.inpos, "postRebalance_current_allocation"].mean()
    out["gross_gain_per_bar"] = B.gain.mean()
    out["fee_per_bar"] = B.fee.mean()
    I = B[B.inpos].dropna(subset=["gain", "ret60"])
    I["trend60"] = pd.qcut(I.ret60, 5, labels=False)
    out["gain_by_ret60_quintile"] = I.groupby("trend60").agg(n=("gain", "size"), mean_gain=("gain", "mean"), mean_r1=("r1", "mean"), ret60_mid=("ret60", "median"))
    I["above50"] = I.ma50dist > 0
    g = I.groupby("above50")
    out["gain_by_above_ma50"] = g.agg(n=("gain", "size"), mean_gain=("gain", "mean"), mean_r1=("r1", "mean"))
    out["by_coin"] = B.groupby("coin").agg(gain=("gain", "mean"), fee=("fee", "mean"), inpos=("inpos", "mean"))
    # Trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items()])
    T["days"] = T.duration_minutes / 1440
    out["trades"] = pd.Series({"n": len(T), "mean_net": T.net_profit_loss_percent.mean(), "mean_gross": T.profit_loss_percent.mean(),
                               "median_days": T.days.median(), "win": (T.net_profit_loss_percent > 0).mean()})
    T["dur_b"] = pd.cut(T.days, [0, 1.5, 3.5, 7.5, 1000])
    out["trades_by_dur"] = T.groupby("dur_b").agg(n=("days", "size"), net=("net_profit_loss_percent", "mean"))
    # Hold-days profile after entry: gain by bars since position opened
    B["entry"] = B.inpos & ~(B.previous_allocation.abs() > 1e-9)
    B["grp"] = B.groupby(["coin", "w"]).entry.cumsum()
    B["k"] = B[B.inpos].groupby(["coin", "w", "grp"]).cumcount()
    out["gain_by_bar_since_entry"] = B[B.inpos].groupby(B.k.clip(upper=6)).agg(n=("gain", "size"), mean_gain=("gain", "mean"), mean_r1=("r1", "mean"))
    # worst 20 days of portfolio: share explained by ret60 state
    return out
