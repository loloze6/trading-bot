def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            r3 = c / c.shift(3) - 1
            z3 = r3 / (sd30 * np.sqrt(3))
            r1z = r1 / sd30
            f5 = c.shift(-5) / c - 1
            f2 = c.shift(-2) / c - 1
            rng = (b["high"] - b["low"]) / c
            clpos = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            r10 = c / c.shift(10) - 1
            z10 = r10 / (sd30 * np.sqrt(10))
            d = pd.DataFrame({
                "coin": coin, "w": w, "pos": np.arange(len(b)),
                "inprof": (b["regime"] == "unknown").astype(int),
                "z3": z3, "z10": z10, "r1z": r1z, "f5": f5, "f2": f2,
                "clpos": clpos, "rngz": rng / sd30,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "alloc": b["postRebalance_current_allocation"],
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["f5"].apply(lambda s: s[D.loc[s.index, "pos"] % 5 == 0].mean())
    D["u5"] = D["f5"] - D["coin"].map(drift)
    G = D[(D["pos"] % 5 == 0)].dropna(subset=["u5", "z3"])
    out = {}
    def tab(df, col, q=5):
        df = df.copy()
        df["b"] = pd.qcut(df[col], q, labels=False, duplicates="drop")
        g = df.groupby("b")["u5"].agg(["count", "mean", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        g["lo"] = df.groupby("b")[col].min()
        return g.round(4)
    out["share_in_profile_grid"] = float(G["inprof"].mean())
    out["u5_by_z3_inprof"] = tab(G[G.inprof == 1], "z3")
    out["u5_by_z3_outprof"] = tab(G[G.inprof == 0], "z3")
    out["u5_by_z10_inprof"] = tab(G[G.inprof == 1].dropna(subset=["z10"]), "z10")
    out["u5_by_z10_outprof"] = tab(G[G.inprof == 0].dropna(subset=["z10"]), "z10")
    out["u5_by_r1z_inprof"] = tab(G[G.inprof == 1].dropna(subset=["r1z"]), "r1z")
    out["u5_by_clpos_all"] = tab(G.dropna(subset=["clpos"]), "clpos")
    out["u5_by_rngz_all"] = tab(G.dropna(subset=["rngz"]), "rngz")
    out["u5_by_weekday"] = G.groupby("wd")["u5"].agg(["count", "mean"]).round(4)
    # correlation per coin in profile
    cc = {}
    for coin, g in G[G.inprof == 1].groupby("coin"):
        if len(g) > 10:
            r, p = stats.spearmanr(g["z3"], g["u5"]); cc[coin] = (len(g), round(r, 3), round(p, 3))
    out["spearman_z3_u5_inprof_by_coin"] = pd.DataFrame(cc, index=["n", "rho", "p"]).T
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    out["trades"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median"]).round(3)
    # 2-day horizon in profile
    G2 = D[(D["pos"] % 2 == 0)].dropna(subset=["f2", "z3"])
    G2 = G2[G2.inprof == 1].copy()
    G2["b"] = pd.qcut(G2["z3"], 5, labels=False)
    g2 = G2.groupby("b")["f2"].agg(["count", "mean", "std"]); g2["t"] = g2["mean"] / (g2["std"] / np.sqrt(g2["count"]))
    out["f2_by_z3_inprof"] = g2.round(4)
    return out
