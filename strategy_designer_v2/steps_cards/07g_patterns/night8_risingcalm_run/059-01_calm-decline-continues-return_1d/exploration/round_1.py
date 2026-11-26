def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            r14 = c / c.shift(14) - 1
            s14 = r14 / (sd30 * np.sqrt(14))
            r1s = r1 / sd30
            r60 = c / c.shift(60) - 1
            rng = (b["high"] - b["low"]) / c / sd30
            clo = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            f5 = c.shift(-5) / c - 1
            f1 = c.shift(-1) / c - 1
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "agit": (b["regime"] == "chop").astype(int),
                               "s14": s14, "r1s": r1s, "r60": r60, "rng": rng, "clo": clo,
                               "f5": f5, "f1": f1, "fc": b["forecast"],
                               "alloc": b["postRebalance_current_allocation"],
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A["pos"] % 5 == 0) & A["f5"].notna()].copy()
    G["ex5"] = G["f5"] - G.groupby("coin")["f5"].transform("mean")
    out = {}
    def tab(df, key, col="ex5", q=5):
        d = df.dropna(subset=[key, col]).copy()
        d["b"] = pd.qcut(d[key], q, labels=False, duplicates="drop")
        g = d.groupby("b")[col].agg(["count", "mean", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        g["kmean"] = d.groupby("b")[key].mean()
        return g.round(4)
    for a in [0, 1]:
        out[f"s14 quintiles agit={a}"] = tab(G[G.agit == a], "s14")
        out[f"r1s quintiles agit={a}"] = tab(G[G.agit == a], "r1s")
        out[f"r60 quintiles agit={a}"] = tab(G[G.agit == a], "r60")
        out[f"range quintiles agit={a}"] = tab(G[G.agit == a], "rng")
    out["share agit grid"] = float(G.agit.mean())
    # daily next-day by weekday
    D = A.dropna(subset=["f1"]).copy()
    D["ex1"] = D["f1"] - D.groupby("coin")["f1"].transform("mean")
    g = D.groupby("wd")["ex1"].agg(["count", "mean", "std"]); g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["weekday next-day excess"] = g.round(5)
    # book on positions
    P = A[A.alloc.abs() > 1e-6]
    out["book pos gain by agit"] = P.assign(g=P.alloc * P.f1).groupby("agit")["g"].agg(["count", "mean"]).round(5)
    # by window share of excess in s14 bottom vs top calm
    C = G[G.agit == 0].dropna(subset=["s14"])
    C["neg"] = (C.s14 < 0).astype(int)
    out["calm by window neg/pos s14"] = C.groupby(["w", "neg"])["ex5"].mean().unstack().round(4)
    return out
