def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            d = pd.DataFrame({
                "coin": coin, "w": w, "ts": pd.to_datetime(b["timestamp"]),
                "regime": b["regime"].astype(str),
                "r1": r1, "r3": c.pct_change(3), "r5": c.pct_change(5),
                "sd30": sd30,
                "wick": (h - c) / c / sd30,
                "lwick": (c - l) / c / sd30,
                "rng": (h - l) / c / sd30,
                "clv": (c - l) / (h - l).replace(0, np.nan),
                "f1": c.shift(-1) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "pos": np.arange(len(b)),
                "alloc": b["postRebalance_current_allocation"],
            })
            d["z1"] = d["r1"] / d["sd30"]
            d["z3"] = d["r3"] / (d["sd30"] * np.sqrt(3))
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu1 = D.groupby("coin")["f1"].transform("mean")
    D["x1"] = D["f1"] - D.groupby("coin")["r1"].transform("mean")
    D["x3"] = D["f3"] - 3 * D.groupby("coin")["r1"].transform("mean")
    D["day"] = D["ts"].dt.floor("D")
    D["inprof"] = D["regime"] != "chop"

    def ct(s, days):
        g = pd.DataFrame({"v": s - s.mean() + s.mean(), "d": days}).dropna()
        if len(g) < 5: return (np.nan, len(g), 0)
        m = g["v"].mean()
        dev = (g["v"] - m).groupby(g["d"]).sum()
        n = len(g); D_ = len(dev)
        se = np.sqrt((dev ** 2).sum() * D_ / max(D_ - 1, 1)) / n
        return (m, n, m / se if se > 0 else np.nan, D_)

    out = {}
    def tab(sub, col, target, q=5, name=None):
        s = sub.dropna(subset=[col, target]).copy()
        if len(s) < 30: return None
        s["b"] = pd.qcut(s[col].rank(method="first"), q, labels=False)
        res = []
        for k, g in s.groupby("b"):
            m, n, t, nd = ct(g[target], g["day"])
            res.append({"bin": k, "mean_x": g[col].mean(), "mean_target": m, "n": n, "t": t})
        return pd.DataFrame(res)

    P = D[D["inprof"]]
    O = D[~D["inprof"]]
    out["share_in_profile"] = D["inprof"].mean()
    out["prof_n"] = len(P)
    out["prof_z1_vs_x1"] = tab(P, "z1", "x1")
    out["prof_z3_vs_x1"] = tab(P, "z3", "x1")
    P3 = P[P["pos"] % 3 == 0]
    out["prof_z3_vs_x3_nonoverlap"] = tab(P3, "z3", "x3")
    out["prof_wick_vs_x1"] = tab(P, "wick", "x1")
    out["prof_clv_vs_x1"] = tab(P, "clv", "x1")
    out["prof_rng_vs_x1"] = tab(P, "rng", "x1")
    out["out_z1_vs_x1"] = tab(O, "z1", "x1")
    out["out_clv_vs_x1"] = tab(O, "clv", "x1")
    out["out_rng_vs_x1"] = tab(O, "rng", "x1")
    # brief situation: up day with r3>0 in profile
    up = P[(P["r1"] > 0) & (P["r3"] > 0)]
    out["prof_up_r3pos_x1"] = pd.Series(ct(up["x1"], up["day"]), index=["m", "n", "t", "days"])
    up3 = up[up["pos"] % 3 == 0]
    out["prof_up_r3pos_x3"] = pd.Series(ct(up3["x3"], up3["day"]), index=["m", "n", "t", "days"])
    dn = P[(P["r1"] < 0)]
    out["prof_down_x1"] = pd.Series(ct(dn["x1"], dn["day"]), index=["m", "n", "t", "days"])
    # weekday in and out of profile
    wk = []
    for nm, S in [("in", P), ("out", O)]:
        for k, g in S.groupby(S["ts"].dt.weekday):
            m, n, t, nd = ct(g["x1"], g["day"])
            wk.append({"set": nm, "wd": k, "m": m, "n": n, "t": t})
    out["weekday_x1"] = pd.DataFrame(wk)
    # by year in profile
    yr = []
    for k, g in P.groupby(P["ts"].dt.year):
        m, n, t, nd = ct(g["x1"], g["day"])
        yr.append({"year": k, "m": m, "n": n, "t": t})
    out["prof_year_x1"] = pd.DataFrame(yr)
    # book: largest days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    DD = pd.concat(dd)
    bk = DD.groupby("day")["book_return"].mean().dropna()
    out["book_days"] = pd.Series({"n": len(bk), "mean": bk.mean(), "sd": bk.std(),
                                  "top10_sum": bk.nlargest(10).sum(), "bot10_sum": bk.nsmallest(10).sum(),
                                  "total_sum": bk.sum()})
    act = D[D["alloc"].fillna(0) != 0]
    out["active_by_year"] = act.groupby(act["ts"].dt.year).apply(lambda g: pd.Series({"n": len(g), "gain": (g["alloc"] * g["f1"]).mean()}))
    return out
