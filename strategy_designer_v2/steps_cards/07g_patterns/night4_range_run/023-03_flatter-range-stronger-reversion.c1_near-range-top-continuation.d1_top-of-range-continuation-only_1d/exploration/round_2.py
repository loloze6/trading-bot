def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    D = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            lr = np.log(c).diff()
            vol = lr.rolling(30).std()
            r1 = c.pct_change()
            r3 = c / c.shift(3) - 1
            f1 = c.shift(-1) / c - 1
            f3 = c.shift(-3) / c - 1
            trend = np.log(c / c.shift(30)) / (vol * np.sqrt(30))
            d = pd.DataFrame(dict(coin=coin, w=w, i=np.arange(len(b)), ts=ts, r1=r1, r3=r3, f1=f1, f3=f3,
                                  z1=r1 / vol, z3=r3 / (vol * np.sqrt(3)), trend=trend,
                                  dow=ts.dt.dayofweek, yr=ts.dt.year, vol=vol))
            D.append(d)
    D = pd.concat(D, ignore_index=True)
    D["f1x"] = D["f1"] - D.groupby("coin")["f1"].transform("mean")
    D["f3x"] = D["f3"] - D.groupby("coin")["f3"].transform("mean")
    E = D.dropna(subset=["z1", "f1x"])
    # graded slope per coin
    rows = {}
    for coin, g in E.groupby("coin"):
        s = stats.linregress(g["z1"].clip(-4, 4), g["f1x"])
        rows[coin] = dict(n=len(g), slope=s.slope, t=s.slope / s.stderr)
    s = stats.linregress(E["z1"].clip(-4, 4), E["f1x"])
    rows["ALL"] = dict(n=len(E), slope=s.slope, t=s.slope / s.stderr)
    out["f1x on z1 by coin"] = pd.DataFrame(rows).T.round(5)
    rows = {}
    for yr, g in E.groupby("yr"):
        s = stats.linregress(g["z1"].clip(-4, 4), g["f1x"])
        rows[yr] = dict(n=len(g), slope=s.slope, t=s.slope / s.stderr)
    out["f1x on z1 by year"] = pd.DataFrame(rows).T.round(5)
    # date-clustered: per day, cross-coin
    E2 = E.copy(); E2["zq"] = pd.cut(E2["z1"], [-99, -2, -1, 0, 1, 2, 99])
    a = E2.groupby(["ts", "zq"], observed=True)["f1x"].mean().reset_index().groupby("zq", observed=True)["f1x"].agg(["count", "mean", "std"])
    a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["f1x by z1, clustered by date"] = a.round(4)
    # trend split
    E2["trq"] = pd.qcut(E2["trend"], 3, labels=["down", "flat", "up"])
    a = E2.groupby(["trq", "zq"], observed=True)["f1x"].agg(["count", "mean", "std"])
    a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["f1x by trend x z1"] = a.round(4)
    # 3-day horizon, non-overlapping grid
    G = D[(D["i"] % 3 == 0)].dropna(subset=["z3", "f3x"])
    G["zq"] = pd.cut(G["z3"], [-99, -2, -1, 0, 1, 2, 99])
    a = G.groupby("zq", observed=True)["f3x"].agg(["count", "mean", "std"])
    a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["f3x by 3d z, grid"] = a.round(4)
    s = stats.linregress(G["z3"].clip(-4, 4), G["f3x"])
    out["f3x slope on z3"] = f"slope {s.slope:.5f} t {s.slope/s.stderr:.2f} n {len(G)}"
    # weekday: clustered by date and by year
    F = E.groupby(["ts", "dow", "yr"])["f1x"].mean().reset_index()
    a = F.groupby("dow")["f1x"].agg(["count", "mean", "std"]); a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["f1x by dow, clustered by date"] = a.round(4)
    F["thfr"] = F["dow"].isin([3, 4])
    a = F.groupby(["yr", "thfr"])["f1x"].mean().unstack().round(4)
    out["f1x thu/fri vs rest by year"] = a
    # by vol level
    E2["vq"] = E2.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    rows = {}
    for v, g in E2.groupby("vq"):
        s = stats.linregress(g["z1"].clip(-4, 4), g["f1x"]); rows[v] = dict(n=len(g), slope=s.slope, t=s.slope / s.stderr)
    out["f1x on z1 by vol tercile"] = pd.DataFrame(rows).T.round(5)
    return out
