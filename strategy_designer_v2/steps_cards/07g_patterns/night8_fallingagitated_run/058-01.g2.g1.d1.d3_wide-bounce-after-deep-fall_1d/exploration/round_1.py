def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            r = c.pct_change()
            vol = r.rolling(30, min_periods=20).std()
            d = pd.DataFrame({
                "coin": coin, "w": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "r1": r, "z1": r / vol,
                "z3": (c / c.shift(3) - 1) / vol,
                "z3lag": (c.shift(1) / c.shift(4) - 1) / vol,
                "rng": (b["high"] - b["low"]) / c / vol,
                "clv": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "f1": c.shift(-1) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "pos3": (np.arange(len(b)) % 3 == 0),
                "regime": b["regime"].astype(str),
                "alloc": b["postRebalance_current_allocation"],
                "fc": b["forecast"],
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    m1 = D.groupby("coin")["f1"].transform("mean")
    D["x1"] = D["f1"] - m1
    m3 = D[D.pos3].groupby("coin")["f3"].mean()
    D["x3"] = D["f3"] - D["coin"].map(m3)
    D["inprof"] = D["regime"].isin(["mean_reversion", "unknown"])
    D["wd"] = D["ts"].dt.dayofweek
    out = {}
    def summ(g, col):
        s = g[col].dropna()
        n = len(s)
        return pd.Series({"n": n, "mean%": 100 * s.mean(),
                          "t": s.mean() / (s.std() / np.sqrt(n)) if n > 2 else np.nan})
    out["regime share"] = D["regime"].value_counts(normalize=True)
    for prof, lab in [(True, "in"), (False, "out")]:
        S = D[D.inprof == prof].dropna(subset=["z1", "x1"])
        S = S.assign(q=pd.qcut(S["z1"], 5, labels=False))
        out[f"{lab}prof next1 by z1 quintile"] = S.groupby("q").apply(lambda g: summ(g, "x1"))
        S3 = D[(D.inprof == prof) & D.pos3].dropna(subset=["z3", "x3"])
        S3 = S3.assign(q=pd.qcut(S3["z3"], 5, labels=False))
        out[f"{lab}prof next3 by z3 quintile (grid)"] = S3.groupby("q").apply(lambda g: summ(g, "x3"))
        Sr = D[D.inprof == prof].dropna(subset=["rng", "x1"])
        Sr = Sr.assign(q=pd.qcut(Sr["rng"], 5, labels=False))
        out[f"{lab}prof next1 by range quintile"] = Sr.groupby("q").apply(lambda g: summ(g, "x1"))
        Sc = D[D.inprof == prof].dropna(subset=["clv", "x1"])
        Sc = Sc.assign(q=pd.qcut(Sc["clv"], 5, labels=False))
        out[f"{lab}prof next1 by close-location quintile"] = Sc.groupby("q").apply(lambda g: summ(g, "x1"))
    out["all next1 by weekday"] = D.dropna(subset=["x1"]).groupby("wd").apply(lambda g: summ(g, "x1"))
    out["inprof next1 by weekday"] = D[D.inprof].dropna(subset=["x1"]).groupby("wd").apply(lambda g: summ(g, "x1"))
    # book
    days = []
    for coin, ws in data["days"].items():
        for w, dd in ws.items():
            days.append(dd.assign(coin=coin, w=w))
    Y = pd.concat(days, ignore_index=True)
    bk = Y.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book by window"] = bk.groupby(level=0).agg(["mean", "count"])
    # active positions: realised short pnl by coin
    A = D[D.alloc.abs() > 0].dropna(subset=["f1"])
    A = A.assign(pnl=A["alloc"] * A["f1"])
    out["active by coin"] = A.groupby("coin").apply(lambda g: pd.Series({"n": len(g), "pnl_mean%": 100*g.pnl.mean(),
        "t": g.pnl.mean()/(g.pnl.std()/np.sqrt(len(g))), "x1_short%": -100*g.x1.mean()}))
    return out
