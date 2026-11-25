def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            hi5 = c.rolling(5, min_periods=5).max()
            dip = (c - hi5) / hi5 / sd30
            tr = c / c.shift(60) - 1
            sd30l = sd30
            sdrel = sd30 / sd30.expanding(min_periods=30).median()
            ret1 = r1
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ret3 = c / c.shift(3) - 1
            ts = pd.to_datetime(b["timestamp"])
            inprof = b["regime"] != "chop"
            idx = np.arange(len(b))
            df = pd.DataFrame({"coin": coin, "w": w, "pos": idx, "dip": dip, "tr": tr,
                               "sdrel": sdrel, "r1z": ret1 / sd30, "r3z": ret3 / (sd30 * np.sqrt(3)),
                               "fwd": fwd, "fwd1": fwd1, "inprof": inprof.values,
                               "wd": ts.dt.weekday.values, "alloc": b["postRebalance_current_allocation"].values,
                               "yr": ts.dt.year.values})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d[d.pos % H == 0].groupby("coin")["fwd"].mean()
    d["ex"] = d["fwd"] - d["coin"].map(drift)
    g = d[(d.pos % H == 0)].dropna(subset=["ex"])
    g["trend"] = np.where(g.tr > 0.10, "rising", np.where(g.tr < -0.10, "falling", np.where(g.tr.notna(), "choppy", "na")))
    g["agit"] = np.where(g.sdrel > 1, "agit", "calm")
    out = {}
    def slope(sub, x):
        sub = sub.dropna(subset=[x, "ex"])
        if len(sub) < 20: return (len(sub), np.nan, np.nan)
        s = stats.linregress(sub[x], sub["ex"])
        return (len(sub), s.slope, s.slope / s.stderr)
    res = []
    for (t, a), sub in g.groupby(["trend", "agit"]):
        n, sl, tt = slope(sub, "dip")
        q = sub.dropna(subset=["dip"])
        deep = q[q.dip <= q.dip.quantile(0.33)]["ex"].mean() if len(q) > 10 else np.nan
        res.append([t, a, n, sl, tt, deep])
    out["dip slope ex5 by trend/agit"] = pd.DataFrame(res, columns=["trend", "agit", "n", "slope", "t", "deep3_ex"])
    res = []
    for p, sub in g.groupby("inprof"):
        n, sl, tt = slope(sub, "dip"); res.append([p, n, sl, tt, sub.ex.mean()])
    out["dip slope by in-profile"] = pd.DataFrame(res, columns=["inprof", "n", "slope", "t", "mean_ex"])
    # quintiles of dip overall
    q = g.dropna(subset=["dip"]).copy()
    q["qd"] = pd.qcut(q.dip, 5, labels=False, duplicates="drop")
    out["ex5 by dip quintile all"] = q.groupby("qd")["ex"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    # 1-day move z, 5-day forward
    q = g.dropna(subset=["r1z"]).copy()
    q["qr"] = pd.qcut(q.r1z, 5, labels=False)
    out["ex5 by 1d move z quintile"] = q.groupby("qr")["ex"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    q["qv"] = pd.qcut(q.sdrel, 3, labels=False)
    out["ex5 by vol tercile"] = q.groupby("qv")["ex"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    out["ex5 by trend"] = g.groupby("trend")["ex"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    # weekday on daily returns (all bars, 1-day)
    out["1d fwd by weekday"] = d.dropna(subset=["fwd1"]).groupby("wd")["fwd1"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    # book
    days = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd[["book_return", "coin_return"]].copy(); x["coin"] = coin; x["w"] = w; days.append(x)
    D = pd.concat(days)
    out["book by window"] = D.groupby("w")[["book_return", "coin_return"]].mean()
    out["share in profile"] = float(d.inprof.mean())
    out["years by window"] = d.groupby("w")["yr"].agg(["min", "max"])
    return out
