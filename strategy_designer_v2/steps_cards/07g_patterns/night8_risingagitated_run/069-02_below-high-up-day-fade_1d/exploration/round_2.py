def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            allr.append(b["close"].pct_change().shift(-1).dropna())
        mu = pd.concat(allr).mean()
        sdall = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            sdall.append(b["close"].pct_change().rolling(30, min_periods=25).std())
        medsd = pd.concat(sdall).median()
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            r = c.pct_change()
            sd20 = r.rolling(20, min_periods=15).std()
            hi20 = h.rolling(20, min_periods=15).max()
            df = pd.DataFrame({
                "coin": coin, "w": w, "day": b["timestamp"].dt.floor("D"),
                "r": r, "ex": r.shift(-1) - mu,
                "ex2": (c.shift(-2) / c - 1) - 2 * mu,
                "ex3": (c.shift(-3) / c - 1) - 3 * mu,
                "depth": (hi20 - c) / c / sd20,
                "rz": r / sd20,
                "tr60": c / c.shift(60) - 1,
                "tr30": c / c.shift(30) - 1,
                "agit": r.rolling(30, min_periods=25).std() > medsd,
                "alloc": b["postRebalance_current_allocation"],
                "pos_i": np.arange(len(b)),
            })
            rows.append(df)
    D = pd.concat(rows).dropna(subset=["ex", "r"])
    def ct(s, days):
        s = s.dropna(); days = days.loc[s.index] if False else days
        g = pd.DataFrame({"x": s.values - s.mean(), "d": days.values}).groupby("d")["x"].sum()
        n = len(g); se = np.sqrt((g**2).sum() * n / (n - 1)) / len(s)
        return s.mean() / se if se > 0 else np.nan
    def tab(sub, key, y="ex", q=3):
        sub = sub.dropna(subset=[key, y]).copy()
        sub["b"] = pd.qcut(sub[key], q, labels=False, duplicates="drop")
        out = []
        for k, g in sub.groupby("b"):
            out.append({"bin": k, "lo": g[key].min(), "hi": g[key].max(), "n": len(g),
                        "mean%": 100 * g[y].mean(), "t_day": ct(g[y], g["day"])})
        return pd.DataFrame(out)
    up = D[D.r > 0].copy()
    up["trend"] = np.where(up.tr60 > 0.1, "rising", np.where(up.tr60 < -0.1, "falling", np.where(up.tr60.notna(), "choppy", "na")))
    up["prof"] = up.trend + "_" + np.where(up.agit, "agit", "calm")
    res = {}
    out = []
    for p, g in up[up.trend != "na"].groupby("prof"):
        g = g.dropna(subset=["depth"])
        if len(g) < 60: 
            out.append({"prof": p, "n": len(g)}); continue
        q = g.depth.quantile([1/3, 2/3]).values
        d = g[g.depth > q[1]]; s = g[g.depth <= q[0]]
        out.append({"prof": p, "n": len(g), "all%": 100*g.ex.mean(), "deep%": 100*d.ex.mean(), "t_deep": ct(d.ex, d.day),
                    "shallow%": 100*s.ex.mean(), "deep_minus_shallow%": 100*(d.ex.mean()-s.ex.mean())})
    res["up_profile_deep_vs_shallow"] = pd.DataFrame(out)
    nr = up[up.trend == "falling"]
    res["falling_up_by_depth"] = tab(nr, "depth", q=4)
    res["notrising_up_by_depth"] = tab(up[up.trend.isin(["falling", "choppy"])], "depth", q=5)
    res["rising_up_by_depth"] = tab(up[up.trend == "rising"], "depth", q=4)
    # horizon: deep up days, 2 and 3 day (non-overlap not enforced on signals; cases sparse)
    u = up.dropna(subset=["depth"]).copy()
    u["dq"] = pd.qcut(u.depth, 5, labels=False)
    hz = []
    for k, g in u.groupby("dq"):
        hz.append({"dq": k, "n": len(g), "ex1%": 100*g.ex.mean(), "ex2%": 100*g.ex2.mean(), "t2": ct(g.ex2.dropna(), g.dropna(subset=["ex2"]).day),
                   "ex3%": 100*g.ex3.mean(), "t3": ct(g.ex3.dropna(), g.dropna(subset=["ex3"]).day)})
    res["up_depth_horizons"] = pd.DataFrame(hz)
    # depth x size of up day
    u["big"] = u.rz > u.rz.median()
    u["deep"] = u.depth > u.depth.median()
    res["up_deep_x_bigrise"] = u.groupby(["deep", "big"]).apply(lambda g: pd.Series({"n": len(g), "mean%": 100*g.ex.mean(), "t": ct(g.ex, g.day)}))
    # down days near high by trend
    dn = D[D.r < 0].copy()
    dn["trend"] = np.where(dn.tr60 > 0.1, "rising", np.where(dn.tr60 < -0.1, "falling", np.where(dn.tr60.notna(), "choppy", "na")))
    dn = dn.dropna(subset=["depth"])
    dn["shallow"] = dn.depth < dn.depth.quantile(0.3)
    res["down_shallow_by_trend"] = dn.groupby(["trend", "shallow"]).apply(lambda g: pd.Series({"n": len(g), "mean%": 100*g.ex.mean(), "t": ct(g.ex, g.day)}))
    # book: gain per bar by depth quintile of up days, in the held position
    u["bk_gain"] = u.alloc * (u.ex + 0)
    res["book_alloc_by_dq"] = u.groupby("dq")["alloc"].mean()
    return res
