def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            r = c.pct_change()
            d = pd.DataFrame({"coin": coin, "w": w, "date": ts.dt.floor("D"), "wd": ts.dt.weekday,
                              "year": ts.dt.year, "fwd1": c.shift(-1) / c - 1, "fwd3": c.shift(-3) / c - 1,
                              "r1": r, "vol20": r.rolling(20, min_periods=15).std(), "pos": np.arange(len(b)),
                              "alloc": b["postRebalance_current_allocation"].astype(float)})
            for L in [2, 3, 5, 7, 10, 14]:
                d[f"skip{L}"] = c.shift(1) / c.shift(1 + L) - 1
                d[f"full{L}"] = c / c.shift(L) - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["ex1"] = D["fwd1"] - D.groupby("coin")["fwd1"].transform("mean")
    D["z1"] = D["ex1"] / D["vol20"]
    D["r1z"] = D["r1"] / D["vol20"]
    for L in [2, 3, 5, 7, 10, 14]:
        D[f"skip{L}z"] = D[f"skip{L}"] / (D["vol20"] * np.sqrt(L))
        D[f"full{L}z"] = D[f"full{L}"] / (D["vol20"] * np.sqrt(L))

    def cl(df, xs, y):
        df = df[xs + [y, "date"]].dropna()
        if len(df) < 50: return {"n": len(df)}
        X = np.column_stack([np.ones(len(df))] + [df[x].values for x in xs])
        Y = df[y].values
        beta = np.linalg.lstsq(X, Y, rcond=None)[0]
        e = Y - X @ beta
        XtX = np.linalg.inv(X.T @ X)
        sc = pd.DataFrame(X * e[:, None]).groupby(df["date"].values).sum().values
        G = len(sc)
        V = XtX @ (sc.T @ sc) @ XtX * G / (G - 1)
        o = {"days": G}
        for i, x in enumerate(xs):
            o["b_" + x] = beta[i + 1]; o["t_" + x] = beta[i + 1] / np.sqrt(V[i + 1, i + 1])
        return o

    out = {}
    out["skip-one vs full lookback, next day z"] = pd.DataFrame(
        [dict(L=L, **cl(D, [f"skip{L}z", "r1z"], "z1")) for L in [2, 3, 5, 7, 10, 14]])
    out["skip4 by coin"] = pd.DataFrame({k: cl(g, ["skip3z", "r1z"], "z1") for k, g in D.groupby("coin")}).T
    out["skip3 by year"] = pd.DataFrame({k: cl(g, ["skip3z", "r1z"], "z1") for k, g in D.groupby("year")}).T
    out["skip3 by weekday of signal"] = pd.DataFrame({k: cl(g, ["skip3z", "r1z"], "z1") for k, g in D.groupby("wd")}).T
    # sign split: rising vs falling side
    out["skip3 up side"] = pd.Series(cl(D[D.skip3 > 0], ["skip3z"], "z1"))
    out["skip3 down side"] = pd.Series(cl(D[D.skip3 <= 0], ["skip3z"], "z1"))
    # quintiles of skip3z, next-day excess mean, day-clustered
    D["q"] = pd.qcut(D["skip3z"], 5, labels=False)
    def dm(g):
        s = g.groupby("date")["ex1"].mean().dropna()
        return pd.Series({"mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))), "days": len(s)})
    out["next ex by skip3z quintile"] = pd.DataFrame({k: dm(g) for k, g in D.groupby("q")}).T
    # 3-day horizon, non-overlapping
    g3 = D[D["pos"] % 3 == 0].copy()
    g3["ex3"] = g3["fwd3"] - g3.groupby("coin")["fwd3"].transform("mean")
    g3["z3"] = g3["ex3"] / (g3["vol20"] * np.sqrt(3))
    out["3d horizon nonoverlap, skip3 & full4"] = pd.DataFrame([cl(g3, ["skip3z", "r1z"], "z3"), cl(g3, ["full5z"], "z3")])
    # book: days around largest gains/losses
    days = []
    for coin, ws in data["days"].items():
        for w, dd in ws.items():
            x = dd.copy(); x["coin"] = coin; days.append(x)
    DD = pd.concat(days); DD["day"] = pd.to_datetime(DD["day"])
    bk = DD.groupby("day")["book_return"].mean().dropna()
    out["book return by weekday of day"] = bk.groupby(bk.index.weekday).agg(["mean", "count"])
    top = bk.abs().quantile(0.98)
    big = bk[bk.abs() >= top]
    out["largest book days: sign count, mean"] = pd.Series({"n_gain": (big > 0).sum(), "n_loss": (big < 0).sum(),
        "mean_gain": big[big > 0].mean(), "mean_loss": big[big < 0].mean(), "share_of_total": big.sum() / bk.sum()})
    return out
