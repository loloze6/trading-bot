def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    out = {}
    # --- book decomposition by coin
    rows = []
    allday = []
    for c in bars:
        # coin mean daily return over all windows
        cr = pd.concat([days[c][w]["coin_return"] for w in days[c]]).dropna()
        mu = cr.mean()
        for w in bars[c]:
            b = bars[c][w].copy()
            d = days[c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            pos = b.groupby("day")["postRebalance_current_allocation"].last().shift(1)
            d["day"] = pd.to_datetime(d["day"]).dt.floor("D")
            d = d.set_index("day")
            d["pos"] = pos.reindex(d.index)
            d["mkt"] = d["pos"] * mu
            d["coin"] = c; d["win"] = w
            d["year"] = d.index.year
            allday.append(d.reset_index())
    A = pd.concat(allday)
    A = A.dropna(subset=["book_return"])
    out["by_coin"] = A.groupby("coin").agg(mean_book=("book_return","mean"), mkt_part=("mkt","mean"),
                                         mean_pos=("pos","mean"), days=("book_return","size"))
    out["by_year"] = A.groupby("year").agg(mean_book=("book_return","mean"), mkt_part=("mkt","mean"),
                                         coin_ret=("coin_return","mean"), mean_pos=("pos","mean"))
    out["by_window_sum_book"] = A.groupby("win")["book_return"].sum().sort_values()
    tot = A["book_return"].mean(); mk = A["mkt"].mean()
    out["total"] = pd.Series({"mean_book_per_coin_day": tot, "mkt_part": mk, "timing": tot-mk})
    # --- entry cases, forward returns at horizons
    hs = [1,2,3,5,10,15,20,30]
    recs = []
    drift = {}
    for c in bars:
        for h in hs:
            r = []
            for w in bars[c]:
                cl = bars[c][w]["close"].values
                idx = np.arange(0, len(cl)-h, h)
                r.append(cl[idx+h]/cl[idx]-1)
            r = np.concatenate(r); drift[(c,h)] = r.mean()
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True)
            f = b["forecast"].fillna(0).values; cl = b["close"].values
            ts = pd.to_datetime(b["timestamp"])
            md = b.get("debug_info.components.ma_dist.last_history_value")
            bk = b.get("debug_info.components.break.last_history_value")
            # 60-day return and own past 20-day return
            for i in range(1, len(b)):
                if f[i] > 0 and f[i-1] <= 0:
                    rec = {"coin": c, "year": ts[i].year, "fc": f[i],
                           "md": md.iloc[i] if md is not None else np.nan,
                           "bk": bk.iloc[i] if bk is not None else np.nan,
                           "r20": cl[i]/cl[i-20]-1 if i>=20 else np.nan}
                    for h in hs:
                        rec[f"u{h}"] = cl[i+h]/cl[i]-1-drift[(c,h)] if i+h < len(cl) else np.nan
                        rec[f"t{h}"] = cl[i+h]/cl[i]-1 if i+h < len(cl) else np.nan
                    recs.append(rec)
    E = pd.DataFrame(recs)
    hz = []
    for h in hs:
        u = E[f"u{h}"].dropna()
        hz.append({"h": h, "n": len(u), "unusual": u.mean(), "t": u.mean()/(u.std()/np.sqrt(len(u))),
                   "total": E[f"t{h}"].mean()})
    out["entries_by_horizon"] = pd.DataFrame(hz)
    out["entries_by_coin_u5_u20"] = E.groupby("coin").agg(n=("u5","count"), u5=("u5","mean"), u20=("u20","mean"))
    out["entries_by_year"] = E.groupby("year").agg(n=("u5","count"), u5=("u5","mean"), u10=("u10","mean"), u20=("u20","mean"))
    for col in ["md","bk","r20","fc"]:
        s = E.dropna(subset=[col,"u5"])
        if len(s) > 20:
            q = pd.qcut(s[col].rank(method="first"), 4, labels=False)
            out[f"q_{col}"] = s.groupby(q).agg(lo=(col,"min"), hi=(col,"max"), n=("u5","count"),
                                               u5=("u5","mean"), u10=("u10","mean"), u20=("u20","mean"))
    # trades concentration
    T = pd.concat([trades[c][w].assign(coin=c) for c in trades for w in trades[c] if len(trades[c][w])])
    p = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(p), "sum": p.sum(), "top10_sum": p.head(10).sum(),
                               "top5pct_sum": p.head(int(len(p)*0.05)).sum(), "win_share": (p>0).mean(),
                               "median": p.median(), "mean_days": T["duration_minutes"].mean()/1440})
    return out
