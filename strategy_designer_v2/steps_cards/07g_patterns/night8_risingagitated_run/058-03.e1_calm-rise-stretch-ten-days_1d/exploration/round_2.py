def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    coinmean = {}; coinsd = {}
    for coin, ws in bars.items():
        g = []
        for w, b in ws.items():
            c = b["close"].values
            for i in range(0, len(c) - 10, 10):
                g.append(c[i + 10] / c[i] - 1)
        coinmean[coin] = np.mean(g); coinsd[coin] = np.std(g, ddof=1)
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            b["dist"] = (c / c.rolling(20).mean() - 1) * 100
            b["r60"] = (c / c.shift(60) - 1) * 100
            r1 = c.pct_change()
            b["vol30"] = r1.rolling(30).std()
            b["r5"] = c / c.shift(5) - 1
            b["r10"] = c / c.shift(10) - 1
            for h in (1, 3, 5, 10):
                b["f%d" % h] = c.shift(-h) / c - 1
            b["ex10"] = b["f10"] - coinmean[coin]
            b["ex5"] = b["f5"] - coinmean[coin] / 2
            b["pos"] = np.arange(len(b)); b["coin"] = coin; b["win"] = w
            ts = pd.to_datetime(b["timestamp"])
            b["day"] = ts.dt.normalize(); b["wd"] = ts.dt.weekday; b["yr"] = ts.dt.year
            rows.append(b)
    D = pd.concat(rows, ignore_index=True)
    D["vrank"] = D.groupby("coin")["vol30"].rank(pct=True)
    D["agit"] = np.where(D["vrank"] > 0.5, "agit", "calm")
    D["trend"] = np.where(D["regime"] == "unknown", "rising_calm",
                 np.where(D["r60"] > 10, "rising", np.where(D["r60"] < -10, "falling",
                 np.where(D["r60"].notna(), "choppy", "na"))))
    out = {}
    def cl_slope(df, x, y):
        df = df.dropna(subset=[x, y])
        if len(df) < 15: return [np.nan, np.nan, len(df), np.nan]
        X = df[x].values; Y = df[y].values
        r = stats.linregress(X, Y)
        e = (Y - r.intercept - r.slope * X) * (X - X.mean())
        s = pd.Series(e).groupby(df["day"].values).sum()
        se = np.sqrt((s ** 2).sum()) / ((X - X.mean()) ** 2).sum()
        return [r.slope, r.slope / se, len(df), df["day"].nunique()]
    G = D[D["pos"] % 10 == 0].dropna(subset=["ex10", "dist"]).copy()
    res = []
    for (t, a), df in G.groupby(["trend", "agit"]):
        res.append([t, a] + cl_slope(df, "dist", "ex10") + [df["ex10"].mean()])
    for t, df in G.groupby("trend"):
        res.append([t, "all"] + cl_slope(df, "dist", "ex10") + [df["ex10"].mean()])
        res.append([t, "r5"] + cl_slope(df, "r5", "ex10") + [np.nan])
        res.append([t, "r10"] + cl_slope(df, "r10", "ex10") + [np.nan])
    out["slope_clustered_trend_agit"] = pd.DataFrame(res, columns=["trend", "agit", "slope", "t_cl", "n", "days", "mean_ex10"])
    ch = G[G["trend"] == "choppy"].copy()
    ch["side"] = np.where(ch["dist"] < 0, "below", "above")
    out["choppy_by_side_window"] = ch.pivot_table(index="win", columns="side", values="ex10", aggfunc=["mean", "count"])
    out["choppy_below_slope"] = pd.Series(cl_slope(ch[ch.dist < 0], "dist", "ex10"), index=["slope", "t", "n", "days"])
    out["choppy_above_slope"] = pd.Series(cl_slope(ch[ch.dist >= 0], "dist", "ex10"), index=["slope", "t", "n", "days"])
    out["choppy_by_coin"] = ch.groupby("coin").apply(lambda d: pd.Series(cl_slope(d, "dist", "ex10"), index=["slope", "t", "n", "days"]))
    # 5-day grid for choppy and falling, more cases
    G5 = D[D["pos"] % 5 == 0].dropna(subset=["ex5", "dist"])
    r5 = []
    for t, df in G5.groupby("trend"):
        r5.append([t] + cl_slope(df, "dist", "ex5"))
    out["slope5_by_trend"] = pd.DataFrame(r5, columns=["trend", "slope", "t_cl", "n", "days"])
    # weekday, day-clustered (mean over coins per day)
    dm = D.dropna(subset=["f1"]).groupby(["day", "wd", "trend"])["f1"].mean().reset_index()
    out["weekday_daymean"] = dm.groupby("wd")["f1"].agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    dm["thufri"] = dm["wd"].isin([3, 4])
    out["thufri_by_trend"] = dm.pivot_table(index="trend", columns="thufri", values="f1", aggfunc="mean")
    out["thufri_by_year"] = dm.assign(yr=pd.to_datetime(dm["day"]).dt.year).pivot_table(index="yr", columns="thufri", values="f1", aggfunc="mean")
    return out
