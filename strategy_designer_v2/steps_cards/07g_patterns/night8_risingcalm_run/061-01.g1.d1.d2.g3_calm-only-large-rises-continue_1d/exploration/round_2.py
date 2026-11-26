def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=20).std().shift(1)
            z = r1 / sd
            z3 = (c / c.shift(3) - 1) / (sd * np.sqrt(3))
            z5 = (c / c.shift(5) - 1) / (sd * np.sqrt(5))
            tr60 = c / c.shift(60) - 1
            n = len(b)
            for h in (3, 5, 10):
                idx = np.arange(0, n, h)
                fh = (c.shift(-h) / c - 1).values[idx]
                d = pd.DataFrame({"coin": coin, "win": w, "h": h,
                    "day": pd.to_datetime(b["timestamp"]).dt.floor("D").values[idx],
                    "z": z.values[idx], "z3": z3.values[idx], "z5": z5.values[idx],
                    "tr60": tr60.values[idx], "f": fh,
                    "calm": (b["regime"] != "chop").values[idx]})
                rows.append(d)
    D = pd.concat(rows, ignore_index=True).dropna(subset=["f"])
    D["drift"] = D.groupby(["coin", "h"])["f"].transform("mean")
    D["u"] = D["f"] - D["drift"]
    D["usual"] = D.groupby(["coin", "h"])["f"].transform("std")

    def tcl(g, col="u"):
        m = g[col].mean()
        s = g.groupby("day")[col].apply(lambda x: (x - m).sum())
        G = len(s)
        se = np.sqrt((s ** 2).sum()) / len(g) * np.sqrt(G / max(G - 1, 1))
        return pd.Series({"n": len(g), "days": G, "mean": m, "t": m / se if se > 0 else np.nan})

    def slope(g, x):
        g = g.dropna(subset=[x])
        xx = g[x].clip(-4, 4); xc = xx - xx.mean()
        b = (xc * g["u"]).sum() / (xc ** 2).sum()
        e = g["u"] - g["u"].mean() - b * xc
        s = (xc * e).groupby(g["day"]).sum()
        G = len(s)
        se = np.sqrt((s ** 2).sum() * G / (G - 1)) / (xc ** 2).sum()
        return pd.Series({"n": len(g), "days": G, "slope": b, "t": b / se})

    out = {}
    for x in ("z", "z3", "z5"):
        out["slope_" + x] = D.groupby(["h", "calm"]).apply(lambda g: slope(g, x))
    C = D[D["calm"]].dropna(subset=["z3"]).copy()
    C["side"] = np.where(C["z3"] >= 1, "up>=1", np.where(C["z3"] <= -1, "down<=-1", "mid"))
    out["calm_z3_side_h"] = C.groupby(["h", "side"]).apply(tcl)
    A = D[~D["calm"]].dropna(subset=["z3"]).copy()
    A["side"] = np.where(A["z3"] >= 1, "up>=1", np.where(A["z3"] <= -1, "down<=-1", "mid"))
    out["agit_z3_side_h"] = A.groupby(["h", "side"]).apply(tcl)
    C5 = D[(D["h"] == 5) & D["calm"]].dropna(subset=["tr60"]).copy()
    C5["trend"] = np.where(C5["tr60"] > 0.1, "rising", np.where(C5["tr60"] < -0.1, "falling", "choppy"))
    out["calm_h5_slope_z3_by_trend"] = C5.groupby("trend").apply(lambda g: slope(g, "z3"))
    out["calm_h5_slope_z3_by_coin"] = C5.groupby("coin").apply(lambda g: slope(g, "z3"))
    out["calm_h5_slope_z3_by_window"] = D[(D["h"] == 5) & D["calm"]].groupby("win").apply(lambda g: slope(g, "z3"))
    # strength of graded effect in usual move units: slope / usual
    return out
