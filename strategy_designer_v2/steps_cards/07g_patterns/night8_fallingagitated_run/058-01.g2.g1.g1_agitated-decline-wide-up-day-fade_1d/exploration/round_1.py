def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "r0": r, "sd": sd,
                "z0": r / sd,
                "rng": (b["high"] - b["low"]) / c / sd,
                "z3": (c / c.shift(3) - 1) / (sd * np.sqrt(3)),
                "z5": (c / c.shift(5) - 1) / (sd * np.sqrt(5)),
                "clpos": (c - b["low"]) / (b["high"] - b["low"]),
                "f1": c.shift(-1) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "inprof": b["regime"] != "chop",
                "alloc": b["postRebalance_current_allocation"],
                "pos": np.arange(len(b)),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    mu1 = d.groupby("coin")["f1"].mean()
    d["u1"] = d["f1"] - d["coin"].map(mu1)
    # 3-day non-overlap grid
    mu3 = d[d["pos"] % 3 == 0].groupby("coin")["f3"].mean()
    d["u3"] = d["f3"] - d["coin"].map(mu3)

    def ct(sub, col):
        s = sub.dropna(subset=[col])
        n = len(s)
        if n < 10:
            return pd.Series({"n": n, "mean": np.nan, "t": np.nan})
        m = s[col].mean()
        ds = (s[col] - m).groupby(s["day"]).sum()
        D = len(ds)
        se = np.sqrt(D / (D - 1) * (ds ** 2).sum()) / n
        return pd.Series({"n": n, "days": D, "mean": m, "t": m / se})

    out = {}
    g = []
    for ip in [True, False]:
        for up in [True, False]:
            s = d[(d.inprof == ip) & ((d.r0 > 0) == up)]
            x = ct(s, "u1"); x["inprof"] = ip; x["up"] = up; g.append(x)
    out["next1_by_profile_updown"] = pd.DataFrame(g)

    for ip in [True, False]:
        s = d[d.inprof == ip].dropna(subset=["z0", "u1"]).copy()
        s["q"] = pd.qcut(s["z0"], 5, labels=False)
        out[f"next1_by_z0_quintile_inprof{ip}"] = s.groupby("q").apply(lambda x: ct(x, "u1"))
        s["qr"] = pd.qcut(s["rng"], 5, labels=False)
        out[f"next1_by_range_quintile_inprof{ip}"] = s.groupby("qr").apply(lambda x: ct(x, "u1"))
    # brief's own: multi-day rise z3, 3-day horizon, grid
    s = d[(d.inprof) & (d.pos % 3 == 0)].dropna(subset=["z3", "u3"]).copy()
    s["q"] = pd.qcut(s["z3"], 5, labels=False)
    out["next3_by_z3_quintile_inprof_grid"] = s.groupby("q").apply(lambda x: ct(x, "u3"))
    s = d[(~d.inprof) & (d.pos % 3 == 0)].dropna(subset=["z3", "u3"]).copy()
    s["q"] = pd.qcut(s["z3"], 5, labels=False)
    out["next3_by_z3_quintile_outprof_grid"] = s.groupby("q").apply(lambda x: ct(x, "u3"))
    # close position on up days in profile
    s = d[d.inprof & (d.r0 > 0)].dropna(subset=["clpos", "u1"]).copy()
    s["q"] = pd.qcut(s["clpos"], 3, labels=False)
    out["inprof_up_next1_by_closepos_tercile"] = s.groupby("q").apply(lambda x: ct(x, "u1"))
    # weekday all bars
    out["next1_by_weekday_all"] = d.groupby("wd").apply(lambda x: ct(x, "u1"))
    out["share_inprof"] = float(d.inprof.mean())
    # book daily returns: largest
    dl = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            tt = t.copy(); tt["coin"] = coin; dl.append(tt)
    dd = pd.concat(dl)
    dd = dd[dd.book_return.abs() > 0]
    out["book_active_days_stats"] = dd.groupby("coin")["book_return"].agg(["count", "mean", "std"])
    return out
