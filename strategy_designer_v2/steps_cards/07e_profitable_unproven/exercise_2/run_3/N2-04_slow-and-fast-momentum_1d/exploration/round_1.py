import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for c, wd in data["days"].items():
        for w, d in wd.items():
            b = data["bars"][c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            al = b.groupby("day")["postRebalance_current_allocation"].last()
            fc = b.groupby("day")["forecast"].last()
            dd = d.copy()
            dd["day"] = pd.to_datetime(dd["day"]).dt.floor("D")
            dd = dd.set_index("day")
            dd["alloc_prev"] = al.reindex(dd.index).shift(1)
            dd["fc_prev"] = fc.reindex(dd.index).shift(1)
            dd["coin"] = c; dd["window"] = w
            dd["year"] = dd.index.year
            rows.append(dd.reset_index())
    D = pd.concat(rows, ignore_index=True)
    D = D.dropna(subset=["book_return", "coin_return"])
    mu = D.groupby("coin")["coin_return"].mean()
    D["mkt_part"] = D["alloc_prev"] * D["coin"].map(mu)
    D["timing"] = D["book_return"] - D["mkt_part"]
    book = D.groupby(["window", "day"]).agg(br=("book_return", "mean"), mk=("mkt_part", "mean"),
                                           tm=("timing", "mean"), cr=("coin_return", "mean"), year=("year", "first"))
    out["book_decomp"] = pd.Series({"book_mean": book.br.mean(), "market_part": book.mk.mean(),
                                    "timing_part": book.tm.mean(), "hold_mean": book.cr.mean(),
                                    "sharpe": book.br.mean()/book.br.std()*np.sqrt(365), "n_days": len(book),
                                    "mean_alloc": D.alloc_prev.mean(), "share_days_in": (D.alloc_prev > 0).mean()})
    # per coin contribution (book = mean over coins => contribution = coin's sum / ndays /6)
    nd = len(book)
    pc = D.groupby("coin").agg(book_mean=("book_return", "mean"), mkt=("mkt_part", "mean"),
                               tim=("timing", "mean"), hold=("coin_return", "mean"))
    pc["contrib"] = D.groupby("coin")["book_return"].sum() / D.groupby(["window","day"]).ngroups / 6
    out["per_coin"] = pc
    pw = book.groupby(level="window").agg(br=("br", "mean"), mk=("mk", "mean"), tm=("tm", "mean"), cr=("cr", "mean"), n=("br", "size"))
    pw["sum_br"] = pw.br * pw.n
    out["per_window"] = pw
    out["per_year"] = book.groupby("year").agg(br=("br", "mean"), mk=("mk", "mean"), tm=("tm", "mean"), cr=("cr", "mean"), n=("br", "size"))
    # in-position days: coin return when in vs coin mean
    D["in"] = D.alloc_prev > 0
    g = D.groupby("in")["coin_return"].agg(["mean", "std", "count"])
    out["coin_ret_in_vs_out"] = g
    # trades concentration
    T = pd.concat([t.assign(coin=c) for c, wt in data["trades"].items() for t in wt.values()], ignore_index=True)
    p = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(T), "sum": p.sum(), "top10_sum": p.head(10).sum(), "top20_sum": p.head(20).sum(),
                               "win_rate": (p > 0).mean(), "median_dur_days": T.duration_minutes.median()/1440,
                               "mean_net": p.mean()})
    # forward returns at several horizons, active vs coin mean, non-overlapping
    res = []
    for h in [1, 5, 10, 20, 40]:
        ex_all, ex_q = [], []
        for c, wb in data["bars"].items():
            allr = []
            for w, b in wb.items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                r = cl[idx + h] / cl[idx] - 1
                allr.append(pd.DataFrame({"r": r, "f": b["forecast"].values[idx]}))
            A = pd.concat(allr); m = A.r.mean()
            A["ex"] = A.r - m; A["coin"] = c
            ex_all.append(A)
        A = pd.concat(ex_all)
        act = A[A.f > 0]; ina = A[A.f <= 0]
        t = act.ex.mean() / (act.ex.std() / np.sqrt(len(act)))
        tw = stats.ttest_ind(act.ex, ina.ex, equal_var=False).statistic
        res.append({"h": h, "act_ex": act.ex.mean(), "t_act": t, "n_act": len(act),
                    "inact_ex": ina.ex.mean(), "t_act_minus_inact": tw, "n_inact": len(ina)})
    out["horizons"] = pd.DataFrame(res)
    return out
