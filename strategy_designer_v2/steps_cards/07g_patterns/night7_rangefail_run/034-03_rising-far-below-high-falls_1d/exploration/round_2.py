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
            hi = c.rolling(20, min_periods=20).max().shift(1)
            sd = r1.rolling(20, min_periods=15).std()
            dist = (c / hi - 1) / sd
            r60 = c / c.shift(60) - 1
            sd30 = r1.rolling(30, min_periods=25).std()
            fwd = c.shift(-H) / c - 1
            pos = np.arange(len(b))
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({
                "coin": coin, "w": w, "dist": dist, "fwd": fwd, "grid": (pos % H == 0),
                "rising": (b["regime"] != "chop"), "r60": r60, "sd30": sd30,
                "day": ts.dt.floor("D"), "wd": ts.dt.weekday, "yr": ts.dt.year,
                "next1": c.shift(-1) / c - 1,
            }))
    d = pd.concat(rows, ignore_index=True)
    coinmean = d[d.grid].groupby("coin")["fwd"].mean()
    d["ex"] = d["fwd"] - d["coin"].map(coinmean)
    g = d[d.grid].dropna(subset=["ex", "dist"]).copy()

    def ct(x):
        # day-clustered t about zero
        s = x.groupby(x.index.map(lambda i: g.at[i, "day"]))
        ds = s.sum(); n = len(x); nd = len(ds)
        m = x.mean()
        se = np.sqrt(((s.apply(lambda v: (v - m).sum())) ** 2).sum()) / n
        return pd.Series({"n": n, "days": nd, "mean_ex": m, "t_day": m / se if se > 0 else np.nan})

    out = {}
    g["deep"] = pd.cut(g["dist"], [-np.inf, -2.5, -1, 0, np.inf], labels=["<-2.5", "-2.5..-1", "-1..0", ">0"])
    out["notrising_deep_daycl"] = g[~g.rising].groupby("deep")["ex"].apply(ct).unstack()
    out["rising_deep_daycl"] = g[g.rising].groupby("deep")["ex"].apply(ct).unstack()
    # non-rising: split by known r60 (falling < -10% vs choppy)
    nr = g[~g.rising].dropna(subset=["r60"]).copy()
    nr["tr"] = np.where(nr.r60 < -0.10, "falling", "choppy")
    out["notrising_trend_x_deep"] = nr.groupby(["tr", "deep"])["ex"].apply(ct).unstack()
    # non-rising deep (<-1) by window
    out["notrising_deep_by_window"] = g[(~g.rising) & (g.dist < -1)].groupby("w")["ex"].apply(ct).unstack()
    # slope in non-rising, below high only, by year
    res = {}
    sub = g[(~g.rising) & (g.dist < 0)]
    for y, s in sub.groupby("yr"):
        if len(s) > 20:
            lr = stats.linregress(s["dist"].clip(-6, 0), s["ex"])
            res[y] = {"n": len(s), "slope": lr.slope, "t": lr.slope / lr.stderr}
    out["notrising_below_slope_by_year"] = pd.DataFrame(res).T
    lr = stats.linregress(sub["dist"].clip(-6, 0), sub["ex"])
    out["notrising_below_slope_all"] = f"slope {lr.slope:.5f} t {lr.slope/lr.stderr:.2f} n {len(sub)}"
    # rising above high, by window
    out["rising_above_by_window"] = g[g.rising & (g.dist > 0)].groupby("w")["ex"].apply(ct).unstack()
    # weekday: per-day mean across coins, excess over overall daily mean
    dd = d.dropna(subset=["next1"])
    daym = dd.groupby("day").agg(r=("next1", "mean"), wd=("wd", "first"), w=("w", "first"), yr=("yr", "first"))
    daym["ex"] = daym["r"] - daym["r"].mean()
    def tt(x):
        return pd.Series({"days": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    out["weekday_day_mean"] = daym.groupby("wd")["ex"].apply(tt).unstack()
    daym["thufri"] = daym.wd.isin([3, 4])
    out["thufri_minus_rest_by_year"] = daym.groupby(["yr", "thufri"])["ex"].mean().unstack()
    return out
