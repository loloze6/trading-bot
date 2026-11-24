def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]
            r = c.pct_change()
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "r": r,
                "vol20": r.rolling(20).std(),
                "vol60m": r.rolling(20).std().rolling(60).mean(),
                "loc": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "rng": (b["high"] - b["low"]) / b["open"],
                "body": (c - b["open"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "r5p": c / c.shift(5) - 1,
                "f1": c.shift(-1) / c - 1,
                "f2_3": c.shift(-3) / c.shift(-1) - 1,
                "f3": c.shift(-3) / c - 1,
                "alloc": b["postRebalance_current_allocation"],
            })
            d["z"] = d["r"] / d["vol20"]
            d["volrel"] = d["vol20"] / d["vol60m"]
            d["rngz"] = d["rng"] / d["rng"].rolling(20).mean()
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu1 = D.groupby("coin")["f1"].mean()
    D["x1"] = D["f1"] - D["coin"].map(mu1)
    mu3 = D[D.pos % 3 == 0].groupby("coin")["f3"].mean()
    D["x3"] = D["f3"] - D["coin"].map(mu3)
    D["x23"] = D["f2_3"] - D["coin"].map(D.groupby("coin")["f2_3"].mean())

    def ct(s, col):
        s = s.dropna(subset=[col])
        if len(s) < 5: return pd.Series({"n": len(s), "days": s.day.nunique(), "mean": np.nan, "t": np.nan})
        m = s[col].mean()
        g = (s[col] - m).groupby(s["day"]).sum()
        se = np.sqrt((g ** 2).sum()) / len(s)
        return pd.Series({"n": len(s), "days": s.day.nunique(), "mean": m, "t": m / se if se > 0 else np.nan})

    out = {}
    zb = pd.cut(D["z"], [-99, -3, -2, -1, 1, 2, 3, 99])
    out["x1_by_z"] = D.groupby(zb).apply(lambda s: ct(s, "x1"))
    dn = D[D.z <= -2]
    out["z<=-2_x1_by_loc"] = dn.groupby(pd.cut(dn["loc"], [-0.01, 0.25, 0.5, 1.01])).apply(lambda s: ct(s, "x1"))
    up = D[D.z >= 2]
    out["z>=2_x1_by_loc"] = up.groupby(pd.cut(up["loc"], [-0.01, 0.75, 1.01])).apply(lambda s: ct(s, "x1"))
    cap = D[(D.z <= -2) & (D["loc"] <= 0.25)]
    out["cap_x1_by_volrel_tercile"] = cap.groupby(pd.qcut(cap["volrel"], 3)).apply(lambda s: ct(s, "x1"))
    out["cap_x23_days2to3"] = ct(cap, "x23")
    out["cap_x1_by_prior5d"] = cap.groupby(pd.qcut(cap["r5p"], 3)).apply(lambda s: ct(s, "x1"))
    out["cap_x1_by_year"] = cap.groupby(cap.day.dt.year).apply(lambda s: ct(s, "x1"))
    out["cap_by_coin"] = cap.groupby("coin").apply(lambda s: ct(s, "x1"))
    out["all_x1_by_volrel_quint"] = D.groupby(pd.qcut(D["volrel"], 5)).apply(lambda s: ct(s, "x1"))
    out["all_x1_by_weekday"] = D.groupby("wd").apply(lambda s: ct(s, "x1"))
    # brief: wide range flat close after run
    run = D["r5p"].abs() / (D["vol20"] * np.sqrt(5))
    D["run"] = run
    fl = D[(D.run > 1) & (D["body"].abs() < 0.2)]
    fl = fl.assign(xs=-np.sign(fl["r5p"]) * fl["x1"])
    out["flat_after_run_xs_by_rngz"] = fl.groupby(pd.qcut(fl["rngz"], 3)).apply(lambda s: ct(s, "xs"))
    return out
