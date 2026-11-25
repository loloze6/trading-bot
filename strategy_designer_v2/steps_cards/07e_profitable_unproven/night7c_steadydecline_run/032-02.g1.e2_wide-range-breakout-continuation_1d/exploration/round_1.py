def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    coins = list(bars.keys())
    H = [1, 3, 5, 10, 20]
    # coin mean h-return over all windows (non-overlapping grid)
    cmean = {}
    for c in coins:
        for h in H:
            rs = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            cmean[(c, h)] = np.mean(rs)
    # daily mean coin return
    dmean = {}
    for c in coins:
        rr = pd.concat([d["coin_return"] for d in days[c].values()]).dropna()
        dmean[c] = rr.mean()
    # book decomposition per day
    rows = []
    for c in coins:
        for w, d in days[c].items():
            b = bars[c][w]
            alloc = b["postRebalance_current_allocation"].fillna(0).values
            dd = d.copy().reset_index(drop=True)
            n = min(len(dd), len(alloc))
            dd = dd.iloc[:n]
            dd["pos"] = np.r_[np.nan, alloc[:n - 1]]
            dd["mkt"] = dd["pos"] * dmean[c]
            dd["coin"] = c; dd["w"] = w
            dd["year"] = pd.to_datetime(dd["day"]).dt.year
            rows.append(dd)
    D = pd.concat(rows).dropna(subset=["book_return"])
    daily = D.groupby(["w", "day"]).agg(book=("book_return", "mean"), mkt=("mkt", "mean"), hold=("coin_return", "mean")).reset_index()
    out["book_decomp"] = pd.Series({"book_mean": daily.book.mean(), "mkt_part": daily.mkt.mean(),
                                    "timing": daily.book.mean() - daily.mkt.mean(),
                                    "t_book": stats.ttest_1samp(daily.book, 0).statistic,
                                    "t_timing": stats.ttest_1samp(daily.book - daily.mkt, 0).statistic,
                                    "hold_mean": daily.hold.mean(), "n_days": len(daily)})
    bycoin = D.groupby("coin").apply(lambda g: pd.Series({"book_sum": g.book_return.sum(), "mkt_sum": g.mkt.sum(), "mean_pos": g.pos.mean(), "hold_mean": g.coin_return.mean()}))
    out["by_coin"] = bycoin
    byw = daily.groupby("w").agg(book=("book", "sum"), mkt=("mkt", "sum"), hold=("hold", "sum"))
    out["by_window"] = byw
    # trades concentration
    T = pd.concat([t.assign(coin=c) for c in coins for t in trades[c].values()])
    p = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(T), "sum": p.sum(), "top10_sum": p.head(10).sum(), "win_share": (p > 0).mean(), "mean": p.mean(), "median": p.median()})
    # features and forward returns at horizons
    feats = []
    for c in coins:
        for w, b in bars[c].items():
            cl = b["close"]; hi = b["high"]; lo = b["low"]
            rng = (hi - lo) / cl
            rr = rng / rng.rolling(28).mean()
            pe = cl / cl.shift(28) - 1
            mx = cl.rolling(28).max()
            dist = (mx - cl) / mx
            f = pd.DataFrame({"pe": pe, "rr": rr, "dist": dist, "fc": b["forecast"], "pos": b["postRebalance_current_allocation"]})
            n = len(cl)
            for h in H:
                fr = cl.shift(-h) / cl - 1
                g = np.zeros(n, bool); g[np.arange(0, n, h)] = True
                f[f"x{h}"] = np.where(g, fr - cmean[(c, h)], np.nan)
            f["coin"] = c; f["w"] = w
            feats.append(f)
    F = pd.concat(feats)
    act = F[F.fc > 0]; reg = F[(F.pe > 0) & (F.rr >= 1)]
    up = F[F.pe > 0]; dn = F[F.pe <= 0]
    def summ(s):
        s = s.dropna(); return f"{s.mean():+.4f} t{stats.ttest_1samp(s,0).statistic:.2f} n{len(s)}" if len(s) > 2 else ""
    tab = {}
    for nm, sub in [("active", act), ("regime", reg), ("up28_all", up), ("down28", dn), ("up28_narrow", F[(F.pe > 0) & (F.rr < 1)])]:
        tab[nm] = {f"h{h}": summ(sub[f"x{h}"]) for h in H}
    out["by_group_horizon"] = pd.DataFrame(tab).T
    # grading within up28 days
    U = up.copy()
    for col in ["dist", "rr", "pe"]:
        U["q"] = pd.qcut(U[col], 5, labels=False, duplicates="drop")
        out[f"up28_{col}_quint"] = pd.DataFrame({f"h{h}": U.groupby("q")[f"x{h}"].apply(summ) for h in [5, 10, 20]})
    # grading pe across all days
    A = F.copy(); A["q"] = pd.qcut(A["pe"], 5, labels=False)
    out["all_pe_quint"] = pd.DataFrame({f"h{h}": A.groupby("q")[f"x{h}"].apply(summ) for h in [5, 10, 20]})
    return out
