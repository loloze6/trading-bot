def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    # ---- per window book vs coin
    rows = []
    dayrows = []
    for c in days:
        for w, d in days[c].items():
            d = d.copy(); d["coin"] = c; d["window"] = w
            dayrows.append(d)
    D = pd.concat(dayrows)
    D["wnum"] = D["window"].str[1:].astype(int)
    port = D.groupby(["wnum", "day"]).agg(book=("book_return", "mean"), coin=("coin_return", "mean")).dropna().reset_index()
    port = port.sort_values(["wnum", "day"])
    pw = port.groupby("wnum").agg(book_sum=("book", "sum"), coin_sum=("coin", "sum"), n=("book", "size"))
    out["per_window_book_vs_coin"] = pw
    # drawdown of chained book
    v = (1 + port["book"]).cumprod().values
    peak = np.maximum.accumulate(v); dd = v / peak - 1
    port["dd"] = dd
    port["v"] = v
    i_min = int(np.argmin(dd)); i_peak = int(np.argmax(v[:i_min + 1]))
    seg = port.iloc[i_peak:i_min + 1]
    out["deepest_fall"] = pd.Series({"depth": dd[i_min], "days": len(seg), "windows": ",".join(map(str, sorted(seg.wnum.unique()))),
                                     "coin_mean_ret_sum_during": seg.coin.sum()})
    # dd by window min
    out["min_dd_by_window"] = port.groupby("wnum")["dd"].min()
    # ---- per coin bar features, grid cases
    feats = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True).copy()
            cl = b["close"]; vol = b["volume"]
            b["fwd5"] = cl.shift(-5) / cl - 1
            b["past5"] = cl / cl.shift(5) - 1
            b["past30"] = cl / cl.shift(30) - 1
            b["past60"] = cl / cl.shift(60) - 1
            lr = np.log(cl).diff()
            b["vol10"] = lr.rolling(10).std()
            b["vol30"] = lr.rolling(30).std()
            b["low30dist"] = cl / cl.rolling(30).min() - 1
            b["vr"] = np.log(vol.rolling(30).mean() / vol.shift(30).rolling(30).mean())
            b["vr5"] = np.log(vol.rolling(5).mean() / vol.rolling(30).mean())
            b["pos"] = np.arange(len(b))
            b["grid"] = b["pos"] % 5 == 0
            b["coin"] = c; b["window"] = w
            b["pnl_next"] = b["postRebalance_current_allocation"] * (cl.shift(-1) / cl - 1)
            feats.append(b)
    F = pd.concat(feats, ignore_index=True)
    drift = F[F.grid]["fwd5"].mean()
    out["drift5"] = drift
    F["short_unusual"] = -(F["fwd5"] - drift)
    F["short_total"] = -F["fwd5"]
    G = F[F.grid & F.fwd5.notna()]
    mr = G[G.regime == "mean_reversion"].copy()
    mr["sig"] = mr["forecast"] < 0
    def summ(x):
        return pd.Series({"n": len(x), "unusual": x.short_unusual.mean(), "total": x.short_total.mean(),
                          "t": stats.ttest_1samp(x.short_unusual, 0).statistic if len(x) > 2 else np.nan})
    out["mr_grid_signal_vs_not"] = mr.groupby("sig").apply(summ)
    out["regime_counts_grid"] = G.groupby("regime").apply(summ)
    S = mr[mr.sig].copy()
    for col in ["past5", "past30", "low30dist", "vol10", "vr5", "forecast"]:
        q = pd.qcut(S[col], 3, labels=["lo", "mid", "hi"], duplicates="drop")
        out[f"sig_by_{col}"] = S.groupby(q).apply(summ)
        qn = pd.qcut(mr[~mr.sig][col].dropna(), 3, labels=["lo", "mid", "hi"], duplicates="drop") if col != "forecast" else None
        if qn is not None:
            out[f"nosig_by_{col}"] = mr[~mr.sig].loc[qn.index].groupby(qn).apply(summ)
    out["sig_by_window"] = S.groupby(S.window.str[1:].astype(int)).apply(summ)
    out["sig_by_coin"] = S.groupby("coin").apply(summ)
    # book pnl by bar features (in position bars)
    P = F[F.postRebalance_current_allocation.abs() > 0].dropna(subset=["pnl_next"])
    out["inpos_pnl_by_past5"] = P.groupby(pd.qcut(P.past5, 4))["pnl_next"].agg(["count", "mean", "sum"])
    out["inpos_pnl_by_low30dist"] = P.groupby(pd.qcut(P.low30dist, 4))["pnl_next"].agg(["count", "mean", "sum"])
    # trades
    T = []
    for c in trades:
        for w, t in trades[c].items():
            t = t.copy(); t["coin"] = c; t["window"] = w; T.append(t)
    T = pd.concat(T, ignore_index=True)
    T["days"] = T.duration_minutes / 1440
    out["trades_summary"] = T.groupby("side").agg(n=("net_profit_loss_percent", "size"), gross=("profit_loss_percent", "mean"),
                                                 net=("net_profit_loss_percent", "mean"), med=("net_profit_loss_percent", "median"),
                                                 days=("days", "mean"), win=("net_profit_loss_percent", lambda x: (x > 0).mean()))
    out["trades_by_duration"] = T.groupby(pd.cut(T.days, [0, 5.5, 10, 20, 1000]))["net_profit_loss_percent"].agg(["count", "mean", "sum"])
    out["trades_by_entry_forecast"] = T.groupby(pd.qcut(T.entry_forecast, 3, duplicates="drop"))["net_profit_loss_percent"].agg(["count", "mean", "sum"])
    out["worst_trades_by_exit_regime_reason"] = T.nsmallest(10, "net_profit_loss_percent")[["coin", "window", "days", "net_profit_loss_percent", "entry_forecast", "exit_forecast"]].reset_index(drop=True)
    return out
