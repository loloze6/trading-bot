def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(20, min_periods=15).std()
            z = r1 / vol
            vr = b["volume"] / b["volume"].rolling(20, min_periods=15).mean()
            z3 = (c / c.shift(3) - 1) / (vol * np.sqrt(3))
            df = pd.DataFrame({
                "coin": coin, "win": w, "wd": ts.dt.weekday, "year": ts.dt.year,
                "pos": np.arange(len(b)), "r1": r1, "z": z, "z3": z3, "vr": vr, "vol": vol,
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1, "f5": c.shift(-5) / c - 1,
                "alloc": b["postRebalance_current_allocation"].astype(float)})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    for h in ["f1", "f2", "f5"]:
        d[h + "x"] = d[h] - d.groupby("coin")[h].transform("mean")
    out = {}
    def slope(sub, x, y):
        s = sub[[x, y]].dropna()
        if len(s) < 30: return (np.nan, np.nan, len(s))
        res = stats.linregress(s[x], s[y])
        return (res.slope, res.slope / res.stderr, len(s))
    # slope of fwd on z, by weekday of the move bar (events 7 days apart -> non-overlapping)
    t = []
    for wd in range(7):
        sub = d[d.wd == wd]
        a = slope(sub, "z", "f1x"); bb = slope(sub, "z", "f2x"); cc = slope(sub, "z", "f5x")
        t.append({"wd": wd, "n": a[2], "s_f1": a[0], "t_f1": a[1], "s_f2": bb[0], "t_f2": bb[1], "t_f5": cc[1],
                  "mean_f1x": sub.f1x.mean(), "t_meanf1": stats.ttest_1samp(sub.f1x.dropna(), 0).statistic,
                  "mean_vr": sub.vr.mean()})
    out["by_weekday_of_move"] = pd.DataFrame(t)
    # day-of-week of return day: mean daily return
    d["nwd"] = (d.wd + 1) % 7
    g = d.groupby("nwd")["f1"].agg(["mean", "std", "count"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["next_day_ret_by_weekday_of_that_day"] = g
    # all days, grid of 2: z quintiles -> f2x
    gr = d[d.pos % 2 == 0].dropna(subset=["z", "f2x"]).copy()
    gr["q"] = pd.qcut(gr.z, 5, labels=False)
    q = gr.groupby("q")["f2x"].agg(["mean", "count"])
    q["t"] = gr.groupby("q")["f2x"].apply(lambda s: s.mean() / (s.std() / np.sqrt(len(s))))
    out["z_quintile_f2x_grid2"] = q
    # z3 (3-day) quintiles -> f5x on grid 5
    gr5 = d[d.pos % 5 == 0].dropna(subset=["z3", "f5x"]).copy()
    gr5["q"] = pd.qcut(gr5.z3, 5, labels=False)
    q5 = gr5.groupby("q")["f5x"].agg(["mean", "count"])
    q5["t"] = gr5.groupby("q")["f5x"].apply(lambda s: s.mean() / (s.std() / np.sqrt(len(s))))
    out["z3_quintile_f5x_grid5"] = q5
    # vol level terciles: slope of f2x on z (grid2)
    gr["vq"] = gr.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["slope_by_vol_tercile"] = pd.DataFrame([dict(zip(["slope", "t", "n"], slope(gr[gr.vq == k], "z", "f2x")), vq=k) for k in range(3)])
    # volume ratio terciles: slope f2x on z (grid2)
    gr["vrq"] = pd.qcut(gr.vr, 3, labels=False)
    out["slope_by_volratio_tercile"] = pd.DataFrame([dict(zip(["slope", "t", "n"], slope(gr[gr.vrq == k], "z", "f2x")), vrq=k) for k in range(3)])
    # sunday: interaction low weekend volume
    sun = d[d.wd == 6].dropna(subset=["z", "f2x", "vr"]).copy()
    sun["vrq"] = pd.qcut(sun.vr, 3, labels=False)
    out["sunday_slope_by_volratio"] = pd.DataFrame([dict(zip(["slope", "t", "n"], slope(sun[sun.vrq == k], "z", "f2x")), vrq=k) for k in range(3)])
    # by year slope on all days grid2
    out["slope_by_year_grid2"] = pd.DataFrame([dict(zip(["slope", "t", "n"], slope(gr[gr.year == y], "z", "f2x")), year=y) for y in sorted(gr.year.unique())])
    # book: days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    dd = pd.concat(dd)
    dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
    bk = dd.groupby("day").agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    bk["wd"] = pd.to_datetime(bk.index).weekday
    out["book_by_weekday"] = bk.groupby("wd")[["book", "coin"]].agg(["mean", "count"])
    out["book_sharpe"] = float(bk.book.mean() / bk.book.std() * np.sqrt(365))
    return out
