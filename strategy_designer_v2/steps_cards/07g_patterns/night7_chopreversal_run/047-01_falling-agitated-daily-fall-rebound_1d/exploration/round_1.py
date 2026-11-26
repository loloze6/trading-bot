def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r": r, "rn": c.shift(-1)/c - 1, "rn2": c.shift(-2)/c.shift(-1) - 1,
                "rng": (b["high"]-b["low"])/c, "clo": (c-b["low"])/(b["high"]-b["low"]),
                "inp": (b["regime"] != "chop").astype(int),
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            d["z"] = r / r.abs().rolling(60, min_periods=20).mean()
            d["wd"] = d["day"].dt.weekday
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["rn"].mean()
    D["xn"] = D["rn"] - D["coin"].map(drift)
    D["xn2"] = D["rn2"] - D["coin"].map(drift)
    D = D.dropna(subset=["z", "xn"])

    def ct(g, col):
        g = g.dropna(subset=[col])
        m = g[col].mean()
        s = (g[col]-m).groupby(g["day"]).sum()
        se = np.sqrt((s**2).sum())/len(g) if len(g) > 1 else np.nan
        return pd.Series({"n": len(g), "days": g["day"].nunique(), "mean%": 100*m, "t": m/se if se else np.nan})

    D["zb"] = pd.cut(D["z"], [-99, -2, -1, -0.5, 0, 0.5, 1, 2, 99])
    out = {}
    out["in_profile_by_z_next"] = D[D.inp == 1].groupby("zb", observed=True).apply(lambda g: ct(g, "xn"))
    out["out_profile_by_z_next"] = D[D.inp == 0].groupby("zb", observed=True).apply(lambda g: ct(g, "xn"))
    out["in_profile_by_z_day2"] = D[D.inp == 1].groupby("zb", observed=True).apply(lambda g: ct(g, "xn2"))
    dn = D[(D.z < -1)]
    out["bigfall_by_profile_wd"] = dn.groupby(["inp", "wd"]).apply(lambda g: ct(g, "xn")).round(3)
    dn2 = D[(D.inp == 1) & (D.z < 0)].copy()
    dn2["clob"] = pd.cut(dn2["clo"], [0, 0.2, 0.4, 0.6, 1.0001], include_lowest=True)
    out["infall_by_closeloc"] = dn2.groupby("clob", observed=True).apply(lambda g: ct(g, "xn"))
    dn2["rngq"] = dn2.groupby("coin")["rng"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["infall_by_rangetercile"] = dn2.groupby("rngq").apply(lambda g: ct(g, "xn"))
    out["by_coin_infall_z_lt_-1"] = D[(D.inp == 1) & (D.z < -1)].groupby("coin").apply(lambda g: ct(g, "xn"))
    out["by_window_in_profile_share"] = D.groupby("win")["inp"].mean().round(3)
    return out
