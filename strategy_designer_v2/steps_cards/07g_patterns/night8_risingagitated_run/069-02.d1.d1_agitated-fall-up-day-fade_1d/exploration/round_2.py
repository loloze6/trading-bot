def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            hh = b["high"].rolling(20, min_periods=20).max()
            sd = r.rolling(20, min_periods=20).std()
            depth = (c / hh - 1) / sd
            tr60 = c / c.shift(60) - 1
            df = pd.DataFrame({"coin": coin, "w": w, "ts": pd.to_datetime(b["timestamp"]),
                               "r": r, "nxt": nxt, "depth": depth, "tr60": tr60,
                               "regime": b["regime"], "alloc": b["postRebalance_current_allocation"]})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["nxt"].mean()
    D["e"] = D["nxt"] - D["coin"].map(mu)
    D = D.dropna(subset=["e", "depth"])
    D["day"] = D["ts"].dt.floor("D")
    D["yr"] = D["ts"].dt.year
    D["trend"] = np.where(D["tr60"] > 0.10, "rising", np.where(D["tr60"] < -0.10, "falling", np.where(D["tr60"].notna(), "choppy", "na")))
    D["side"] = np.where(D["r"] > 0, "up", "down")
    def ct(g):
        x = g.dropna(subset=["e"])
        n = len(x)
        if n < 10:
            return pd.Series({"n": n, "days": np.nan, "mean_e%": np.nan, "t_day": np.nan, "slope_t_day": np.nan})
        s = x.groupby("day")["e"].agg(["sum", "count"])
        m = x["e"].mean()
        dev = x.groupby("day")["e"].apply(lambda v: (v - m).sum())
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / max(G - 1, 1)) / n
        # slope of e on depth, clustered
        d = x["depth"].values; e = x["e"].values
        X = np.column_stack([np.ones(n), d])
        beta = np.linalg.lstsq(X, e, rcond=None)[0]
        u = e - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((2, 2))
        for _, idx in x.reset_index(drop=True).groupby("day").indices.items():
            sc = (X[idx] * u[idx][:, None]).sum(0)
            meat += np.outer(sc, sc)
        V = XtXi @ meat @ XtXi * G / max(G - 1, 1)
        return pd.Series({"n": n, "days": G, "mean_e%": 100 * m, "t_day": m / se,
                          "slope%perunit": 100 * beta[1], "slope_t_day": beta[1] / np.sqrt(V[1, 1])})
    out = {}
    up = D[D.side == "up"].copy()
    dn = D[D.side == "down"].copy()
    up["dq"] = pd.qcut(up["depth"], 5, labels=False)
    dn["dq"] = pd.qcut(dn["depth"], 5, labels=False)
    out["up: all, graded"] = ct(up).to_frame().T
    out["up: by trend"] = up.groupby("trend").apply(ct)
    # agitation proxy: up day, falling trend: regime mean_reversion = agitated, else calm
    uf = up[up.trend == "falling"].copy()
    uf["agit"] = np.where(uf["regime"] == "mean_reversion", "agitated", "calm")
    out["up falling: by agitation"] = uf.groupby("agit").apply(ct)
    out["up falling: agitation x depth quintile"] = uf.groupby(["agit", "dq"]).apply(lambda g: pd.Series({"n": len(g), "mean_e%": 100 * g.e.mean()}))
    out["up deepest quintile: by year"] = up[up.dq == 0].groupby("yr").apply(ct)
    out["up deepest quintile: by coin"] = up[up.dq == 0].groupby("coin").apply(ct)
    out["up: by trend x depth quintile"] = up[up.trend != "na"].groupby(["trend", "dq"]).apply(lambda g: pd.Series({"n": len(g), "mean_e%": 100 * g.e.mean()}))
    out["down: all graded"] = ct(dn).to_frame().T
    out["down: by trend"] = dn.groupby("trend").apply(ct)
    out["down shallowest quintile: by year"] = dn[dn.dq == 4].groupby("yr").apply(ct)
    out["down shallowest quintile: by coin"] = dn[dn.dq == 4].groupby("coin").apply(ct)
    out["down: trend x depth quintile"] = dn[dn.trend != "na"].groupby(["trend", "dq"]).apply(lambda g: pd.Series({"n": len(g), "mean_e%": 100 * g.e.mean()}))
    return out
