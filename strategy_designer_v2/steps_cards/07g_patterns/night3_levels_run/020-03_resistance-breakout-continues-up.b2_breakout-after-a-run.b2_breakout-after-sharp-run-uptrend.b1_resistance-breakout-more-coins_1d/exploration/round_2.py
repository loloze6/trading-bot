def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w, "r1": r1,
                "r10": c / c.shift(10) - 1,
                "r30": c / c.shift(30) - 1,
                "vol20": r1.rolling(20, min_periods=15).std(),
                "dhi": c / c.rolling(60, min_periods=30).max() - 1,
                "rng": (b["high"] - b["low"]) / c,
                "rngz": ((b["high"] - b["low"]) / c) / (((b["high"] - b["low"]) / c).rolling(20, min_periods=15).mean()),
                "volu": b["volume"] / b["volume"].rolling(20, min_periods=15).mean(),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "f5": c.shift(-5) / c - 1,
                "f20": c.shift(-20) / c - 1,
                "pos": np.arange(n),
            })
            df["r30z"] = df["r30"] / (df["vol20"] * np.sqrt(30))
            rows.append(df)
    D = pd.concat(rows)
    G5 = D[D["pos"] % 5 == 0].copy()
    G20 = D[D["pos"] % 20 == 0].copy()
    G5["x"] = G5["f5"] - G5["coin"].map(G5.groupby("coin")["f5"].mean())
    G20["x"] = G20["f20"] - G20["coin"].map(G20.groupby("coin")["f20"].mean())
    G5["xn"] = G5["x"] / G5["coin"].map(G5.groupby("coin")["f5"].std())
    G20["xn"] = G20["x"] / G20["coin"].map(G20.groupby("coin")["f20"].std())

    def robust(G, col, q=5):
        d = G.dropna(subset=[col, "x"]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        r = d.groupby("q").agg(mean=("x", "mean"), strength=("xn", "mean"), n=("x", "size"))
        # window-clustered t: per-window mean of xn, t across windows
        wm = d.groupby(["q", "win"])["xn"].mean().unstack(0)
        r["win_t"] = (wm.mean() / (wm.std() / np.sqrt(wm.count()))).values
        r["win_pos_share"] = (wm > 0).mean().values
        cmn = d.groupby(["q", "coin"])["xn"].mean().unstack(0)
        r["coin_pos_share"] = (cmn > 0).mean().values
        # spearman per coin
        rho = d.groupby("coin").apply(lambda s: stats.spearmanr(s[col], s["x"])[0])
        r["rho_med"] = rho.median()
        r["rho_pos"] = (rho > 0).mean()
        return r.round(4)
    for col in ["r30", "r30z", "dhi", "rng", "rngz", "volu"]:
        out["h5_" + col] = robust(G5, col)
    for col in ["r30", "r30z", "dhi", "rngz"]:
        out["h20_" + col] = robust(G20, col)
    # weekday robustness, window clustered
    d = G5.dropna(subset=["x"])
    wm = d.groupby(["wd", "win"])["xn"].mean().unstack(0)
    wdr = pd.DataFrame({"mean": d.groupby("wd")["x"].mean(),
                        "win_t": wm.mean() / (wm.std() / np.sqrt(wm.count())),
                        "win_pos": (wm > 0).mean(),
                        "coin_pos": (d.groupby(["wd", "coin"])["xn"].mean().unstack(0) > 0).mean()})
    out["weekday_h5"] = wdr.round(4)
    # next-day return by weekday, all bars
    D["n1"] = D.groupby(["coin", "win"])["r1"].shift(-1)
    D["n1x"] = D["n1"] - D["coin"].map(D.groupby("coin")["n1"].mean())
    wm1 = D.dropna(subset=["n1x"]).groupby(["wd", "win"])["n1x"].mean().unstack(0)
    out["weekday_next1d"] = pd.DataFrame({"mean": D.groupby("wd")["n1x"].mean(),
                                          "win_t": wm1.mean() / (wm1.std() / np.sqrt(wm1.count()))}).round(5)
    # range day split by direction
    d = G5.dropna(subset=["rngz", "r1", "x"]).copy()
    d["big"] = d.groupby("coin")["rngz"].transform(lambda s: s.rank(pct=True)) > 0.8
    d["up"] = d["r1"] > 0
    out["bigrange_dir"] = d.groupby(["big", "up"]).agg(mean=("x", "mean"), strength=("xn", "mean"), n=("x", "size")).round(4)
    return out
