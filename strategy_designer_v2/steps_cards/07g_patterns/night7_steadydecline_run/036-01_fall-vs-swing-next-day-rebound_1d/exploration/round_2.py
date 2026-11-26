def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]
            r = c.pct_change()
            sd = r.rolling(30).std()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "r": r, "z": r / sd, "sd": sd,
                "f1": c.shift(-1) / c - 1,
                "clv": (c - b["low"]) / (b["high"] - b["low"]),
                "pos": b["postRebalance_current_allocation"],
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")
    m = D.groupby("coin")["f1"].mean()
    D["x"] = D["f1"] - D["coin"].map(m)
    D["sdrel"] = D["sd"] / D["coin"].map(D.groupby("coin")["sd"].median())
    D["gain"] = D["pos"] * D["f1"]

    def ct(s, days):
        s = pd.Series(s.values, index=days.values).dropna()
        n = len(s)
        if n < 5:
            return pd.Series({"n": n, "mean%": np.nan, "t": np.nan, "days": 0})
        dev = (s - s.mean()).groupby(level=0).sum()
        D_ = len(dev)
        se = np.sqrt(D_ / (D_ - 1) * (dev ** 2).sum()) / n
        return pd.Series({"n": n, "mean%": 100 * s.mean(), "t": s.mean() / se, "days": D_})

    def tab(df, by, col="x"):
        return df.groupby(by, observed=True).apply(lambda g: ct(g[col], g["day"]))

    def slope(df, xcols, ycol="x"):
        df = df.dropna(subset=xcols + [ycol])
        X = np.column_stack([np.ones(len(df))] + [df[c].values for c in xcols])
        y = df[ycol].values
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        sc = pd.DataFrame(X * e[:, None]).groupby(df["day"].values).sum().values
        V = XtXi @ (sc.T @ sc) @ XtXi
        se = np.sqrt(np.diag(V))
        return pd.DataFrame({"beta": beta, "t": beta / se}, index=["const"] + xcols).assign(n=len(df))

    out = {}
    D["clvc"] = D["clv"] - 0.5
    out["slope_all_z"] = slope(D, ["z"])
    out["slope_all_clv"] = slope(D, ["clvc"])
    out["slope_all_z_clv"] = slope(D, ["z", "clvc"])
    out["slope_all_r_clv"] = slope(D, ["r", "clvc"])
    N = D[D["z"] < 0]
    out["slope_neg_z_clv"] = slope(N, ["z", "clvc"])
    out["slope_neg_r_sd"] = slope(N, ["r", "sdrel"])
    F = D[D["z"] <= -1].copy()
    out["slope_falls_z"] = slope(F, ["z"])
    out["slope_falls_r"] = slope(F, ["r"])
    out["slope_falls_r_sdrel"] = slope(F, ["r", "sdrel"])
    F["rb"] = pd.qcut(F["r"], 4)
    out["falls_by_rawfall"] = tab(F, "rb")
    # clv grading by window halves
    D["half"] = D["win"].map(lambda w: "w7-w12" if int(w[1:]) <= 12 else "w13-w18")
    D["clvb"] = pd.cut(D["clv"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01])
    out["clv_by_half"] = D.groupby(["half", "clvb"], observed=True).apply(lambda g: ct(g["x"], g["day"]))
    # clv on down days vs up days
    D["sign"] = np.where(D["r"] < 0, "down", "up")
    out["clv_by_sign"] = D.groupby(["sign", "clvb"], observed=True).apply(lambda g: ct(g["x"], g["day"]))
    # sdrel grading all down days
    N = D[D["r"] < 0].copy()
    N["sdb"] = pd.qcut(N["sdrel"], 4)
    out["down_by_swing"] = tab(N, "sdb")
    # book: position-day gains by z bucket of the bar
    P = D[D["pos"].abs() > 0].copy()
    P["zb"] = pd.cut(P["z"], [-99, -2.5, -1.75, -1.25, -1])
    out["book_gain_by_z"] = tab(P, "zb", "gain")
    return out
