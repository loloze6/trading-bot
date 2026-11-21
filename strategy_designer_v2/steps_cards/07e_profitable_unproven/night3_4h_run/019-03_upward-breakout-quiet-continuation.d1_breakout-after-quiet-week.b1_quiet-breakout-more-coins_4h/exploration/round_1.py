def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    # per coin decomposition
    rows = []
    allday = []
    for c in bars:
        br = []; cr = []; expo = []
        for w in bars[c]:
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            a = b.groupby("day")["postRebalance_current_allocation"].mean()
            d = days[c][w].copy()
            d["day"] = pd.to_datetime(d["day"]).dt.floor("D") if not np.issubdtype(d["day"].dtype, np.number) else d["day"]
            d = d.set_index("day")
            d["expo"] = a.shift(1).reindex(d.index)
            d["coin"] = c; d["window"] = w
            d["year"] = pd.to_datetime(d.index).year
            allday.append(d.reset_index())
        dd = pd.concat([x for x in allday if x["coin"].iloc[0] == c])
        mcr = dd["coin_return"].mean()
        rows.append({"coin": c, "days": dd["book_return"].notna().sum(),
                     "book_mean_bps": dd["book_return"].mean()*1e4,
                     "coin_mean_bps": mcr*1e4,
                     "expo": dd["expo"].mean(),
                     "market_part_bps": dd["expo"].mean()*mcr*1e4})
    pc = pd.DataFrame(rows).set_index("coin")
    pc["timing_bps"] = pc["book_mean_bps"] - pc["market_part_bps"]
    out["per_coin"] = pc.round(2)
    D = pd.concat(allday)
    D["mcr"] = D.groupby("coin")["coin_return"].transform("mean")
    D["mkt"] = D["expo"] * D["mcr"]
    D["tim"] = D["book_return"] - D["mkt"]
    daily = D.groupby("day")[["book_return", "mkt", "tim", "coin_return"]].mean()
    out["overall_bps"] = (daily.mean()*1e4).round(2)
    D2 = D.merge(daily.rename(columns=lambda x: "d_"+x), left_on="day", right_index=True)
    dw = D.groupby(["window", "day"])[["book_return", "mkt", "tim", "coin_return"]].mean().reset_index()
    out["by_window_bps"] = (dw.groupby("window")[["book_return", "mkt", "tim", "coin_return"]].mean()*1e4).round(1)
    dw["year"] = pd.to_datetime(dw["day"]).dt.year
    out["by_year_bps"] = (dw.groupby("year")[["book_return", "mkt", "tim", "coin_return"]].mean()*1e4).round(1)
    # trades concentration
    T = []
    for c in trades:
        for w in trades[c]:
            t = trades[c][w].copy(); t["coin"] = c; t["window"] = w; T.append(t)
    T = pd.concat(T)
    p = T["net_profit_loss_percent"].dropna().sort_values(ascending=False)
    k = max(1, int(len(p)*0.05))
    out["trades"] = pd.Series({"n": len(p), "mean_net": p.mean(), "median_net": p.median(),
                               "win_share": (p > 0).mean(), "sum_net": p.sum(),
                               "sum_top5pct": p.iloc[:k].sum(), "sum_excl_top5pct": p.iloc[k:].sum(),
                               "mean_dur_h": T["duration_minutes"].mean()/60})
    # forward moves after entries, different horizons, and by prior 30-day return
    H = [6, 18, 36, 72, 108]
    recs = []
    for c in bars:
        drift = {}
        for h in H:
            rr = []
            for w in bars[c]:
                cl = bars[c][w]["close"].values
                idx = np.arange(0, len(cl)-h, h)
                rr.append(cl[idx+h]/cl[idx]-1)
            drift[h] = np.concatenate(rr).mean() if rr else np.nan
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True)
            cl = b["close"].values
            ts = pd.to_datetime(b["timestamp"])
            if c not in trades or w not in trades[c]:
                continue
            t = trades[c][w]
            if len(t) == 0: continue
            et = pd.to_datetime(t["entry_time"])
            pos = ts.searchsorted(et.values)
            for i, p0 in enumerate(pos):
                # entry on bar close: entry time may be bar start or close
                if p0 >= len(cl): continue
                r = {"coin": c}
                for h in H:
                    r[f"u{h}"] = cl[p0+h]/cl[p0]-1-drift[h] if p0+h < len(cl) else np.nan
                    r[f"t{h}"] = cl[p0+h]/cl[p0]-1 if p0+h < len(cl) else np.nan
                r["prior30"] = cl[p0]/cl[p0-180]-1 if p0 >= 180 else np.nan
                r["prior7"] = cl[p0]/cl[p0-42]-1 if p0 >= 42 else np.nan
                r["fc"] = b["forecast"].iloc[p0]
                recs.append(r)
    R = pd.DataFrame(recs)
    hz = []
    for h in H:
        x = R[f"u{h}"].dropna()
        hz.append({"h_bars": h, "n": len(x), "unusual_pct": x.mean()*100,
                   "t": x.mean()/(x.std()/np.sqrt(len(x))), "total_pct": R[f"t{h}"].mean()*100})
    out["entries_by_horizon"] = pd.DataFrame(hz).round(3)
    for v in ["prior30", "prior7"]:
        q = R.dropna(subset=[v, "u18"]).copy()
        q["bin"] = pd.qcut(q[v], 5, labels=False)
        g = q.groupby("bin").agg(n=("u18", "size"), prior_med=(v, "median"),
                                 u18=("u18", "mean"), u36=("u36", "mean"), u72=("u72", "mean"))
        g["t18"] = q.groupby("bin")["u18"].apply(lambda x: x.mean()/(x.std()/np.sqrt(len(x))))
        out[f"entries_by_{v}"] = g.round(4)
    return out
