def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(20).std()
            hi = c.shift(1).rolling(20).max()
            dist = (c / hi - 1) / sd
            hi10 = c.shift(1).rolling(10).max()
            dist10 = (c / hi10 - 1) / sd
            r60 = c / c.shift(60) - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)), "ts": ts.values,
                "year": ts.dt.year.values, "wd": ts.dt.weekday.values,
                "inprof": (b["regime"] == "unknown").values,
                "dist": dist.values, "dist10": dist10.values, "r60": r60.values,
                "z1": (r / sd).values,
                "fwd5": (c.shift(-5) / c - 1).values, "fwd1": (c.shift(-1) / c - 1).values,
                "fwd10": (c.shift(-10) / c - 1).values})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)

    def ctstat(v, days):
        d = pd.DataFrame({"v": v.values, "d": days.values}).dropna()
        n = len(d); m = d["v"].mean()
        s = (d["v"] - m).groupby(d["d"]).sum()
        G = len(s)
        se = np.sqrt((s ** 2).sum() * G / max(G - 1, 1)) / n
        return m, m / se if se > 0 else np.nan, n, G

    def cslope(x, y, days):
        d = pd.DataFrame({"x": x.values, "y": y.values, "d": days.values}).dropna()
        n = len(d)
        X = np.column_stack([np.ones(n), d["x"].values])
        beta = np.linalg.lstsq(X, d["y"].values, rcond=None)[0]
        e = d["y"].values - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        u = pd.DataFrame(X * e[:, None]).groupby(d["d"].values).sum().values
        G = len(u)
        V = XtXi @ (u.T @ u) @ XtXi * G / (G - 1)
        return beta[1], beta[1] / np.sqrt(V[1, 1]), n, G

    out = {}
    G5 = A[A["pos"] % 5 == 0].dropna(subset=["fwd5"]).copy()
    G5["ex5"] = G5["fwd5"] - G5["coin"].map(G5.groupby("coin")["fwd5"].mean())
    G5["trend"] = np.where(G5["r60"] > 0.10, "rising", np.where(G5["r60"] < -0.10, "falling", np.where(G5["r60"].notna(), "choppy", "na")))
    G5.loc[G5["inprof"], "trend"] = "rising"
    G5["dbin"] = pd.cut(G5["dist"], [-99, -3, -1.5, -0.5, 0, 99], labels=["<-3", "-3..-1.5", "-1.5..-0.5", "-0.5..0", ">0"])
    res = []
    for tr in ["rising", "choppy", "falling"]:
        sub = G5[G5["trend"] == tr]
        for bn, s2 in sub.groupby("dbin", observed=True):
            m, t, n, g = ctstat(s2["ex5"], s2["ts"])
            res.append({"trend": tr, "bin": bn, "mean": round(m, 4), "t_day": round(t, 2), "n": n, "days": g})
    out["dist_by_trend_clustered"] = pd.DataFrame(res)
    sl = []
    for tr in ["rising", "choppy", "falling"]:
        sub = G5[G5["trend"] == tr]
        for col in ["dist", "dist10"]:
            b_, t, n, g = cslope(sub[col].clip(-6, 4), sub["ex5"], sub["ts"])
            sl.append({"trend": tr, "x": col, "slope": round(b_, 5), "t_day": round(t, 2), "n": n, "days": g})
    allsub = G5[G5["trend"] != "na"]
    b_, t, n, g = cslope(allsub["dist"].clip(-6, 4), allsub["ex5"], allsub["ts"])
    sl.append({"trend": "all_known", "x": "dist", "slope": round(b_, 5), "t_day": round(t, 2), "n": n, "days": g})
    b_, t, n, g = cslope(G5["dist"].clip(-6, 4), G5["ex5"], G5["ts"])
    sl.append({"trend": "every", "x": "dist", "slope": round(b_, 5), "t_day": round(t, 2), "n": n, "days": g})
    out["slopes"] = pd.DataFrame(sl)
    # by year: slope of ex5 on dist, all bars
    yr = []
    for y, s2 in G5.groupby("year"):
        b_, t, n, g = cslope(s2["dist"].clip(-6, 4), s2["ex5"], s2["ts"])
        yr.append({"year": y, "slope": round(b_, 5), "t_day": round(t, 2), "n": n})
    out["slope_by_year_all"] = pd.DataFrame(yr)
    # 10-day horizon
    G10 = A[A["pos"] % 10 == 0].dropna(subset=["fwd10"]).copy()
    G10["ex10"] = G10["fwd10"] - G10["coin"].map(G10.groupby("coin")["fwd10"].mean())
    h = []
    for nm, s2 in [("in", G10[G10.inprof]), ("out", G10[~G10.inprof]), ("all", G10)]:
        b_, t, n, g = cslope(s2["dist"].clip(-6, 4), s2["ex10"], s2["ts"])
        h.append({"set": nm, "slope10": round(b_, 5), "t_day": round(t, 2), "n": n})
    out["slope_10day"] = pd.DataFrame(h)
    # weekday, day-clustered and by year
    A1 = A.dropna(subset=["fwd1"]).copy()
    A1["ex1"] = A1["fwd1"] - A1["coin"].map(A1.groupby("coin")["fwd1"].mean())
    wdr = []
    for wd, s2 in A1.groupby("wd"):
        m, t, n, g = ctstat(s2["ex1"], s2["ts"])
        wdr.append({"wd": wd, "mean": round(m, 5), "t_day": round(t, 2), "days": g})
    out["weekday_clustered"] = pd.DataFrame(wdr)
    piv = A1.groupby(["year", "wd"])["ex1"].mean().unstack().round(4)
    out["weekday_by_year"] = piv
    # small down day out of profile, clustered
    o = G5[~G5.inprof].copy()
    o["zb"] = pd.qcut(o["z1"], 5, labels=False)
    zr = []
    for zb, s2 in o.groupby("zb"):
        m, t, n, g = ctstat(s2["ex5"], s2["ts"])
        zr.append({"zbin": zb, "lo": round(s2["z1"].min(), 2), "hi": round(s2["z1"].max(), 2), "mean": round(m, 4), "t_day": round(t, 2), "n": n})
    out["z1_out_clustered"] = pd.DataFrame(zr)
    return out
