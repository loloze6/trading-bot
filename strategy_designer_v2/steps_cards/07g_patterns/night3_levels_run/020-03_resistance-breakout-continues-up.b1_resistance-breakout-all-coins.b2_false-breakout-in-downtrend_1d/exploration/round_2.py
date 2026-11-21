def explore(data):
    import numpy as np, pandas as pd
    H = 10
    drift = {}; usual = {}
    for coin, wins in data["bars"].items():
        g = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - H, H):
                g.append(c[i + H] / c[i] - 1)
        g = np.array(g); drift[coin] = g.mean(); usual[coin] = g.std()
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True); c = b["close"]; n = len(b)
            ts = pd.to_datetime(b["timestamp"])
            fwd = c.shift(-H) / c - 1
            fwd20 = c.shift(-20) / c - 1
            r30 = c / c.shift(30) - 1
            r10p = c / c.shift(10) - 1
            hi30 = c.rolling(30).max()
            vol30 = c.pct_change().rolling(30).std()
            rows.append(pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(n), "fwd": fwd, "fwd20": fwd20,
                "adj": fwd - drift[coin], "z": (fwd - drift[coin]) / usual[coin],
                "r30": r30, "r10p": r10p, "r30v": r30 / (vol30 * np.sqrt(30)), "near": c / hi30 - 1,
                "raw": b.get("debug_info.components.break.last_history_value", np.nan),
                "alloc": b["postRebalance_current_allocation"], "year": ts.dt.year}))
    A = pd.concat(rows, ignore_index=True)
    grid = A[(A["pos"] % H == 0) & A["fwd"].notna() & A["r30"].notna()].copy()
    def summ(gr):
        s = gr["z"]
        return pd.Series({"n": len(s), "adj_pct": gr["adj"].mean() * 100, "z": s.mean(),
                          "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})
    out = {}
    grid["q10"] = grid.groupby("coin")["r30"].transform(lambda x: pd.qcut(x.rank(method="first"), 10, labels=False))
    out["r30_decile_long"] = grid.groupby("q10").apply(summ)
    grid["qv"] = grid.groupby("coin")["r30v"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["r30_volscaled_quintile_long"] = grid.groupby("qv").apply(summ)
    top = grid[grid["q10"] >= 8]
    out["top_r30_by_year"] = top.groupby("year").apply(summ)
    out["top_r30_by_coin"] = top.groupby("coin").apply(summ)
    low = grid[grid["q10"].isin([2, 3])]
    out["lowmid_r30_by_year"] = low.groupby("year").apply(summ)
    # within positive r30: graded? correlation of r30 rank with z
    pos = grid[grid["r30"] > 0]
    out["spearman_r30_z_posr30"] = float(pos[["r30", "z"]].corr(method="spearman").iloc[0, 1])
    out["n_posr30"] = int(len(pos))
    out["spearman_r30_z_negr30"] = float(grid[grid["r30"] < 0][["r30", "z"]].corr(method="spearman").iloc[0, 1])
    # nearness to 30-day high
    grid["nq"] = grid.groupby("coin")["near"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["near30high_quintile_long"] = grid.groupby("nq").apply(summ)
    # trades: entry r30 and losses
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t):
                t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T, ignore_index=True)
    out["trades_side"] = T.groupby("side").agg(n=("net_profit_loss_percent", "size"), mean_net=("net_profit_loss_percent", "mean"),
                                               mean_gross=("profit_loss_percent", "mean"))
    T["durq"] = pd.cut(T["duration_minutes"] / 1440, [-1, 2, 9, 11, 20, 1000])
    out["trades_by_duration"] = T.groupby("durq").agg(n=("net_profit_loss_percent", "size"), mean_net=("net_profit_loss_percent", "mean"),
                                                      mean_gross=("profit_loss_percent", "mean"))
    return out
