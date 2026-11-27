def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        allret = [pd.Series(b["close"].values).pct_change().dropna().values for b in wins.values()]
        mu = np.concatenate(allret).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            ts = pd.to_datetime(b["timestamp"])
            d = b["debug_info.components.depth.last_history_value"]
            for h in (2, 3, 5, 7, 10):
                fwd = c.shift(-h) / c - 1
                sd = (c.pct_change().rolling(20).std()) * np.sqrt(h)
                rows.append(pd.DataFrame({
                    "coin": coin, "w": w, "h": h, "pos": np.arange(len(b)),
                    "day": ts.dt.normalize(), "year": ts.dt.year,
                    "depth": -d, "chop": b["regime"] == "unknown",
                    "up": b["close"] > b["open"],
                    "ex": fwd - ((1 + mu) ** h - 1), "sd": sd}))
    D = pd.concat(rows)
    D = D[D["chop"] & D["depth"].notna() & D["ex"].notna() & (D["depth"] > 0)]
    D = D[D["pos"] % D["h"] == 0]

    def clus(g):
        if len(g) < 30:
            return pd.Series({"n": len(g)})
        x = g["depth"].values; y = g["ex"].values
        X = np.column_stack([np.ones(len(x)), x])
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        e = y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        S = np.zeros((2, 2))
        for _, idx in pd.Series(np.arange(len(x))).groupby(g["day"].values):
            s = X[idx.values].T @ e[idx.values]
            S += np.outer(s, s)
        V = XtXi @ S @ XtXi
        return pd.Series({"n": len(g), "days": g["day"].nunique(), "slope_bp": beta[1] * 1e4,
                          "t_clus": beta[1] / np.sqrt(V[1, 1]), "mean_ex_%": y.mean() * 100,
                          "strength": (g["ex"] / g["sd"]).mean()})
    out = {}
    out["by horizon clustered"] = D.groupby("h").apply(clus)
    D5 = D[D["h"] == 5].copy()
    out["h5 by year"] = D5.groupby("year").apply(clus)
    out["h5 by window"] = D5.groupby("w").apply(lambda g: pd.Series({"n": len(g), "slope_bp": stats.linregress(g["depth"], g["ex"]).slope * 1e4 if len(g) > 5 else np.nan}))
    D5["q"] = pd.qcut(D5["depth"], 5, labels=False)
    out["h5 depth quintile"] = D5.groupby("q").agg(n=("ex", "size"), depth=("depth", "mean"),
        mean_ex_pct=("ex", lambda x: x.mean() * 100), t=("ex", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    D3 = D[D["h"] == 3]
    out["h3 by up/down"] = D3.groupby("up").apply(clus)
    D7 = D[D["h"] == 7]
    out["h7 by up/down"] = D7.groupby("up").apply(clus)
    out["h5 by up/down clustered"] = D5.groupby("up").apply(clus)
    return out
