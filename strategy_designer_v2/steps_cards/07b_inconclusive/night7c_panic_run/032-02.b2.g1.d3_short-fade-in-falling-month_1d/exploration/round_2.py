def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            allr.append(pd.Series(b["close"].values).pct_change().dropna())
        mu1 = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            rng = (h - l).replace(0, np.nan)
            cl = (c - l) / rng
            rm = rng / rng.rolling(20).mean()
            r20 = c / c.shift(20) - 1
            fcl = -b.get("debug_info.components.close_loc.post_pipeline_value", pd.Series(np.nan, index=b.index))
            frm = -b.get("debug_info.components.range_mult.post_pipeline_value", pd.Series(np.nan, index=b.index))
            d = pd.DataFrame({"coin": coin, "w": w, "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                              "f": b["forecast"], "cl": cl, "rm": rm, "r20": r20,
                              "fcl": fcl, "frm": frm,
                              "yr": pd.to_datetime(b["timestamp"]).dt.year})
            d["x1"] = -(c.shift(-1) / c - 1 - mu1)
            rows.append(d)
    D = pd.concat(rows).dropna(subset=["x1", "cl"])
    C = D[D.f < 0].copy()
    def wm_t(g, wcol):
        g = g.dropna(subset=[wcol]); wts = g[wcol].abs()
        if wts.sum() == 0 or len(g) < 10: return pd.Series({"n": len(g), "wmean": np.nan, "t": np.nan})
        m = (g.x1 * wts).sum() / wts.sum()
        dev = (wts * (g.x1 - m)).groupby(g.day).sum()
        Dn = len(dev)
        se = np.sqrt((dev ** 2).sum() * Dn / (Dn - 1)) / wts.sum()
        return pd.Series({"n": len(g), "days": Dn, "wmean": m, "t": m / se})
    def slope_t(g, xcol):
        g = g.dropna(subset=[xcol])
        x = g[xcol] - g[xcol].mean(); y = g.x1
        b1 = (x * y).sum() / (x ** 2).sum()
        e = y - y.mean() - b1 * x
        s = (x * e).groupby(g.day).sum()
        se = np.sqrt((s ** 2).sum()) / (x ** 2).sum()
        return pd.Series({"n": len(g), "slope": b1, "t": b1 / se})
    out = {}
    out["weighted_by_component"] = pd.DataFrame({
        "full_forecast": wm_t(C, "f"),
        "closeloc_only": wm_t(C, "fcl"),
        "rangemult_only": wm_t(C, "frm")}).T
    out["slope_x1_on_cl_regime"] = slope_t(C, "cl")
    out["slope_x1_on_cl_nonregime"] = slope_t(D[D.r20 >= 0], "cl")
    out["slope_x1_on_rm_regime"] = slope_t(C, "rm")
    out["slope_cl_by_year"] = C.groupby("yr").apply(lambda g: slope_t(g, "cl"))
    out["slope_cl_by_coin"] = C.groupby("coin").apply(lambda g: slope_t(g, "cl"))
    C["rmh"] = (C.rm > C.rm.median()).map({True: "wide", False: "narrow"})
    out["slope_cl_by_rm_half"] = C.groupby("rmh").apply(lambda g: slope_t(g, "cl"))
    C["clq"] = pd.qcut(C.cl, 5, labels=False, duplicates="drop")
    out["clq_mean_by_year"] = C.groupby(["yr", "clq"]).x1.mean().unstack()
    return out
