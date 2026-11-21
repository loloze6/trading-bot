def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # trades
    tr = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t):
                t = t.copy(); t["coin"] = c; tr.append(t)
    tr = pd.concat(tr)
    out["trades_summary"] = pd.Series({
        "n": len(tr),
        "mean_duration_min": tr["duration_minutes"].mean(),
        "median_duration_min": tr["duration_minutes"].median(),
        "mean_gross_pct": tr["profit_loss_percent"].mean(),
        "mean_net_pct": tr["net_profit_loss_percent"].mean(),
        "share_long": (tr["side"] == "LONG").mean(),
        "t_gross": stats.ttest_1samp(tr["profit_loss_percent"].dropna(), 0).statistic,
    })
    out["trades_by_coin"] = tr.groupby("coin").agg(n=("side", "size"), gross=("profit_loss_percent", "mean"),
                                                 net=("net_profit_loss_percent", "mean"), dur=("duration_minutes", "mean"))
    # regime bars: 1h, 24h forward, and how long position held
    rows = []
    for c, ws in data["bars"].items():
        allr24 = []
        for w, b in ws.items():
            cl = b["close"].values
            g = cl[24::24] / cl[0:-24:24][:len(cl[24::24])] - 1 if len(cl) > 24 else []
            allr24.extend(list(g))
        m24 = np.nanmean(allr24) if allr24 else np.nan
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            n = len(b)
            fwd1 = np.full(n, np.nan); fwd1[:-1] = cl[1:] / cl[:-1] - 1
            fwd24 = np.full(n, np.nan); fwd24[:-24] = cl[24:] / cl[:-24] - 1
            fwd2_24 = np.full(n, np.nan); fwd2_24[:-24] = cl[24:] / cl[1:-23] - 1
            idx = np.where(b["regime"].values == "mean_reversion")[0]
            for i in idx:
                rows.append(dict(coin=c, w=w, f=b["forecast"].iloc[i],
                                 alloc=b["postRebalance_current_allocation"].iloc[i],
                                 nextalloc=b["postRebalance_current_allocation"].iloc[i + 1] if i + 1 < n else np.nan,
                                 r1=fwd1[i], r24=fwd24[i], r2_24=fwd2_24[i], ex24=fwd24[i] - m24))
    r = pd.DataFrame(rows)
    out["n_regime"] = len(r)
    pos = r[r.f > 0]
    out["pos_bars"] = pd.Series({
        "n": len(pos), "mean_alloc": pos.alloc.mean(), "mean_next_alloc": pos.nextalloc.mean(),
        "mean_r1": pos.r1.mean(), "t_r1": stats.ttest_1samp(pos.r1.dropna(), 0).statistic,
        "mean_r24": pos.r24.mean(), "mean_ex24": pos.ex24.mean(),
        "t_ex24": stats.ttest_1samp(pos.ex24.dropna(), 0).statistic,
        "mean_r2_24": pos.r2_24.mean()})
    r["fq"] = np.where(r.f > 0, pd.qcut(r.f.where(r.f > 0), 4, labels=False, duplicates="drop"), -1)
    out["by_forecast_quartile"] = r.groupby("fq").agg(n=("f", "size"), f=("f", "mean"), r1=("r1", "mean"),
                                                    ex24=("ex24", "mean"), r24=("r24", "mean"))
    # book daily
    d = []
    for c, ws in data["days"].items():
        for w, x in ws.items():
            x = x.copy(); x["coin"] = c; x["w"] = w; d.append(x)
    d = pd.concat(d)
    out["book_daily"] = pd.Series({"mean_book": d.book_return.mean(), "mean_coin": d.coin_return.mean()})
    # fee estimate: commission per trade
    out["commission_mean"] = tr["total_commission"].mean()
    out["gross_minus_net_pct"] = (tr["profit_loss_percent"] - tr["net_profit_loss_percent"]).mean()
    return out
