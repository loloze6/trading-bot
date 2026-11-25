def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol30 = r1.rolling(30).std()
            vol90 = r1.rolling(90, min_periods=60).std()
            er = (c - c.shift(30)).abs() / c.diff().abs().rolling(30).sum()
            r7 = c / c.shift(7) - 1
            r30 = c / c.shift(30) - 1
            df = pd.DataFrame({
                "coin": coin, "w": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]),
                "vol30": vol30, "volratio": vol30 / vol90, "er": er,
                "r7s": r7 / (vol30 * np.sqrt(7)), "r30": r30,
                "fc": b["forecast"].astype(float),
            })
            for h in (3, 7, 14):
                df["f%d" % h] = c.shift(-h) / c - 1
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["day"] = d["ts"].dt.floor("D")
    d["y"] = d["ts"].dt.year
    out = {}
    # drift from non-overlapping grid per horizon
    for h in (3, 7, 14):
        g = d[d["pos"] % h == 0]
        m = g.groupby("coin")["f%d" % h].mean()
        sd = g.groupby("coin")["f%d" % h].std()
        d["x%d" % h] = d["f%d" % h] - d["coin"].map(m)
        d["usual%d" % h] = d["coin"].map(sd)

    def slope_day(sub, xcol, ycol):
        s = sub.dropna(subset=[xcol, ycol])
        if len(s) < 30:
            return (len(s), np.nan, np.nan)
        xm = s[xcol] - s[xcol].mean()
        beta = (xm * (s[ycol] - s[ycol].mean())).sum() / (xm ** 2).sum()
        e = s[ycol] - s[ycol].mean() - beta * xm
        sc = (xm * e).groupby(s["day"]).sum()
        se = np.sqrt((sc ** 2).sum()) / (xm ** 2).sum()
        return (len(s), beta, beta / se)

    g7 = d[d["pos"] % 7 == 0].copy()
    g7["vb"] = pd.qcut(g7["volratio"], 3, labels=["calmer", "mid", "agitated"])
    g7["calm"] = g7["vb"] != "agitated"
    # by coin, calmer+mid volratio
    res = []
    for k, s in g7[g7["calm"]].groupby("coin"):
        n, b_, t_ = slope_day(s, "r7s", "x7"); res.append({"coin": k, "n": n, "slope": b_, "t": t_})
    out["r7s->x7, volratio not top tercile, by coin"] = pd.DataFrame(res)
    res = []
    for k, s in g7[g7["calm"]].groupby("y"):
        n, b_, t_ = slope_day(s, "r7s", "x7"); res.append({"y": k, "n": n, "slope": b_, "t": t_})
    out["same, by year"] = pd.DataFrame(res)
    res = []
    for k, s in g7.groupby("w"):
        n, b_, t_ = slope_day(s[s["calm"]], "r7s", "x7"); res.append({"w": k, "n": n, "slope": b_, "t": t_})
    out["same, by window"] = pd.DataFrame(res)
    # graded interaction: r7s * (1 - volratio)  and r7s/volratio
    g7["int"] = g7["r7s"] / g7["volratio"]
    out["all grid: r7s->x7 / r7s*(1/volratio)->x7"] = pd.DataFrame(
        [dict(zip(["n", "slope", "t"], slope_day(g7, "r7s", "x7"))),
         dict(zip(["n", "slope", "t"], slope_day(g7, "int", "x7")))], index=["r7s", "r7s/volratio"])
    # volratio quintiles finer
    g7["vq"] = pd.qcut(g7["volratio"], 5, labels=False)
    res = []
    for k, s in g7.groupby("vq"):
        n, b_, t_ = slope_day(s, "r7s", "x7"); res.append({"vq": k, "vr_mean": s["volratio"].mean(), "n": n, "slope": b_, "t": t_})
    out["r7s->x7 by volratio quintile"] = pd.DataFrame(res)
    # active signal at multiple horizons, on each horizon's grid, size & t by day
    res = []
    for h in (3, 7, 14):
        g = d[(d["pos"] % h == 0) & (d["fc"] != 0)].dropna(subset=["x%d" % h])
        sx = np.sign(g["fc"]) * g["x%d" % h]
        sf = np.sign(g["fc"]) * g["f%d" % h]
        pdsum = sx.groupby(g["day"]).sum()
        ndays = len(pdsum)
        tt = sx.sum() / np.sqrt(((pdsum - pdsum / pdsum.size * 0) ** 2).sum()) if ndays > 2 else np.nan
        # simpler t: mean over SE with day clustering
        e = sx - sx.mean()
        se = np.sqrt((e.groupby(g["day"]).sum() ** 2).sum()) / len(sx)
        res.append({"h_days": h, "cases": len(sx), "days": ndays, "unusual": sx.mean(), "total": sf.mean(),
                    "t": sx.mean() / se, "strength": (sx / g["usual%d" % h]).mean()})
    out["active signal: move per case by horizon"] = pd.DataFrame(res)
    # same on all chop-agnostic grid: sign(r7s) scaled by r7s, in calmer two terciles, horizon 7, size per case
    g = g7[g7["calm"]].dropna(subset=["x7", "r7s"])
    g = g[g["r7s"].abs() > g["r7s"].abs().median()]
    sx = np.sign(g["r7s"]) * g["x7"]; sf = np.sign(g["r7s"]) * g["f7"]
    e = sx - sx.mean(); se = np.sqrt((e.groupby(g["day"]).sum() ** 2).sum()) / len(sx)
    out["calm, |r7s| above median: 7d move per case"] = pd.Series({"cases": len(sx), "unusual": sx.mean(), "total": sf.mean(), "t": sx.mean() / se})
    return out
