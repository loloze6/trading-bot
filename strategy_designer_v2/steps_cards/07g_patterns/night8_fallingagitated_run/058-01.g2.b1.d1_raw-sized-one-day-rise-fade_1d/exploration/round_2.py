def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=20).std()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "inprof": (b["regime"] == "unknown").astype(int),
                "z1": r1 / sd,
                "z3": (c / c.shift(3) - 1) / (sd * np.sqrt(3)),
                "z10": (c / c.shift(10) - 1) / (sd * np.sqrt(10)),
                "tr60": c / c.shift(60) - 1,
                "f3": c.shift(-3) / c - 1,
                "f5": c.shift(-5) / c - 1,
                "pos": b["postRebalance_current_allocation"].astype(float),
            })
            d["i"] = np.arange(len(d))
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")
    D["year"] = D["ts"].dt.year
    for h in [3, 5]:
        col = "f%d" % h
        g = D[D["i"] % h == 0]
        D.loc[g.index, "u%d" % h] = g[col] - g.groupby("coin")[col].transform("mean")

    def slope(sub, x, y):
        s = sub.dropna(subset=[x, y])
        if len(s) < 10:
            return pd.Series({"n": len(s), "days": s["day"].nunique(), "slope": np.nan, "t": np.nan})
        X = s[x] - s[x].mean()
        b = (X * s[y]).sum() / (X ** 2).sum()
        e = s[y] - s[y].mean() - b * X
        sc = (X * e).groupby(s["day"]).sum()
        se = np.sqrt((sc ** 2).sum()) / (X ** 2).sum()
        return pd.Series({"n": len(s), "days": s["day"].nunique(), "slope": b, "t": b / se})

    out = {}
    P = D[D["inprof"] == 1].copy()
    P["z1pos"] = P["z1"].clip(lower=0)
    P["z1neg"] = P["z1"].clip(upper=0)
    out["prof1_slopes"] = pd.DataFrame({
        "z1_u3": slope(P, "z1", "u3"),
        "z1pos_u3": slope(P, "z1pos", "u3"),
        "z1neg_u3": slope(P, "z1neg", "u3"),
        "z3_u3": slope(P, "z3", "u3"),
        "z10_u5": slope(P, "z10", "u5"),
    }).T
    out["prof1_z1_u3_by_year"] = P.groupby("year").apply(lambda s: slope(s, "z1", "u3"))
    out["prof1_z1pos_u3_by_year"] = P.groupby("year").apply(lambda s: slope(s, "z1pos", "u3"))

    O = D[D["inprof"] == 0].copy()
    O["trend"] = pd.cut(O["tr60"], [-np.inf, -0.10, 0.10, np.inf], labels=["falling", "choppy", "rising"])
    out["prof0_z10_u5_by_trend"] = O.groupby("trend").apply(lambda s: slope(s, "z10", "u5"))
    out["prof0_z3_u3_by_trend"] = O.groupby("trend").apply(lambda s: slope(s, "z3", "u3"))
    out["prof0_z10_u5_by_year"] = O.groupby("year").apply(lambda s: slope(s, "z10", "u5"))
    out["prof0_z10_u5_by_coin"] = O.groupby("coin").apply(lambda s: slope(s, "z10", "u5"))
    out["all_z10_u5"] = slope(D, "z10", "u5")
    return out
