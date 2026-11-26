def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({
                "coin": coin, "win": w, "day": ts.dt.floor("D"), "yr": ts.dt.year,
                "r0": r, "sd": sd, "z0": r / sd,
                "rng": (b["high"] - b["low"]) / c / sd,
                "wick": (b["high"] - c) / c / sd,
                "lwick": (c - b["low"]) / c / sd,
                "f1": c.shift(-1) / c - 1,
                "f2": c.shift(-2) / c - 1,
                "inprof": b["regime"] != "chop",
                "alloc": b["postRebalance_current_allocation"],
                "pos": np.arange(len(b))}))
    d = pd.concat(rows, ignore_index=True)
    d["u1"] = d["f1"] - d["coin"].map(d.groupby("coin")["f1"].mean())
    d["u2"] = d["f2"] - d["coin"].map(d[d.pos % 2 == 0].groupby("coin")["f2"].mean())
    def ct(s, col):
        s = s.dropna(subset=[col]); n = len(s)
        if n < 10: return pd.Series({"n": n})
        m = s[col].mean(); ds = (s[col] - m).groupby(s["day"]).sum(); D = len(ds)
        return pd.Series({"n": n, "days": D, "mean": m, "t": m / (np.sqrt(D/(D-1)*(ds**2).sum())/n)})
    out = {}
    p = d[d.inprof].dropna(subset=["z0", "u1", "wick"]).copy()
    up = p[p.r0 > 0].copy()
    up["qw"] = pd.qcut(up.wick, 4, labels=False)
    out["inprof_up_next1_by_upperwick_quartile"] = up.groupby("qw").apply(lambda x: ct(x, "u1"))
    up["ql"] = pd.qcut(up.lwick, 4, labels=False)
    out["inprof_up_next1_by_lowerwick_quartile"] = up.groupby("ql").apply(lambda x: ct(x, "u1"))
    up["wh"] = up.wick > up.wick.median()
    out["inprof_up_wickhi_by_year"] = up.groupby(["wh", "yr"]).apply(lambda x: ct(x, "u1"))
    # out of profile: upper wick on up days
    o = d[(~d.inprof) & (d.r0 > 0)].dropna(subset=["wick", "u1"]).copy()
    o["qw"] = pd.qcut(o.wick, 4, labels=False)
    out["outprof_up_next1_by_upperwick_quartile"] = o.groupby("qw").apply(lambda x: ct(x, "u1"))
    # all days in profile, graded by upper wick (any day)
    p["qw"] = pd.qcut(p.wick, 4, labels=False)
    out["inprof_all_next1_by_upperwick_quartile"] = p.groupby("qw").apply(lambda x: ct(x, "u1"))
    # book: gain by up-day range quartile (pnl of position)
    up["pnl"] = up.alloc * up.f1
    up["qr"] = pd.qcut(up.rng, 4, labels=False)
    out["book_pnl_by_range_quartile"] = up.groupby("qr")["pnl"].agg(["count", "mean", "sum"])
    out["book_pnl_by_wick_quartile"] = up.groupby("qw")["pnl"].agg(["count", "mean", "sum"])
    return out
