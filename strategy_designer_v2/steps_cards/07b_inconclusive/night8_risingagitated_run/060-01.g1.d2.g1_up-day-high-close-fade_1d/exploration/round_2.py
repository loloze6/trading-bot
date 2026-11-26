def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            rng = (h - l).replace(0, np.nan)
            loc = (c - l) / rng
            r1 = c / c.shift(1) - 1
            lr = np.log(c).diff()
            vol20 = lr.rolling(20, min_periods=10).std().shift(1)
            df = pd.DataFrame({"coin": coin, "win": w,
                               "ts": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                               "loc": loc, "r1": r1, "z1": lr / vol20,
                               "n1": c.shift(-1) / c - 1, "n2": c.shift(-2) / c - 1, "n3": c.shift(-3) / c - 1,
                               "regime": b["regime"].astype(str), "pos": np.arange(len(b))})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    for k, hh in [("n1", 1), ("n2", 2), ("n3", 3)]:
        dr = d[d["pos"] % hh == 0].groupby("coin")[k].mean()
        d["u" + k] = -(d[k] - d["coin"].map(dr))
    def summ(x, col="un1"):
        x = x.dropna(subset=[col])
        n = len(x)
        if n < 5: return pd.Series({"n": n, "days": np.nan, "mean": np.nan, "t": np.nan})
        m = x[col].mean()
        dev = (x[col] - m).groupby(x["ts"]).sum()
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / n
        return pd.Series({"n": n, "days": G, "mean": m, "t": m / se if se > 0 else np.nan})
    d["inprof"] = d["regime"].isin(["mean_reversion", "unknown"])
    d = d.dropna(subset=["loc", "r1"])
    out = {}
    up = d[d["inprof"] & (d["r1"] > 0)].copy()
    up["z1q"] = pd.qcut(up["z1"], 4, labels=False)
    out["inprof_up_by_z1q"] = up.groupby("z1q").apply(summ)
    up["r1q"] = pd.qcut(up["r1"], 4, labels=False)
    out["inprof_up_by_r1q"] = up.groupby("r1q").apply(summ)
    out["inprof_up_all_h1"] = summ(up, "un1")
    out["inprof_up_all_h2_grid"] = summ(up[up["pos"] % 2 == 0], "un2")
    out["inprof_up_all_h3_grid"] = summ(up[up["pos"] % 3 == 0], "un3")
    uh = up[up["loc"] > 0.5]
    out["inprof_uphigh_h2_grid"] = summ(uh[uh["pos"] % 2 == 0], "un2")
    out["inprof_uphigh_h3_grid"] = summ(uh[uh["pos"] % 3 == 0], "un3")
    cc = up.dropna(subset=["un1", "z1"])
    out["inprof_up_spearman"] = pd.Series({
        "loc_vs_un1": stats.spearmanr(cc["loc"], cc["un1"])[0],
        "r1_vs_un1": stats.spearmanr(cc["r1"], cc["un1"])[0],
        "z1_vs_un1": stats.spearmanr(cc["z1"], cc["un1"])[0], "n": len(cc)})
    out["inprof_up_by_coin"] = up.groupby("coin").apply(summ)
    upo = d[~d["inprof"] & (d["r1"] > 0)].copy()
    upo["z1q"] = pd.qcut(upo["z1"], 4, labels=False)
    out["outprof_up_by_z1q"] = upo.groupby("z1q").apply(summ)
    return out
