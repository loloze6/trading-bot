def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd.shift(1)
            tr = c / c.shift(60) - 1
            vol30 = sd
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            rng = (b["high"] - b["low"]) / c
            clpos = (b["close"] - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "r": r, "z": z, "tr": tr,
                               "fwd": fwd, "fwd1": fwd1, "clpos": clpos, "wd": ts.dt.weekday,
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "fc": b["forecast"].astype(float), "regime": b["regime"]})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = A.groupby("coin")["fwd"].transform(lambda s: s.mean())
    A["unus"] = A["fwd"] - A.groupby("coin")["fwd"].transform("mean")
    G = A[(A["pos"] % H == 0)].dropna(subset=["fwd", "z"])
    out = {}
    def summ(g, col="unus"):
        x = g[col].dropna()
        n = len(x)
        return pd.Series({"n": n, "mean%": 100 * x.mean() if n else np.nan,
                          "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    G = G.copy()
    G["zb"] = pd.cut(G["z"], [-99, -3, -2, -1, 0, 1, 2, 3, 99])
    G["trb"] = np.where(G["tr"].isna(), "na", np.where(G["tr"] > 0.1, "rising", np.where(G["tr"] < -0.1, "falling", "choppy")))
    out["fwd5 unusual by z bucket (all)"] = G.groupby("zb").apply(summ)
    out["fwd5 by z bucket x trend"] = G.groupby(["trb", "zb"]).apply(summ)
    # all days (overlapping) at extreme z, by close position
    E = G[G["z"].abs() >= 2].copy()
    E["side"] = np.where(E["z"] > 0, "up", "down")
    E["clb"] = pd.cut(E["clpos"], [-0.01, 0.33, 0.66, 1.01])
    out["extreme days fwd5 by side x close position"] = E.groupby(["side", "clb"]).apply(summ)
    out["extreme days fwd1 by side x trend"] = E.groupby(["side", "trb"]).apply(lambda g: summ(g, "fwd1"))
    out["fwd5 by weekday"] = G.groupby("wd").apply(summ)
    out["fwd5 by window"] = G.groupby("w").apply(summ)
    # book trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t):
                t = t.copy(); t["coin"] = coin; t["w"] = w; T.append(t)
    if T:
        T = pd.concat(T)
        out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
        out["trades overall"] = T["net_profit_loss_percent"].describe()
    # correlation z vs fwd per trend
    for k, g in G.groupby("trb"):
        g2 = g.dropna(subset=["z", "unus"])
        if len(g2) > 30:
            rr, p = stats.spearmanr(g2["z"], g2["unus"])
            out[f"spearman z vs fwd5 {k}"] = f"rho {rr:.3f} p {p:.3f} n {len(g2)}"
    return out
