def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            h, l, c, o = b["high"], b["low"], b["close"], b["open"]
            rng = (h - l)
            base = rng.shift(1).rolling(30, min_periods=20).mean()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "clv": (c - l) / rng.replace(0, np.nan),
                "rw": rng / base,
                "ret0": c / c.shift(1) - 1,
                "ret3": c / c.shift(3) - 1,
                "nxt": c.shift(-1) / c - 1,
                "nxt2": c.shift(-2) / c - 1,
                "agit": (b["regime"] != "chop").astype(int),
                "tr60": c / c.shift(60) - 1,
                "pos": np.arange(len(b)),
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["dm"] = D["nxt"] - D.groupby("coin")["nxt"].transform("mean")
    D["dm2"] = D["nxt2"] - D.groupby("coin")["nxt2"].transform("mean")
    D["day"] = D["ts"].dt.floor("D")
    D["trend"] = np.where(D["tr60"] > 0.1, "rising", np.where(D["tr60"] < -0.1, "falling", np.where(D["tr60"].notna(), "choppy", None)))
    D["lowsc"] = (1 - D["clv"]) * D["rw"]   # idea's product
    out = {}

    def cell(x, col="dm"):
        x = x.dropna(subset=[col])
        m = x[col].mean()
        dev = (x[col] - m).groupby(x["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(x) if len(x) else np.nan
        return pd.Series({"n": len(x), "mean%": 100 * m, "t": m / se if se else np.nan})

    def slope(x, xc, yc="dm"):
        x = x.dropna(subset=[xc, yc])
        if len(x) < 50: return pd.Series({"n": len(x), "slope": np.nan, "t": np.nan})
        xv = x[xc] - x[xc].mean(); yv = x[yc] - x[yc].mean()
        b = (xv * yv).sum() / (xv ** 2).sum()
        e = yv - b * xv
        g = (e * xv).groupby(x["day"]).sum()
        G = len(g)
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / (xv ** 2).sum()
        return pd.Series({"n": len(x), "days": G, "slope": b, "t": b / se})

    # slope of next-day on idea product, by trend x agit
    out["slope lowsc by trend x agit"] = D.groupby(["trend", "agit"]).apply(lambda x: slope(x, "lowsc"))
    out["slope ret0 by trend x agit"] = D.groupby(["trend", "agit"]).apply(lambda x: slope(x, "ret0"))
    # graded inside falling agitated
    F = D[(D["trend"] == "falling") & (D["agit"] == 1)].copy()
    F["q"] = pd.qcut(F["lowsc"], 5, labels=False)
    out["falling agit: lowsc quintile"] = F.groupby("q").apply(cell)
    F["q0"] = pd.qcut(F["ret0"], 5, labels=False)
    out["falling agit: ret0 quintile"] = F.groupby("q0").apply(cell)
    # by window sign, falling agit slope on lowsc
    out["falling agit slope by window"] = F.groupby("win").apply(lambda x: slope(x, "lowsc"))
    # by coin
    out["falling agit slope by coin"] = F.groupby("coin").apply(lambda x: slope(x, "lowsc"))
    # double sort in agitated: ret0 sign x clv half
    A = D[D["agit"] == 1].copy()
    A["up"] = (A["ret0"] > 0).astype(int)
    A["clvh"] = (A["clv"] > 0.5).astype(int)
    out["agit: up-day x clv-half"] = A.groupby(["up", "clvh"]).apply(cell)
    # 2-day horizon, non-overlapping grid (pos even)
    G2 = D[D["pos"] % 2 == 0]
    out["2d slope lowsc by trend x agit"] = G2.groupby(["trend", "agit"]).apply(lambda x: slope(x, "lowsc", "dm2"))
    # rising agit: does high close/wide continue?
    R = D[(D["trend"] == "rising")].copy()
    R["hisc"] = R["clv"] * R["rw"]
    out["rising: slope hisc by agit"] = R.groupby("agit").apply(lambda x: slope(x, "hisc"))
    # 3-day fall in falling agitated
    out["slope ret3 by trend x agit"] = D.groupby(["trend", "agit"]).apply(lambda x: slope(x, "ret3"))
    return out
