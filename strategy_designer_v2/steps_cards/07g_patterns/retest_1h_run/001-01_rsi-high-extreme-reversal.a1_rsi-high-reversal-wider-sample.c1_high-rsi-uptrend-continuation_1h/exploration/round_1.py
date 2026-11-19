def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    # 1) book: gross vs fees, per coin
    rows = []
    for c in bars:
        g = []; f = []; br = []; cr = []; pos = []
        for w, b in bars[c].items():
            b = b.sort_values("timestamp")
            r1 = b["close"].shift(-1) / b["close"] - 1
            a = b["postRebalance_current_allocation"]
            g.append((a * r1).dropna())
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            f.append(fee.dropna())
            pos.append(a)
        for w, d in days[c].items():
            br.append(d["book_return"].dropna()); cr.append(d["coin_return"].dropna())
        g = pd.concat(g); f = pd.concat(f); br = pd.concat(br); cr = pd.concat(cr); pos = pd.concat(pos)
        rows.append({"coin": c, "gross_hourly_mean_bp": g.mean() * 1e4, "fee_hourly_mean_bp": f.mean() * 1e4,
                     "book_daily_mean": br.mean(), "coin_daily_mean": cr.mean(),
                     "mean_pos": pos.mean(), "mean_abs_pos": pos.abs().mean(), "share_long": (pos > 0).mean(), "share_short": (pos < 0).mean()})
    out["book_by_coin"] = pd.DataFrame(rows).set_index("coin")

    # 2) forecast quintiles vs forward returns at several horizons (non-overlapping grid), trending bars
    recs = []
    for c in bars:
        allf = []
        for w, b in bars[c].items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            cl = b["close"].values
            for h in (24, 72, 240):
                idx = np.arange(0, len(b) - h, h)
                fr = cl[idx + h] / cl[idx] - 1
                past = np.full(len(idx), np.nan)
                ok = idx >= h
                past[ok] = cl[idx[ok]] / cl[idx[ok] - h] - 1
                vol = pd.Series(cl).pct_change().rolling(168).std().values[idx]
                allf.append(pd.DataFrame({"coin": c, "w": w, "h": h, "fc": b["forecast"].values[idx],
                                          "reg": b["regime"].values[idx], "fr": fr, "past": past, "vol": vol,
                                          "hour": pd.to_datetime(b["timestamp"]).dt.hour.values[idx],
                                          "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek.values[idx]}))
        recs.append(pd.concat(allf))
    R = pd.concat(recs)
    R["ex"] = R["fr"] - R.groupby(["coin", "h"])["fr"].transform("mean")
    res = []
    for h in (24, 72, 240):
        s = R[(R.h == h)]
        tr = s[s.reg == "trending"].copy()
        tr["q"] = pd.qcut(tr["fc"].rank(method="first"), 5, labels=False)
        for q, gq in tr.groupby("q"):
            res.append({"h": h, "grp": f"trend_q{q}", "n": len(gq), "mean_fc": gq.fc.mean(), "mean_ex": gq.ex.mean(),
                        "t": gq.ex.mean() / (gq.ex.std() / np.sqrt(len(gq)))})
        nt = s[s.reg != "trending"]
        res.append({"h": h, "grp": "not_trending", "n": len(nt), "mean_fc": nt.fc.mean(), "mean_ex": nt.ex.mean(),
                    "t": nt.ex.mean() / (nt.ex.std() / np.sqrt(len(nt)))})
    out["fc_quintiles_by_h"] = pd.DataFrame(res)

    # 3) reversal after large past moves: past h return quintile vs next h excess, all bars
    res = []
    for h in (24, 72, 240):
        s = R[(R.h == h)].dropna(subset=["past", "fr"]).copy()
        s["pz"] = s.groupby("coin")["past"].transform(lambda x: (x - x.mean()) / x.std())
        s["q"] = pd.qcut(s["pz"].rank(method="first"), 5, labels=False)
        for q, gq in s.groupby("q"):
            res.append({"h": h, "past_q": q, "n": len(gq), "mean_ex": gq.ex.mean(), "t": gq.ex.mean() / (gq.ex.std() / np.sqrt(len(gq)))})
        sl = stats.linregress(s["pz"], s["ex"] / s.groupby("coin")["fr"].transform("std"))
        res.append({"h": h, "past_q": "slope", "n": len(s), "mean_ex": sl.slope, "t": sl.slope / sl.stderr})
    out["past_ret_quintiles"] = pd.DataFrame(res)

    # 4) volatility tercile vs next 24h excess and abs
    s = R[R.h == 24].dropna(subset=["vol", "fr"]).copy()
    s["vq"] = s.groupby("coin")["vol"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    out["vol_tercile_24h"] = s.groupby("vq").agg(n=("ex", "size"), mean_ex=("ex", "mean"), sd=("ex", "std"))
    # 5) hourly returns by hour of day and weekday (1h non-overlap = every bar)
    hr = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.sort_values("timestamp")
            r = b["close"].shift(-1) / b["close"] - 1
            ts = pd.to_datetime(b["timestamp"])
            hr.append(pd.DataFrame({"r": r.values, "hour": ts.dt.hour.values, "wd": ts.dt.dayofweek.values,
                                    "g": (b["postRebalance_current_allocation"] * r).values}))
    H = pd.concat(hr).dropna()
    Hh = H.groupby("hour").agg(n=("r", "size"), mean_bp=("r", lambda x: x.mean() * 1e4), sd=("r", "std"), book_bp=("g", lambda x: x.mean() * 1e4))
    Hh["t"] = Hh.mean_bp / 1e4 / (Hh.sd / np.sqrt(Hh.n))
    out["by_hour"] = Hh.drop(columns="sd")
    Hw = H.groupby("wd").agg(n=("r", "size"), mean_bp=("r", lambda x: x.mean() * 1e4), sd=("r", "std"))
    Hw["t"] = Hw.mean_bp / 1e4 / (Hw.sd / np.sqrt(Hw.n))
    out["by_weekday"] = Hw.drop(columns="sd")
    # 6) trades summary
    T = pd.concat([t.assign(coin=c) for c in trades for t in trades[c].values()])
    out["trades"] = T.groupby("side").agg(n=("profit_loss_percent", "size"), gross=("profit_loss_percent", "mean"),
                                          net=("net_profit_loss_percent", "mean"), dur_h=("duration_minutes", lambda x: x.mean() / 60))
    return out
