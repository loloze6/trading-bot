def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    tr = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            f24 = c.shift(-24)/c - 1
            p24 = c/c.shift(24) - 1
            vol = r1.rolling(240, min_periods=200).std()
            vrank = vol.rolling(720, min_periods=300).apply(lambda x: (x[:-1] < x[-1]).mean() if len(x) > 1 else np.nan, raw=True)
            d = pd.DataFrame({"coin": coin, "w": w,
                              "hc": ((ts + pd.Timedelta(hours=1)).dt.hour).values,
                              "wd": ts.dt.weekday.values,
                              "f1": c.shift(-1).values/c.values - 1, "f24": f24.values, "p24": p24.values,
                              "vol": vol.values, "vr": vrank.values,
                              "alloc": b["postRebalance_current_allocation"].values,
                              "fc": b["forecast"].values})
            rows.append(d)
        for w, t in data["trades"][coin].items():
            t = t.copy(); t["coin"] = coin; tr.append(t)
    D = pd.concat(rows, ignore_index=True)
    T = pd.concat(tr, ignore_index=True)
    out["trades"] = pd.Series({"n": len(T), "dur_h_median": T["duration_minutes"].median()/60,
                               "dur_h_mean": T["duration_minutes"].mean()/60,
                               "pnl_mean": T["profit_loss_percent"].mean(),
                               "net_mean": T["net_profit_loss_percent"].mean(),
                               "comm_mean": T["total_commission"].mean()})
    D["held"] = D["alloc"].abs() > 1e-6
    out["held_by_hour"] = D[D.held].groupby("hc").size()
    # coin-demeaned 1h returns by hour of close
    D["f1x"] = D["f1"] - D.groupby("coin")["f1"].transform("mean")
    g = D.groupby("hc")["f1x"].agg(["mean", "std", "count"])
    g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["f1_excess_by_close_hour_bp"] = (g.assign(mean=g["mean"]*1e4)[["mean", "t", "count"]]).round(2)
    # 24h reversal by decision hour: sample one per day at each hour (nonoverlapping)
    D["f24x"] = D["f24"] - D.groupby("coin")["f24"].transform("mean")
    res = []
    for h in range(24):
        s = D[(D.hc == h)].dropna(subset=["f24x", "p24", "vr"])
        for lab, ss in [("hi", s[s.vr >= 0.5]), ("lo", s[s.vr < 0.5])]:
            z = -ss["p24"]/ss.groupby("coin")["p24"].transform("std")
            sl = stats.linregress(z, ss["f24x"])
            fall = ss[ss.p24 < 0]
            res.append({"hc": h, "vol": lab, "n": len(ss), "slope_bp": sl.slope*1e4, "t": sl.slope/sl.stderr,
                        "fall_mean_bp": fall["f24x"].mean()*1e4,
                        "fall_t": fall["f24x"].mean()/(fall["f24x"].std()/np.sqrt(len(fall)))})
    out["rev24_by_hour_vol"] = pd.DataFrame(res).round(2).set_index(["hc", "vol"]).iloc[::1]
    return out
