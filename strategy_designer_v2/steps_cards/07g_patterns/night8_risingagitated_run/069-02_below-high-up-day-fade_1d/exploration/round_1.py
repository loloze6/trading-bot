def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; r = c.pct_change()
            allr.append(r.shift(-1).dropna())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]
            r = c.pct_change()
            sd20 = r.rolling(20, min_periods=15).std()
            hi20 = h.rolling(20, min_periods=15).max(); lo20 = l.rolling(20, min_periods=15).min()
            df = pd.DataFrame({
                "coin": coin, "w": w, "day": b["timestamp"].dt.floor("D"),
                "wd": b["timestamp"].dt.dayofweek,
                "r": r, "nxt": r.shift(-1), "ex": r.shift(-1) - mu,
                "depth": (hi20 - c) / c / sd20,
                "pos": (c - lo20) / (hi20 - lo20),
                "rz": r / sd20,
                "clv": (c - l) / (h - l),
                "tr20": c / c.shift(20) - 1,
                "tr40": c / c.shift(40) - 1,
                "volr": sd20 / r.rolling(60, min_periods=40).std(),
                "alloc": b["postRebalance_current_allocation"],
                "bk": b["postRebalance_total_value"].pct_change().shift(-1),
            })
            rows.append(df)
    D = pd.concat(rows).dropna(subset=["nxt", "r"])
    def ct(s, days):
        g = pd.DataFrame({"x": s.values - s.mean(), "d": days.values}).groupby("d")["x"].sum()
        n = len(g); se = np.sqrt((g**2).sum() * n / (n - 1)) / len(s)
        return s.mean() / se if se > 0 else np.nan
    def tab(sub, key, q=5):
        sub = sub.dropna(subset=[key, "ex"]).copy()
        sub["b"] = pd.qcut(sub[key], q, labels=False, duplicates="drop")
        out = []
        for k, g in sub.groupby("b"):
            out.append({"bin": k, "lo": g[key].min(), "hi": g[key].max(), "n": len(g),
                        "mean_ex%": 100 * g["ex"].mean(), "t_day": ct(g["ex"], g["day"])})
        return pd.DataFrame(out)
    up = D[D.r > 0]; dn = D[D.r < 0]
    res = {}
    res["up_by_depth"] = tab(up, "depth")
    res["down_by_depth"] = tab(dn, "depth")
    res["up_by_pos20"] = tab(up, "pos")
    res["down_by_pos20"] = tab(dn, "pos")
    res["all_by_rz"] = tab(D, "rz", 10)
    res["up_by_clv"] = tab(up, "clv")
    res["down_by_clv"] = tab(dn, "clv")
    res["up_by_tr40"] = tab(up, "tr40")
    res["up_by_volr"] = tab(up, "volr")
    res["all_by_volr"] = tab(D, "volr")
    # depth effect by trend sign
    u2 = up.dropna(subset=["depth", "tr40"]).copy()
    u2["deep"] = u2.groupby("coin")["depth"].transform(lambda s: s > s.median())
    u2["trend"] = np.where(u2.tr40 > 0.1, "rising", np.where(u2.tr40 < -0.1, "falling", "choppy"))
    res["up_trend_x_deep"] = u2.groupby(["trend", "deep"])["ex"].agg(["count", lambda s: 100 * s.mean()])
    res["wd_all"] = D.groupby("wd")["ex"].agg(["count", lambda s: 100 * s.mean(), lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    res["by_coin_up_depth_corr"] = up.dropna(subset=["depth"]).groupby("coin").apply(lambda g: pd.Series({"n": len(g), "rho": stats.spearmanr(g.depth, g.ex)[0]}))
    res["by_window_up_deep_minus_shallow"] = u2.groupby("w").apply(lambda g: 100 * (g[g.deep].ex.mean() - g[~g.deep].ex.mean()))
    # book: daily returns by coin, by year
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, w=w))
    dd = pd.concat(dd)
    dd["yr"] = pd.to_datetime(dd["day"]).dt.year
    res["book_by_coin"] = dd.groupby("coin")[["book_return", "coin_return"]].mean() * 100
    res["book_by_year"] = dd.groupby("yr")[["book_return", "coin_return"]].mean() * 100
    return res
