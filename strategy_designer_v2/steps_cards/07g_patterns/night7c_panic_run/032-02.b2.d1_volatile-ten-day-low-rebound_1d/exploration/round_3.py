def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            if len(b) < 40: continue
            c = b["close"]; h = b["high"]; l = b["low"]
            mr = (h - l).rolling(30).mean().shift(1)
            ts = pd.to_datetime(b["timestamp"])
            r1 = c / c.shift(1) - 1
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "fwd": c.shift(-1) / c - 1,
                "clv": (c - l) / (h - l).replace(0, np.nan),
                "dist_hi": (h - c) / mr,
                "r1z": r1 / r1.rolling(30).std().shift(1),
                "rng_rel": (h - l) / mr,
                "day": ts.dt.floor("D"), "year": ts.dt.year,
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True).dropna(subset=["fwd", "clv", "dist_hi", "r1z", "rng_rel"])
    dr = d.groupby("coin")["fwd"].mean(); sd = d.groupby("coin")["fwd"].std()
    d["u"] = d["fwd"] - d["coin"].map(dr)
    d["s"] = d["u"] / d["coin"].map(sd)
    for col in ["clv", "dist_hi", "r1z", "rng_rel"]:
        d["z_" + col] = d.groupby("coin")[col].transform(lambda v: (v - v.mean()) / v.std())

    def slope(g, xs):
        X = np.column_stack([np.ones(len(g))] + [g[x].values for x in xs])
        y = g["s"].values
        XtX = X.T @ X; b = np.linalg.solve(XtX, X.T @ y)
        e = y - X @ b
        sc = pd.DataFrame(X * e[:, None]).groupby(g["day"].values).sum().values
        V = np.linalg.inv(XtX) @ (sc.T @ sc) @ np.linalg.inv(XtX)
        t = b / np.sqrt(np.diag(V))
        out = {}
        for i, x in enumerate(["const"] + xs):
            out["b_" + x] = b[i]; out["t_" + x] = t[i]
        out["n"] = len(g); out["days"] = g["day"].nunique()
        return pd.Series(out)

    out = {}
    out["clv_alone"] = slope(d, ["z_clv"])
    out["clv_with_r1z_range"] = slope(d, ["z_clv", "z_r1z", "z_rng_rel"])
    out["disthi_with_r1z_range"] = slope(d, ["z_dist_hi", "z_r1z", "z_rng_rel"])
    out["clv_by_year"] = d.groupby("year").apply(lambda g: slope(g, ["z_clv"]))
    out["clv_by_coin"] = d.groupby("coin").apply(lambda g: slope(g, ["z_clv"]))
    d["wn"] = d["win"].str[1:].astype(int)
    out["clv_by_window"] = d.groupby("win").apply(lambda g: slope(g, ["z_clv"]))
    # graded within wide-range days
    d["rq"] = d.groupby("coin")["rng_rel"].transform(lambda v: pd.qcut(v, 3, labels=False, duplicates="drop"))
    out["clv_by_range_tercile"] = d.groupby("rq").apply(lambda g: slope(g, ["z_clv"]))
    return out
