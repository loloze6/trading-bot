def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    # book daily returns
    rows = []
    for c in days:
        for w, d in days[c].items():
            b = bars[c][w]
            alloc = b["postRebalance_current_allocation"].shift(1).values
            dd = d.copy()
            dd["coin"] = c; dd["w"] = w
            dd["pos_prev"] = alloc[:len(dd)] if len(alloc) == len(dd) else np.nan
            rows.append(dd)
    D = pd.concat(rows)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    mu = D.groupby("coin")["coin_return"].mean()
    D["mkt_part"] = D["pos_prev"] * D["coin"].map(mu)
    bk = D.groupby(["w", "day"]).agg(book=("book_return", "mean"), hold=("coin_return", "mean"), mkt=("mkt_part", "mean"), year=("year", "first")).dropna()
    out["book_summary"] = pd.Series({"mean_daily": bk.book.mean(), "mkt_part": bk.mkt.mean(), "timing": bk.book.mean() - bk.mkt.mean(),
                                     "sharpe": bk.book.mean() / bk.book.std() * np.sqrt(365), "hold_sharpe": bk.hold.mean() / bk.hold.std() * np.sqrt(365), "n_days": len(bk)})
    out["book_by_window"] = bk.groupby("w").agg(book_sum=("book", "sum"), hold_sum=("hold", "sum"), n=("book", "size"))
    out["book_by_year"] = bk.groupby("year").agg(book_sum=("book", "sum"), hold_sum=("hold", "sum"))
    pc = D.groupby("coin").agg(book_ret_sum=("book_return", "sum"), mkt=("mkt_part", "sum"), share_in=("pos_prev", lambda x: (x.abs() > 1e-9).mean()))
    out["by_coin"] = pc
    # trades
    T = []
    for c in trades:
        for w, t in trades[c].items():
            if t is None or len(t) == 0: continue
            tt = t.copy(); tt["coin"] = c; tt["w"] = w; T.append(tt)
    T = pd.concat(T)
    p = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(T), "mean_net": p.mean(), "median_net": p.median(), "win_share": (p > 0).mean(),
                               "sum_all": p.sum(), "sum_top5": p.head(5).sum(), "sum_top10": p.head(10).sum(),
                               "mean_days": T["duration_minutes"].mean() / 1440})
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "sum"])
    # cases: onset bars of forecast>0, forward returns at several horizons
    H = [1, 3, 5, 10, 20]
    cases = []; drift = {}
    for c in bars:
        for h in H:
            r = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                r += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(r)
        for w, b in bars[c].items():
            f = b["forecast"].fillna(0).values; cl = b["close"].values
            raw = b["debug_info.components.break_up.last_history_value"].values
            cl60 = pd.Series(cl).pct_change(60).values
            cl20 = pd.Series(cl).pct_change(20).values
            for i in range(1, len(f)):
                if f[i] > 0 and f[i - 1] <= 0:
                    rec = {"coin": c, "w": w, "f": f[i], "raw": raw[i], "r60": cl60[i], "r20": cl20[i], "day": str(b["timestamp"].iloc[i])[:10]}
                    for h in H:
                        rec[f"u{h}"] = cl[i + h] / cl[i] - 1 - drift[(c, h)] if i + h < len(cl) else np.nan
                    cases.append(rec)
    C = pd.DataFrame(cases)
    res = {}
    for h in H:
        x = C[f"u{h}"].dropna()
        res[h] = {"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))), "hit": (x > 0).mean()}
    out["onset_by_horizon"] = pd.DataFrame(res).T
    C["rawbin"] = pd.qcut(C["raw"], 3, labels=["small", "mid", "large"], duplicates="drop")
    out["onset_by_break_size"] = C.groupby("rawbin")[["raw", "u1", "u5", "u10", "u20"]].mean().join(C.groupby("rawbin").size().rename("n"))
    C["r60bin"] = pd.qcut(C["r60"], 3, labels=["low", "mid", "high"])
    out["onset_by_prior60"] = C.groupby("r60bin")[["r60", "u5", "u10", "u20"]].mean().join(C.groupby("r60bin").size().rename("n"))
    out["onset_by_coin"] = C.groupby("coin")[["u5", "u10", "u20"]].agg(["mean", "count"])
    out["onset_spearman_raw_u5_u20"] = pd.Series({"u5": stats.spearmanr(C["raw"], C["u5"], nan_policy="omit")[0], "u20": stats.spearmanr(C["raw"], C["u20"], nan_policy="omit")[0]})
    return out
