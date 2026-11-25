def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd20 = r.rolling(20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]),
                "regime": b["regime"].values,
                "z": (c / c.shift(5) - 1) / (sd20 * np.sqrt(5)),
                "z10": (c / c.shift(10) - 1) / (sd20 * np.sqrt(10)),
                "f5": c.shift(-5) / c - 1, "f10": c.shift(-10) / c - 1,
                "ret60": c / c.shift(60) - 1,
            })
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")
    D["year"] = D["ts"].dt.year
    for h in (5, 10):
        D[f"x{h}"] = D[f"f{h}"] - D.groupby("coin")[f"f{h}"].transform("mean")
    D["calm"] = np.where(D["regime"] == "chop", "agitated", "calm")

    def cl_slope(s, xc, yc):
        s = s.dropna(subset=[xc, yc])
        if len(s) < 20:
            return (np.nan, np.nan, len(s), 0)
        x = s[xc].values; y = s[yc].values
        X = np.column_stack([np.ones(len(x)), x])
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((2, 2))
        for _, idx in s.groupby("day").indices.items():
            g = (X[idx] * e[idx][:, None]).sum(0)
            meat += np.outer(g, g)
        V = XtXi @ meat @ XtXi
        return (beta[1], beta[1] / np.sqrt(V[1, 1]), len(s), s["day"].nunique())

    def tday(s, col):
        s = s.dropna(subset=[col])
        if len(s) < 5: return (np.nan, np.nan, len(s))
        m = s[col].mean()
        gd = (s[col] - m).groupby(s["day"]).sum()
        se = np.sqrt((gd ** 2).sum()) / len(s)
        return (m, m / se, len(s))

    out = {}
    G5 = D[D["pos"] % 5 == 0]
    G10 = D[D["pos"] % 10 == 0]
    res = []
    for cl in ("calm", "agitated"):
        for side, cond in (("all", lambda s: s), ("falls", lambda s: s[s["z"] < 0]), ("rises", lambda s: s[s["z"] > 0])):
            sl, t, n, nd = cl_slope(cond(G5[G5["calm"] == cl]), "z", "x5")
            res.append({"profile": cl, "side": side, "h": 5, "slope_%": round(100 * sl, 3), "t_day": round(t, 2), "n": n, "days": nd})
        for side, cond in (("all", lambda s: s), ("falls", lambda s: s[s["z10"] < 0])):
            sl, t, n, nd = cl_slope(cond(G10[G10["calm"] == cl]), "z10", "x10")
            res.append({"profile": cl, "side": side, "h": 10, "slope_%": round(100 * sl, 3), "t_day": round(t, 2), "n": n, "days": nd})
    out["clustered slopes"] = pd.DataFrame(res)
    res = []
    for y, s in G5[(G5["calm"] == "calm")].groupby("year"):
        sl, t, n, nd = cl_slope(s, "z", "x5")
        m, tm, nn = tday(s[s["z"] < -0.75], "x5")
        res.append({"year": y, "slope_%": round(100 * sl, 3), "t": round(t, 2), "n": n,
                    "bigdn_x5_%": round(100 * m, 3), "bigdn_t": round(tm, 2), "bigdn_n": nn})
    out["calm by year"] = pd.DataFrame(res)
    res = []
    for coin, s in G5[(G5["calm"] == "calm")].groupby("coin"):
        sl, t, n, nd = cl_slope(s, "z", "x5")
        res.append({"coin": coin, "slope_%": round(100 * sl, 3), "t": round(t, 2), "n": n})
    out["calm by coin"] = pd.DataFrame(res)
    G5c = G5[G5["calm"] == "calm"].copy()
    G5c["trend"] = pd.cut(G5c["ret60"], [-99, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    res = []
    for tr, s in G5c.groupby("trend", observed=True):
        sl, t, n, nd = cl_slope(s, "z", "x5")
        res.append({"trend": str(tr), "slope_%": round(100 * sl, 3), "t": round(t, 2), "n": n})
    out["calm slope by 60d trend"] = pd.DataFrame(res)
    return out
