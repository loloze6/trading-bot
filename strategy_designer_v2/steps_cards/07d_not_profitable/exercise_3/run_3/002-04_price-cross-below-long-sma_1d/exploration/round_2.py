def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values.astype(float)
            n = len(b)
            col = "debug_info.components.below_ma.last_history_value"
            dist = b[col].values.astype(float) if col in b else np.full(n, np.nan)
            alloc = b["postRebalance_current_allocation"].values.astype(float)
            val = b["postRebalance_total_value"].values.astype(float)
            sma = cl / (1 + dist / 100)
            for t in range(20, n - 1):
                r1 = cl[t + 1] / cl[t] - 1
                gross = alloc[t] * r1
                book = val[t + 1] / val[t] - 1
                rows.append(dict(coin=c, win=w, alloc=alloc[t], dist=dist[t],
                                 mom20=cl[t] / cl[t - 20] - 1,
                                 mom5=cl[t] / cl[t - 5] - 1,
                                 slope=sma[t] / sma[t - 20] - 1,
                                 vol=np.std(np.diff(np.log(cl[t - 20:t + 1]))),
                                 gross=gross, book=book, fee=gross - book,
                                 year=pd.Timestamp(b["timestamp"].iloc[t]).year))
    df = pd.DataFrame(rows)
    act = df[df.alloc < 0].copy()
    out = {}
    out["totals daily"] = pd.Series(dict(n_all=len(df), n_short=len(act), mean_book_all=df.book.mean(),
        mean_gross_all=df.gross.mean(), mean_fee_all=df.fee.mean(),
        sharpe_gross=df.gross.mean()/df.gross.std()*np.sqrt(365), sharpe_book=df.book.mean()/df.book.std()*np.sqrt(365)))
    def g(x):
        return pd.Series(dict(n=len(x), mean_book=x.book.mean(), t_book=x.book.mean()/(x.book.std()/np.sqrt(len(x))),
                              mean_gross=x.gross.mean(), sum_book=x.book.sum(), mean_alloc=x.alloc.mean()))
    act["mom20q"] = pd.qcut(act.mom20, 5, labels=False)
    out["short days by mom20 quintile"] = act.groupby("mom20q").apply(g)
    act["mom5q"] = pd.qcut(act.mom5, 5, labels=False)
    out["short days by mom5 quintile"] = act.groupby("mom5q").apply(g)
    act["distq"] = pd.qcut(act.dist, 5, labels=False)
    out["short days by dist quintile"] = act.groupby("distq").apply(g)
    act["volq"] = pd.qcut(act.vol, 5, labels=False)
    out["short days by vol quintile"] = act.groupby("volq").apply(g)
    act["slope_neg"] = act.slope < 0
    act["mom_neg"] = act.mom20 < 0
    out["short days slope x mom20 sign"] = act.groupby(["slope_neg", "mom_neg"]).apply(g)
    # graded: correlation of dist and mom20 with gross gain
    out["corr gross vs"] = pd.Series(dict(dist=stats.spearmanr(act.dist, act.gross)[0],
        mom20=stats.spearmanr(act.mom20, act.gross)[0], mom5=stats.spearmanr(act.mom5, act.gross)[0]))
    # share of loss in worst 5% days
    q = act.book.quantile(0.05)
    worst = act[act.book <= q]
    out["worst 5% short days state"] = pd.Series(dict(n=len(worst), sum_book=worst.book.sum(),
        total_short_sum=act.book.sum(), mean_mom20=worst.mom20.mean(), all_mean_mom20=act.mom20.mean(),
        mean_dist=worst.dist.mean(), all_mean_dist=act.dist.mean(), mean_vol=worst.vol.mean(), all_vol=act.vol.mean()))
    return out
