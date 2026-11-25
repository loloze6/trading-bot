def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            hh = h.rolling(20, min_periods=20).max(); ll = l.rolling(20, min_periods=20).min()
            r = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "rangepos": (c - ll) / (hh - ll),
                "lowdist": c / ll - 1,
                "r1": r, "r60back": c / c.shift(60) - 1,
                "fwd3": c.shift(-3) / c - 1, "fwd5": c.shift(-5) / c - 1,
                "calm": (b["regime"] != "chop").astype(int),
                "vol20": r.rolling(20).std(),
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["r1z"] = A["r1"] / A["vol20"]
    A["tr"] = np.where(A["r60back"] > 0.10, "rising", np.where(A["r60back"] < -0.10, "falling", "choppy"))
    A.loc[A["r60back"].isna(), "tr"] = np.nan
    out = {}
    def slope_cl(d, x, y):
        d = d.dropna(subset=[x, y])
        if len(d) < 30: return (np.nan, np.nan, len(d), 0)
        xm = d[x] - d[x].mean()
        b = (xm * (d[y] - d[y].mean())).sum() / (xm ** 2).sum()
        res = d[y] - d[y].mean() - b * xm
        s = (xm * res).groupby(d["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / (xm ** 2).sum()
        return (round(b, 5), round(b / se, 2), len(d), d["day"].nunique())
    res = {}
    for h in [3, 5]:
        G = A[A["pos"] % h == 0].copy()
        G["ex"] = G[f"fwd{h}"] - G.groupby("coin")[f"fwd{h}"].transform("mean")
        for tr in ["falling", "choppy", "rising"]:
            for cm in [1, 0]:
                sub = G[(G.tr == tr) & (G.calm == cm)]
                res[(h, tr, cm, "rangepos")] = slope_cl(sub, "rangepos", "ex")
                res[(h, tr, cm, "r1z")] = slope_cl(sub, "r1z", "ex")
        res[(h, "all", 1, "rangepos")] = slope_cl(G[G.calm == 1], "rangepos", "ex")
        res[(h, "all", 0, "r1z")] = slope_cl(G[G.calm == 0], "r1z", "ex")
        if h == 3:
            G3 = G
    out["slopes_daycluster"] = pd.DataFrame(res, index=["slope", "t_cl", "n", "days"]).T
    # falling calm, rangepos by window/year
    fc = G3[(G3.tr == "falling") & (G3.calm == 1)].dropna(subset=["rangepos", "ex"])
    out["fallcalm_by_year"] = fc.groupby("year").apply(lambda d: pd.Series({"slope_t": slope_cl(d, "rangepos", "ex")[1], "n": len(d), "low_mean": d[d.rangepos < 0.2]["ex"].mean()})).round(4)
    fc5 = fc.copy(); fc5["q"] = pd.qcut(fc5["rangepos"], 4, labels=False)
    out["fallcalm_quart"] = fc5.groupby("q")["ex"].agg(["mean", "count"]).round(4)
    # agitated r1z by year and quintile within agitated
    ag = G3[G3.calm == 0].dropna(subset=["r1z", "ex"])
    out["agit_r1z_by_year"] = ag.groupby("year").apply(lambda d: pd.Series({"slope_t": slope_cl(d, "r1z", "ex")[1], "n": len(d)})).round(3)
    # calm rangepos by year
    cl = G3[G3.calm == 1].dropna(subset=["rangepos", "ex"])
    out["calm_rangepos_by_year"] = cl.groupby("year").apply(lambda d: pd.Series({"slope_t": slope_cl(d, "rangepos", "ex")[1], "n": len(d)})).round(3)
    return out
