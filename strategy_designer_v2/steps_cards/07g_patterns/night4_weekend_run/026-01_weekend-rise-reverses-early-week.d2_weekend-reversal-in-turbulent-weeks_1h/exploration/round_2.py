def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    mon = []; hrs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            b["ts"] = pd.to_datetime(b["timestamp"], utc=True) + pd.Timedelta(hours=1)
            b = b.set_index("ts"); b = b[~b.index.duplicated()]
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(720, min_periods=200).std()
            vrank = vol.rolling(4320, min_periods=500).apply(lambda a: (a[:-1] < a[-1]).mean() if len(a) > 1 else np.nan, raw=True)
            z = c[c.index.hour == 0]
            full = z.reindex(pd.date_range(z.index.min(), z.index.max(), freq="1D", tz="UTC"))
            df = pd.DataFrame({"prev": full / full.shift(2) - 1, "next": full.shift(-2) / full - 1,
                               "wd": full.index.weekday, "vol": vol.reindex(full.index),
                               "vrank": vrank.reindex(full.index), "coin": coin, "win": w,
                               "year": full.index.year})
            mon.append(df.dropna(subset=["prev", "next", "vol"]))
            fwd4 = c.shift(-4) / c - 1
            fwd24 = c.shift(-24) / c - 1
            h = pd.DataFrame({"r": r1, "rs": r1 / vol, "rnext": r1.shift(-1), "f4": fwd4, "f24": fwd24,
                              "hour": c.index.hour, "wd": c.index.weekday, "year": c.index.year,
                              "vrank": vrank, "coin": coin, "pos": np.arange(len(c))})
            hrs.append(h.dropna(subset=["rs", "rnext"]))
    D = pd.concat(mon)
    D["z"] = D["prev"] / (D["vol"] * np.sqrt(48)); D["nz"] = D["next"] / (D["vol"] * np.sqrt(48))
    M = D[(D.wd == 0)].dropna(subset=["vrank"]).copy()
    M["vr_bin"] = pd.cut(M["vrank"], [-0.01, 0.25, 0.5, 0.75, 1.01], labels=False)
    res = []
    for vb, g in M.groupby("vr_bin"):
        sl = stats.linregress(g.z, g.nz)
        up = g[g.z > 0]["next"]; dn = g[g.z < 0]["next"]
        res.append({"vrank_bin": vb, "n": len(g), "slope": sl.slope, "t": sl.slope / sl.stderr,
                    "next_after_up": up.mean(), "t_up": up.mean() / (up.std() / np.sqrt(len(up))),
                    "next_after_dn": dn.mean(), "t_dn": dn.mean() / (dn.std() / np.sqrt(len(dn)))})
    out["monday_by_vrank_quarter"] = pd.DataFrame(res)
    # same for other weekdays, low vrank only (weekday comparison)
    res = []
    for wd, g in D.dropna(subset=["vrank"]).groupby("wd"):
        for lo, gg in g.groupby(g.vrank < 0.5):
            sl = stats.linregress(gg.z, gg.nz)
            res.append({"wd": wd, "low_vrank": lo, "n": len(gg), "slope": sl.slope, "t": sl.slope / sl.stderr})
    out["slope_by_weekday_vrank_half"] = pd.DataFrame(res)
    out["monday_slope_by_year"] = M.groupby("year").apply(lambda g: pd.Series({"n": len(g),
        "slope": stats.linregress(g.z, g.nz).slope, "t": stats.linregress(g.z, g.nz).slope / stats.linregress(g.z, g.nz).stderr}))
    H = pd.concat(hrs)
    # hours 22-23 close: 2h return from 21:00 close to 23:00 close, one per day
    H["late"] = H["hour"].isin([22, 23])
    L = H[H.late].groupby(["coin", "year"])["r"].agg(["mean", "count"])
    out["late_hours_mean_by_year"] = H[H.late].groupby("year")["r"].agg(
        mean="mean", t=lambda s: s.mean() / (s.std() / np.sqrt(len(s))), n="count")
    out["late_hours_mean_by_coin"] = H[H.late].groupby("coin")["r"].agg(
        mean="mean", t=lambda s: s.mean() / (s.std() / np.sqrt(len(s))), n="count")
    out["saturday_hourly_by_year"] = H[H.wd == 5].groupby("year")["r"].agg(
        mean="mean", t=lambda s: s.mean() / (s.std() / np.sqrt(len(s))))
    # 1h drop reversal: next 4h and 24h after large 1h drops, non-overlapping-ish: take events spaced
    H["q"] = pd.qcut(H["rs"], 20, labels=False)
    ev = H[H.q == 0]
    out["after_big_1h_drop_by_year"] = ev.groupby("year").agg(n=("rnext", "size"), next1=("rnext", "mean"),
        f4=("f4", "mean"), f24=("f24", "mean"))
    out["after_big_1h_drop_by_coin"] = ev.groupby("coin").agg(n=("rnext", "size"), next1=("rnext", "mean"),
        f4=("f4", "mean"), f24=("f24", "mean"))
    allb = H.groupby("q").agg(next1=("rnext", "mean"), f4=("f4", "mean"), f24=("f24", "mean"), n=("f4", "size"))
    out["fwd_by_1h_move_vingtile"] = allb
    ev2 = ev.dropna(subset=["f4"])
    out["big_drop_f4_t"] = float(ev2.f4.mean() / (ev2.f4.std() / np.sqrt(len(ev2))))
    out["big_drop_by_vrank_half"] = ev.dropna(subset=["vrank"]).groupby(ev.vrank >= 0.5).agg(
        n=("f4", "size"), next1=("rnext", "mean"), f4=("f4", "mean"), f24=("f24", "mean"))
    # trades by duration
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    T["dur_h"] = T["duration_minutes"] / 60
    T["db"] = pd.cut(T["dur_h"], [-1, 2, 47, 49, 200, 1e5])
    out["trades_by_duration"] = T.groupby("db").agg(n=("dur_h", "size"), gross=("profit_loss_percent", "mean"),
        net=("net_profit_loss_percent", "mean"), sum_net=("net_profit_loss_percent", "sum"))
    return out
