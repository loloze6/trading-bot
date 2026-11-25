def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    # coin mean daily return over all windows
    rows = []
    for c in days:
        allr = pd.concat([days[c][w]["coin_return"] for w in days[c]]).dropna()
        mu = allr.mean()
        for w in days[c]:
            d = days[c][w].copy()
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            pos = b.groupby("day")["postRebalance_current_allocation"].last()
            prevpos = pos.shift(1)
            d["day"] = pd.to_datetime(d["day"]).dt.floor("D")
            d = d.set_index("day")
            d["pos_prev"] = prevpos.reindex(d.index)
            d["mkt"] = d["pos_prev"] * mu
            d["coin"] = c; d["window"] = w
            d["year"] = d.index.year
            rows.append(d.reset_index())
    D = pd.concat(rows)
    D = D.dropna(subset=["book_return"])
    # by coin
    g = D.groupby("coin").agg(book_mean=("book_return", "mean"), mkt_part=("mkt", "mean"),
                              coin_mean=("coin_return", "mean"), share_in=("pos_prev", lambda x: (x.abs() > 0).mean()))
    g["timing"] = g["book_mean"] - g["mkt_part"]
    g["sum_contrib"] = D.groupby("coin")["book_return"].sum()
    out["by coin"] = g
    # book daily = mean over coins per day
    bk = D.groupby("day").agg(book=("book_return", "mean"), mkt=("mkt", "mean"), hold=("coin_return", "mean"))
    out["book overall"] = pd.Series({"book_mean": bk.book.mean(), "mkt_part": bk.mkt.mean(),
                                     "timing": bk.book.mean() - bk.mkt.mean(),
                                     "t_book": bk.book.mean() / bk.book.std() * np.sqrt(len(bk)), "n_days": len(bk)})
    D["year"] = pd.to_datetime(D["day"]).dt.year
    out["by window"] = D.groupby("window").agg(book_sum=("book_return", "sum"), mkt_sum=("mkt", "sum"),
                                              hold_sum=("coin_return", "sum"), inpos=("pos_prev", lambda x: (x.abs() > 0).mean()))
    out["by year"] = D.groupby("year").agg(book_sum=("book_return", "sum"), mkt_sum=("mkt", "sum"), hold_sum=("coin_return", "sum"))
    # trades concentration
    T = pd.concat([trades[c][w].assign(coin=c) for c in trades for w in trades[c] if len(trades[c][w])])
    p = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(p), "mean": p.mean(), "median": p.median(), "win_share": (p > 0).mean(),
                               "top5_sum": p.head(5).sum(), "top10_sum": p.head(10).sum(), "all_sum": p.sum(),
                               "mean_days": T["duration_minutes"].mean() / 1440})
    # forecast vs forward returns at several horizons, situation bars (raw ma_dist>0 in regime unknown)
    res = []
    for h in [1, 2, 3, 5, 10, 20]:
        recs = []
        for c in bars:
            allfr = []
            for w in bars[c]:
                b = bars[c][w].reset_index(drop=True)
                fr = b["close"].shift(-h) / b["close"] - 1
                allfr.append(fr.iloc[::h])
            mu = pd.concat(allfr).dropna().mean()
            for w in bars[c]:
                b = bars[c][w].reset_index(drop=True)
                fr = b["close"].shift(-h) / b["close"] - 1
                gsel = b.iloc[::h].copy(); gsel["fr"] = fr.iloc[::h] - mu
                gsel = gsel[(gsel["forecast"] > 0)].dropna(subset=["fr"])
                gsel["day"] = pd.to_datetime(gsel["timestamp"]).dt.floor("D")
                recs.append(gsel[["forecast", "fr", "day"]])
        R = pd.concat(recs)
        sl = stats.linregress(R["forecast"], R["fr"])
        dd = R.groupby("day")["fr"].sum()
        tm = R["fr"].mean() / (dd.std() * np.sqrt(len(dd)) / len(R))
        q = pd.qcut(R["forecast"], 3, labels=False, duplicates="drop")
        m = R.groupby(q)["fr"].mean()
        res.append({"h": h, "n": len(R), "slope_t": sl.slope / sl.stderr, "unusual_mean": R["fr"].mean(), "t_mean_dayclust": tm,
                    "low_third": m.iloc[0], "mid_third": m.iloc[1] if len(m) > 2 else np.nan, "high_third": m.iloc[-1]})
    out["horizons"] = pd.DataFrame(res)
    # all profiles: ma distance (recompute) vs 5d fwd return, by regime veto (unknown vs chop)
    res2 = []
    for c in bars:
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True)
            sma = b["close"].rolling(20).mean()
            dist = b["close"] / sma - 1
            fr = b["close"].shift(-5) / b["close"] - 1
            r60 = b["close"] / b["close"].shift(60) - 1
            g5 = pd.DataFrame({"dist": dist, "fr": fr, "regime": b["regime"], "r60": r60}).iloc[::5].dropna()
            g5["coin"] = c
            res2.append(g5)
    R2 = pd.concat(res2)
    R2["dq"] = pd.qcut(R2["dist"], 5, labels=False)
    out["dist quintile x regime 5d fwd mean"] = R2.pivot_table(index="dq", columns="regime", values="fr", aggfunc="mean")
    out["dist quintile x regime count"] = R2.pivot_table(index="dq", columns="regime", values="fr", aggfunc="count")
    return out
