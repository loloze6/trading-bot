def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    out = {}
    # 1) the 21:00-23:00 UTC block (bars starting 21 and 22) per day, and other blocks
    blk = []; mon = []
    for coin in bars:
        for w, b in bars[coin].items():
            ts = pd.to_datetime(b["timestamp"]).values
            c = b["close"].values.astype(float); n = len(c)
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            vol = pd.Series(r1).rolling(720, min_periods=500).std().values
            vrank = pd.Series(vol).rolling(2000, min_periods=500).rank(pct=True).values
            tsp = pd.to_datetime(ts); hour = tsp.hour.values; wd = tsp.weekday.values; yr = tsp.year.values
            # block: from close of bar starting 20 to close of bar starting 22
            for i in np.where(hour == 20)[0]:
                if i+2 < n and (ts[i+2]-ts[i]) == np.timedelta64(2,'h') and i-24 >= 0 and (ts[i]-ts[i-24]) == np.timedelta64(24,'h'):
                    g = c[i+2]/c[i]-1
                    p24 = c[i]/c[i-24]-1
                    # control block: from close of 18 to close of 20
                    ctl = c[i]/c[i-2]-1 if (ts[i]-ts[i-2]) == np.timedelta64(2,'h') else np.nan
                    blk.append((coin, w, yr[i], wd[i], g, p24, vol[i], ctl))
            for i in np.where(hour == 23)[0]:
                if (wd[i]+1) % 7 != 0: continue
                if i-48 < 0 or i+48 >= n: continue
                if (ts[i]-ts[i-48]) != np.timedelta64(48,'h') or (ts[i+48]-ts[i]) != np.timedelta64(48,'h'): continue
                mon.append((coin, w, yr[i], c[i]/c[i-48]-1, c[i+48]/c[i]-1, vol[i], vrank[i], b["forecast"].iloc[i]))
    B = pd.DataFrame(blk, columns=["coin","w","yr","wd","g","p24","vol","ctl"])
    B["gz"] = B.g/(B.vol*np.sqrt(2))
    def tt(s): s = s.dropna(); return pd.Series(dict(n=len(s), mean=s.mean(), t=s.mean()/(s.std()/np.sqrt(len(s)))))
    out["blk2122_by_coin"] = B.groupby("coin")["g"].apply(tt).unstack().reset_index()
    out["blk2122_by_year"] = B.groupby("yr")["g"].apply(tt).unstack().reset_index()
    out["blk2122_by_weekday"] = B.groupby("wd")["g"].apply(tt).unstack().reset_index()
    wm = B.groupby(["coin","w"])["g"].mean()
    out["blk2122_share_coinwindows_positive"] = pd.Series(dict(share=(wm > 0).mean(), n=len(wm)))
    B["vq"] = B.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"), 4, labels=False))
    out["blk2122_by_vol_quartile"] = B.groupby("vq").agg(n=("g","size"), mean=("g","mean"), mean_z=("gz","mean")).reset_index()
    B["pq"] = B.groupby("coin")["p24"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["blk2122_by_prior24h_quintile"] = B.groupby("pq").agg(n=("g","size"), mean_p24=("p24","mean"), mean=("g","mean")).reset_index()
    # 2) Monday: weekend return vs next 48h, by vol rank half (within-window rank) and by year
    M = pd.DataFrame(mon, columns=["coin","w","yr","p48","f48","vol","vrank","fc"])
    M["f48d"] = M.f48 - M.groupby("coin")["f48"].transform("mean")
    M["z"] = M.p48/(M.vol*np.sqrt(48)); M["y"] = M.f48d/(M.vol*np.sqrt(48))
    res = []
    for g, d in M.dropna(subset=["z","y"]).groupby("yr"):
        s = stats.linregress(d.z, d.y); res.append(dict(yr=g, n=len(d), slope=s.slope, t=s.slope/s.stderr,
            fall_short_move=-d[d.p48 < 0].f48d.mean()))
    out["monday_slope_by_year"] = pd.DataFrame(res)
    res = []
    M2 = M.dropna(subset=["z","y","vrank"])
    for g, d in M2.groupby(pd.cut(M2.vrank, [0, .33, .66, 1.0])):
        s = stats.linregress(d.z, d.y); res.append(dict(vrank=str(g), n=len(d), slope=s.slope, t=s.slope/s.stderr))
    out["monday_slope_by_vrank"] = pd.DataFrame(res)
    # 3) trades: gross by entry forecast and by year
    T = pd.concat([trades[c][w].assign(coin=c) for c in trades for w in trades[c] if len(trades[c][w])])
    T["fq"] = pd.cut(T.entry_forecast, [-21, -10, -5, -2, -0.5, 0.5, 21])
    out["trades_by_entry_forecast"] = T.groupby("fq").agg(n=("profit_loss_percent","size"), gross=("profit_loss_percent","mean"),
        dur_h=("duration_minutes", lambda s: s.mean()/60)).reset_index().astype(str)
    T["ewd"] = pd.to_datetime(T.entry_time).dt.weekday; T["eh"] = pd.to_datetime(T.entry_time).dt.hour
    out["trades_by_entry_weekday"] = T.groupby("ewd").agg(n=("profit_loss_percent","size"), gross=("profit_loss_percent","mean")).reset_index()
    # 4) Friday & Saturday daily coin return by coin and year
    dd = []
    for coin in days:
        for w, d in days[coin].items():
            d = d.copy(); d["wd"] = pd.to_datetime(d["day"]).dt.weekday; d["yr"] = pd.to_datetime(d["day"]).dt.year; d["coin"] = coin; dd.append(d)
    DD = pd.concat(dd).dropna(subset=["coin_return"])
    S = DD[DD.wd == 5]
    out["saturday_by_coin"] = S.groupby("coin")["coin_return"].apply(tt).unstack().reset_index()
    out["saturday_by_year"] = S.groupby("yr")["coin_return"].apply(tt).unstack().reset_index()
    return out
