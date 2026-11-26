def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            allr.append(b["close"].astype(float).reset_index(drop=True).pct_change().dropna())
        drift = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(30).std()
            rows.append(pd.DataFrame({
                "coin": coin, "win": w,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "fc": b["forecast"].astype(float),
                "srise": r1 / sd,
                "prior5": (c.shift(1) / c.shift(6) - 1) / (sd * np.sqrt(5)),
                "f1": c.shift(-1) / c - 1 - drift,
                "f2": c.shift(-2) / c - 1 - 2 * drift,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
            }))
    d = pd.concat(rows)
    a = d[d.fc < 0].dropna(subset=["f1", "srise", "prior5"]).copy()
    out = {}
    def clslope(g, x, y="f1"):
        g = g.dropna(subset=[x, y])
        X = np.column_stack([np.ones(len(g)), g[x].values])
        Y = g[y].values
        XtX = np.linalg.inv(X.T @ X)
        b = XtX @ X.T @ Y
        e = Y - X @ b
        meat = np.zeros((2, 2))
        for _, idx in g.groupby("day").indices.items():
            s = X[idx].T @ e[idx]
            meat += np.outer(s, s)
        G = g.day.nunique(); n = len(g)
        V = XtX @ meat @ XtX * G / (G - 1) * (n - 1) / (n - 2)
        return pd.Series({"n": n, "days": G, "slope": b[1], "t": b[1] / np.sqrt(V[1, 1])})
    a["depth"] = -a.prior5
    a["depth_clip"] = a.depth.clip(lower=0)
    a["neg_fc"] = -a.fc
    out["slopes_f1"] = pd.DataFrame({x: clslope(a, x) for x in ["neg_fc", "srise", "depth", "depth_clip"]}).T
    out["slopes_f2"] = pd.DataFrame({x: clslope(a, x, "f2") for x in ["srise", "depth", "depth_clip"]}).T
    out["depth_by_year"] = a.groupby("year").apply(lambda g: clslope(g, "depth"))
    out["depth_by_coin"] = a.groupby("coin").apply(lambda g: pd.Series({"n": len(g), "rho": stats.spearmanr(g.depth, g.f1)[0]}))
    pdn = a[a.prior5 < 0]
    out["depth_within_prior_down"] = clslope(pdn, "depth")
    a["q_rise"] = pd.qcut(a.srise, 3, labels=False)
    a["q_depth"] = pd.qcut(a.depth, 3, labels=False)
    out["grid_mean%"] = a.pivot_table(index="q_depth", columns="q_rise", values="f1", aggfunc="mean") * 100
    out["grid_n"] = a.pivot_table(index="q_depth", columns="q_rise", values="f1", aggfunc="count")
    return out
