def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            ts = pd.to_datetime(b["timestamp"])
            out = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "day": ts.dt.floor("D"), "year": ts.dt.year, "wd": ts.dt.weekday,
                "inprof": (b["regime"] != "chop").astype(int),
                "s1": r1 / sd30,
                "s2": (c / c.shift(2) - 1) / (sd30 * np.sqrt(2)),
                "range_s": ((b["high"] - b["low"]) / c.shift(1)) / sd30,
            })
            for h in (1, 2):
                out[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(out)
    D = pd.concat(rows, ignore_index=True)
    for h in (1, 2):
        g = D[D["pos"] % h == 0]
        dr = g.groupby("coin")[f"f{h}"].mean()
        D[f"u{h}"] = D[f"f{h}"] - D["coin"].map(dr)

    def dayt(x, col):
        x = x.dropna(subset=[col])
        if len(x) < 3: return (len(x), np.nan, np.nan, 0)
        m = x[col].mean()
        dev = (x[col] - m).groupby(x["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(x)
        return (len(x), m, m / se if se else np.nan, dev.size)

    res = {}
    P = D[D["inprof"] == 1]
    # up days 0..1 swing, next day
    up = P[(P["s1"] > 0) & (P["s1"] <= 1)]
    n, m, t, d = dayt(up, "u1")
    res["in prof up 0-1 next day u1"] = pd.Series({"n": n, "mean": m, "t_day": t, "days": d})
    allup = P[P["s1"] > 0]
    n, m, t, d = dayt(allup, "u1")
    res["in prof all up days u1"] = pd.Series({"n": n, "mean": m, "t_day": t, "days": d})
    # graded: correlation of s1 with u1 in profile, all bars
    x = P.dropna(subset=["s1", "u1"])
    res["in prof corr s1,u1 (spearman)"] = float(stats.spearmanr(x["s1"], x["u1"]).correlation)
    xo = D[D["inprof"] == 0].dropna(subset=["s1", "u1"])
    res["out prof corr s1,u1 (spearman)"] = float(stats.spearmanr(xo["s1"], xo["u1"]).correlation)
    # by year: up days 0-1 next day, and down days next day
    yr = []
    for y, g in P.groupby("year"):
        a = dayt(g[(g["s1"] > 0) & (g["s1"] <= 1)], "u1")
        b_ = dayt(g[g["s1"] < 0], "u1")
        yr.append({"year": y, "up_n": a[0], "up_mean": a[1], "up_t": a[2],
                   "down_n": b_[0], "down_mean": b_[1], "down_t": b_[2]})
    res["in prof by year"] = pd.DataFrame(yr)
    # by coin
    cc = []
    for co, g in P.groupby("coin"):
        a = dayt(g[(g["s1"] > 0) & (g["s1"] <= 1)], "u1")
        cc.append({"coin": co, "n": a[0], "mean": a[1], "t": a[2]})
    res["in prof up 0-1 by coin"] = pd.DataFrame(cc)
    # 2-day rise in profile next day
    s2t = []
    for lo, hi in [(-9, -1), (-1, 0), (0, 0.5), (0.5, 1), (1, 9)]:
        a = dayt(P[(P["s2"] > lo) & (P["s2"] <= hi)], "u1")
        s2t.append({"s2_bin": f"{lo}..{hi}", "n": a[0], "mean": a[1], "t": a[2], "days": a[3]})
    res["in prof s2 -> u1"] = pd.DataFrame(s2t)
    # out-profile weekday by year (Wed and Thu/Fri)
    O = D[D["inprof"] == 0]
    wy = []
    for y, g in O.groupby("year"):
        r = {"year": y}
        for wd in (2, 3, 4):
            a = dayt(g[g["wd"] == wd], "u1")
            r[f"wd{wd}_mean"] = a[1]; r[f"wd{wd}_t"] = a[2]
        wy.append(r)
    res["out prof weekday by year"] = pd.DataFrame(wy)
    for wd in (2, 3, 4):
        a = dayt(O[O["wd"] == wd], "u1")
        res[f"out wd{wd} day-clustered"] = pd.Series({"n": a[0], "mean": a[1], "t": a[2], "days": a[3]})
    # wide range in profile by direction of the day
    wr = []
    for lab, cond in [("wide up", (P["range_s"] > 2) & (P["s1"] > 0)), ("wide down", (P["range_s"] > 2) & (P["s1"] < 0))]:
        a = dayt(P[cond], "u2")
        wr.append({"case": lab, "n": a[0], "mean": a[1], "t": a[2], "days": a[3]})
    res["in prof wide range u2"] = pd.DataFrame(wr)
    return res
