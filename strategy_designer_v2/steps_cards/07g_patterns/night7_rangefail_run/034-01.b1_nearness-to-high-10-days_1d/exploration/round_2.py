def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            hi = c.shift(1).rolling(20, min_periods=20).max()
            vol = r1.rolling(20, min_periods=15).std()
            vol30 = r1.rolling(30, min_periods=25).std()
            b["dist"] = (c / hi - 1) / vol
            b["vol"] = vol; b["vol30"] = vol30; b["r1"] = r1
            b["ret5"] = c / c.shift(5) - 1
            b["ret5z"] = b["ret5"] / (vol * np.sqrt(5))
            for h in (5, 10):
                b[f"f{h}"] = c.shift(-h) / c - 1
            b["rising"] = (b["regime"] == "unknown").astype(int)
            b["coin"] = coin; b["win"] = w; b["pos"] = np.arange(len(b))
            ts = pd.to_datetime(b["timestamp"])
            b["wd"] = ts.dt.weekday; b["year"] = ts.dt.year
            b["dayk"] = ts.dt.floor("D").astype("int64")
            b["alloc"] = b["postRebalance_current_allocation"].fillna(0)
            rows.append(b[["coin","win","pos","dist","vol","vol30","r1","ret5","ret5z","f5","f10","rising","wd","year","dayk","alloc"]])
    D = pd.concat(rows, ignore_index=True)
    for h in (5, 10):
        g = D[D["pos"] % h == 0]
        m = g.groupby("coin")[f"f{h}"].mean()
        D[f"x{h}"] = D[f"f{h}"] - D["coin"].map(m)
    D["vrank"] = D.groupby("coin")["vol30"].rank(pct=True)
    D["agit"] = (D["vrank"] > 0.5).astype(int)

    def cl_slope(df, x, y):
        d = df[[x, y, "dayk"]].dropna()
        if len(d) < 30: return (np.nan, np.nan, len(d), np.nan)
        X = d[x] - d[x].mean(); Y = d[y]
        b = (X * (Y - Y.mean())).sum() / (X**2).sum()
        e = (Y - Y.mean()) - b * X
        s = (X * e).groupby(d["dayk"]).sum()
        se = np.sqrt((s**2).sum()) / (X**2).sum()
        return (round(b, 5), round(b / se, 2), len(d), d["dayk"].nunique())

    G10 = D[D["pos"] % 10 == 0]
    G5 = D[D["pos"] % 5 == 0]
    res = {}
    for prof in (1, 0):
        for a in (0, 1):
            s = G10[(G10.rising == prof) & (G10.agit == a)]
            res[f"x10 dist rising{prof} agit{a}"] = cl_slope(s, "dist", "x10")
            s5 = G5[(G5.rising == prof) & (G5.agit == a)]
            res[f"x5 dist rising{prof} agit{a}"] = cl_slope(s5, "dist", "x5")
        res[f"x10 ret5z rising{prof}"] = cl_slope(G10[G10.rising == prof], "ret5z", "x10")
        res[f"x5 ret5z rising{prof}"] = cl_slope(G5[G5.rising == prof], "ret5z", "x5")
    res["x5 dist all"] = cl_slope(G5, "dist", "x5")
    res["x5 ret5z all"] = cl_slope(G5, "ret5z", "x5")
    G5z = G5.assign(z=G5["r1"] / G5["vol"])
    res["x5 1d z all"] = cl_slope(G5z, "z", "x5")
    res["x5 1d z pos only"] = cl_slope(G5z[G5z.z > 0], "z", "x5")
    out["clustered slopes (b,t,n,days)"] = pd.DataFrame(res, index=["b","t","n","days"]).T

    # above-high cases by window in non-rising
    ab = G10[(G10.dist > 0)]
    out["above-high x10 by rising & year"] = ab.groupby(["rising","year"])["x10"].agg(["mean","count"]).round(4)

    # weekday: day-clustered (mean over coins per day first)
    dm = D.dropna(subset=["r1"]).groupby(["dayk","wd"])["r1"].mean().reset_index()
    out["weekday daily ret, per-day means"] = dm.groupby("wd")["r1"].agg(["mean","count", lambda s: s.mean()/s.std()*np.sqrt(len(s))]).round(4)
    out["weekday by year (mean per day)"] = dm.assign(year=pd.to_datetime(dm.dayk).dt.year).groupby(["year","wd"])["r1"].mean().unstack().round(4)

    # book by side and profile on daily: gain before costs per bar
    D["nxt"] = D.groupby(["coin","win"])["r1"].shift(-1)
    D["gain"] = D["alloc"] * D["nxt"]
    D["side"] = np.sign(D["alloc"])
    out["gain by rising & side"] = D.groupby(["rising","side"])["gain"].agg(["mean","sum","count"]).round(5)
    return out
