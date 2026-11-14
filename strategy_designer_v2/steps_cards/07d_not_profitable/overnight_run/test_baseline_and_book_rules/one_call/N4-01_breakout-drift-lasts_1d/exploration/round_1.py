def explore(data):
    import pandas as pd, numpy as np
    out = {}
    # book daily returns
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            t = d[["day", "book_return", "coin_return"]].copy()
            t["coin"] = c; t["w"] = w
            rows.append(t)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    book = D.groupby(["wn", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index().dropna()
    book["year"] = pd.to_datetime(book["day"]).dt.year
    # drawdown per window chain (compounded in order)
    eq = (1 + book.sort_values(["wn", "day"])["br"]).cumprod()
    dd = eq / eq.cummax() - 1
    out["book_overall"] = pd.Series({"mean": book.br.mean(), "sd": book.br.std(), "n": len(book),
                                     "maxDD_chained": dd.min(), "ann_ret": book.br.mean() * 365})
    gw = book.groupby("wn").agg(mean=("br", "mean"), sum=("br", "sum"), cr=("cr", "sum"), n=("br", "size"))
    gw["minDD"] = book.groupby("wn")["br"].apply(lambda s: ((1 + s).cumprod() / (1 + s).cumprod().cummax() - 1).min())
    out["by_window"] = gw.round(4)
    out["by_year"] = book.groupby("year").agg(mean=("br", "mean"), sum=("br", "sum"), cr=("cr", "sum")).round(4)
    # market state: coin-average up vs down day, and volatility tercile
    book["mkt_up"] = book.cr > 0
    out["by_mkt_updown"] = book.groupby("mkt_up")["br"].agg(["mean", "sum", "size"]).round(5)
    # per-coin contributions
    out["by_coin"] = D.groupby("coin")["book_return"].agg(["mean", "sum", "std"]).round(5)
    # trades
    tr = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t) == 0: continue
            t = t.copy(); t["coin"] = c; t["w"] = w; tr.append(t)
    T = pd.concat(tr)
    T["days"] = T.duration_minutes / 1440
    out["trades_summary"] = T.groupby("side").agg(n=("days", "size"), hold_mean=("days", "mean"), hold_med=("days", "median"),
                                                gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"),
                                                comm=("total_commission", "mean"), win=("profit_loss_percent", lambda s: (s > 0).mean())).round(4)
    T["hb"] = pd.cut(T.days, [0, 1.5, 3.5, 7.5, 15, 1e4])
    out["trades_by_hold"] = T.groupby("hb").agg(n=("days", "size"), gross=("profit_loss_percent", "mean"),
                                               net=("net_profit_loss_percent", "mean"), sum_net=("net_profit_loss_percent", "sum")).round(3)
    T["ef"] = pd.cut(T.entry_forecast.abs(), [0, 5, 10, 15, 20.01])
    out["trades_by_entry_fc"] = T.groupby("ef").agg(n=("days", "size"), gross=("profit_loss_percent", "mean"),
                                                   net=("net_profit_loss_percent", "mean")).round(3)
    # bars: forecast vs next-bar return
    br = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy(); b["nr"] = b.close.shift(-1) / b.close - 1; b["coin"] = c; b["w"] = w
            br.append(b[["forecast", "nr", "regime", "coin", "w", "postRebalance_current_allocation"]])
    B = pd.concat(br).dropna(subset=["nr"])
    B["fb"] = pd.cut(B.forecast, [-21, -0.01, 0.01, 5, 10, 15, 20.01])
    out["fc_bucket_nextret"] = B.groupby("fb")["nr"].agg(["mean", "size"]).round(5)
    out["regime_counts"] = B.groupby("regime").agg(n=("nr", "size"), active=("forecast", lambda s: (s != 0).mean()))
    out["share_active"] = float((B.forecast != 0).mean())
    return out
