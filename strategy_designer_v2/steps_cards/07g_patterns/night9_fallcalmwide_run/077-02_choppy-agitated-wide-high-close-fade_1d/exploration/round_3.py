def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; r = c.pct_change()
            sd30 = r.rolling(30, min_periods=30).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "nxt": c.shift(-1) / c - 1,
                "n5": c.shift(-5) / c - 1,
                "r7": c / c.shift(7) - 1,
                "r30": c / c.shift(30) - 1,
                "tr60": c / c.shift(60) - 1,
                "sd30": sd30,
                "pos5": (np.arange(len(b)) % 5 == 0),
                "inprof": b["regime"].astype(str) != "chop",
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["unx"] = d["nxt"] - d.groupby("coin")["nxt"].transform("mean")
    g5 = d[d["pos5"]]
    d["unx5"] = d["n5"] - d["coin"].map(g5.groupby("coin")["n5"].mean())
    d["day"] = d["ts"].dt.floor("D"); d["year"] = d["ts"].dt.year

    def ct(x, days):
        x = pd.Series(x).dropna(); days = days.loc[x.index]; n = len(x)
        if n < 5: return pd.Series({"n": n, "days": days.nunique(), "mean%": np.nan, "t": np.nan})
        m = x.mean(); rd = (x - m).groupby(days).sum(); D = len(rd)
        se = np.sqrt((rd ** 2).sum() * D / max(D - 1, 1)) / n
        return pd.Series({"n": n, "days": D, "mean%": 100 * m, "t": m / se if se > 0 else np.nan})

    out = {}
    p = d[d["inprof"]]
    out["inprof next-day unx"] = ct(p["unx"], p["day"])
    out["outprof next-day unx"] = ct(d[~d["inprof"]]["unx"], d[~d["inprof"]]["day"])
    p5 = p[p["pos5"]]
    out["inprof 5d unx (grid)"] = ct(p5["unx5"], p5["day"])
    out["inprof by year"] = p.groupby("year").apply(lambda g: ct(g["unx"], g["day"]))
    out["inprof by coin"] = p.groupby("coin").apply(lambda g: ct(g["unx"], g["day"]))
    q = p.dropna(subset=["r7"]).copy(); q["b"] = pd.qcut(q["r7"], 3, labels=False)
    out["inprof by 7d return tercile"] = q.groupby("b").apply(lambda g: ct(g["unx"], g["day"]))
    q = p.dropna(subset=["tr60"]).copy(); q["b"] = pd.qcut(q["tr60"], 3, labels=False)
    out["inprof by 60d return tercile"] = q.groupby("b").apply(lambda g: ct(g["unx"], g["day"]))
    # choppy agitated proxy outside the recorded regime: choppy trend, sd30 above coin median
    d["agi"] = d["sd30"] > d.groupby("coin")["sd30"].transform("median")
    ca = d[(d["tr60"].abs() <= 0.1) & d["agi"]]
    out["proxy choppy-agitated next-day unx"] = ct(ca["unx"], ca["day"])
    cc = d[(d["tr60"].abs() <= 0.1) & ~d["agi"] & d["sd30"].notna()]
    out["proxy choppy-calm next-day unx"] = ct(cc["unx"], cc["day"])
    return out
