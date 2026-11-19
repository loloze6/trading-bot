def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            b["hour"] = ts.dt.hour.values
            b["wd"] = ts.dt.weekday.values
            c = b["close"].astype(float)
            lr = np.log(c).diff()
            b["r1"] = c.shift(-1) / c - 1
            b["f2"] = c.shift(-2) / c - 1
            b["f24"] = c.shift(-24) / c - 1
            b["f72"] = c.shift(-72) / c - 1
            vol = lr.rolling(20).std()
            b["z24"] = (np.log(c) - np.log(c.shift(24))) / (vol * np.sqrt(24))
            # grind vs jump: share of abs path carried by largest hour
            ab = lr.abs()
            b["jumpshare"] = ab.rolling(24).max() / ab.rolling(24).sum()
            b["eff"] = (np.log(c) - np.log(c.shift(24))).abs() / ab.rolling(24).sum()
            v = b["volume"].astype(float)
            b["vrel"] = v / v.rolling(168).mean()
            b["pos"] = b["postRebalance_current_allocation"].astype(float)
            b["pg"] = b["pos"] * b["r1"]
            b["pos_i"] = np.arange(len(b))
            b["coin"] = coin; b["win"] = w
            rows.append(b[["coin","win","hour","wd","r1","f2","f24","f72","z24","jumpshare","eff","vrel","pos","pg","pos_i","forecast"]])
    d = pd.concat(rows, ignore_index=True)
    def tt(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean_bp": x.mean()*1e4, "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out["hourly_ret_by_hour"] = d.groupby("hour")["r1"].apply(tt).unstack().round(2)
    out["hourly_ret_by_weekday"] = d.groupby("wd")["r1"].apply(tt).unstack().round(2)
    # slope of f2 on z24 at each hour (one per day per coin)
    res = []
    for h in range(24):
        s = d[d.hour == h][["f2","z24"]].dropna()
        sl = stats.linregress(s.z24, s.f2)
        res.append({"hour": h, "n": len(s), "slope_bp": sl.slope*1e4, "t": sl.slope/sl.stderr})
    out["f2_on_z24_by_hour"] = pd.DataFrame(res).round(2)
    # longer horizons on non-overlapping grids
    res = []
    for hz, col in [(24,"f24"),(72,"f72")]:
        s = d[d.pos_i % hz == 0][[col,"z24","jumpshare","eff"]].dropna()
        X = np.column_stack([np.ones(len(s)), s.z24, s.z24*s.eff])
        beta, *_ = np.linalg.lstsq(X, s[col].values, rcond=None)
        resid = s[col].values - X@beta
        cov = np.linalg.inv(X.T@X) * resid.var(ddof=3)
        tv = beta/np.sqrt(np.diag(cov))
        res.append({"h": hz, "n": len(s), "b_z_bp": beta[1]*1e4, "t_z": tv[1], "b_zXeff_bp": beta[2]*1e4, "t_zXeff": tv[2]})
    out["fwd_on_z24_and_efficiency"] = pd.DataFrame(res).round(2)
    # volume spikes: forward 24h return by vrel quintile, signed by last 24h direction
    s = d[d.pos_i % 24 == 0][["f24","vrel","z24"]].dropna().copy()
    s["sf"] = np.sign(s.z24) * s.f24
    s["vq"] = pd.qcut(s.vrel, 5, labels=False)
    out["signed_f24_by_volume_quintile"] = s.groupby("vq")["sf"].apply(tt).unstack().round(2)
    # book: position gain by hour held
    a = d[d.pos.abs() > 0]
    out["pos_gain_by_hour"] = a.groupby("hour")["pg"].apply(tt).unstack().round(2)
    out["share_bars_in_position"] = float((d.pos.abs()>0).mean())
    out["mean_pos_when_in"] = float(a.pos.mean())
    return out
