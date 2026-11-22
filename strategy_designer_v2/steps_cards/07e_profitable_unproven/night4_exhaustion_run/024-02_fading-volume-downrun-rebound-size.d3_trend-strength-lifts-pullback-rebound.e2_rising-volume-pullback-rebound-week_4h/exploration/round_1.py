def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    coins = list(bars.keys())
    allday = []
    rows = []
    for c in coins:
        dr = []
        for w, d in days[c].items():
            b = bars[c][w]
            day = pd.to_datetime(b["timestamp"]).dt.floor("D")
            pos = b["postRebalance_current_allocation"].groupby(day.values).last()
            dd = d.copy()
            dd["day"] = pd.to_datetime(dd["day"]).dt.floor("D")
            dd = dd.set_index("day")
            dd["pos"] = pos.reindex(dd.index).shift(1).values
            dd["w"] = w; dd["coin"] = c; dd["year"] = dd.index.year
            dr.append(dd.reset_index())
        dr = pd.concat(dr)
        mu = dr["coin_return"].mean()
        dr["mkt"] = dr["pos"] * mu
        allday.append(dr)
        r = dr["book_return"].dropna()
        rows.append({"coin": c, "book_mean": r.mean(), "book_t": r.mean() / r.std() * np.sqrt(len(r)),
                     "mkt_part": dr["mkt"].mean(), "avg_pos": dr["pos"].mean(),
                     "coin_mean": mu, "share_days_in": (dr["pos"].abs() > 0.01).mean()})
    out["by_coin"] = pd.DataFrame(rows).set_index("coin")
    A = pd.concat(allday)
    port = A.groupby(["w", "day"]).agg(book=("book_return", "mean"), mkt=("mkt", "mean"),
                                        coin=("coin_return", "mean"), year=("year", "first"))
    out["port"] = pd.Series({"book": port.book.mean(), "mkt": port.mkt.mean(),
                             "timing": port.book.mean() - port.mkt.mean(), "n_days": port.book.notna().sum()})
    out["by_window"] = port.groupby(level=0).agg(book=("book", "mean"), coin=("coin", "mean"), n=("book", "count"))
    out["by_year"] = port.groupby("year").agg(book=("book", "mean"), coin=("coin", "mean"), n=("book", "count"))
    T = pd.concat([t.assign(coin=c) for c in coins for t in trades[c].values() if len(t)])
    p = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(p), "mean": p.mean(), "median": p.median(), "win": (p > 0).mean(),
                               "top10_sum": p.head(10).sum(), "total_sum": p.sum(),
                               "mean_dur_days": T["duration_minutes"].mean() / 1440})
    res = []
    for H in [6, 18, 42, 84]:
        S = {"signal": [], "trend_grid": [], "not_trend_grid": [], "trend_flatfc_grid": []}
        for c in coins:
            allr = []
            for b in bars[c].values():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - H, H)
                allr += list(cl[idx + H] / cl[idx] - 1)
            drift = np.mean(allr)
            for b in bars[c].values():
                cl = b["close"].values; n = len(cl)
                f = b["forecast"].fillna(0).values
                reg = (b["regime"].values == "trending")
                for s in range(0, n - H, H):
                    r0 = cl[s + H] / cl[s] - 1 - drift
                    S["trend_grid" if reg[s] else "not_trend_grid"].append(r0)
                    if reg[s] and f[s] == 0:
                        S["trend_flatfc_grid"].append(r0)
                    k = np.where(f[s:s + H] >= 2)[0]
                    if len(k):
                        t = s + k[0]
                        if t + H < n:
                            S["signal"].append(cl[t + H] / cl[t] - 1 - drift)
        for name, v in S.items():
            v = np.array(v)
            if len(v) > 1:
                res.append({"H_days": H / 6, "set": name, "n": len(v), "mean_unusual": v.mean(),
                            "t": v.mean() / v.std() * np.sqrt(len(v))})
    out["fwd"] = pd.DataFrame(res)
    return out
