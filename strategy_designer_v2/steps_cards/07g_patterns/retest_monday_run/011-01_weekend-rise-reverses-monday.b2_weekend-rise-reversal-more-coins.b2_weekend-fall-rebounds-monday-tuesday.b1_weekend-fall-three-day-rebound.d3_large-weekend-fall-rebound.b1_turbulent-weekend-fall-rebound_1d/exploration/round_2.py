def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        d3 = []; d1 = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 3, 3)
            d3 += list(c[idx + 3] / c[idx] - 1)
            d1 += list(c[1:] / c[:-1] - 1)
        drift3 = np.mean(d3); drift1 = np.mean(d1)
        for w, b in wins.items():
            ts = pd.to_datetime(b["timestamp"])
            r = b["close"].pct_change()
            vol = r.rolling(20, min_periods=15).std().shift(1)
            vol365m = vol.rolling(365, min_periods=60).mean()
            f = pd.DataFrame({
                "coin": coin, "win": w, "ts": ts.values, "wd": ts.dt.weekday.values,
                "year": ts.dt.year.values,
                "z": (r / vol).values,
                "f1": (b["close"].shift(-1) / b["close"] - 1 - drift1).values,
                "f3": (b["close"].shift(-3) / b["close"] - 1 - drift3).values,
                "f3_4": (b["close"].shift(-7) / b["close"].shift(-4) - 1 - drift3).values,
                "vratio": (b["volume"] / b["volume"].rolling(20, min_periods=15).mean().shift(1)).values,
                "vr": (vol / vol365m).values,
            })
            rows.append(f)
    A = pd.concat(rows, ignore_index=True).dropna(subset=["z", "f3"])
    A["zc"] = A["z"].clip(-6, 6)
    out = {}

    def clustered(g, col="f3", sign=1.0):
        # mean per date across coins, then t over dates
        x = (sign * g[col]).groupby(g["ts"]).mean().dropna()
        n = len(x)
        if n < 3: return pd.Series({"cases": len(g), "dates": n, "mean": np.nan, "t_dates": np.nan})
        return pd.Series({"cases": len(g), "dates": n, "mean": x.mean(), "t_dates": x.mean() / (x.std() / np.sqrt(n))})

    # 1. date-clustered slope: per date cross-sectional regression? Use per-coin slopes and date-demeaned slope
    res = []
    for wd, g in A.groupby("wd"):
        g = g.copy()
        g["f3d"] = g["f3"] - g.groupby("ts")["f3"].transform("mean")
        g["zd"] = g["zc"] - g.groupby("ts")["zc"].transform("mean")
        lr = stats.linregress(g["zd"], g["f3d"])
        cs = []
        for c, h in g.groupby("coin"):
            if len(h) > 30:
                cs.append(stats.linregress(h["zc"], h["f3"]).slope)
        cs = np.array(cs)
        # time-series slope from per-date mean z vs mean f3
        m = g.groupby("ts")[["zc", "f3"]].mean()
        lt = stats.linregress(m["zc"], m["f3"])
        res.append({"wd": wd, "slope_within_date": lr.slope, "t_within": lr.slope / lr.stderr,
                    "slope_date_means": lt.slope, "t_date_means": lt.slope / lt.stderr, "dates": len(m),
                    "coins_neg_slope": int((cs < 0).sum()), "coins": len(cs)})
    out["slope f3 on z by weekday, robust"] = pd.DataFrame(res).round(5)

    S = A[A.wd == 6].copy()
    # 2. Sunday rises and falls, clustered
    S["zb"] = pd.cut(S["z"], [-np.inf, -2, -1, 1, 2, np.inf], labels=["<-2", "-2..-1", "mid", "1..2", ">2"])
    out["Sun f3 by z bucket, date-clustered"] = S.groupby("zb", observed=True).apply(clustered).round(4)
    out["Sun f3_4 (days 4-7) by z bucket, date-clustered"] = S.dropna(subset=["f3_4"]).groupby("zb", observed=True).apply(lambda g: clustered(g, "f3_4")).round(4)
    out["Sun f1 by z bucket, date-clustered"] = S.dropna(subset=["f1"]).groupby("zb", observed=True).apply(lambda g: clustered(g, "f1")).round(4)
    # 3. Sunday rises z>=1: by vr regime and by volume
    R = S[S.z >= 1].dropna(subset=["vr"]).copy()
    R["vrq"] = np.where(R["vr"] >= 1, "vr>=1", "vr<1")
    out["Sun rises z>=1 by vol regime"] = R.groupby("vrq").apply(clustered).round(4)
    R2 = S[S.z >= 1].dropna(subset=["vratio"]).copy()
    R2["vq"] = pd.qcut(R2["vratio"], 3, labels=["lowvol", "midvol", "highvol"])
    out["Sun rises z>=1 by volume tercile"] = R2.groupby("vq", observed=True).apply(clustered).round(4)
    out["Sun rises z>=1 by year"] = S[S.z >= 1].groupby("year").apply(clustered).round(4)
    # 4. Sunday slope by year
    ys = []
    for y, g in S.groupby("year"):
        g = g.copy()
        g["f3d"] = g["f3"] - g.groupby("ts")["f3"].transform("mean")
        g["zd"] = g["zc"] - g.groupby("ts")["zc"].transform("mean")
        lr = stats.linregress(g["zd"], g["f3d"])
        ys.append({"year": y, "slope_within": lr.slope, "t": lr.slope / lr.stderr, "n": len(g)})
    out["Sun slope within date by year"] = pd.DataFrame(ys).round(5)
    # 5. Friday moves continue into weekend
    F = A[A.wd == 4].copy()
    F["zb"] = pd.cut(F["z"], [-np.inf, -2, -1, 1, 2, np.inf], labels=["<-2", "-2..-1", "mid", "1..2", ">2"])
    out["Fri f3 by z bucket, date-clustered"] = F.groupby("zb", observed=True).apply(clustered).round(4)
    fy = []
    for y, g in F.groupby("year"):
        g = g.copy()
        g["f3d"] = g["f3"] - g.groupby("ts")["f3"].transform("mean")
        g["zd"] = g["zc"] - g.groupby("ts")["zc"].transform("mean")
        lr = stats.linregress(g["zd"], g["f3d"])
        fy.append({"year": y, "slope_within": lr.slope, "t": lr.slope / lr.stderr, "n": len(g)})
    out["Fri slope within date by year"] = pd.DataFrame(fy).round(5)
    # 6. Sunday slope by vr regime and by volume tercile (within-date)
    sv = []
    for lab, g in [("vr>=1", S[S.vr >= 1]), ("vr<1", S[S.vr < 1])] + \
                  [(f"vol_t{i}", gg) for i, (k, gg) in enumerate(S.dropna(subset=["vratio"]).groupby(pd.qcut(S.dropna(subset=["vratio"])["vratio"], 3, labels=False)))]:
        g = g.copy()
        g["f3d"] = g["f3"] - g.groupby("ts")["f3"].transform("mean")
        g["zd"] = g["zc"] - g.groupby("ts")["zc"].transform("mean")
        lr = stats.linregress(g["zd"], g["f3d"])
        sv.append({"group": lab, "slope_within": lr.slope, "t": lr.slope / lr.stderr, "n": len(g)})
    out["Sun slope within date by regime/volume"] = pd.DataFrame(sv).round(5)
    return out
