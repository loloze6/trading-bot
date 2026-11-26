def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            rngraw = (b["high"] - b["low"]).replace(0, np.nan)
            rows.append(pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r1": r1, "sd30": sd30, "s1": r1 / sd30,
                "s3": (c / c.shift(3) - 1) / sd30,
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1, "f3": c.shift(-3) / c - 1,
                "inprof": (b["regime"] == "unknown").astype(int),
                "rng": rngraw / c / sd30,
                "clpos": (c - b["low"]) / rngraw,
            }))
    A = pd.concat(rows, ignore_index=True)
    A["wd"] = A["day"].dt.weekday
    for h in (1, 2, 3):
        A["u%d" % h] = A["f%d" % h] - A["coin"].map(A[A["pos"] % h == 0].groupby("coin")["f%d" % h].mean())

    def ct(x, d):
        m = pd.DataFrame({"x": x, "d": d}).dropna()
        n = len(m)
        if n < 5: return pd.Series({"n": n, "days": 0, "mean%": np.nan, "t_day": np.nan})
        mu = m["x"].mean()
        s = (m["x"] - mu).groupby(m["d"]).sum()
        G = len(s)
        se = np.sqrt((s ** 2).sum() * G / (G - 1)) / n
        return pd.Series({"n": n, "days": G, "mean%": 100 * mu, "t_day": mu / se})

    def slope(y, x, d):
        m = pd.DataFrame({"y": y, "x": x, "d": d}).dropna()
        xc = m["x"] - m["x"].mean()
        b = (xc * m["y"]).sum() / (xc ** 2).sum()
        e = m["y"] - m["y"].mean() - b * xc
        s = (xc * e).groupby(m["d"]).sum()
        G = len(s)
        se = np.sqrt((s ** 2).sum() * G / (G - 1)) / (xc ** 2).sum()
        return pd.Series({"n": len(m), "days": G, "slope%": 100 * b, "t_day": b / se})

    out = {}
    a = A.dropna(subset=["s1", "u1", "clpos", "rng"]).copy()
    a["q"] = pd.qcut(a["s1"], 10, labels=False)
    out["s1 decile -> u1 day-clustered"] = a.groupby("q").apply(lambda g: ct(g["u1"], g["day"]))
    dn = a[a["s1"] < 0]
    out["down days: slope u1 on s1 (neg slope=bigger fall bigger rebound)"] = pd.DataFrame({
        "all": slope(dn["u1"], dn["s1"], dn["day"]),
        "inprof0": slope(dn[dn.inprof == 0]["u1"], dn[dn.inprof == 0]["s1"], dn[dn.inprof == 0]["day"]),
        "inprof1": slope(dn[dn.inprof == 1]["u1"], dn[dn.inprof == 1]["s1"], dn[dn.inprof == 1]["day"])}).T
    a["cq"] = pd.qcut(a["clpos"], 5, labels=False)
    out["close-in-range quintile -> u1 clustered"] = a.groupby("cq").apply(lambda g: ct(g["u1"], g["day"]))
    out["slope u1 on clpos, all / by year-split windows"] = pd.DataFrame(
        {w: slope(g["u1"], g["clpos"], g["day"]) for w, g in a.groupby("win")}).T
    a["rq"] = pd.qcut(a["rng"], 5, labels=False)
    a["su"] = a["u1"] * np.sign(a["r1"])
    out["range quintile -> u1 signed by day direction, clustered"] = a.groupby("rq").apply(lambda g: ct(g["su"], g["day"]))
    a["sg"] = a["rng"] * np.sign(a["r1"])
    out["slope u1 on signed range, by window"] = pd.DataFrame(
        {w: slope(g["u1"], g["sg"], g["day"]) for w, g in a.groupby("win")}).T
    out["slope u1 on signed range / s1 / clpos, by inprof"] = pd.DataFrame({
        "sg_p%d" % k: slope(g["u1"], g["sg"], g["day"]) for k, g in a.groupby("inprof")}).T
    # down day with low close: 2-day reversal on grid
    g2 = A[(A["pos"] % 2 == 0)].dropna(subset=["s1", "u2", "clpos"]).copy()
    g2["q"] = pd.qcut(g2["s1"], 5, labels=False)
    out["s1 quintile -> u2 (grid 2) clustered"] = g2.groupby("q").apply(lambda g: ct(g["u2"], g["day"]))
    # in-profile s3 continuation, clustered & by window
    g3 = A[(A["pos"] % 3 == 0)].dropna(subset=["s3", "u3"]).copy()
    ip = g3[(g3.inprof == 1) & (g3.s3 < 0)]
    out["inprof falls: u3 clustered, slope u3 on s3"] = pd.DataFrame({
        "mean": ct(ip["u3"], ip["day"]), "slope": slope(ip["u3"], ip["s3"], ip["day"]).rename({"slope%": "mean%"})}).T
    out["inprof falls: u3 by window"] = ip.groupby("win").apply(lambda g: ct(g["u3"], g["day"]))
    op = g3[(g3.inprof == 0)]
    out["out-of-profile: slope u3 on s3"] = slope(op["u3"], op["s3"], op["day"]).to_frame().T
    # weekday on one-per-day market mean
    dm = A.dropna(subset=["r1"]).groupby(["day"]).agg(r=("r1", "mean"), wd=("wd", "first"))
    out["weekday -> mean coin r1 per day"] = dm.groupby("wd")["r"].apply(
        lambda x: pd.Series({"n": len(x), "mean%": 100 * x.mean(), "t": x.mean() / x.std() * np.sqrt(len(x))})).unstack()
    return out
