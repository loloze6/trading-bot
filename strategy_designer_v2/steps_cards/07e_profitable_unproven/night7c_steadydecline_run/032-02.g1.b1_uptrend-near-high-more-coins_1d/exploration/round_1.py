def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # --- book daily returns, market part vs timing
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            b = data["bars"][c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            pos = b.groupby("day")["postRebalance_current_allocation"].last()
            dd = d.copy(); dd["day"] = pd.to_datetime(dd["day"]).dt.floor("D")
            dd["pos_prev"] = dd["day"].map(pos).shift(1)
            dd["coin"] = c; dd["win"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D = D.dropna(subset=["book_return", "coin_return"])
    cm = D.groupby("coin")["coin_return"].mean()
    D["mkt"] = D["pos_prev"].fillna(0) * D["coin"].map(cm)
    daily = D.groupby(["win", "day"]).agg(book=("book_return", "mean"), mkt=("mkt", "mean"), hold=("coin_return", "mean"))
    out["book_decomp"] = pd.Series({"book_mean": daily.book.mean(), "mkt_part": daily.mkt.mean(),
                                    "timing": daily.book.mean() - daily.mkt.mean(), "hold_mean": daily.hold.mean(),
                                    "book_sharpe": daily.book.mean() / daily.book.std() * np.sqrt(365),
                                    "t_book": daily.book.mean() / (daily.book.std() / np.sqrt(len(daily))), "ndays": len(daily)})
    bywin = daily.groupby("win").agg(book=("book", "mean"), mkt=("mkt", "mean"), hold=("hold", "mean"), n=("book", "size"))
    out["by_window"] = bywin
    pc = D.groupby("coin").agg(book_sum=("book_return", "sum"), mkt_sum=("mkt", "sum"), coin_mean=("coin_return", "mean"), n=("book_return", "size"))
    out["by_coin"] = pc
    # --- forward returns on grid, in/out regime, by horizon, by proximity thirds
    recs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            cl = b["close"].values; n = len(cl)
            r28 = pd.Series(cl).pct_change(28).values
            hi28 = pd.Series(cl).rolling(28, min_periods=28).max().values
            prox = cl / hi28
            r28r = pd.Series(cl).pct_change(28).values
            for h in (1, 5, 10, 20):
                for i in range(0, n - h, h):
                    recs.append((c, w, h, i, cl[i + h] / cl[i] - 1, b["regime"].iloc[i], r28[i], prox[i], b["forecast"].iloc[i]))
    R = pd.DataFrame(recs, columns=["coin", "win", "h", "i", "ret", "regime", "r28", "prox", "fc"])
    R["drift"] = R.groupby(["coin", "h"])["ret"].transform("mean")
    R["ex"] = R["ret"] - R["drift"]
    def tt(x):
        x = x.dropna(); return pd.Series({"mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan, "n": len(x)})
    R["inreg"] = R["regime"] == "trending"
    out["ex_by_h_regime"] = R.groupby(["h", "inreg"])["ex"].apply(tt).unstack()
    # graded by r28 quintile within trending, h=5 and 20
    T = R[R.inreg].copy()
    T["r28q"] = T.groupby("h")["r28"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["ex_by_r28q_trend"] = T.groupby(["h", "r28q"])["ex"].mean().unstack()
    T["proxq"] = T.groupby("h")["prox"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["ex_by_proxq_trend"] = T.groupby(["h", "proxq"])["ex"].mean().unstack()
    # all bars r28 quintiles (incl negative)
    A = R.dropna(subset=["r28"]).copy()
    A["r28q"] = A.groupby("h")["r28"].transform(lambda s: pd.qcut(s, 6, labels=False, duplicates="drop"))
    out["ex_by_r28sext_all"] = A.groupby(["h", "r28q"])["ex"].mean().unstack()
    out["corr_r28_ex"] = A.groupby("h").apply(lambda g: pd.Series({"spearman": stats.spearmanr(g.r28, g.ex)[0], "n": len(g)}))
    # trades
    tr = pd.concat([t.assign(coin=c, win=w) for c, ws in data["trades"].items() for w, t in ws.items() if len(t)])
    trn = tr["net_profit_loss_percent"]
    out["trades"] = pd.Series({"n": len(tr), "mean": trn.mean(), "median": trn.median(), "win_share": (trn > 0).mean(),
                               "top10_share_of_sum": trn.nlargest(10).sum() / trn.sum(), "sum": trn.sum(),
                               "mean_days": tr.duration_minutes.mean() / 1440})
    return out
