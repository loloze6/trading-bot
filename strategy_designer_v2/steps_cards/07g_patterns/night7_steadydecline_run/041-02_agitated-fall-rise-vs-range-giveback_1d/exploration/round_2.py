def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            rng = (h - l).rolling(30).mean().shift(1)
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "mv": (c - c.shift(1)) / rng,
                "r1": c.shift(-1) / c - 1,
                "r2": c.shift(-2) / c.shift(-1) - 1,
                "tr60": c / c.shift(60) - 1,
                "inprof": (b["regime"] == "unknown"),
                "clv": ((c - l) / (h - l)).where(h > l),
                "body": (c - o) / rng,
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["r1"].mean()
    D["x1"] = D["r1"] - D["coin"].map(drift)
    D["x2"] = D["r2"] - D["coin"].map(drift)
    D = D.dropna(subset=["mv", "x1"])

    def slope(sub, xcol, ycol="x1"):
        s = sub.dropna(subset=[xcol, ycol])
        if len(s) < 20: return {"n": len(s), "days": 0, "slope": np.nan, "t": np.nan}
        x = s[xcol].values; y = s[ycol].values
        X = np.column_stack([np.ones(len(x)), x])
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        e = y - X @ beta
        XtX_inv = np.linalg.inv(X.T @ X)
        g = pd.DataFrame(X * e[:, None]).groupby(s["day"].values).sum().values
        G = len(g)
        V = XtX_inv @ (g.T @ g) @ XtX_inv * G / (G - 1)
        return {"n": len(s), "days": G, "slope": beta[1], "t": beta[1] / np.sqrt(V[1, 1])}

    D["trend"] = pd.cut(D["tr60"], [-9, -0.1, 0.1, 99], labels=["fall", "chop", "rise"]).astype(str)
    D["grp"] = np.where(D["inprof"], "prof", "out_" + D["trend"])
    res = {}
    out = []
    for g, s in D.groupby("grp"):
        dn = s[s["mv"] < 0]; up = s[s["mv"] > 0]
        for nm, ss, xc in [("down_mv", dn, "mv"), ("up_mv", up, "mv"), ("all_mv", s, "mv"), ("all_clv", s, "clv"), ("down_clv", dn, "clv"), ("all_mv_day2", s, "mv")]:
            r = slope(ss, xc, "x2" if nm.endswith("day2") else "x1"); r["grp"] = g; r["test"] = nm; out.append(r)
    res["slopes_by_group"] = pd.DataFrame(out)
    P = D[D["inprof"]]
    dn = P[P["mv"] < 0]
    out = []
    for y, s in dn.groupby("year"):
        r = slope(s, "mv"); r["year"] = y; out.append(r)
    res["prof_down_mv_by_year"] = pd.DataFrame(out)
    out = []
    for y, s in dn.groupby("coin"):
        r = slope(s, "mv"); r["coin"] = y; out.append(r)
    res["prof_down_mv_by_coin"] = pd.DataFrame(out)
    # mv vs clv jointly on down days in profile: residual of x1 on mv, then slope on clv
    s = dn.dropna(subset=["clv"]).copy()
    b = np.polyfit(s["mv"], s["x1"], 1)
    s["res"] = s["x1"] - np.polyval(b, s["mv"])
    res["prof_down_clv_after_mv"] = pd.Series(slope(s, "clv", "res"))
    s = P.dropna(subset=["clv"]).copy()
    b = np.polyfit(s["clv"], s["x1"], 1)
    s["res"] = s["x1"] - np.polyval(b, s["clv"])
    res["prof_all_mv_after_clv"] = pd.Series(slope(s, "mv", "res"))
    # down-day bounce mean in short-term grades, prof
    dn2 = dn.assign(q=pd.qcut(dn["mv"], 4, labels=False))
    res["prof_down_quartiles"] = dn2.groupby("q").agg(n=("x1", "size"), mv=("mv", "mean"), x1=("x1", "mean"), x2=("x2", "mean"))
    return res
