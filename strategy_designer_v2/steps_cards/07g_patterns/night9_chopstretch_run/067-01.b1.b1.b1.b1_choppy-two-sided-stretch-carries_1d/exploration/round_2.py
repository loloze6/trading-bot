def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(20).std()
            sma = c.rolling(20).mean()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "day": ts.dt.floor("D"), "year": ts.dt.year,
                               "r1z": r1 / sd.shift(1), "stretch": (c / sma - 1) / sd,
                               "ret60": c / c.shift(60) - 1,
                               "vol30": r1.rolling(30).std(),
                               "regime": b["regime"].astype(str)})
            for h in (1, 3, 5, 10):
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    for h in (1, 3, 5, 10):
        g = D[D.pos % h == 0]
        D[f"u{h}"] = D[f"f{h}"] - D["coin"].map(g.groupby("coin")[f"f{h}"].mean())
    D["trend"] = np.where(D.ret60 > .1, "rising", np.where(D.ret60 < -.1, "falling", np.where(D.ret60.notna(), "choppy", "na")))
    # agitation proxy: vol30 vs coin median of vol30 over all windows
    D["agit"] = np.where(D.vol30 > D.coin.map(D.groupby("coin").vol30.median()), "agit", "calm")
    def ctab(df, key, val):
        a = df.groupby(key)[val].agg(["mean", "count", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        return a.drop(columns="std")
    def slope_t(df, x, y):
        df = df.dropna(subset=[x, y])
        if len(df) < 10: return pd.Series({"slope": np.nan, "t": np.nan, "n": len(df), "days": 0})
        X = np.column_stack([np.ones(len(df)), df[x].values]); Y = df[y].values
        XtX = np.linalg.inv(X.T @ X); beta = XtX @ X.T @ Y; e = Y - X @ beta
        meat = np.zeros((2, 2))
        for _, idx in df.groupby("day").indices.items():
            s = (X[idx] * e[idx, None]).sum(0); meat += np.outer(s, s)
        V = XtX @ meat @ XtX
        return pd.Series({"slope": beta[1], "t": beta[1] / np.sqrt(V[1, 1]), "n": len(df), "days": df.day.nunique()})
    out = {}
    res = {}
    for tr in ("falling", "rising", "choppy"):
        for h in (1, 3, 5, 10):
            g = D[(D.pos % h == 0) & (D.trend == tr)]
            res[(tr, h, "r1z")] = slope_t(g, "r1z", f"u{h}")
            res[(tr, h, "stretch")] = slope_t(g, "stretch", f"u{h}")
    out["slopes of unusual move on 1d z and stretch, by trend and horizon"] = pd.DataFrame(res).T
    G3 = D[(D.pos % 3 == 0) & (D.trend == "falling")].dropna(subset=["r1z", "u3"]).copy()
    G3["zq"] = pd.qcut(G3.r1z, 5, labels=False)
    out["falling 3d by z quintile x agitation"] = ctab(G3, ["agit", "zq"], "u3")
    up = G3[G3.zq == 4]
    out["falling top z quintile 3d by window"] = ctab(up, "w", "u3")
    out["falling top z quintile 3d by year"] = ctab(up, "year", "u3")
    out["falling top z quintile 3d by coin"] = ctab(up, "coin", "u3")
    # choppy via regime (all bars) stretch
    G10 = D[D.pos % 10 == 0].copy()
    G10["choppy_reg"] = G10.regime
    res2 = {}
    for rg in G10.regime.unique():
        res2[rg] = slope_t(G10[G10.regime == rg], "stretch", "u10")
    out["10d stretch slope by recorded regime"] = pd.DataFrame(res2).T
    return out
