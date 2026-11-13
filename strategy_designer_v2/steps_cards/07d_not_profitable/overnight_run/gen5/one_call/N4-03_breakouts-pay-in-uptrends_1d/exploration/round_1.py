def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    # trades
    tr = []
    for c, ws in data["trades"].items():
        for w, df in ws.items():
            if df is None or len(df) == 0: continue
            d = df.copy(); d["coin"] = c; d["win"] = w; tr.append(d)
    T = pd.concat(tr, ignore_index=True)
    T["days"] = T["duration_minutes"] / 1440
    g = T.groupby(["side", "entry_regime"]).agg(n=("side", "size"), days=("days", "mean"),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"),
        comm=("total_commission", "mean"), win=("profit_loss_percent", lambda x: (x > 0).mean()),
        gross_sum=("profit_loss_percent", "sum"), net_sum=("net_profit_loss_percent", "sum"))
    out["trades_by_side_regime"] = g
    out["trades_duration_quantiles"] = T["days"].quantile([.1, .25, .5, .75, .9])
    T["entry_abs"] = T["entry_forecast"].abs()
    T["fb"] = pd.cut(T["entry_abs"], [-0.01, 2, 5, 10, 15, 20.01])
    out["trades_by_entry_size"] = T.groupby("fb").agg(n=("side", "size"), gross=("profit_loss_percent", "mean"),
        net=("net_profit_loss_percent", "mean"), days=("days", "mean"))
    # bars-level
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            r = b["close"].pct_change()
            pos = b["postRebalance_current_allocation"].shift(1)
            v = b["postRebalance_total_value"]
            br = v.pct_change()
            vol = r.rolling(20).std()
            r10 = b["close"].shift(-10) / b["close"] - 1
            past20 = b["close"] / b["close"].shift(20) - 1
            d = pd.DataFrame({"coin": c, "win": w, "year": b["timestamp"].dt.year, "ret": r, "pos": pos,
                              "pnl": pos * r, "book": br, "regime": b["regime"].shift(1), "fc": b["forecast"],
                              "vol": vol, "r10": r10, "past20": past20, "i": np.arange(len(b))})
            rows.append(d)
    B = pd.concat(rows, ignore_index=True)
    B["turn"] = B.groupby(["coin", "win"])["pos"].diff().abs()
    out["book_by_regime"] = B.groupby("regime").agg(n=("book", "size"), book_mean=("book", "mean"),
        pnl_gross=("pnl", "mean"), coin_mean=("ret", "mean"), mean_pos=("pos", "mean"),
        active=("pos", lambda x: (x.abs() > 1e-6).mean()), turn=("turn", "mean"))
    B["side"] = np.sign(B["pos"]).map({1: "long", -1: "short", 0: "flat"})
    out["book_by_side"] = B.groupby("side").agg(n=("book", "size"), book_mean=("book", "mean"),
        pnl_gross=("pnl", "mean"), book_sum=("book", "sum"), pnl_sum=("pnl", "sum"))
    out["book_by_year"] = B.groupby("year").agg(book=("book", "mean"), pnl=("pnl", "mean"), coin=("ret", "mean"))
    out["book_by_coin"] = B.groupby("coin").agg(book=("book", "mean"), pnl=("pnl", "mean"), coin=("ret", "mean"))
    wb = B.groupby("win").agg(book=("book", "mean"), coin=("ret", "mean"))
    out["book_by_window"] = wb
    B["volt"] = B.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=["calm", "mid", "vol"]))
    out["by_vol_side"] = B.groupby(["volt", "side"]).agg(n=("book", "size"), book=("book", "mean"), pnl=("pnl", "mean"))
    # non-overlapping forecast buckets: signed fwd return
    G = B[B["i"] % 10 == 0].dropna(subset=["r10"]).copy()
    G["hold"] = G.groupby("coin")["r10"].transform("mean")
    G["fbk"] = pd.cut(G["fc"], [-20.01, -10, -2, -1e-9, 1e-9, 2, 10, 20.01])
    def tstat(x):
        return x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 else np.nan
    out["fwd10_by_fc_bucket"] = G.groupby("fbk").agg(n=("r10", "size"), r10=("r10", "mean"),
        ex=("r10", lambda x: np.nan), t=("r10", tstat))
    G["ex"] = G["r10"] - G["hold"]
    out["excess10_by_fc_bucket"] = G.groupby("fbk")["ex"].agg(["size", "mean", tstat])
    # market state: past 20d return sign for longs/shorts
    B["mkt"] = np.where(B["past20"] > 0, "up20", "down20")
    out["by_mkt_side"] = B.groupby(["mkt", "side"]).agg(n=("book", "size"), book=("book", "mean"), pnl=("pnl", "mean"))
    out["total_fee_vs_gross"] = pd.Series({"gross_sum_pct": T["profit_loss_percent"].sum(),
        "net_sum_pct": T["net_profit_loss_percent"].sum(), "n_trades": len(T),
        "mean_active_share": (B["pos"].abs() > 1e-6).mean(), "mean_abs_pos_active": B.loc[B["pos"].abs() > 1e-6, "pos"].abs().mean()})
    return out
