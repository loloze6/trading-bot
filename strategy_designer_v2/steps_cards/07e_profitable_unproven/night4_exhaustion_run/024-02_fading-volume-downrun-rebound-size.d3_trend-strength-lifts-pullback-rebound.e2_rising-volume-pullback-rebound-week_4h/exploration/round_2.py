def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    coins = list(bars.keys())
    allday = []
    inpos = []
    for c in coins:
        dr = []
        for w, d in days[c].items():
            b = bars[c][w]
            ts = pd.to_datetime(b["timestamp"], utc=True)
            key = ts.dt.strftime("%Y-%m-%d").values
            pos = pd.Series(b["postRebalance_current_allocation"].values, index=key).groupby(level=0).last()
            reg = pd.Series((b["regime"].values == "trending").astype(float), index=key).groupby(level=0).last()
            dd = d.copy()
            dk = pd.to_datetime(dd["day"], utc=True).dt.strftime("%Y-%m-%d").values
            dd["pos"] = pos.reindex(dk).shift(1).values
            dd["trend_prev"] = reg.reindex(dk).shift(1).values
            dd["w"] = w; dd["coin"] = c
            dd["year"] = pd.to_datetime(dd["day"], utc=True).dt.year.values
            dr.append(dd)
            a = b["postRebalance_current_allocation"].values
            inpos.append({"coin": c, "share_bars_in": (np.abs(a) > 0.01).mean(),
                          "share_trend_bars": (b["regime"].values == "trending").mean(),
                          "share_in_given_trend": (np.abs(a[b["regime"].values == "trending"]) > 0.01).mean() if (b["regime"].values == "trending").any() else np.nan,
                          "share_in_given_not": (np.abs(a[b["regime"].values != "trending"]) > 0.01).mean() if (b["regime"].values != "trending").any() else np.nan})
        dr = pd.concat(dr)
        mu = dr["coin_return"].mean()
        dr["mkt"] = dr["pos"] * mu
        allday.append(dr)
    out["inpos_by_coin"] = pd.DataFrame(inpos).groupby("coin").mean()
    A = pd.concat(allday)
    port = A.groupby(["w", "day"]).agg(book=("book_return", "mean"), mkt=("mkt", "mean"), coin=("coin_return", "mean"))
    out["port"] = pd.Series({"book": port.book.mean(), "mkt": port.mkt.mean(),
                             "timing": port.book.mean() - port.mkt.mean(), "avg_pos": A["pos"].mean(),
                             "coin_mean": A["coin_return"].mean()})
    A["state"] = np.where(A["pos"].abs() > 0.01, "in", "out")
    g = A.groupby("state")
    out["coin_days_by_state"] = pd.DataFrame({"n": g["book_return"].count(), "book": g["book_return"].mean(),
                                              "coin": g["coin_return"].mean(), "pos": g["pos"].mean()})
    # trend regime grading on 3-day and 7-day grids, by 30-day return quintile, and signal vs non-signal within trend
    res = []; grade = []
    for H in [18, 42]:
        recs = []
        for c in coins:
            allr = []
            for b in bars[c].values():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - H, H)
                allr += list(cl[idx + H] / cl[idx] - 1)
            drift = np.mean(allr)
            for w, b in bars[c].items():
                cl = b["close"].values; n = len(cl)
                f = b["forecast"].fillna(0).values
                for s in range(0, n - H, H):
                    if s >= 180:
                        r30 = cl[s] / cl[s - 180] - 1
                    else:
                        r30 = np.nan
                    sig = (f[s] >= 2)
                    recs.append({"coin": c, "w": w, "r30": r30, "trend": b["regime"].values[s] == "trending",
                                 "sig": sig, "u": cl[s + H] / cl[s] - 1 - drift})
        R = pd.DataFrame(recs)
        T = R[R.trend]
        a = T[T.sig].u; bb = T[~T.sig].u
        tt = stats.ttest_ind(a, bb, equal_var=False)
        res.append({"H_days": H / 6, "n_sig": len(a), "u_sig": a.mean(), "n_nosig": len(bb), "u_nosig": bb.mean(),
                    "diff_t": tt.statistic})
        Rr = R.dropna(subset=["r30"]).copy()
        Rr["q"] = pd.qcut(Rr["r30"], 5, labels=False)
        q = Rr.groupby("q").agg(r30=("r30", "mean"), n=("u", "count"), u=("u", "mean"), sd=("u", "std"))
        q["t"] = q.u / q.sd * np.sqrt(q.n); q["H_days"] = H / 6
        grade.append(q.reset_index())
        Tc = T.groupby("coin").agg(n=("u", "count"), u=("u", "mean"), sd=("u", "std"))
        Tc["t"] = Tc.u / Tc.sd * np.sqrt(Tc.n)
        out[f"trend_by_coin_H{H}"] = Tc
        sp = stats.spearmanr(Rr["r30"], Rr["u"])
        res[-1]["spearman_r30_u"] = sp.correlation; res[-1]["sp_p"] = sp.pvalue
    out["sig_vs_nosig_in_trend"] = pd.DataFrame(res)
    out["r30_quintiles"] = pd.concat(grade)
    Tr = pd.concat([t.assign(coin=c) for c in coins for t in trades[c].values() if len(t)])
    Tr["dur_d"] = Tr["duration_minutes"] / 1440
    Tr["dq"] = pd.qcut(Tr["dur_d"], 4, labels=False, duplicates="drop")
    out["trades_by_duration"] = Tr.groupby("dq").agg(n=("dur_d", "count"), dur=("dur_d", "mean"),
                                                     pl=("net_profit_loss_percent", "mean"), sum_pl=("net_profit_loss_percent", "sum"))
    return out
