def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    # book daily returns per coin/window
    rows = []
    for c in days:
        for w, d in days[c].items():
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            alloc = b.groupby("day")["postRebalance_current_allocation"].last().shift(1)
            dd = d.copy(); dd["day"] = pd.to_datetime(dd["day"]).dt.floor("D")
            dd = dd.merge(alloc.rename("pos").reset_index(), on="day", how="left")
            dd["coin"] = c; dd["win"] = w
            rows.append(dd)
    D = pd.concat(rows, ignore_index=True).dropna(subset=["book_return"])
    D["pos"] = D["pos"].fillna(0)
    cm = D.groupby("coin")["coin_return"].mean()
    D["mkt"] = D["pos"] * D["coin"].map(cm)
    book = D.groupby("day")[["book_return", "coin_return", "mkt"]].mean()
    out["book_mean_daily"] = pd.Series({"book": book.book_return.mean(), "market_part": book.mkt.mean(),
                                        "hold": book.coin_return.mean(),
                                        "sharpe": book.book_return.mean()/book.book_return.std()*np.sqrt(365),
                                        "n_days": len(book)})
    # by coin and window: sum of book returns contributions (divided by coins that day)
    ncoin = D.groupby("day")["coin"].transform("count")
    D["contrib"] = D["book_return"]/ncoin
    D["contrib_mkt"] = D["mkt"]/ncoin
    out["by_coin"] = D.groupby("coin")[["contrib", "contrib_mkt"]].sum().assign(share=lambda x: x.contrib/x.contrib.sum())
    out["by_window"] = D.groupby("win")[["contrib", "contrib_mkt"]].sum()
    D["year"] = pd.to_datetime(D["day"]).dt.year
    out["by_year"] = D.groupby("year")[["contrib", "contrib_mkt"]].sum()
    # trades
    T = pd.concat([t.assign(coin=c, win=w) for c in trades for w, t in trades[c].items() if len(t)], ignore_index=True)
    p = T["net_profit_loss_percent"]
    ps = p.sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(T), "mean": p.mean(), "median": p.median(), "win_rate": (p > 0).mean(),
                               "top5_sum": ps.head(5).sum(), "total_sum": p.sum(), "dur_days_mean": T.duration_minutes.mean()/1440})
    # cases recomputed: situation bars, features, forward returns
    H = [5, 10, 20, 40]
    recs = []; drift = {h: {} for h in H}; sd = {}
    for c in bars:
        allr = {h: [] for h in H}
        for w, b in bars[c].items():
            cl = b["close"].values
            for h in H:
                idx = np.arange(0, len(cl)-h, h)
                allr[h] += list(cl[idx+h]/cl[idx]-1)
        for h in H:
            drift[h][c] = np.mean(allr[h]) if allr[h] else np.nan
        sd[c] = np.std(allr[20]) if allr[20] else np.nan
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; hi = b["high"]; lo = b["low"]
            er = (cl - cl.shift(60)).abs() / cl.diff().abs().rolling(60).sum()
            ph = hi.shift(1).rolling(60).max(); pl = lo.shift(1).rolling(60).min()
            brk = cl/ph - 1
            rng = (ph - pl)/cl
            ret60 = cl/cl.shift(60) - 1
            ret180 = cl/cl.shift(180) - 1
            situ = (er <= 0.3) & (brk > 0)
            n = len(b)
            for start in range(0, n, 20):
                cell = [i for i in range(start, min(start+20, n)) if situ.iloc[i]]
                if not cell: continue
                i = cell[0]
                r = {"coin": c, "win": w, "day": b["timestamp"].iloc[i], "brk": brk.iloc[i], "er": er.iloc[i],
                     "rng": rng.iloc[i], "ret60": ret60.iloc[i], "ret180": ret180.iloc[i],
                     "fc": b["forecast"].iloc[i]}
                for h in H:
                    r[f"r{h}"] = cl.iloc[i+h]/cl.iloc[i]-1 - drift[h][c] if i+h < n else np.nan
                recs.append(r)
    C = pd.DataFrame(recs)
    out["cases_n"] = len(C)
    out["case_mean_by_h"] = pd.DataFrame({f"r{h}": [C[f"r{h}"].mean(), C[f"r{h}"].count(),
                          stats.ttest_1samp(C[f"r{h}"].dropna(), 0).statistic] for h in H}, index=["mean", "n", "t"])
    res = {}
    for f in ["brk", "er", "rng", "ret60", "ret180", "fc"]:
        x = C[[f, "r20"]].dropna()
        q = pd.qcut(x[f].rank(method="first"), 3, labels=["lo", "mid", "hi"])
        g = x.groupby(q)["r20"].mean()
        res[f] = {"spearman": stats.spearmanr(x[f], x.r20).correlation, "lo": g["lo"], "mid": g["mid"], "hi": g["hi"], "n": len(x)}
    out["feature_terciles_r20"] = pd.DataFrame(res).T
    out["case_r20_by_coin"] = C.groupby("coin")["r20"].agg(["mean", "count"])
    C["year"] = pd.to_datetime(C["day"]).dt.year
    out["case_r20_by_year"] = C.groupby("year")["r20"].agg(["mean", "count"])
    return out
