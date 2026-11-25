def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c, h, l = b["close"], b["high"], b["low"]
            rng = (h - l).replace(0, np.nan)
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b))})
            d["loc"] = (h - c) / rng
            d["ret"] = c.pct_change()
            d["rngrel"] = (h - l) / c
            d["rngratio"] = d["rngrel"] / d["rngrel"].rolling(20, min_periods=10).mean().shift(1)
            d["vol20"] = d["ret"].rolling(20, min_periods=10).std()
            d["volratio"] = d["vol20"] / d["vol20"].rolling(60, min_periods=20).mean()
            d["ret20"] = c / c.shift(20) - 1
            d["newlow30"] = (c < c.shift(1).rolling(30, min_periods=20).min()).astype(int)
            d["f1"] = c.shift(-1) / c - 1
            d["f5"] = c.shift(-5) / c - 1
            hk = h.rolling(5, min_periods=5).max(); lk = l.rolling(5, min_periods=5).min()
            d["loc5"] = (hk - c) / (hk - lk).replace(0, np.nan)
            d["ts"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            d["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for k in ["f1", "f5"]:
        D[k + "d"] = D[k] - D.groupby("coin")[k].transform("mean")
    D["dev"] = D["loc"] - 0.5
    out = {}
    def tab(g, col):
        a = g[col].agg(["mean", "count", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        return a.drop(columns="std")
    def ols(df, x, y):
        df = df.dropna(subset=[x, y])
        r = stats.linregress(df[x], df[y])
        return pd.Series({"slope": r.slope, "t": r.slope / r.stderr, "n": len(df)})
    # graded interaction: dev x rngratio
    D["dev_x_rr"] = D["dev"] * D["rngratio"].clip(upper=4)
    D["dev_x_rel"] = D["dev"] * D["rngrel"]
    out["slopes_f1"] = pd.DataFrame({
        "dev": ols(D, "dev", "f1d"),
        "dev_x_rngratio": ols(D, "dev_x_rr", "f1d"),
        "dev_x_rngrel": ols(D, "dev_x_rel", "f1d"),
        "ret_z": ols(D.assign(z=-D["ret"] / D["vol20"]), "z", "f1d"),
    }).T
    D["rq"] = pd.qcut(D["rngratio"], 4, labels=False)
    D["dr"] = np.sign(D["dev"]) * D["f1d"]
    top = D[D["rq"] == 3]
    out["topRR_dirret_by_coin"] = tab(top.groupby("coin"), "dr")
    out["topRR_dirret_by_year"] = tab(top.groupby("year"), "dr")
    out["topRR_dirret_long_vs_short"] = tab(top.groupby(np.sign(top["dev"])), "dr")
    # multiple regression: which carries it
    X = D.dropna(subset=["dev", "dev_x_rel", "f1d"])
    A = np.column_stack([np.ones(len(X)), X["dev"], X["dev_x_rel"]])
    beta, *_ = np.linalg.lstsq(A, X["f1d"], rcond=None)
    res = X["f1d"] - A @ beta
    s2 = (res**2).sum() / (len(X) - 3)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(A.T @ A)))
    out["multi_dev_and_devxrel"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["c", "dev", "dev_x_rel"])
    # 5-day location over 5 days, grid, by window and year
    G = D[D["pos"] % 5 == 0].copy()
    G["d5"] = G["loc5"] - 0.5
    out["grid5_slope_loc5"] = ols(G, "d5", "f5d").to_frame().T
    G["dr5"] = np.sign(G["d5"]) * G["f5d"]
    out["grid5_dr5_by_year"] = tab(G.groupby("year"), "dr5")
    out["grid5_dr5_by_coin"] = tab(G.groupby("coin"), "dr5")
    # brief: new 30-day low in volatile decline
    D["volfall"] = ((D["ret20"] < 0) & (D["volratio"] > 1)).astype(int)
    out["f1_by_volfall_newlow"] = tab(D.groupby(["volfall", "newlow30"]), "f1d")
    G2 = G.copy()
    G2["volfall"] = ((G2["ret20"] < 0) & (G2["volratio"] > 1)).astype(int)
    out["f5_by_volfall_newlow_grid"] = tab(G2.groupby(["volfall", "newlow30"]), "f5d")
    return out
