def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd30 = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "pos": np.arange(len(b)), "reg": b["regime"].astype(str),
                "sr": r / sd30,
                "sr3": c.pct_change(3) / (sd30 * np.sqrt(3)),
                "sr5": c.pct_change(5) / (sd30 * np.sqrt(5)),
                "sr10": c.pct_change(10) / (sd30 * np.sqrt(10)),
                "dh20": c / c.rolling(20, min_periods=10).max() - 1,
                "vol": b["volume"].astype(float) / b["volume"].astype(float).rolling(30, min_periods=20).mean(),
            })
            for h in (1, 2, 3, 5):
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    for h in (1, 2, 3, 5):
        g = d[d["pos"] % h == 0]
        m = g.groupby("coin")[f"f{h}"].mean()
        d[f"x{h}"] = d[f"f{h}"] - d["coin"].map(m)
    d["day"] = d["ts"].dt.floor("D")
    d["yr"] = d["ts"].dt.year
    P = d[d["reg"] == "unknown"]

    def slope_t(sub, col, h):
        s = sub[sub["pos"] % h == 0].dropna(subset=[col, f"x{h}"])
        x = s[col].values; y = s[f"x{h}"].values
        if len(s) < 40: return {"n": len(s)}
        X = np.column_stack([np.ones(len(x)), x])
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        e = y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        sc = pd.DataFrame(X * e[:, None]).groupby(s["day"].values).sum().values
        G = len(sc)
        V = XtXi @ (sc.T @ sc) @ XtXi * G / (G - 1)
        return {"n": len(s), "days": G, "slope%": 100 * beta[1],
                "t": beta[1] / np.sqrt(V[1, 1])}

    res = {}
    out = []
    for col in ("sr", "sr3", "sr5", "sr10", "dh20", "vol"):
        for h in (1, 2, 3, 5):
            dd = slope_t(P, col, h); dd.update({"var": col, "h": h}); out.append(dd)
    res["P_slopes"] = pd.DataFrame(out)
    out = []
    for col in ("sr3", "sr5", "sr10", "dh20"):
        for yr, gg in P.groupby("yr"):
            dd = slope_t(gg, col, 3); dd.update({"var": col, "yr": yr}); out.append(dd)
        for coin, gg in P.groupby("coin"):
            dd = slope_t(gg, col, 3); dd.update({"var": col, "coin": coin}); out.append(dd)
    res["P_split_h3"] = pd.DataFrame(out)
    return res
