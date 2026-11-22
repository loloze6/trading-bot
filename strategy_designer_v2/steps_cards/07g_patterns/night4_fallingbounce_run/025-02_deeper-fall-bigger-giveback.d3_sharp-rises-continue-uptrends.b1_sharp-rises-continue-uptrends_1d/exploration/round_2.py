def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd20 = r1.rolling(20, min_periods=20).std().shift(1)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "z": r1 / sd20,
                               "z20": (c / c.shift(20) - 1) / (sd20 * np.sqrt(20)),
                               "ret20": c / c.shift(20) - 1,
                               "f10": c.shift(-10) / c - 1, "f1": c.shift(-1) / c - 1,
                               "f3": c.shift(-3) / c - 1,
                               "up90": (b["regime"] == "trending").values,
                               "year": ts.dt.year, "pos": np.arange(len(b))})
            rows.append(df)
    a = pd.concat(rows)
    out = {}
    def summ(x):
        x = x.dropna(); n = len(x); m = x.mean(); s = x.std()
        return pd.Series({"n": n, "mean": m, "t": m / (s / np.sqrt(n)) if n > 2 and s > 0 else np.nan})
    # 10d grid, ret20 graded by regime
    g = a[a["pos"] % 10 == 0].dropna(subset=["f10", "z20"]).copy()
    g["un"] = g["f10"] - g["coin"].map(g.groupby("coin")["f10"].mean())
    res = []
    for reg, x in g.groupby("up90"):
        for col in ["z20", "ret20", "z"]:
            xx = x.dropna(subset=[col])
            r, p = stats.spearmanr(xx[col], xx["un"])
            res.append({"up90": reg, "var": col, "n": len(xx), "spearman": r, "p": p})
    out["10d grid spearman by regime"] = pd.DataFrame(res)
    g["half"] = np.where(g["year"] <= 2021, "2018-21", "2022-25")
    res = []
    for (reg, h), x in g.groupby(["up90", "half"]):
        r, p = stats.spearmanr(x["z20"], x["un"])
        res.append({"up90": reg, "half": h, "n": len(x), "spearman": r, "p": p})
    out["10d z20 spearman by regime x half"] = pd.DataFrame(res)
    res = []
    for (reg, cn), x in g.groupby(["up90", "coin"]):
        r, p = stats.spearmanr(x["z20"], x["un"])
        res.append({"up90": reg, "coin": cn, "n": len(x), "spearman": r})
    out["10d z20 spearman by regime x coin"] = pd.DataFrame(res)
    # 1d reversal on z, all bars (each 1-day return independent)
    d = a.dropna(subset=["f1", "z"]).copy()
    d["u1"] = d["f1"] - d["coin"].map(d.groupby("coin")["f1"].mean())
    res = []
    for key, x in list(d.groupby("coin")) + list(d.groupby("year")) + list(d.groupby("up90")):
        r, p = stats.spearmanr(x["z"], x["u1"])
        res.append({"group": str(key), "n": len(x), "spearman": r, "p": p})
    r, p = stats.spearmanr(d["z"], d["u1"])
    res.append({"group": "all", "n": len(d), "spearman": r, "p": p})
    out["1d next-day vs z spearman"] = pd.DataFrame(res)
    dn = d[d["z"] < 0].copy()
    r, p = stats.spearmanr(dn["z"], dn["u1"])
    up = d[d["z"] > 0].copy()
    r2, p2 = stats.spearmanr(up["z"], up["u1"])
    out["1d spearman down days / up days"] = pd.DataFrame({"n": [len(dn), len(up)], "spearman": [r, r2], "p": [p, p2]}, index=["z<0", "z>0"])
    # 3d grid after down days
    g3 = a[a["pos"] % 3 == 0].dropna(subset=["f3", "z"]).copy()
    g3["u3"] = g3["f3"] - g3["coin"].map(g3.groupby("coin")["f3"].mean())
    g3["zb"] = pd.cut(g3["z"], [-99, -2, -1, 0, 1, 2, 99])
    out["3d grid unusual by z"] = g3.groupby("zb", observed=True)["u3"].apply(summ).unstack()
    r, p = stats.spearmanr(g3["z"], g3["u3"])
    out["3d spearman z"] = pd.Series({"n": len(g3), "spearman": r, "p": p})
    return out
