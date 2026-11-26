def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            d = pd.DataFrame({
                "coin": coin, "ts": pd.to_datetime(b["timestamp"]),
                "regime": b["regime"].astype(str),
                "r1": r1, "r2": c.pct_change(2), "r3": c.pct_change(3), "r5": c.pct_change(5),
                "sd30": sd30,
                "wick": (h - c) / c / sd30,
                "clv": (c - l) / (h - l).replace(0, np.nan),
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1,
                "pos": np.arange(len(b)),
                "fc": b["forecast"],
                "alloc": b["postRebalance_current_allocation"],
            })
            d["z1"] = d["r1"] / d["sd30"]
            d["z3"] = d["r3"] / (d["sd30"] * np.sqrt(3))
            d["z5"] = d["r5"] / (d["sd30"] * np.sqrt(5))
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["r1"].transform("mean")
    D["x1"] = D["f1"] - mu; D["x2"] = D["f2"] - 2 * mu
    D["day"] = D["ts"].dt.floor("D")
    D["inprof"] = D["regime"] != "chop"

    def ct(s, days):
        g = pd.DataFrame({"v": s, "d": days}).dropna()
        if len(g) < 5: return (np.nan, len(g), np.nan, 0)
        m = g["v"].mean(); dev = (g["v"] - m).groupby(g["d"]).sum()
        n = len(g); k = len(dev)
        se = np.sqrt((dev ** 2).sum() * k / max(k - 1, 1)) / n
        return (m, n, m / se if se > 0 else np.nan, k)

    def tab(sub, col, target, q=4):
        s = sub.dropna(subset=[col, target]).copy()
        if len(s) < 30: return None
        s["b"] = pd.qcut(s[col].rank(method="first"), q, labels=False)
        res = []
        for k, g in s.groupby("b"):
            m, n, t, nd = ct(g[target], g["day"])
            res.append({"bin": k, "mean_x": g[col].mean(), "m": m, "n": n, "t": t, "days": nd})
        return pd.DataFrame(res)

    def one(s, target="x1"):
        return pd.Series(ct(s[target], s["day"]), index=["m", "n", "t", "days"])

    P = D[D["inprof"]]; O = D[~D["inprof"]]
    UP = P[P["r1"] > 0]
    out = {}
    out["prof_up_all_x1"] = one(UP)
    out["prof_up_r3neg_x1"] = one(UP[UP["r3"] < 0])
    out["prof_up_r3pos_x1"] = one(UP[UP["r3"] > 0])
    out["prof_up_z1_x1"] = tab(UP, "z1", "x1")
    out["prof_up_z3_x1"] = tab(UP, "z3", "x1")
    out["prof_up_wick_x1"] = tab(UP, "wick", "x1")
    out["prof_up_clv_x1"] = tab(UP, "clv", "x1")
    R3 = P[P["r3"] > 0]
    out["prof_r3pos_z3_x1"] = tab(R3, "z3", "x1")
    R3g = R3[R3["pos"] % 2 == 0]
    out["prof_r3pos_z3_x2_grid2"] = tab(R3g, "z3", "x2")
    P2 = P[P["pos"] % 2 == 0]
    out["prof_z3_x2_grid2"] = tab(P2, "z3", "x2")
    out["prof_z5_x1"] = tab(P, "z5", "x1")
    UO = O[O["r1"] > 0]
    out["out_up_x1"] = one(UO)
    out["out_up_r3pos_x1"] = one(UO[UO["r3"] > 0])
    out["out_up_z1_x1"] = tab(UO, "z1", "x1")
    # by year: up days in profile
    yr = []
    for k, g in UP.groupby(UP["ts"].dt.year):
        m, n, t, nd = ct(g["x1"], g["day"]); yr.append({"year": k, "m": m, "n": n, "t": t})
    out["prof_up_year"] = pd.DataFrame(yr)
    co = []
    for k, g in UP.groupby("coin"):
        m, n, t, nd = ct(g["x1"], g["day"]); co.append({"coin": k, "m": m, "n": n, "t": t})
    out["prof_up_coin"] = pd.DataFrame(co)
    # active bars of the book: forecast cases split by r3 bucket
    A = P[P["fc"].fillna(0) < 0]
    out["cases_z3_x1"] = tab(A, "z3", "x1", q=3)
    return out
