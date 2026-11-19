def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    out = {}
    # 1. forecast buckets vs forward returns at several horizons (non-overlapping grid), excess over coin mean
    rows = []
    for h in [24, 72, 168, 336]:
        recs = []
        for c in bars:
            cr = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                if len(idx) == 0: continue
                r = cl[idx + h] / cl[idx] - 1
                f = b["forecast"].values[idx]
                reg = b["regime"].values[idx]
                cr.append(pd.DataFrame({"coin": c, "r": r, "f": f, "reg": reg}))
            if cr:
                d = pd.concat(cr); d["ex"] = d["r"] - d["r"].mean(); recs.append(d)
        d = pd.concat(recs)
        d["grp"] = np.where(d["reg"] != "trending", "notrend",
                   np.where(d["f"] <= 0, "trend_f0", np.where(d["f"] < d.loc[d["f"] > 0, "f"].median(), "trend_flow", "trend_fhigh")))
        for g, s in d.groupby("grp"):
            rows.append({"h": h, "grp": g, "n": len(s), "mean_ex": s["ex"].mean(),
                         "t": s["ex"].mean() / (s["ex"].std() / np.sqrt(len(s)))})
    out["fwd_by_group"] = pd.DataFrame(rows)
    # 2. book: gross vs fees; position-weighted
    tot = []
    for c in bars:
        for w, b in bars[c].items():
            cl = b["close"].values
            nxt = np.r_[cl[1:] / cl[:-1] - 1, np.nan]
            a = b["postRebalance_current_allocation"].values
            g = a * nxt
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            tot.append({"coin": c, "gross_sum": np.nansum(g), "fee_sum": fee.sum(), "bars": len(b),
                        "mean_alloc": np.nanmean(a), "turnover": b["allocation_change"].abs().sum() if "allocation_change" in b else np.nan})
    t = pd.DataFrame(tot).groupby("coin").sum(numeric_only=True)
    t["gross_per_day"] = t["gross_sum"] / t["bars"] * 24
    t["fee_per_day"] = t["fee_sum"] / t["bars"] * 24
    out["book_gross_vs_fee"] = t[["gross_per_day", "fee_per_day", "turnover"]]
    # 3. hourly returns after large 24h moves, by vol tercile: next 24h return non-overlapping
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            cl = b["close"].values
            idx = np.arange(24, len(cl) - 24, 24)
            past = cl[idx] / cl[idx - 24] - 1
            fut = cl[idx + 24] / cl[idx] - 1
            lr = np.diff(np.log(cl))
            vol = np.array([lr[max(0, i - 168):i].std() for i in idx])
            rows.append(pd.DataFrame({"coin": c, "past": past, "fut": fut, "vol": vol}))
    d = pd.concat(rows)
    d["pz"] = d.groupby("coin")["past"].transform(lambda x: (x - x.mean()) / x.std())
    d["pq"] = pd.qcut(d["pz"], 5, labels=False)
    out["next24_by_past24_quint"] = d.groupby("pq")["fut"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    d["vq"] = d.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False))
    out["next24_by_vol_tercile"] = d.groupby("vq")["fut"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    # 4. hour-of-day and weekday mean 1h return
    hr = []
    for c in bars:
        for w, b in bars[c].items():
            ts = pd.to_datetime(b["timestamp"])
            r = b["close"].pct_change()
            hr.append(pd.DataFrame({"h": ts.dt.hour.values, "wd": ts.dt.weekday.values, "r": r.values}))
    hr = pd.concat(hr).dropna()
    gh = hr.groupby("h")["r"].agg(["count", "mean", "std"]); gh["t"] = gh["mean"] / gh["std"] * np.sqrt(gh["count"])
    out["hour"] = gh[["mean", "t"]]
    # trades
    tr = pd.concat([trades[c][w].assign(coin=c) for c in trades for w in trades[c] if len(trades[c][w])])
    tr["dur_h"] = tr["duration_minutes"] / 60
    tr["dq"] = pd.qcut(tr["dur_h"], 5, duplicates="drop")
    out["trades_by_duration"] = tr.groupby("dq")[["profit_loss_percent", "net_profit_loss_percent"]].agg(["count", "mean"])
    return out
