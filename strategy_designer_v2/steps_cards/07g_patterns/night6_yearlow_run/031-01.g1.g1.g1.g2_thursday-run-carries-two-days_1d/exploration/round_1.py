def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            r1 = c.pct_change()
            vol = r1.rolling(20, min_periods=15).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "wd": ts.dt.weekday.values, "day": ts.dt.normalize().values,
                "r1": r1, "vol": vol,
                "z14": (c / c.shift(14) - 1) / (vol * np.sqrt(14)),
                "z1": r1 / vol,
                "z3": (c / c.shift(3) - 1) / (vol * np.sqrt(3)),
                "lo60": c / c.rolling(60, min_periods=40).min() - 1,
                "hi60": c / c.rolling(60, min_periods=40).max() - 1,
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1,
                "f3": c.shift(-3) / c - 1, "f5": c.shift(-5) / c - 1,
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    # drift per coin per horizon on non-overlapping grid
    for h in [1, 2, 3, 5]:
        g = d[d["pos"] % h == 0].groupby("coin")[f"f{h}"].mean()
        d[f"x{h}"] = d[f"f{h}"] - d["coin"].map(g)
        d[f"sd{h}"] = d["coin"].map(d[d["pos"] % h == 0].groupby("coin")[f"f{h}"].std())

    def tday(s, day):
        x = pd.DataFrame({"v": s - s.mean(), "day": day}).dropna().groupby("day")["v"].sum()
        n = len(x)
        se = np.sqrt((x ** 2).sum()) / len(s.dropna())
        return s.mean() / se if se > 0 else np.nan, n

    out = {}
    # 1. momentum score by weekday: sign-agnostic graded measure z14 (clipped) x drift-removed fwd2
    res = []
    for wd in range(7):
        s = d[(d["wd"] == wd)].dropna(subset=["z14", "x2"])
        v = s["z14"].clip(-3, 3) * s["x2"]
        t, n = tday(v, s["day"])
        top = s[s["z14"] > s["z14"].quantile(2/3)]["x2"].mean()
        bot = s[s["z14"] < s["z14"].quantile(1/3)]["x2"].mean()
        res.append({"wd": wd, "mean_z_x2": v.mean(), "t": t, "days": n, "top_minus_bot_x2": top - bot})
    out["z14 x fwd2 by weekday (0=Mon)"] = pd.DataFrame(res)
    # weekday raw mean returns 1d
    res = []
    for wd in range(7):
        s = d[d["wd"] == wd].dropna(subset=["x1"])
        t, n = tday(s["x1"], s["day"])
        res.append({"wd_of_bar_start": wd, "next_day_x1_mean": s["x1"].mean(), "t": t, "n": n})
    out["next day drift-removed return by weekday of bar"] = pd.DataFrame(res)
    # 2. after large 1-day moves: z1 quintile -> next 1d,3d (grid)
    res = []
    for h in [1, 3, 5]:
        s = d[d["pos"] % h == 0].dropna(subset=["z1", f"x{h}"]).copy()
        s["q"] = pd.qcut(s["z1"], 5, labels=False)
        for q, g in s.groupby("q"):
            t, n = tday(g[f"x{h}"], g["day"])
            res.append({"h": h, "z1_quint": q, "z1_mean": g["z1"].mean(), "x_mean": g[f"x{h}"].mean(), "t": t, "n": len(g)})
    out["after 1-day move (vol units)"] = pd.DataFrame(res)
    # 3. z14 quintile all days, h=2,5
    res = []
    for h in [2, 5]:
        s = d[d["pos"] % h == 0].dropna(subset=["z14", f"x{h}"]).copy()
        s["q"] = pd.qcut(s["z14"], 5, labels=False)
        for q, g in s.groupby("q"):
            t, n = tday(g[f"x{h}"], g["day"])
            res.append({"h": h, "z14_quint": q, "x_mean": g[f"x{h}"].mean(), "t": t, "n": len(g)})
    out["z14 quintile all days"] = pd.DataFrame(res)
    # 4. distance from 60-day low/high (in-window proxy for yearly low)
    res = []
    s = d[d["pos"] % 5 == 0].dropna(subset=["lo60", "x5", "vol"]).copy()
    s["lo_units"] = s["lo60"] / (s["vol"] * np.sqrt(5))
    s["q"] = pd.qcut(s["lo_units"], 5, labels=False, duplicates="drop")
    for q, g in s.groupby("q"):
        t, n = tday(g["x5"], g["day"])
        res.append({"dist_from_60d_low_quint": q, "mean_units": g["lo_units"].mean(), "x5": g["x5"].mean(), "t": t, "n": len(g)})
    out["after distance from 60d low, 5d"] = pd.DataFrame(res)
    # 5. vol level: vol quintile -> fwd5 drift-removed and z14 momentum strength
    res = []
    s = d[d["pos"] % 2 == 0].dropna(subset=["vol", "x2", "z14"]).copy()
    s["vr"] = s.groupby("coin")["vol"].rank(pct=True)
    s["q"] = pd.cut(s["vr"], [0, .2, .4, .6, .8, 1], labels=False)
    for q, g in s.groupby("q"):
        v = g["z14"].clip(-3, 3) * g["x2"]
        t, n = tday(v, g["day"])
        res.append({"vol_quint": q, "x2": g["x2"].mean(), "mom_x2": v.mean(), "t_mom": t, "n": len(g)})
    out["by vol level"] = pd.DataFrame(res)
    # 6. book: daily returns, by weekday, by window
    dd = []
    for coin, wins in data["days"].items():
        for w, t_ in wins.items():
            x = t_.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    dd = pd.concat(dd)
    bk = dd.groupby(["win", "day"])[["book_return", "coin_return"]].mean().reset_index()
    bk["wd"] = pd.to_datetime(bk["day"], utc=True).dt.weekday
    out["book by weekday"] = bk.groupby("wd")[["book_return", "coin_return"]].agg(["mean", "count"])
    out["book by window"] = bk.groupby("win")["book_return"].agg(["mean", "std", "count"])
    # 7. long vs short trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t_ in wins.items():
            x = t_.copy(); x["coin"] = coin; tr.append(x)
    tr = pd.concat(tr)
    out["trades by side"] = tr.groupby("side")["net_profit_loss_percent"].agg(["mean", "count", "std"])
    out["trades by coin"] = tr.groupby(["coin", "side"])["net_profit_loss_percent"].agg(["mean", "count"]).unstack()
    return out
