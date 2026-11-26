def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
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
    ncoin = D.groupby("day")["coin"].transform("count")
    D["contrib"] = D["book_return"]/ncoin
    D["contrib_mkt"] = D["mkt"]/ncoin
    bc = D.groupby("coin")[["contrib", "contrib_mkt"]].sum()
    bc["share"] = bc.contrib/bc.contrib.sum()
    out["by_coin"] = bc
    out["by_window"] = D.groupby("win")[["contrib", "contrib_mkt"]].sum()
    D["year"] = pd.to_datetime(D["day"]).dt.year
    out["by_year"] = D.groupby("year")[["contrib", "contrib_mkt"]].sum()
    try:
        T = pd.concat([t.assign(coin=c, win=w) for c in trades for w, t in trades[c].items() if len(t)], ignore_index=True)
        p = T["net_profit_loss_percent"]; ps = p.sort_values(ascending=False)
        out["trades"] = pd.Series({"n": len(T), "mean": p.mean(), "median": p.median(), "win_rate": (p > 0).mean(),
                                   "top3_sum": ps.head(3).sum(), "top5_sum": ps.head(5).sum(), "total_sum": p.sum(),
                                   "dur_days_mean": T.duration_minutes.mean()/1440})
        out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "sum"])
    except Exception as e:
        out["trades_err"] = str(e)
    H = [5, 10, 20, 40]
    recs = []; drift = {h: {} for h in H}
    for c in bars:
        allr = {h: [] for h in H}
        for w, b in bars[c].items():
            cl = b["close"].values
            for h in H:
                idx = np.arange(0, len(cl)-h, h)
                allr[h] += list(cl[idx+h]/cl[idx]-1)
        for h in H:
            drift[h][c] = np.mean(allr[h]) if allr[h] else np.nan
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; hi = b["high"]; lo = b["low"]
            er = (cl - cl.shift(60)).abs() / cl.diff().abs().rolling(60).sum()
            ph = hi.shift(1).rolling(60).max(); pl = lo.shift(1).rolling(60).min()
            up = cl/ph - 1; dn = pl/cl - 1
            rng = (ph - pl)/cl
            ret60 = cl/cl.shift(60) - 1
            n = len(b)
            # kinds: flat-up (the tested), trend-up, flat-down, trend-down
            kinds = {"flat_up": (er <= 0.3) & (up > 0), "trend_up": (er > 0.3) & (up > 0),
                     "flat_dn": (er <= 0.3) & (dn > 0), "trend_dn": (er > 0.3) & (dn > 0)}
            for k, situ in kinds.items():
                situ = situ.fillna(False).values
                for start in range(0, n, 20):
                    cell = [i for i in range(start, min(start+20, n)) if situ[i]]
                    if not cell: continue
                    i = cell[0]
                    r = {"kind": k, "coin": c, "win": w, "day": b["timestamp"].iloc[i],
                         "brk": up.iloc[i] if "up" in k else dn.iloc[i], "er": er.iloc[i],
                         "rng": rng.iloc[i], "ret60": ret60.iloc[i], "fc": b["forecast"].iloc[i]}
                    for h in H:
                        r[f"r{h}"] = cl.iloc[i+h]/cl.iloc[i]-1 - drift[h][c] if i+h < n else np.nan
                    recs.append(r)
    C = pd.DataFrame(recs)
    tab = {}
    for k, g in C.groupby("kind"):
        for h in H:
            x = g[f"r{h}"].dropna()
            tab[(k, h)] = {"mean": x.mean(), "n": len(x), "t": stats.ttest_1samp(x, 0).statistic if len(x) > 2 else np.nan,
                           "share_pos": (x > 0).mean()}
    out["by_kind_h_unusual_long"] = pd.DataFrame(tab).T
    F = C[C.kind == "flat_up"].copy()
    res = {}
    for f in ["brk", "er", "rng", "ret60", "fc"]:
        x = F[[f, "r20"]].dropna()
        if len(x) < 9: continue
        q = pd.qcut(x[f].rank(method="first"), 3, labels=["lo", "mid", "hi"])
        g = x.groupby(q)["r20"].mean()
        res[f] = {"spearman": stats.spearmanr(x[f], x.r20).correlation, "lo": g["lo"], "mid": g["mid"], "hi": g["hi"], "n": len(x)}
    out["flat_up_feature_terciles_r20"] = pd.DataFrame(res).T
    out["flat_up_r20_by_coin"] = F.groupby("coin")["r20"].agg(["mean", "count"])
    F["year"] = pd.to_datetime(F["day"]).dt.year
    out["flat_up_r20_by_year"] = F.groupby("year")["r20"].agg(["mean", "count"])
    out["flat_up_r20_by_window"] = F.groupby("win")["r20"].agg(["mean", "count"])
    return out
