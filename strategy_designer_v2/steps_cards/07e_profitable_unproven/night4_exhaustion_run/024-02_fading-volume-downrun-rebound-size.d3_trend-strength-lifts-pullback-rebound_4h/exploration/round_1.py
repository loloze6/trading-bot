def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    coins = list(bars.keys())
    # book daily: mean over coins per (window, day)
    rows = []
    for c in coins:
        for w, d in days[c].items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    # market part: per bar alloc * coin mean 4h return
    mk = []
    for c in coins:
        allr = []
        for w, b in bars[c].items():
            allr.append(b["close"].pct_change().shift(-1).dropna())
        mu = pd.concat(allr).mean()
        for w, b in bars[c].items():
            b = b.copy()
            b["g"] = b["postRebalance_current_allocation"] * (b["close"].shift(-1) / b["close"] - 1)
            b["m"] = b["postRebalance_current_allocation"] * mu
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            s = b.groupby("day")[["g", "m"]].sum()
            s["coin"] = c; s["w"] = w
            mk.append(s.reset_index())
    M = pd.concat(mk)
    M["year"] = M["day"].dt.year
    bk = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book_mean_daily_vs_hold"] = pd.Series({"book": bk.book_return.mean(), "hold": bk.coin_return.mean(),
        "book_t": bk.book_return.mean() / bk.book_return.std() * np.sqrt(len(bk)), "n_days": len(bk)})
    mm = M.groupby(["w", "day"])[["g", "m"]].mean()
    out["bar_gain_vs_market_part_daily"] = pd.Series({"gain": mm.g.mean(), "market": mm.m.mean(), "timing": mm.g.mean() - mm.m.mean()})
    pc = D.groupby("coin")["book_return"].agg(["mean", "count"])
    pc["market_part"] = M.groupby("coin")["m"].mean()
    pc["gain_bar"] = M.groupby("coin")["g"].mean()
    out["per_coin"] = pc
    py = D.groupby("year")[["book_return", "coin_return"]].mean()
    out["per_year"] = py
    pw = D.groupby("w")["book_return"].agg(["mean", "sum"]).sort_values("sum")
    out["per_window_sum_sorted"] = pw
    # trades
    T = pd.concat([t.assign(coin=c, w=w) for c in coins for w, t in trades[c].items() if len(t)])
    r = T["net_profit_loss_percent"]
    rs = r.sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(T), "mean": r.mean(), "median": r.median(), "win": (r > 0).mean(),
        "top10_share_of_sum": rs.head(10).sum() / r.sum(), "top5pct_share": rs.head(int(len(rs)*0.05)).sum() / r.sum(),
        "mean_dur_h": T.duration_minutes.mean() / 60, "short_share": (T.side == "SHORT").mean()})
    # horizon of signal: entries forecast 0 -> >0 ; and generic rise30 conditioning
    H = [1, 3, 6, 12, 18, 30, 42, 60]
    res = {}; gen = {}
    for h in H:
        ent = []; up = []; dn = []; pr = []
        for c in coins:
            allf = []
            for w, b in bars[c].items():
                cl = b["close"].values
                f = cl[h:] / cl[:-h] - 1
                allf.append(f[::h])
            mu = np.concatenate(allf).mean()
            for w, b in bars[c].items():
                cl = b["close"].values; n = len(cl)
                fc = b["forecast"].fillna(0).values
                fr = np.full(n, np.nan); fr[:n-h] = cl[h:] / cl[:n-h] - 1
                r30 = np.full(n, np.nan); r30[180:] = cl[180:] / cl[:-180] - 1
                prev = np.r_[0, fc[:-1]]
                st = np.where((fc > 0) & (prev <= 0))[0]
                # one per grid cell
                cells = {}
                for i in st:
                    if not np.isnan(fr[i]): cells.setdefault(i // h, i)
                ent += [fr[i] - mu for i in cells.values()]
                g = np.arange(0, n, h)
                for i in g:
                    if np.isnan(fr[i]) or np.isnan(r30[i]): continue
                    (up if r30[i] > 0 else dn).append(fr[i] - mu)
        e = np.array(ent); u = np.array(up); dd = np.array(dn)
        res[h * 4] = {"entry_mean": e.mean(), "t": stats.ttest_1samp(e, 0).statistic, "n": len(e)}
        gen[h * 4] = {"r30up_mean": u.mean(), "r30dn_mean": dd.mean(), "t_up_minus_dn": stats.ttest_ind(u, dd, equal_var=False).statistic, "n_up": len(u), "n_dn": len(dd)}
    out["entry_unusual_by_horizon_hours"] = pd.DataFrame(res).T
    out["generic_30d_trend_unusual_by_horizon_hours"] = pd.DataFrame(gen).T
    return out
