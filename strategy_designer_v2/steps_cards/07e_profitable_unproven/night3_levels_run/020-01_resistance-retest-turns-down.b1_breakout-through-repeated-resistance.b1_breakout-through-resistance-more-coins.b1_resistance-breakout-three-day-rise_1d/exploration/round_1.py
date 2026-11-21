def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
    ev = []
    trades = []
    for coin, wins in data["bars"].items():
        # coin drift (daily) over all windows
        dr = pd.concat([data["days"][coin][w]["coin_return"] for w in wins]).dropna()
        drift = dr.mean()
        # h-day drift, non-overlapping
        drifts = {}
        for h in [1,3,5,10,20]:
            xs = []
            for w, b in wins.items():
                c = b["close"].values
                for i in range(0, len(c)-h, h):
                    xs.append(c[i+h]/c[i]-1)
            drifts[h] = np.mean(xs)
        for w, b in wins.items():
            d = data["days"][coin][w].copy()
            b = b.reset_index(drop=True)
            al = b["postRebalance_current_allocation"].values
            n = min(len(d), len(b))
            d = d.iloc[:n].copy()
            d["alloc_prev"] = np.r_[np.nan, al[:n-1]]
            d["coin"] = coin; d["window"] = w
            d["year"] = pd.to_datetime(d["day"]).dt.year
            d["drift"] = drift
            # prior 30d return for state
            c = b["close"].values
            p30 = pd.Series(c).pct_change(30).values
            d["p30_prev"] = np.r_[np.nan, p30[:n-1]]
            rows.append(d)
            f = b["forecast"].fillna(0).values
            raw = b.get("debug_info.components.res_break.last_history_value")
            raw = raw.values if raw is not None else np.full(len(b), np.nan)
            for i in range(1, len(b)):
                if f[i] > 0 and f[i-1] <= 0:
                    r = {"coin": coin, "window": w, "f": f[i], "raw": raw[i], "p30": p30[i],
                         "hi90": c[i] >= np.max(c[max(0,i-90):i+1])}
                    for h in [1,3,5,10,20]:
                        if i+h < len(c):
                            r[f"x{h}"] = c[i+h]/c[i]-1 - drifts[h]
                            r[f"t{h}"] = c[i+h]/c[i]-1
                    ev.append(r)
        for w, t in data["trades"][coin].items():
            if t is not None and len(t):
                tt = t.copy(); tt["coin"] = coin; tt["window"] = w; trades.append(tt)
    D = pd.concat(rows)
    D = D.dropna(subset=["book_return"])
    D["mkt"] = D["alloc_prev"] * D["drift"]
    D["hold"] = D["coin_return"]
    day = D.groupby("day").agg(book=("book_return","mean"), mkt=("mkt","mean"), hold=("hold","mean"),
                               window=("window","first"), year=("year","first"))
    out["book_decomp"] = pd.Series({"book_mean": day.book.mean(), "market_part": day.mkt.mean(),
                                    "timing": day.book.mean()-day.mkt.mean(), "hold_mean": day.hold.mean(),
                                    "mean_alloc": D.alloc_prev.mean(), "share_days_in": (D.alloc_prev.abs()>1e-6).mean(),
                                    "n_days": len(day)})
    pc = D.groupby("coin").agg(book_sum=("book_return","sum"), mkt_sum=("mkt","sum"), hold_mean=("hold","mean"), n=("book_return","size"))
    pc["share_of_total_book"] = pc.book_sum / pc.book_sum.sum()
    out["per_coin"] = pc.sort_values("book_sum", ascending=False)
    pw = day.groupby("window").agg(book=("book","mean"), mkt=("mkt","mean"), hold=("hold","mean"), n=("book","size"))
    pw["book_sum_share"] = day.groupby("window").book.sum()/day.book.sum()
    out["per_window"] = pw
    out["per_year"] = day.groupby("year").agg(book=("book","mean"), mkt=("mkt","mean"), hold=("hold","mean"), n=("book","size"))
    # state: coin prior 30d return terciles, book return when in
    Din = D[D.alloc_prev.abs()>1e-6].dropna(subset=["p30_prev"]).copy()
    Din["p30q"] = pd.qcut(Din.p30_prev, 4, labels=False)
    out["book_by_prior30_quartile_when_in"] = Din.groupby("p30q").agg(book=("book_return","mean"), coin=("coin_return","mean"), p30=("p30_prev","mean"), n=("book_return","size"))
    E = pd.DataFrame(ev)
    res = {}
    for h in [1,3,5,10,20]:
        x = E[f"x{h}"].dropna(); t = E[f"t{h}"].dropna()
        res[h] = {"n": len(x), "excess": x.mean(), "t_excess": x.mean()/(x.std()/np.sqrt(len(x))), "total": t.mean()}
    out["events_by_horizon"] = pd.DataFrame(res).T
    E["p30q"] = pd.qcut(E.p30, 4, labels=False)
    out["events_by_p30q"] = E.groupby("p30q").agg(p30=("p30","mean"), x3=("x3","mean"), x10=("x10","mean"), x20=("x20","mean"), n=("x10","count"))
    E["rawq"] = pd.qcut(E.raw.rank(method="first"), 4, labels=False)
    out["events_by_rawq"] = E.groupby("rawq").agg(raw=("raw","mean"), x3=("x3","mean"), x10=("x10","mean"), x20=("x20","mean"), n=("x10","count"))
    out["events_by_hi90"] = E.groupby("hi90").agg(x3=("x3","mean"), x10=("x10","mean"), x20=("x20","mean"), n=("x10","count"))
    T = pd.concat(trades)
    pl = T.net_profit_loss_percent
    s = pl.sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(T), "mean_net": pl.mean(), "median_net": pl.median(), "win": (pl>0).mean(),
                               "top10_share_of_sum": s.head(10).sum()/pl.sum(), "top1pct_share": s.head(max(1,len(s)//100)).sum()/pl.sum(),
                               "sum_net": pl.sum(), "mean_days": T.duration_minutes.mean()/1440, "median_days": T.duration_minutes.median()/1440})
    return out
