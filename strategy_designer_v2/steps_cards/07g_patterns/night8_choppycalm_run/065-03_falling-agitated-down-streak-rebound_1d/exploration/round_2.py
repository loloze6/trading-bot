def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol20 = r.rolling(20).std()
            down = (r < 0).astype(int)
            streak = down.groupby((down == 0).cumsum()).cumsum()
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "fa": (b["regime"] == "unknown").astype(int),
                "r": r, "z1": r / vol20,
                "z5": (c / c.shift(5) - 1) / (vol20 * np.sqrt(5)),
                "r60": c / c.shift(60) - 1,
                "n1": c.shift(-1) / c - 1, "n3": c.shift(-3) / c - 1,
                "streak": streak,
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["tr"] = np.where(d["r60"] > 0.10, "rising", np.where(d["r60"] < -0.10, "falling", np.where(d["r60"].notna(), "choppy", "na")))
    def clust_slope(g, xcol, ycol):
        g = g.dropna(subset=[xcol, ycol])
        if len(g) < 30: return pd.Series({"slope": np.nan, "t": np.nan, "n": len(g), "days": 0})
        y = g[ycol] - g["coin"].map(g.groupby("coin")[ycol].mean())
        x = g[xcol]; xd = x - x.mean()
        b = (xd * (y - y.mean())).sum() / (xd ** 2).sum()
        res = (y - y.mean()) - b * xd
        s = (xd * res).groupby(g["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / (xd ** 2).sum()
        return pd.Series({"slope": b, "t": b / se, "n": len(g), "days": g["day"].nunique()})
    out = {}
    g3 = d[d["pos"] % 3 == 0]
    res = {}
    for (fa, tr), g in g3.groupby(["fa", "tr"]):
        res[(fa, tr, "z5->3d")] = clust_slope(g, "z5", "n3")
    for (fa, tr), g in d.groupby(["fa", "tr"]):
        res[(fa, tr, "z1->1d")] = clust_slope(g, "z1", "n1")
        res[(fa, tr, "z5->1d")] = clust_slope(g, "z5", "n1")
    out["slopes_by_fa_trend"] = pd.DataFrame(res).T
    res2 = {}
    for fa, g in g3.groupby("fa"):
        res2[(fa, "z5->3d")] = clust_slope(g, "z5", "n3")
    for fa, g in d.groupby("fa"):
        res2[(fa, "z1->1d")] = clust_slope(g, "z1", "n1")
        res2[(fa, "streak->1d")] = clust_slope(g, "streak", "n1")
    out["slopes_by_fa"] = pd.DataFrame(res2).T
    # FA: streak effect controlling for z1 (residualise)
    fa = d[d["fa"] == 1].dropna(subset=["z1", "n1"]).copy()
    X = np.column_stack([np.ones(len(fa)), fa["z1"]])
    bz, *_ = np.linalg.lstsq(X, fa["n1"].values, rcond=None)
    fa["resid"] = fa["n1"] - X @ bz
    fa["sk"] = fa["streak"].clip(upper=4)
    out["fa_streak_after_z1"] = fa.groupby("sk")["resid"].agg(["mean", "count"])
    # non-FA z5 3d continuation by year
    nf = g3[g3["fa"] == 0]
    out["nonfa_z5_3d_by_year"] = pd.DataFrame({y: clust_slope(g, "z5", "n3") for y, g in nf.groupby("year")}).T
    out["nonfa_z5_3d_by_window"] = pd.DataFrame({w: clust_slope(g, "z5", "n3") for w, g in nf.groupby("win")}).T
    return out
