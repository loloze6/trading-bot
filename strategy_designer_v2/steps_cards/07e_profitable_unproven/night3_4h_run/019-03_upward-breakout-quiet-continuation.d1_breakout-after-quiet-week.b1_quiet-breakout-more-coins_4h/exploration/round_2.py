def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    def todt(s):
        s = pd.to_datetime(s, utc=True)
        return s.dt.tz_localize(None)
    allday = []
    for c in bars:
        for w in bars[c]:
            b = bars[c][w]
            ts = todt(b["timestamp"]).dt.floor("D")
            a = pd.Series(b["postRebalance_current_allocation"].values, index=ts.values).groupby(level=0).last()
            d = days[c][w].copy()
            d["day"] = todt(d["day"]).dt.floor("D")
            d = d.set_index("day")
            d["expo"] = a.shift(1).reindex(d.index).values
            d["coin"] = c; d["window"] = w
            allday.append(d.reset_index())
    D = pd.concat(allday, ignore_index=True)
    D["mcr"] = D.groupby("coin")["coin_return"].transform("mean")
    D["mkt"] = D["expo"] * D["mcr"]
    D["tim"] = D["book_return"] - D["mkt"]
    D["year"] = D["day"].dt.year
    pc = D.groupby("coin").agg(days=("book_return", "count"), book_bps=("book_return", "mean"),
                               coin_bps=("coin_return", "mean"), expo=("expo", "mean"),
                               mkt_bps=("mkt", "mean"), tim_bps=("tim", "mean"))
    for k in ["book_bps", "coin_bps", "mkt_bps", "tim_bps"]:
        pc[k] = pc[k] * 1e4
    pc["book_sum_share"] = D.groupby("coin")["book_return"].sum() / D["book_return"].sum()
    out["per_coin"] = pc.round(3)
    dw = D.groupby(["window", "day"])[["book_return", "mkt", "tim", "coin_return", "expo"]].mean().reset_index()
    out["overall_bps"] = (dw[["book_return", "mkt", "tim", "coin_return"]].mean() * 1e4).round(2)
    out["mean_expo"] = float(dw["expo"].mean())
    bw = dw.groupby("window")[["book_return", "mkt", "tim", "coin_return"]].mean() * 1e4
    bw["expo"] = dw.groupby("window")["expo"].mean()
    out["by_window_bps"] = bw.round(1)
    dw["year"] = dw["day"].dt.year
    out["by_year_bps"] = (dw.groupby("year")[["book_return", "mkt", "tim", "coin_return"]].mean() * 1e4).round(1)
    # book by coin's own 30d prior return state (daily level)
    try:
        D = D.sort_values(["coin", "window", "day"])
        D["c30"] = D.groupby(["coin", "window"])["close"].transform(lambda s: s / s.shift(30) - 1)
        q = D.dropna(subset=["c30", "book_return"]).copy()
        q["bin"] = pd.qcut(q["c30"], 5, labels=False)
        g = q.groupby("bin").agg(n=("book_return", "size"), c30_med=("c30", "median"), expo=("expo", "mean"),
                                 book_bps=("book_return", "mean"), coin_bps=("coin_return", "mean"))
        g["book_bps"] *= 1e4; g["coin_bps"] *= 1e4
        g["sum_share"] = q.groupby("bin")["book_return"].sum() / q["book_return"].sum()
        out["book_by_coin_30d_return"] = g.round(3)
    except Exception as e:
        out["err_state"] = str(e)
    # trades
    T = []
    for c in trades:
        for w in trades[c]:
            t = trades[c][w]
            if len(t): 
                t = t.copy(); t["coin"] = c; T.append(t)
    T = pd.concat(T, ignore_index=True)
    p = T["net_profit_loss_percent"].dropna().sort_values(ascending=False)
    k = max(1, int(len(p) * 0.05))
    out["trades"] = pd.Series({"n": len(p), "mean_net": p.mean(), "median_net": p.median(),
                               "win_share": (p > 0).mean(), "sum_net": p.sum(),
                               "sum_top5pct": p.iloc[:k].sum(), "sum_excl_top5pct": p.iloc[k:].sum(),
                               "mean_dur_h": T["duration_minutes"].mean() / 60}).round(3)
    # forward moves from breakout cases (forecast rises), by horizon and by prior return
    H = [6, 18, 36, 72, 108]
    recs = []
    for c in bars:
        drift = {}
        for h in H:
            rr = []
            for w in bars[c]:
                cl = bars[c][w]["close"].values
                idx = np.arange(0, len(cl) - h, h)
                if len(idx): rr.append(cl[idx + h] / cl[idx] - 1)
            drift[h] = np.concatenate(rr).mean() if rr else np.nan
        for w in bars[c]:
            b = bars[c][w]
            cl = b["close"].values; f = b["forecast"].fillna(0).values
            n = len(cl)
            ent = np.where((f >= 2) & (np.r_[0, f[:-1]] < 2))[0]
            last = -10**9
            for p0 in ent:
                if p0 - last < 18: continue
                last = p0
                r = {"coin": c}
                for h in H:
                    r[f"u{h}"] = cl[p0 + h] / cl[p0] - 1 - drift[h] if p0 + h < n else np.nan
                    r[f"t{h}"] = cl[p0 + h] / cl[p0] - 1 if p0 + h < n else np.nan
                r["prior30"] = cl[p0] / cl[p0 - 180] - 1 if p0 >= 180 else np.nan
                r["prior7"] = cl[p0] / cl[p0 - 42] - 1 if p0 >= 42 else np.nan
                r["bar0"] = cl[p0] / cl[p0 - 1] - 1 if p0 >= 1 else np.nan
                recs.append(r)
    R = pd.DataFrame(recs)
    hz = []
    for h in H:
        x = R[f"u{h}"].dropna()
        hz.append({"h_hours": h * 4, "n": len(x), "unusual_pct": x.mean() * 100,
                   "t": x.mean() / (x.std() / np.sqrt(len(x))), "total_pct": R[f"t{h}"].mean() * 100})
    out["entries_by_horizon"] = pd.DataFrame(hz).round(3)
    out["signal_bar_move_pct"] = round(float(R["bar0"].mean() * 100), 3)
    for v in ["prior30", "prior7"]:
        q = R.dropna(subset=[v, "u18"]).copy()
        q["bin"] = pd.qcut(q[v], 5, labels=False)
        g = q.groupby("bin").agg(n=("u18", "size"), prior_med=(v, "median"),
                                 u18=("u18", "mean"), u36=("u36", "mean"), u72=("u72", "mean"), t18tot=("t18", "mean"))
        g["t18"] = q.groupby("bin")["u18"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x))))
        g["t72"] = q.groupby("bin")["u72"].apply(lambda x: x.dropna().mean() / (x.dropna().std() / np.sqrt(x.notna().sum())))
        out[f"entries_by_{v}"] = g.round(4)
    return out
