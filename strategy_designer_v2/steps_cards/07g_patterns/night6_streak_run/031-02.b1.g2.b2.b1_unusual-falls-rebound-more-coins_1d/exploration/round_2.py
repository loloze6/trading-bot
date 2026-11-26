def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(20, min_periods=10).std()
            vol60 = r.rolling(60, min_periods=20).std()
            z = r / vol.shift(1)
            z60 = r / vol60.shift(1)
            ts = pd.to_datetime(b["timestamp"])
            for L in (10, 20, 40):
                pass
            r10 = (c / c.shift(10) - 1) / (vol * np.sqrt(10))
            r20 = (c / c.shift(20) - 1) / (vol * np.sqrt(20))
            r40 = (c / c.shift(40) - 1) / (vol60 * np.sqrt(40))
            for h in (2, 5, 10):
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, len(b), h)
                rows.append(pd.DataFrame({
                    "coin": coin, "w": w, "h": h,
                    "day": ts.dt.floor("D").values[idx], "yr": ts.dt.year.values[idx],
                    "z": z.values[idx], "z60": z60.values[idx],
                    "r10": r10.values[idx], "r20": r20.values[idx], "r40": r40.values[idx],
                    "fwd": fwd.values[idx]}))
    D = pd.concat(rows).dropna(subset=["fwd"])
    D["ex"] = D["fwd"] - D.groupby(["coin", "h"])["fwd"].transform("mean")
    D["exs"] = D["ex"] / D.groupby(["coin", "h"])["fwd"].transform("std")

    def slope_t(x, col, y="exs"):
        x = x.dropna(subset=[col, y])
        X = np.column_stack([np.ones(len(x)), x[col].values])
        Y = x[y].values
        beta, *_ = np.linalg.lstsq(X, Y, rcond=None)
        e = Y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        g = pd.DataFrame(X * e[:, None]).groupby(x["day"].values).sum().values
        G = len(g); n = len(x)
        V = XtXi @ (g.T @ g) @ XtXi * G / (G - 1) * (n - 1) / (n - 2)
        return beta[1], beta[1] / np.sqrt(V[1, 1]), n, G

    res = {}
    out = []
    for h in (2, 5, 10):
        X = D[D.h == h]
        for col in ("r10", "r20", "r40"):
            s, t, n, G = slope_t(X, col)
            out.append((h, col, round(s, 4), round(t, 2), n, G))
        s, t, n, G = slope_t(X[X.z60 > 0], "z60"); out.append((h, "z60 up days", round(s, 4), round(t, 2), n, G))
        s, t, n, G = slope_t(X[X.z60 < 0], "z60"); out.append((h, "z60 down days", round(s, 4), round(t, 2), n, G))
    res["slopes"] = pd.DataFrame(out, columns=["h", "x", "slope", "t_day", "n", "days"])
    # robustness of r20 at h5 and h10 by year
    out = []
    for h in (5, 10):
        X = D[D.h == h]
        for y, g in X.groupby("yr"):
            s, t, n, G = slope_t(g, "r20")
            out.append((h, y, round(s, 4), round(t, 2), n))
    res["r20 by year"] = pd.DataFrame(out, columns=["h", "yr", "slope", "t", "n"])
    out = []
    X = D[D.h == 10]
    for coin, g in X.groupby("coin"):
        s, t, n, G = slope_t(g, "r20")
        out.append((coin, round(s, 4), round(t, 2), n))
    res["r20 h10 by coin"] = pd.DataFrame(out, columns=["coin", "slope", "t", "n"])
    return res
