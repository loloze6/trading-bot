def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # ---- book daily returns, pooled ----
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["window"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["window"].str[1:].astype(int)
    P = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().reset_index().sort_values(["wn", "day"])
    P = P.dropna()
    def sh(x): return x.mean() / x.std() * np.sqrt(365)
    out["pooled"] = pd.Series({"book_mean": P.book_return.mean(), "book_sharpe": sh(P.book_return),
                               "hold_mean": P.coin_return.mean(), "hold_sharpe": sh(P.coin_return),
                               "days": len(P)})
    eq = (1 + P.book_return).cumprod().values
    peak = np.maximum.accumulate(eq); dd = eq / peak - 1
    i = dd.argmin(); j = eq[:i + 1].argmax()
    out["deepest_fall"] = pd.Series({"depth": dd[i], "peak_window": P.wn.iloc[j], "trough_window": P.wn.iloc[i],
                                     "days_long": i - j})
    pw = P.groupby("wn").agg(book_sum=("book_return", "sum"), hold_sum=("coin_return", "sum"),
                             book_sh=("book_return", sh), n=("book_return", "size"))
    out["per_window"] = pw
    # ---- exposure and entries ----
    ents = []; expo = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            cl = b["close"].values; al = b["postRebalance_current_allocation"].fillna(0).values
            fc = b["forecast"].fillna(0).values
            n = len(cl)
            expo.append(pd.Series({"in_share": (al > 0).mean(), "mean_alloc_in": al[al > 0].mean() if (al > 0).any() else np.nan}))
            prev = np.r_[0, al[:-1]]
            idx = np.where((al > 0) & (prev <= 0))[0]
            for k in idx:
                if k + 48 >= n: continue
                r48 = cl[k + 48] / cl[k] - 1
                p720 = cl[k] / cl[k - 720] - 1 if k >= 720 else np.nan
                p168 = cl[k] / cl[k - 168] - 1 if k >= 168 else np.nan
                p24 = cl[k] / cl[k - 24] - 1 if k >= 24 else np.nan
                # drawdown within 48 bars
                mn = cl[k:k + 49].min() / cl[k] - 1
                ents.append((c, w, r48, p720, p168, p24, fc[k], al[k], mn))
    E = pd.DataFrame(ents, columns=["coin", "w", "r48", "p720", "p168", "p24", "fc", "al", "min48"])
    out["exposure"] = pd.concat(expo, axis=1).T.mean()
    out["entries_n"] = len(E)
    def summ(g):
        return pd.Series({"n": len(g), "r48": g.r48.mean(), "t": g.r48.mean() / g.r48.std() * np.sqrt(len(g)),
                          "min48": g.min48.mean(), "alloc": g.al.mean()})
    E["fc_q"] = pd.qcut(E.fc.rank(method="first"), 5, labels=False)
    out["by_forecast_q"] = E.groupby("fc_q").apply(summ)
    E["p720_q"] = pd.qcut(E.p720.rank(method="first"), 5, labels=False)
    out["by_prior30d_q"] = E.dropna(subset=["p720"]).groupby("p720_q").apply(summ)
    out["p720_q_edges"] = E.groupby("p720_q").p720.agg(["min", "max"])
    E["p168_q"] = pd.qcut(E.p168.rank(method="first"), 5, labels=False)
    out["by_prior7d_q"] = E.dropna(subset=["p168"]).groupby("p168_q").apply(summ)
    out["by_coin"] = E.groupby("coin").apply(summ)
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items() if len(t)])
    T["dur_h"] = T.duration_minutes / 60
    out["trades"] = pd.Series({"n": len(T), "gross": T.profit_loss_percent.mean(), "net": T.net_profit_loss_percent.mean(),
                               "win": (T.net_profit_loss_percent > 0).mean(), "dur_h_median": T.dur_h.median(),
                               "dur_h_mean": T.dur_h.mean()})
    return out
