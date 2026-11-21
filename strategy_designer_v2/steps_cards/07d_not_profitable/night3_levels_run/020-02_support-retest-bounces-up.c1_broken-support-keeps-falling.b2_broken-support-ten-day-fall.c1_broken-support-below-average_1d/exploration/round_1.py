def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    H = 10
    rows = []
    drift = {}
    usual = {}
    for c in bars:
        rets = []
        for w, df in bars[c].items():
            cl = df["close"].values
            for i in range(0, len(cl) - H, H):
                rets.append(cl[i + H] / cl[i] - 1)
        drift[c] = np.mean(rets); usual[c] = np.std(rets)
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"]
            sma = cl.rolling(50, min_periods=20).mean()
            r30 = cl / cl.shift(30) - 1
            r90 = cl / cl.shift(90) - 1
            hi90 = df["high"].rolling(90, min_periods=20).max()
            lo90 = df["low"].rolling(90, min_periods=20).min()
            vol = cl.pct_change().rolling(30, min_periods=10).std()
            raw = df.get("debug_info.components.support_cluster.last_history_value")
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for i in range(0, len(df) - H, H):
                fwd = cl[i + H] / cl[i] - 1
                rows.append(dict(coin=c, win=w, year=yr[i], f=df["forecast"][i],
                                 alloc=df["postRebalance_current_allocation"][i],
                                 raw=raw[i] if raw is not None else np.nan,
                                 dsma=cl[i] / sma[i] - 1 if sma[i] == sma[i] else np.nan,
                                 r30=r30[i], r90=r90[i],
                                 pos=(cl[i] - lo90[i]) / (hi90[i] - lo90[i]) if hi90[i] > lo90[i] else np.nan,
                                 vol=vol[i],
                                 fwd=fwd, un_short=-(fwd - drift[c]), tot_short=-fwd))
    g = pd.DataFrame(rows)
    out = {}
    out["forecast_dist_cases"] = g[g.f < 0]["f"].describe()
    cs = g[g.f <= -2].copy()
    def summ(x):
        return pd.Series({"n": len(x), "unusual_short_mean": x.un_short.mean(),
                          "total_short_mean": x.tot_short.mean(),
                          "t_unusual": stats.ttest_1samp(x.un_short, 0).statistic if len(x) > 2 else np.nan})
    out["cases_all"] = summ(cs)
    out["by_year"] = cs.groupby("year").apply(summ)
    out["by_coin"] = cs.groupby("coin").apply(summ)
    for col in ["raw", "dsma", "r30", "r90", "pos", "vol"]:
        try:
            cs[col + "_q"] = pd.qcut(cs[col], 4, labels=False, duplicates="drop")
            out["by_" + col + "_quartile"] = cs.groupby(col + "_q").apply(
                lambda x: pd.concat([summ(x), pd.Series({"mean_" + col: x[col].mean()})]))
        except Exception as e:
            out["err_" + col] = str(e)
    # below-sma bars without cluster, for comparison
    nb = g[(g.dsma < 0) & (g.f == 0)]
    out["below_sma_no_signal"] = summ(nb)
    # book daily returns: market vs timing
    br = []
    for c in days:
        for w, d in days[c].items():
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            al = b.groupby("day")["postRebalance_current_allocation"].last()
            dd = d.copy(); dd["day"] = pd.to_datetime(dd["day"])
            dd = dd.set_index("day")
            dd["alloc_prev"] = al.reindex(dd.index).shift(1)
            dd["coin"] = c; dd["win"] = w
            br.append(dd)
    B = pd.concat(br)
    md = B.groupby("coin")["coin_return"].mean()
    B["mkt"] = B["alloc_prev"] * B["coin"].map(md)
    B["gross"] = B["alloc_prev"] * B["coin_return"]
    out["book_parts_mean_daily"] = pd.Series({"book": B.book_return.mean(), "gross_pos_x_ret": B.gross.mean(),
                                               "market_part": B.mkt.mean(),
                                               "timing": B.gross.mean() - B.mkt.mean(),
                                               "cost_drag": B.book_return.mean() - B.gross.mean(),
                                               "share_days_in": (B.alloc_prev.abs() > 1e-6).mean(),
                                               "mean_abs_alloc_when_in": B.alloc_prev[B.alloc_prev.abs() > 1e-6].abs().mean()})
    B["year"] = B.index.year
    out["book_by_year"] = B.groupby("year").agg(book=("book_return", "mean"), coin=("coin_return", "mean"),
                                               timing=("gross", "mean"))
    return out
