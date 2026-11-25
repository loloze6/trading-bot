def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "z": r / sd, "sd": sd, "n1": c.shift(-1) / c - 1,
                "n2": c.shift(-2) / c - 1, "pos": np.arange(len(b)),
                "agit": (b["regime"] != "chop").astype(int),
                "clv": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "r60": c / c.shift(60) - 1,
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["x1"] = d["n1"] - d.groupby("coin")["n1"].transform("mean")
    mu2 = d[d.pos % 2 == 0].groupby("coin")["n2"].mean()
    d["x2"] = d["n2"] - d["coin"].map(mu2)
    d["u1"] = d["x1"] / d["sd"]
    d["day"] = d["ts"].dt.floor("D")
    d["yr"] = d["ts"].dt.year
    d["trend"] = np.where(d.r60 > 0.1, "rising", np.where(d.r60 < -0.1, "falling", "choppy"))

    def slope(s, xcol, ycol):
        s = s.dropna(subset=[xcol, ycol])
        if len(s) < 30: return (len(s), np.nan, np.nan)
        x = s[xcol] - s[xcol].mean(); y = s[ycol] - s[ycol].mean()
        bta = (x * y).sum() / (x ** 2).sum()
        e = y - bta * x
        g = (x * e).groupby(s["day"]).sum()
        se = np.sqrt((g ** 2).sum()) / (x ** 2).sum()
        return (len(s), bta, bta / se)

    out = {}
    res = []
    for a in [0, 1]:
        for side, cond in [("fall", d.z < 0), ("rise", d.z > 0), ("all", d.z.notna())]:
            s = d[(d.agit == a) & cond]
            res.append([a, side, "z->u1"] + list(slope(s, "z", "u1")))
            s2 = s[s.pos % 2 == 0]
            res.append([a, side, "z->x2"] + list(slope(s2, "z", "x2")))
            res.append([a, side, "clv->u1"] + list(slope(s, "clv", "u1")))
    out["slopes"] = pd.DataFrame(res, columns=["agit", "side", "reg", "n", "slope", "t"])

    # clv controlling for z: multivariate in agitated
    res = []
    for a in [0, 1]:
        s = d[d.agit == a].dropna(subset=["z", "clv", "u1"])
        X = np.column_stack([np.ones(len(s)), s.z, s.clv - 0.5])
        y = s.u1.values
        bta, *_ = np.linalg.lstsq(X, y, rcond=None)
        e = y - X @ bta
        XtX = np.linalg.inv(X.T @ X)
        G = pd.DataFrame(X * e[:, None]).groupby(s["day"].values).sum().values
        V = XtX @ (G.T @ G) @ XtX
        se = np.sqrt(np.diag(V))
        res.append([a, len(s), bta[1], bta[1] / se[1], bta[2], bta[2] / se[2]])
    out["multi_z_clv"] = pd.DataFrame(res, columns=["agit", "n", "b_z", "t_z", "b_clv", "t_clv"])

    # by year and by trend: z slope all days, agitated
    res = []
    for y_, s in d[d.agit == 1].groupby("yr"):
        res.append(["yr", y_] + list(slope(s, "z", "u1")))
    for tr, s in d[d.agit == 1].groupby("trend"):
        res.append(["trend_ag", tr] + list(slope(s, "z", "u1")))
    for tr, s in d[d.agit == 0].groupby("trend"):
        res.append(["trend_calm", tr] + list(slope(s, "z", "u1")))
    for co, s in d.groupby("coin"):
        res.append(["coin_all", co] + list(slope(s, "z", "u1")))
    out["slope_z_by_group"] = pd.DataFrame(res, columns=["grp", "val", "n", "slope", "t"])
    return out
