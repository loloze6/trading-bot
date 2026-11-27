def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            r = c.pct_change()
            vol = r.rolling(30, min_periods=20).std()
            rng = h - l
            clv = np.where(rng > 0, 2 * (c - (h + l) / 2) / rng, np.nan)
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "clv": clv, "width": (rng / c) / vol, "z": r / vol.shift(1),
                "ret60": c / c.shift(60) - 1, "vol": vol,
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1, "f3": c.shift(-3) / c - 1,
            })
            d["pos"] = np.arange(len(d))
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for h in (1, 2, 3):
        mu = D[D.pos % h == 0].groupby("coin")[f"f{h}"].mean()
        D[f"x{h}"] = D[f"f{h}"] - D["coin"].map(mu)
    med = D.groupby("coin")["vol"].transform("median")
    D["ag"] = np.where(D["vol"] > med, "agit", "calm")
    D["tr"] = pd.cut(D["ret60"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])

    def agg(g, col):
        g = g.dropna(subset=[col])
        n = len(g)
        if n < 5:
            return pd.Series({"n": n, "days": np.nan, "mean%": np.nan, "t_day": np.nan})
        m = g[col].mean()
        s = (g[col] - m).groupby(g["day"]).sum()
        G = len(s)
        se = np.sqrt((s ** 2).sum() * G / (G - 1)) / n
        return pd.Series({"n": n, "days": G, "mean%": 100 * m, "t_day": m / se})

    out = {}
    # 1: wide low close (signal = -clv * width when clv<0), by trend x agitation, next day
    D["lowsig"] = np.where(D["clv"] < 0, -D["clv"] * D["width"], 0.0)
    q = D.loc[D.lowsig > 0, "lowsig"].quantile([0.5, 0.8]).values
    D["lowq"] = pd.cut(D["lowsig"], [-1, 0, q[0], q[1], 1e9], labels=["none", "low", "mid", "top"])
    out["low-close signal x trend x agit, next day"] = D.groupby(["tr", "ag", "lowq"]).apply(lambda g: agg(g, "x1")).round(3)
    out["low-close top, by year"] = D[D.lowq == "top"].groupby("yr").apply(lambda g: agg(g, "x1")).round(3)
    # 2: up-move fade: z>1 by trend x agit, 3-day grid
    D["zq"] = pd.cut(D["z"], [-99, -2, -1, 1, 2, 99], labels=["<-2", "-2..-1", "mid", "1..2", ">2"])
    g3 = D[D.pos % 3 == 0]
    out["z x trend x agit, 3d grid"] = g3.groupby(["tr", "ag", "zq"]).apply(lambda g: agg(g, "x3")).round(3)
    g2 = D[D.pos % 2 == 0]
    out["z x trend, 2d grid"] = g2.groupby(["tr", "zq"]).apply(lambda g: agg(g, "x2")).round(3)
    # graded checks: slopes within trend
    res = {}
    for tr in ["falling", "choppy", "rising"]:
        s = g3[(g3.tr == tr)].dropna(subset=["z", "x3"])
        if len(s) > 30:
            sl = np.polyfit(s["z"].clip(-4, 4), s["x3"], 1)[0]
            res[tr] = {"slope_x3_on_z": sl, "n": len(s), "corr": s["z"].clip(-4, 4).corr(s["x3"])}
    out["3d slope on z by trend"] = pd.DataFrame(res).T.round(5)
    # up-move fade by year (falling, z>1, 3d)
    out["falling z>1 3d by year"] = g3[(g3.tr == "falling") & (g3.z > 1)].groupby("yr").apply(lambda g: agg(g, "x3")).round(3)
    out["rising z<-1 3d by year"] = g3[(g3.tr == "rising") & (g3.z < -1)].groupby("yr").apply(lambda g: agg(g, "x3")).round(3)
    return out
