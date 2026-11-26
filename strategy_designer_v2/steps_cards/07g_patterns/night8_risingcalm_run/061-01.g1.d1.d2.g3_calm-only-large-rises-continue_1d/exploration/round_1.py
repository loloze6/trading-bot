def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=20).std().shift(1)
            z = r1 / sd
            r3 = c / c.shift(3) - 1
            sd3 = sd * np.sqrt(3)
            z3 = r3 / sd3
            rng = (b["high"] - b["low"]) / c
            clpos = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            f5 = c.shift(-5) / c - 1
            f1 = c.shift(-1) / c - 1
            n = len(b)
            idx = np.arange(0, n, 5)
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": idx,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D").values[idx],
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday.values[idx],
                "z": z.values[idx], "z3": z3.values[idx], "f5": f5.values[idx],
                "f1": f1.values[idx], "clpos": clpos.values[idx],
                "calm": (b["regime"] != "chop").values[idx],
                "regime": b["regime"].values[idx],
                "alloc": b["postRebalance_current_allocation"].values[idx],
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D = D.dropna(subset=["f5"])
    D["drift"] = D.groupby("coin")["f5"].transform("mean")
    D["u"] = D["f5"] - D["drift"]
    usual = D.groupby("coin")["f5"].transform("std")
    D["s"] = D["u"] / usual

    def tcl(g):
        s = g.groupby("day")["u"].apply(lambda x: (x - g["u"].mean()).sum())
        G = len(s)
        if G < 3:
            return pd.Series({"n": len(g), "days": G, "mean_u": g["u"].mean(), "t": np.nan})
        se = np.sqrt((s ** 2).sum()) / len(g) * np.sqrt(G / (G - 1))
        return pd.Series({"n": len(g), "days": G, "mean_u": g["u"].mean(), "strength": g["s"].mean(), "t": g["u"].mean() / se})

    out = {}
    Dz = D.dropna(subset=["z"]).copy()
    Dz["zb"] = pd.cut(Dz["z"], [-np.inf, -2, -1, -0.5, 0, 0.5, 1, 2, np.inf])
    out["z_bucket_by_calm"] = Dz.groupby(["calm", "zb"]).apply(tcl)
    Dz["z3b"] = pd.cut(Dz["z3"], [-np.inf, -2, -1, 0, 1, 2, np.inf])
    out["z3_bucket_by_calm"] = Dz.dropna(subset=["z3"]).groupby(["calm", "z3b"]).apply(tcl)
    Dz["clb"] = pd.cut(Dz["clpos"], [0, 0.2, 0.4, 0.6, 0.8, 1.0], include_lowest=True)
    out["closepos_by_calm"] = Dz.dropna(subset=["clpos"]).groupby(["calm", "clb"]).apply(tcl)
    out["weekday"] = D.groupby("wd").apply(tcl)
    out["by_coin_calm"] = D.groupby(["coin", "calm"]).apply(tcl)
    out["by_regime"] = D.groupby("regime").apply(tcl)
    # correlations of z with u, calm vs agitated
    out["corr_z_u"] = Dz.groupby("calm").apply(lambda g: pd.Series({"rho": g["z"].corr(g["u"], method="spearman"), "n": len(g)}))
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["win"] = w; dd.append(t)
    DD = pd.concat(dd)
    br = DD.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book_by_window"] = br.groupby(level=0).agg(["mean", "std", "count"])
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): t = t.copy(); t["coin"] = coin; tr.append(t)
    T = pd.concat(tr)
    T["fb"] = pd.qcut(T["entry_forecast"], 4, duplicates="drop")
    out["trades_by_entry_fc"] = T.groupby("fb")["net_profit_loss_percent"].agg(["mean", "count", "median"])
    return out
