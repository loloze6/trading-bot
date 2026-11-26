def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            mabs = r1.abs().rolling(60).mean()
            hi = c.shift(1).rolling(60).max(); lo = c.shift(1).rolling(60).min()
            W = (hi - lo) / c / mabs
            brk_up = (c - hi) / c / mabs
            brk_dn = (lo - c) / c / mabs
            brk = np.where(brk_up > 0, brk_up, np.where(brk_dn > 0, -brk_dn, 0.0))
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]).dt.normalize(),
                "fc": b["forecast"].astype(float),
                "W": W, "brk": brk,
                "ret5p": c / c.shift(5) - 1, "ret20p": c / c.shift(20) - 1, "ret60p": c / c.shift(60) - 1,
                "vol20": r1.rolling(20).std(), "vol60": r1.rolling(60).std(),
                "r1": r1,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            for h in (5, 10, 20):
                df[f"f{h}"] = c.shift(-h) / c - 1
            df["f1"] = c.shift(-1) / c - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["vratio"] = D["vol20"] / D["vol60"]
    D["ret20p_z"] = D["ret20p"] / (D["vol60"] * np.sqrt(20))
    D["ret5p_z"] = D["ret5p"] / (D["vol60"] * np.sqrt(5))
    D["ret60p_z"] = D["ret60p"] / (D["vol60"] * np.sqrt(60))

    def cl_t(x, y, d):
        m = pd.DataFrame({"x": x, "y": y, "d": d}).dropna()
        if len(m) < 30: return (np.nan, np.nan, len(m), 0)
        X = np.column_stack([np.ones(len(m)), m["x"].values]); Y = m["y"].values
        beta = np.linalg.lstsq(X, Y, rcond=None)[0]; e = Y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        S = pd.DataFrame(X * e[:, None]).groupby(m["d"].values).sum().values
        V = XtXi @ (S.T @ S) @ XtXi
        return (beta[1], beta[1] / np.sqrt(V[1, 1]), len(m), m["d"].nunique())

    out = {}
    res = []
    for h in (5, 10, 20):
        g = D[D["pos"] % h == 0].copy()
        mean_h = g.groupby("coin")[f"f{h}"].transform("mean")
        g["ex"] = g[f"f{h}"] - mean_h
        g["exz"] = g["ex"] / (g["vol60"] * np.sqrt(h))
        for x in ["fc", "W", "brk", "ret5p_z", "ret20p_z", "ret60p_z", "vratio", "vol60"]:
            s, t, n, nd = cl_t(g[x], g["exz"], g["ts"])
            res.append({"h": h, "x": x, "slope": s, "t": t, "n": n, "dates": nd})
    out["slopes_excess_z"] = pd.DataFrame(res)

    # breakout reversion: |brk|>0 days, 10-day forward return signed against break
    g = D[(D["brk"] != 0)].dropna(subset=["f10", "W"]).copy()
    g["Wq"] = pd.qcut(g["W"], 3, labels=["tight", "mid", "wide"])
    g["side"] = np.sign(g["brk"])
    g["fade10"] = -g["side"] * g["f10"]
    g["fade5"] = -g["side"] * g["f5"]
    out["breakout_fade_by_W"] = g.groupby(["Wq", "side"])[["fade5", "fade10"]].agg(["mean", "count"])

    # quintiles of fc and of ret20p_z on 20 grid
    g = D[D["pos"] % 20 == 0].dropna(subset=["f20"]).copy()
    g["ex"] = g["f20"] - g.groupby("coin")["f20"].transform("mean")
    g["fcq"] = pd.qcut(g["fc"].rank(method="first"), 5, labels=False)
    out["fc_quint_ex20"] = g.groupby("fcq")["ex"].agg(["mean", "count"])
    g2 = g.dropna(subset=["ret20p_z"]).copy()
    g2["mq"] = pd.qcut(g2["ret20p_z"].rank(method="first"), 5, labels=False)
    out["mom20_quint_ex20"] = g2.groupby("mq")["ex"].agg(["mean", "count"])
    g3 = g.dropna(subset=["vratio"]).copy()
    g3["vq"] = pd.qcut(g3["vratio"].rank(method="first"), 5, labels=False)
    out["vratio_quint_ex20"] = g3.groupby("vq")["ex"].agg(["mean", "count"])

    # weekday of 1d returns
    wd = D.dropna(subset=["r1"]).groupby("wd")["r1"].agg(["mean", "std", "count"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["weekday_r1"] = wd

    # book: daily returns by coin and window
    br = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            br.append(pd.DataFrame({"coin": coin, "win": w, "b": d["book_return"], "c": d["coin_return"]}))
    B = pd.concat(br)
    out["book_by_window"] = B.groupby("win")[["b", "c"]].mean()
    out["book_by_coin"] = B.groupby("coin")[["b", "c"]].mean()
    return out
