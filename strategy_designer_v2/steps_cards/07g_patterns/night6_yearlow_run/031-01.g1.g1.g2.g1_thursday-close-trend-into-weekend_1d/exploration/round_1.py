def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float).values
            n = len(c)
            df = pd.DataFrame({"coin": coin, "win": w, "date": ts.dt.floor("D"),
                               "wd_next": ((ts + pd.Timedelta(days=1)).dt.weekday).values,
                               "pos": np.arange(n)})
            s = pd.Series(c)
            df["r1"] = s.pct_change()
            df["r14"] = s / s.shift(14) - 1
            df["z14"] = ((df["r14"] - df["r14"].rolling(60, min_periods=20).mean()) /
                         df["r14"].rolling(60, min_periods=20).std()).clip(-2, 2)
            df["vol20"] = df["r1"].rolling(20).std()
            for h in (1, 2, 5):
                df[f"f{h}"] = s.shift(-h) / s - 1
            lo60 = s.rolling(60, min_periods=30).min()
            hi60 = s.rolling(60, min_periods=30).max()
            df["dlow"] = (s / lo60 - 1)
            df["rng"] = (s - lo60) / (hi60 - lo60)
            df["newlow"] = (s < s.shift(1).rolling(60, min_periods=30).min()).astype(float)
            df["alloc"] = b["postRebalance_current_allocation"].astype(float).values
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    # coin mean 2-bar and 1,5-bar returns on grid
    for h in (1, 2, 5):
        g = D[D["pos"] % h == 0]
        m = g.groupby("coin")[f"f{h}"].mean()
        sd = g.groupby("coin")[f"f{h}"].std()
        D[f"x{h}"] = (D[f"f{h}"] - D["coin"].map(m)) / D["coin"].map(sd)
    out = {}
    # slope of 2-day fwd on z14 by weekday of next bar (one per week per weekday: non overlapping)
    res = []
    for wd in range(7):
        g = D[(D["wd_next"] == wd)].dropna(subset=["z14", "x2"])
        # cluster by date: sum product per date
        X = g["z14"] - g["z14"].mean()
        beta = (X * g["x2"]).sum() / (X ** 2).sum()
        e = g["x2"] - g["x2"].mean() - beta * X
        sc = (X * e).groupby(g["date"]).sum()
        se = np.sqrt((sc ** 2).sum()) / (X ** 2).sum()
        res.append({"next_wd": wd, "slope_x2_per_z": beta, "t_clu": beta / se, "days": g["date"].nunique(), "n": len(g),
                    "mean_x2": g["x2"].mean()})
    out["slope_by_next_weekday_2d"] = pd.DataFrame(res)
    # mean 1-day return by weekday of the day (next bar weekday), in usual-move units
    g = D.dropna(subset=["x1"])
    out["x1_by_weekday"] = g.groupby("wd_next")["x1"].agg(["mean", "count", lambda v: v.mean()/v.std()*np.sqrt(len(v))])
    # after large daily moves: next day and 5d by r1 decile normalised by vol
    g = D.dropna(subset=["r1", "vol20", "x1", "x5"]).copy()
    g["r1z"] = g["r1"] / g["vol20"]
    g["dec"] = pd.qcut(g["r1z"], 10, labels=False)
    g5 = g[g["pos"] % 5 == 0]
    out["after_daily_move_decile"] = pd.concat([g.groupby("dec")["x1"].agg(["mean", "count"]),
                                                g5.groupby("dec")["x5"].agg(["mean", "count"]).add_suffix("_5d")], axis=1)
    # position in 60-day range quintile -> 5 day
    g = D[(D["pos"] % 5 == 0)].dropna(subset=["rng", "x5", "x2"])
    g["q"] = pd.qcut(g["rng"], 5, labels=False, duplicates="drop")
    out["range_pos_quintile_x5"] = g.groupby("q")["x5"].agg(["mean", "count", lambda v: v.mean()/v.std()*np.sqrt(len(v))])
    g = D[(D["pos"] % 5 == 0)].dropna(subset=["x5"])
    out["new60low_x5"] = g.groupby("newlow")["x5"].agg(["mean", "count", lambda v: v.mean()/v.std()*np.sqrt(len(v))])
    # vol tercile: z14 slope on x5 grid
    g = D[(D["pos"] % 5 == 0)].dropna(subset=["z14", "x5", "vol20"]).copy()
    g["vt"] = pd.qcut(g["vol20"], 3, labels=False)
    out["z14_x5_corr_by_vol"] = g.groupby("vt").apply(lambda d: pd.Series({"r": d["z14"].corr(d["x5"]), "n": len(d), "t": d["z14"].corr(d["x5"])*np.sqrt(len(d)-2)}))
    out["z14_x5_all"] = pd.Series({"r": g["z14"].corr(g["x5"]), "n": len(g)})
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            d["wd"] = pd.to_datetime(d["day"]).dt.weekday
            dd.append(d)
    DD = pd.concat(dd).dropna(subset=["book_return"])
    out["book_by_weekday"] = DD.groupby("wd")["book_return"].agg(["mean", "std", "count"])
    out["book_by_year"] = DD.assign(y=pd.to_datetime(DD["day"]).dt.year).groupby("y")["book_return"].agg(["mean", "count"])
    out["book_by_coin"] = DD.groupby("coin")["book_return"].agg(["mean", "count"])
    # trades: long vs short
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    out["trades_side"] = T.groupby("side")["net_profit_loss_percent"].agg(["mean", "count", "std"])
    return out
