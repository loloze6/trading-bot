def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            r = c.pct_change()  # return of this day's bar
            d = pd.DataFrame({
                "coin": coin, "w": w, "date": ts.dt.floor("D"),
                "wd": ts.dt.weekday, "year": ts.dt.year,
                "ret": r,
                "fwd1": c.shift(-1) / c - 1,
                "fwd5": c.shift(-5) / c - 1,
                "past4_lag1": c.shift(1) / c.shift(4) - 1,
                "past4": c / c.shift(4) - 1,
                "past1": r,
                "vol20": r.rolling(20, min_periods=15).std(),
                "pos": np.arange(len(b)),
                "low60": c.rolling(60, min_periods=40).min(),
                "high60": c.rolling(60, min_periods=40).max(),
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            d["fwd_wd"] = (d["wd"] + 1) % 7
            d["dist_low"] = c / d["low60"] - 1
            d["rng_pos"] = (c - d["low60"]) / (d["high60"] - d["low60"])
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    cm = D.groupby("coin")["fwd1"].transform("mean")
    D["ex1"] = D["fwd1"] - cm
    D["z1"] = D["ex1"] / D["vol20"]
    D["past4_lag1_z"] = D["past4_lag1"] / (D["vol20"] * 2)
    D["past4_z"] = D["past4"] / (D["vol20"] * 2)
    D["past1_z"] = D["past1"] / D["vol20"]

    def clslope(df, x, y):
        df = df[[x, y, "date"]].dropna()
        if len(df) < 50: return (np.nan, np.nan, len(df))
        X = np.column_stack([np.ones(len(df)), df[x].values])
        Y = df[y].values
        beta = np.linalg.lstsq(X, Y, rcond=None)[0]
        e = Y - X @ beta
        XtX = np.linalg.inv(X.T @ X)
        sc = pd.DataFrame(X * e[:, None]).groupby(df["date"].values).sum().values
        G = len(sc)
        V = XtX @ (sc.T @ sc) @ XtX * G / (G - 1)
        return (beta[1], beta[1] / np.sqrt(V[1, 1]), G)

    def daymean_t(df, y):
        s = df.groupby("date")[y].mean().dropna()
        return pd.Series({"mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))), "days": len(s)})

    out = {}
    # 1 weekday of the next day: mean excess
    out["next-day weekday mean excess"] = pd.DataFrame({k: daymean_t(g, "ex1") for k, g in D.groupby("fwd_wd")}).T
    # 2 slope of next-day z on past 4d (lag1) and past 4d (lag0), by next weekday
    res = []
    for k, g in D.groupby("fwd_wd"):
        a = clslope(g, "past4_lag1_z", "z1"); b2 = clslope(g, "past4_z", "z1"); c2 = clslope(g, "past1_z", "z1")
        res.append({"next_wd": k, "b_p4lag1": a[0], "t_p4lag1": a[1], "b_p4": b2[0], "t_p4": b2[1], "b_p1": c2[0], "t_p1": c2[1], "days": a[2]})
    out["slopes by next weekday"] = pd.DataFrame(res)
    # 3 all days pooled
    out["all days slopes"] = pd.DataFrame([dict(zip(["b", "t", "days"], clslope(D, x, "z1")), x=x) for x in ["past1_z", "past4_z", "past4_lag1_z"]])
    # 4 Saturday graded on sign side
    sat = D[D["fwd_wd"] == 5]
    out["saturday by midweek side"] = pd.DataFrame({
        "up": clslope(sat[sat.past4_lag1 > 0], "past4_lag1_z", "z1"),
        "down": clslope(sat[sat.past4_lag1 <= 0], "past4_lag1_z", "z1")}, index=["b", "t", "days"]).T
    # 5 prior-day move quintile -> next-day excess z
    D["q1"] = pd.qcut(D["past1_z"], 5, labels=False)
    out["next z by prior-day z quintile"] = pd.DataFrame({k: daymean_t(g, "z1") for k, g in D.groupby("q1")}).T
    # 6 vol tercile (vol relative to coin median)
    D["vrel"] = D["vol20"] / D.groupby("coin")["vol20"].transform("median")
    D["vq"] = pd.qcut(D["vrel"], 3, labels=False)
    out["next ex by vol tercile"] = pd.DataFrame({k: daymean_t(g, "ex1") for k, g in D.groupby("vq")}).T
    # 7 range position within 60d (brief's yearly-low angle, shortened): fwd5 nonoverlap
    g5 = D[D["pos"] % 5 == 0].copy()
    g5["ex5"] = g5["fwd5"] - g5.groupby("coin")["fwd5"].transform("mean")
    g5["rq"] = pd.qcut(g5["rng_pos"], 5, labels=False)
    out["5d ex by 60d range position quintile"] = pd.DataFrame({k: daymean_t(g, "ex5") for k, g in g5.groupby("rq")}).T
    out["5d slope on range position"] = pd.Series(dict(zip(["b", "t", "days"], clslope(g5, "rng_pos", "ex5"))))
    # 8 book by year and Saturday-pos gain
    days = []
    for coin, ws in data["days"].items():
        for w, dd in ws.items():
            x = dd.copy(); x["coin"] = coin; x["w"] = w; days.append(x)
    DD = pd.concat(days)
    DD["day"] = pd.to_datetime(DD["day"])
    bk = DD.groupby("day")["book_return"].mean().dropna()
    out["book by year"] = bk.groupby(bk.index.year).agg(["mean", "std", "count"]).assign(sharpe=lambda x: x["mean"] / x["std"] * np.sqrt(365))
    tr = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t): t = t.copy(); t["coin"] = coin; tr.append(t)
    T = pd.concat(tr)
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    T["yr"] = pd.to_datetime(T["entry_time"]).dt.year
    out["trades by year"] = T.groupby("yr")["net_profit_loss_percent"].agg(["count", "mean"])
    return out
