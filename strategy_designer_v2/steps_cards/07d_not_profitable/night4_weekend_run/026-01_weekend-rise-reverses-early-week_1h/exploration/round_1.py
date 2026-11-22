def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].values.astype(float)
            n = len(c)
            r1 = pd.Series(c).pct_change()
            vol48 = r1.rolling(720, min_periods=200).std().values * np.sqrt(48)
            # anchor bars: bar stamped day d-1 23:00 closes at day d 00:00
            for i in range(n):
                t = ts.iloc[i]
                if t.hour != 23:
                    continue
                if i - 48 < 0 or i + 48 >= n:
                    continue
                if (ts.iloc[i + 48] - t) != pd.Timedelta(hours=48) or (t - ts.iloc[i - 48]) != pd.Timedelta(hours=48):
                    continue
                nextday = (t + pd.Timedelta(hours=1)).dayofweek  # 0=Monday
                past = c[i] / c[i - 48] - 1
                fwd = c[i + 48] / c[i] - 1
                p30 = c[i] / c[i - 720] - 1 if i - 720 >= 0 else np.nan
                rows.append((coin, w, nextday, past, fwd, vol48[i], p30, t.year))
    df = pd.DataFrame(rows, columns=["coin", "w", "dow", "past", "fwd", "vol", "p30", "year"])
    df["z"] = df["past"] / df["vol"]
    df = df.dropna(subset=["z"])
    out = {}
    # slope of fwd on past by anchor weekday (monday anchor = weekend move)
    g = []
    for d, s in df.groupby("dow"):
        # non-overlap: each anchor weekday is once per week -> fine
        sl = stats.linregress(s["past"], s["fwd"])
        up = s[s.past > 0]; dn = s[s.past <= 0]
        g.append(dict(dow=d, n=len(s), slope=sl.slope, t_slope=sl.slope / sl.stderr,
                      fwd_after_up=up.fwd.mean(), fwd_after_dn=dn.fwd.mean(), all_fwd=s.fwd.mean()))
    out["fwd48_on_past48_by_anchor_weekday(0=Mon)"] = pd.DataFrame(g)
    m = df[df.dow == 0].copy()
    m["zq"] = pd.qcut(m["z"], 5, labels=False)
    out["monday_by_weekend_z_quintile"] = m.groupby("zq").agg(n=("fwd", "size"), z=("z", "mean"), past=("past", "mean"), fwd=("fwd", "mean"), fwd_sd=("fwd", "std"))
    m["trend"] = np.where(m.p30 > 0, "30d_up", "30d_down")
    tt = []
    for k, s in m.dropna(subset=["p30"]).groupby("trend"):
        sl = stats.linregress(s["past"], s["fwd"])
        u = s[s.past > 0]
        tt.append(dict(trend=k, n=len(s), slope=sl.slope, t=sl.slope / sl.stderr, fwd_after_up=u.fwd.mean(), n_up=len(u), fwd_after_dn=s[s.past <= 0].fwd.mean()))
    out["monday_by_30d_trend"] = pd.DataFrame(tt)
    m["vq"] = pd.qcut(m["vol"], 3, labels=["lowvol", "mid", "highvol"])
    vv = []
    for k, s in m.groupby("vq"):
        sl = stats.linregress(s["past"], s["fwd"])
        vv.append(dict(vol=k, n=len(s), slope=sl.slope, t=sl.slope / sl.stderr, fwd_after_up=s[s.past > 0].fwd.mean()))
    out["monday_by_vol_tercile"] = pd.DataFrame(vv)
    cc = []
    for k, s in m.groupby("coin"):
        sl = stats.linregress(s["past"], s["fwd"])
        cc.append(dict(coin=k, n=len(s), slope=sl.slope, t=sl.slope / sl.stderr, fwd_after_up=s[s.past > 0].fwd.mean(), fwd_after_dn=s[s.past <= 0].fwd.mean()))
    out["monday_by_coin"] = pd.DataFrame(cc)
    yy = []
    for k, s in m.groupby("year"):
        sl = stats.linregress(s["past"], s["fwd"])
        yy.append(dict(year=k, n=len(s), slope=sl.slope, t=sl.slope / sl.stderr, fwd_after_up=s[s.past > 0].fwd.mean()))
    out["monday_by_year"] = pd.DataFrame(yy)
    # book: daily returns, drift part
    br = []; cr = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            br.append(d["book_return"].dropna()); cr.append(d["coin_return"].dropna())
    br = pd.concat(br); cr = pd.concat(cr)
    out["book"] = pd.Series(dict(book_mean=br.mean(), book_sd=br.std(), coin_mean=cr.mean()))
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            tr.append(t)
    tr = pd.concat(tr)
    out["trades"] = pd.Series(dict(n=len(tr), mean_pl=tr.profit_loss_percent.mean(), mean_net=tr.net_profit_loss_percent.mean(), win=(tr.profit_loss_percent > 0).mean(), mean_hours=tr.duration_minutes.mean() / 60))
    return out
