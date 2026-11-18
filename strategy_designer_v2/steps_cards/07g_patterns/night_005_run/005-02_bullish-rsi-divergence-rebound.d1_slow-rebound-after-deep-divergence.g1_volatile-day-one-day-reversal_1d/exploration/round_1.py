def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(20).std()
            z = r / sd
            vr = sd / sd.rolling(60, min_periods=20).mean()
            nxt = c.shift(-1)/c - 1
            nxt3 = c.shift(-3)/c - 1
            r5 = c/c.shift(5) - 1
            z5 = r5/(sd*np.sqrt(5))
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "r": r, "z": z, "vr": vr,
                               "nxt": nxt, "nxt3": nxt3, "z5": z5, "wd": ts.dt.weekday, "yr": ts.dt.year,
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "fc": b["forecast"].astype(float)})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    mu = d.groupby("coin")["nxt"].transform("mean")
    d["ex"] = d["nxt"] - mu
    d["hv"] = d["vr"] >= 1
    d["vrq"] = pd.qcut(d["vr"], 4, labels=["q1", "q2", "q3", "q4"])

    def slope(g, x, y):
        g = g[[x, y]].dropna()
        if len(g) < 30: return (np.nan, np.nan, len(g))
        res = stats.linregress(g[x], g[y])
        return (res.slope, res.slope/res.stderr, len(g))

    t = []
    for k, g in d.groupby(["coin", "hv"]):
        s = slope(g, "z", "ex"); t.append([*k, *s])
    for k, g in d.groupby("vrq"):
        s = slope(g, "z", "ex"); t.append(["all", k, *s])
    out["slope next-day ex on z by coin/hv and vr quartile"] = pd.DataFrame(t, columns=["coin", "grp", "slope", "t", "n"])

    # up vs down days in high vol
    t = []
    for hv in [True, False]:
        for sgn in ["up", "down"]:
            g = d[(d.hv == hv) & ((d.z > 0) if sgn == "up" else (d.z < 0))]
            s = slope(g, "z", "ex"); t.append([hv, sgn, *s, g["ex"].mean()])
    out["asymmetry up/down"] = pd.DataFrame(t, columns=["hv", "side", "slope", "t", "n", "mean_ex"])

    # z bins high vol: mean next-day ex
    h = d[d.hv].dropna(subset=["z", "ex"]).copy()
    h["zb"] = pd.cut(h.z, [-10, -2, -1, -0.3, 0.3, 1, 2, 10])
    out["hv next ex by z bin"] = h.groupby("zb", observed=True)["ex"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])

    # 3-day horizon non-overlapping, and 5-day z
    g3 = d[(d.pos % 3 == 0)].copy()
    g3["ex3"] = g3["nxt3"] - g3.groupby("coin")["nxt3"].transform("mean")
    t = []
    for hv in [True, False]:
        s = slope(g3[g3.hv == hv], "z", "ex3"); t.append(["z->3d", hv, *s])
        s = slope(g3[g3.hv == hv], "z5", "ex3"); t.append(["z5->3d", hv, *s])
    out["multi-day"] = pd.DataFrame(t, columns=["what", "hv", "slope", "t", "n"])

    # weekday
    out["weekday next ex"] = d.groupby("wd")["ex"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    # by year slope hv
    t = []
    for k, g in d[d.hv].groupby("yr"):
        s = slope(g, "z", "ex"); t.append([k, *s])
    out["hv slope by year"] = pd.DataFrame(t, columns=["yr", "slope", "t", "n"])
    # book: market part vs timing
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            dd.append(x.assign(coin=coin, w=w))
    D = pd.concat(dd)
    out["book stats"] = pd.Series({"book_mean": D.book_return.mean(), "coin_mean": D.coin_return.mean(),
                                   "mean_alloc": d.alloc.mean(), "share_long": (d.alloc > 0).mean(), "share_short": (d.alloc < 0).mean(),
                                   "share_flat": (d.alloc == 0).mean()})
    d["pnl"] = d.alloc*d.nxt
    out["pnl by side"] = d.assign(side=np.sign(d.alloc)).groupby(["coin", "side"])["pnl"].agg(["mean", "sum", "count"])
    return out
