def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        drift = pd.concat([b["close"].astype(float).reset_index(drop=True).pct_change().dropna() for b in wins.values()]).mean()
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
                "sd": sd,
                "f1": c.shift(-1) / c - 1 - drift,
                "f3": c.shift(-3) / c - 1 - 3 * drift,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
            }))
    d = pd.concat(rows)
    a = d[d.fc < 0].dropna(subset=["f1", "srise", "prior5"]).copy()
    out = {}
    def cl(g, x, y):
        g = g.dropna(subset=[x, y])
        X = np.column_stack([np.ones(len(g)), g[x].values]); Y = g[y].values
        XtX = np.linalg.inv(X.T @ X); b = XtX @ X.T @ Y; e = Y - X @ b
        meat = np.zeros((2, 2))
        for _, idx in g.groupby("day").indices.items():
            s = X[idx].T @ e[idx]; meat += np.outer(s, s)
        G = g.day.nunique(); n = len(g)
        V = XtX @ meat @ XtX * G / (G - 1) * (n - 1) / (n - 2)
        return pd.Series({"n": n, "days": G, "slope": b[1], "t": b[1] / np.sqrt(V[1, 1])})
    def daymean(g, y):
        s = g.groupby("day")[y].mean().dropna()
        return pd.Series({"n": len(g), "days": len(s), "mean%": 100 * s.mean(), "t_day": s.mean() / (s.std() / np.sqrt(len(s)))})
    a["depth_rank"] = a.depth_rank if False else (-a.prior5).rank(pct=True)
    a["rise_rank"] = a.srise.rank(pct=True)
    lo, hi = a.f1.quantile([0.02, 0.98]); a["f1w"] = a.f1.clip(lo, hi)
    a["f1s"] = a.f1 / a.sd
    a["f3s"] = a.f3 / (a.sd * np.sqrt(3))
    out["slopes"] = pd.DataFrame({f"{x}~{y}": cl(a, x, y) for x in ["depth_rank", "rise_rank"] for y in ["f1", "f1w", "f1s", "f3s"]}).T
    out["level_day_clustered"] = pd.DataFrame({y: daymean(a, y) for y in ["f1", "f1s", "f3s"]}).T
    a["qd"] = pd.qcut(a.depth_rank, 3, labels=["shallow", "mid", "deep"])
    out["depth_tercile_day"] = a.groupby("qd").apply(lambda g: pd.concat([daymean(g, "f1"), daymean(g, "f1s").rename(lambda s: s + "_s")]))
    out["deep_by_year"] = a[a.qd == "deep"].groupby("year").apply(lambda g: daymean(g, "f1"))
    out["shallow_by_year"] = a[a.qd == "shallow"].groupby("year").apply(lambda g: daymean(g, "f1"))
    return out
