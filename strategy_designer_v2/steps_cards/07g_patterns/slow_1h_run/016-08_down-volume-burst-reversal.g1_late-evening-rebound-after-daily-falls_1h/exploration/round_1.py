def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    rows_h = []; rows_x = []; rows_v = []; rows_d = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"].astype(float)
            r1 = cl.shift(-1)/cl - 1
            hc = (ts + pd.Timedelta(hours=1)).dt.hour  # hour of close
            rows_h.append(pd.DataFrame({"coin": c, "hc": hc, "r1": r1}))
            p24 = cl/cl.shift(24) - 1
            lr = np.log(cl).diff()
            vol24 = lr.rolling(24).std()
            vol720 = lr.rolling(720, min_periods=200).std()
            z = p24/(vol24*np.sqrt(24))
            f2 = cl.shift(-2)/cl - 1
            f24 = cl.shift(-24)/cl - 1
            rows_x.append(pd.DataFrame({"coin": c, "hc": hc, "p24": p24, "z": z, "f2": f2, "f24": f24,
                                        "vr": vol24/vol720, "pos": b["postRebalance_current_allocation"].astype(float)}))
            g = np.arange(len(b)) % 24 == 0
            rows_v.append(pd.DataFrame({"coin": c, "p24": p24[g], "vr": (vol24/vol720)[g], "f24": f24[g],
                                        "absr": (f24[g]).abs()}))
    H = pd.concat(rows_h); X = pd.concat(rows_x); V = pd.concat(rows_v)
    def tm(s):
        s = s.dropna(); return pd.Series({"mean_bp": s.mean()*1e4, "t": s.mean()/(s.std()/np.sqrt(len(s))), "n": len(s)})
    hour_tab = H.groupby("hc")["r1"].apply(tm).unstack()
    # slope of next 2h on past-24h z, by decision close hour, one case per day per hour
    out = {}
    for h, g in X.groupby("hc"):
        g = g.dropna(subset=["z", "f2"])
        g = g[np.isfinite(g.z)]
        res = stats.linregress(g.z, g.f2 - g.groupby("coin").f2.transform("mean"))
        neg = g[g.z < 0]
        r2 = stats.linregress(neg.z, neg.f2)
        out[h] = {"slope_all_t": res.slope/res.stderr, "slope_fallsonly_t": r2.slope/r2.stderr, "n": len(g)}
    hour_rev = pd.DataFrame(out).T
    # 24h grid: past 24h quintile -> next 24h
    V = V.dropna()
    V["q"] = V.groupby("coin").p24.transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    q_tab = V.groupby("q").f24.apply(tm).unstack()
    V["vq"] = V.groupby("coin").vr.transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    vq_tab = V.groupby("vq").f24.apply(tm).unstack()
    # weekday daily
    D = pd.concat([d.assign(coin=c) for c in days for w, d in days[c].items()])
    D["wd"] = pd.to_datetime(D["day"]).dt.dayofweek
    wd_tab = D.groupby("wd").coin_return.apply(tm).unstack()
    # trades
    T = pd.concat([t.assign(coin=c) for c in trades for w, t in trades[c].items()])
    tr = pd.DataFrame({
        "n": [len(T)], "dur_h_mean": [T.duration_minutes.mean()/60], "dur_h_median": [T.duration_minutes.median()/60],
        "pl_gross_mean_pct": [T.profit_loss_percent.mean()], "pl_net_mean_pct": [T.net_profit_loss_percent.mean()],
        "pl_gross_t": [stats.ttest_1samp(T.profit_loss_percent.dropna(), 0).statistic]})
    tr_coin = T.groupby("coin")[["profit_loss_percent", "net_profit_loss_percent"]].mean()
    # book gain per held bar
    Xh = X.copy(); Xh["gain"] = Xh.pos*pd.concat([h_["r1"] for h_ in rows_h]).values
    held = Xh[Xh.pos.abs() > 1e-9]
    held_tab = held.groupby("hc").gain.apply(tm).unstack()
    return {"hour_of_close_ret": hour_tab, "rev_slope_by_hour": hour_rev, "p24_quintile_next24": q_tab,
            "volratio_quintile_next24": vq_tab, "weekday": wd_tab, "trades": tr, "trades_by_coin": tr_coin,
            "held_gain_by_hour": held_tab}
