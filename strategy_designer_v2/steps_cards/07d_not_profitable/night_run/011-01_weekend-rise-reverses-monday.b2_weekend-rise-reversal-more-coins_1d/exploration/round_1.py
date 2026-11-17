def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"].values
            n = len(b)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            nxt1 = np.r_[c[1:] / c[:-1] - 1, np.nan]
            nxt2 = np.full(n, np.nan); nxt2[:-2] = c[2:] / c[:-2] - 1
            d2 = np.full(n, np.nan); d2[:-2] = c[2:] / c[1:-1] - 1
            ret30 = pd.Series(c).pct_change(30).values
            vol = b["volume"].values
            vrel = vol / pd.Series(vol).rolling(28, min_periods=10).mean().values
            # weekend volume (sat+sun) relative
            alloc = b["postRebalance_current_allocation"].values
            gain = alloc * nxt1
            pv = b["postRebalance_total_value"].values
            tpv = b["total_portfolio_value"].values
            fee = np.r_[np.nan, (tpv - pv)[1:] / tpv[1:]] if True else None
            fee = (tpv - pv) / tpv
            df = pd.DataFrame({"coin": coin, "w": w, "wd": ts.dt.weekday.values, "r1": r1,
                               "n1": nxt1, "n2": nxt2, "d2": d2, "ret30": ret30, "vrel": vrel,
                               "fc": b["forecast"].values, "alloc": alloc, "gain": gain, "fee": fee,
                               "year": ts.dt.year.values})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    sun = A[A.wd == 6].dropna(subset=["r1", "n1"])
    out = {}
    # Monday return by weekend return quintile, all sundays
    sun["q"] = pd.qcut(sun.r1, 5, labels=False)
    out["sunday_quintile_next_mon_tue"] = sun.groupby("q").agg(r1=("r1", "mean"), mon=("n1", "mean"),
        tue=("d2", "mean"), mon_tue=("n2", "mean"), n=("n1", "size"))
    # comparison weekday: all days mean next-day return by quintile of r1
    A2 = A.dropna(subset=["r1", "n1"]).copy()
    A2["q"] = A2.groupby("wd")["r1"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["next_day_by_r1_quintile_and_weekday"] = A2.pivot_table(index="q", columns="wd", values="n1", aggfunc="mean")
    out["mean_next_day_by_weekday"] = A2.groupby("wd")["n1"].agg(["mean", "count"])
    # Book: gains on short days
    act = A[A.alloc.abs() > 1e-9]
    out["active_by_weekday"] = act.groupby("wd").agg(n=("gain", "size"), gain=("gain", "mean"), alloc=("alloc", "mean"))
    out["fees_total_vs_gain"] = pd.Series({"sum_gain": A.gain.sum(), "sum_fee": A.fee.sum(),
                                           "n_bars": len(A)})
    # Short Monday gain by trend state (coin's 30d return sign/terciles), by year
    s = sun[sun.r1 > 0].dropna(subset=["ret30"]).copy()
    s["t30"] = pd.qcut(s.ret30, 3, labels=["down", "mid", "up"])
    out["rose_sunday_next_by_30d_trend"] = s.groupby("t30").agg(mon=("n1", "mean"), mon_tue=("n2", "mean"),
        n=("n1", "size"), r30=("ret30", "mean"))
    s["vq"] = pd.qcut(s.vrel, 3, labels=["lowvol", "midvol", "highvol"])
    out["rose_sunday_next_by_volume"] = s.groupby("vq").agg(mon=("n1", "mean"), mon_tue=("n2", "mean"), n=("n1", "size"))
    out["rose_sunday_by_year"] = s.groupby("year").agg(mon=("n1", "mean"), mon_tue=("n2", "mean"), n=("n1", "size"))
    out["fell_sunday_by_30d_trend"] = sun[sun.r1 <= 0].dropna(subset=["ret30"]).assign(
        t30=lambda d: pd.qcut(d.ret30, 3, labels=["down", "mid", "up"])).groupby("t30").agg(
        mon=("n1", "mean"), mon_tue=("n2", "mean"), n=("n1", "size"))
    out["coin_mean_daily"] = A.n1.mean()
    return out
