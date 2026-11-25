def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            f = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"])})
            for L in [14, 28, 56]:
                f["pos%d" % L] = (c - c.rolling(L).min()) / (c.rolling(L).max() - c.rolling(L).min())
            f["ret28"] = c / c.shift(28) - 1
            for H in [5, 10]:
                f["fwd%d" % H] = c.shift(-H) / c - 1
                f["g%d" % H] = (np.arange(len(b)) % H == 0)
            f["yr"] = f["ts"].dt.year
            rows.append(f)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    def slope(d, x, col):
        d = d[[x, col, "ts"]].dropna()
        z = (d[x] - d[x].mean()) / d[x].std()
        X = np.column_stack([np.ones(len(d)), z]); y = d[col].values
        beta = np.linalg.lstsq(X, y, rcond=None)[0]; e = y - X @ beta
        XtXi = np.linalg.inv(X.T @ X); meat = np.zeros((2, 2))
        for _, idx in d.groupby("ts").indices.items():
            s = X[idx].T @ e[idx]; meat += np.outer(s, s)
        se = np.sqrt(np.diag(XtXi @ meat @ XtXi))
        return round(beta[1], 5), round(beta[1] / se[1], 2), len(d), d["ts"].nunique()
    res = []
    for H in [5, 10]:
        G = A[A["g%d" % H] & A["fwd%d" % H].notna()].copy()
        G["ex"] = G["fwd%d" % H] - G.groupby("coin")["fwd%d" % H].transform("mean")
        for x in ["pos14", "pos28", "pos56", "ret28"]:
            res.append((H, x) + slope(G, x, "ex"))
        if H == 5:
            G5 = G
    out["slopes_by_horizon"] = pd.DataFrame(res, columns=["H", "feat", "b", "t", "n", "days"])
    r = []
    for coin, g in G5.groupby("coin"):
        r.append((coin,) + slope(g, "pos28", "ex"))
    out["pos28_by_coin_5d"] = pd.DataFrame(r, columns=["coin", "b", "t", "n", "days"])
    r = []
    for y, g in G5.groupby("yr"):
        if len(g) > 40: r.append((y,) + slope(g, "pos28", "ex"))
    out["pos28_by_year_5d"] = pd.DataFrame(r, columns=["yr", "b", "t", "n", "days"])
    r = []
    for w, g in G5.groupby("win"):
        if len(g) > 30: r.append((w,) + slope(g, "pos28", "ex"))
    out["pos28_by_window_5d"] = pd.DataFrame(r, columns=["win", "b", "t", "n", "days"])
    # pos28 within decline vs rise
    r = []
    for name, g in [("ret28<0", G5[G5["ret28"] < 0]), ("ret28>=0", G5[G5["ret28"] >= 0])]:
        r.append((name,) + slope(g, "pos28", "ex"))
    out["pos28_by_ret28_sign"] = pd.DataFrame(r, columns=["set", "b", "t", "n", "days"])
    return out
