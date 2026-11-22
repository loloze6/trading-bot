def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    rows = []      # weekday-start 48h past vs next 48h, start at 00:00 close
    hrs = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"])
            b["ts"] = ts
            c = b["close"].values.astype(float)
            t = ts.values
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            vol = pd.Series(r1).rolling(720, min_periods=500).std().values
            n = len(b)
            hour = ts.dt.hour.values; wd = ts.dt.weekday.values
            # bars whose close is 00:00 -> start hour 23
            idx = np.where(hour == 23)[0]
            for i in idx:
                if i-48 < 0 or i+48 >= n: continue
                if (t[i]-t[i-48]) != np.timedelta64(48,'h') or (t[i+48]-t[i]) != np.timedelta64(48,'h'): continue
                closewd = (wd[i]+1) % 7  # weekday of the close day
                p48 = c[i]/c[i-48]-1; f48 = c[i+48]/c[i]-1
                f24 = c[i+24]/c[i]-1 if (t[i+24]-t[i]) == np.timedelta64(24,'h') else np.nan
                p24 = c[i]/c[i-24]-1
                rows.append((coin, w, closewd, p48, p24, f48, f24, vol[i], b["forecast"].iloc[i]))
            # hourly returns by hour, daily returns by weekday (non-overlap)
            hrs.append(pd.DataFrame({"coin": coin, "hour": hour, "wd": wd, "r": r1}))
    D = pd.DataFrame(rows, columns=["coin","w","closewd","p48","p24","f48","f24","vol","fc"])
    # demean forward by coin mean f48 over all
    D["f48d"] = D["f48"] - D.groupby("coin")["f48"].transform("mean")
    D["f24d"] = D["f24"] - D.groupby("coin")["f24"].transform("mean")
    D["z"] = D["p48"] / (D["vol"]*np.sqrt(48))
    out = {}
    # regression of next 48h on past 48h (standardised) by closing weekday
    res = []
    for g, d in D.dropna(subset=["z","f48d"]).groupby("closewd"):
        y = d["f48d"]/(d["vol"]*np.sqrt(48)); x = d["z"]
        sl = stats.linregress(x, y)
        dn = d[d.p48 < 0]; up = d[d.p48 > 0]
        res.append(dict(closewd=g, n=len(d), slope=sl.slope, t=sl.slope/sl.stderr,
                        mean_f48d_after_fall=dn.f48d.mean(), t_fall=stats.ttest_1samp(dn.f48d,0).statistic,
                        mean_f48d_after_rise=up.f48d.mean(), t_rise=stats.ttest_1samp(up.f48d,0).statistic))
    out["next48_on_past48_by_close_weekday(0=Mon)"] = pd.DataFrame(res)
    # Monday close: by vol tercile (per coin) and sign
    M = D[D.closewd == 0].dropna(subset=["vol","f48d"]).copy()
    M["vt"] = M.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    M["sign"] = np.where(M.p48 < 0, "fall", "rise")
    out["monday_by_voltercile_sign"] = M.groupby(["vt","sign"]).agg(n=("f48d","size"), mean_f48d=("f48d","mean"),
        mean_f24d=("f24d","mean"), mean_p48=("p48","mean")).reset_index()
    M["zq"] = M.groupby("coin")["z"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["monday_by_weekend_z_quintile"] = M.groupby("zq").agg(n=("f48d","size"), mean_z=("z","mean"),
        mean_f24d=("f24d","mean"), mean_f48d=("f48d","mean")).reset_index()
    out["monday_by_coin"] = M.groupby("coin").apply(lambda d: pd.Series(dict(n=len(d),
        slope_t=(lambda s: s.slope/s.stderr)(stats.linregress(d.z, d.f48d/(d.vol*np.sqrt(48)))),
        fall_f48d=d[d.p48<0].f48d.mean(), rise_f48d=d[d.p48>0].f48d.mean()))).reset_index()
    H = pd.concat(hrs).dropna()
    hh = H.groupby("hour")["r"].agg(["mean","std","count"]); hh["t"] = hh["mean"]/(hh["std"]/np.sqrt(hh["count"]))
    out["hourly_return_by_hour"] = hh[["mean","t"]].reset_index()
    # days: by weekday
    dd = []
    for coin in days:
        for w, d in days[coin].items():
            d = d.copy(); d["wd"] = pd.to_datetime(d["day"]).dt.weekday; d["coin"] = coin; dd.append(d)
    DD = pd.concat(dd).dropna(subset=["coin_return"])
    g = DD.groupby("wd").agg(coin_mean=("coin_return","mean"), coin_sd=("coin_return","std"), n=("coin_return","size"),
                             book_mean=("book_return","mean"), book_sd=("book_return","std"))
    g["coin_t"] = g.coin_mean/(g.coin_sd/np.sqrt(g.n)); g["book_t"] = g.book_mean/(g.book_sd/np.sqrt(g.n))
    out["daily_by_weekday"] = g.reset_index()
    # trades
    T = pd.concat([trades[c][w].assign(coin=c) for c in trades for w in trades[c] if len(trades[c][w])])
    out["trades_by_side"] = T.groupby("side").agg(n=("net_profit_loss_percent","size"), gross=("profit_loss_percent","mean"),
        net=("net_profit_loss_percent","mean"), dur_h=("duration_minutes", lambda s: s.mean()/60)).reset_index()
    out["trades_by_coin"] = T.groupby("coin").agg(n=("net_profit_loss_percent","size"), gross=("profit_loss_percent","mean"),
        net=("net_profit_loss_percent","mean")).reset_index()
    # allocation during short
    A = []
    for coin in bars:
        for w, b in bars[coin].items():
            a = b["postRebalance_current_allocation"]; A.append(a[a != 0].abs())
    A = pd.concat(A)
    out["abs_alloc_when_in"] = pd.Series(dict(mean=A.mean(), median=A.median(), share_bars_in=len(A)/sum(len(b) for c in bars for b in bars[c].values())))
    return out
