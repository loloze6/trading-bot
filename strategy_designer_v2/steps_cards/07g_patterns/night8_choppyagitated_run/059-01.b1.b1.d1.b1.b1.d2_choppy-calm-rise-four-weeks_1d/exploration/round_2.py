def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=20).std()
            z1 = r1 / sd
            rng = (b["high"].astype(float) - b["low"].astype(float)) / c
            clp = (c - b["low"].astype(float)) / (b["high"].astype(float) - b["low"].astype(float))
            r60 = c / c.shift(60) - 1
            trend = np.where(r60.isna(), "na", np.where(r60 > 0.10, "rising", np.where(r60 < -0.10, "falling", "choppy")))
            r3p = c / c.shift(3) - 1
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)), "day": ts.dt.floor("D"),
                               "z1": z1, "r1": r1, "sd": sd, "rng": rng, "clp": clp, "trend": trend,
                               "inprof": (b["regime"] == "unknown").values,
                               "z3": r3p / (sd * np.sqrt(3))})
            for h in (1, 2, 3, 7):
                df["f%d" % h] = c.shift(-h) / c - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    out = {}
    def grid(h):
        g = D[(D["pos"] % h == 0)].dropna(subset=["f%d" % h]).copy()
        g["ex"] = g["f%d" % h] - D.dropna(subset=["f%d" % h]).groupby("coin")["f%d" % h].transform("mean").groupby(D["coin"]).first().reindex(g["coin"]).values
        return g
    def ct(g, col="ex"):
        m = g[col].mean()
        s = (g[col] - m).groupby(g["day"]).sum()
        G = len(s)
        se = np.sqrt(G / (G - 1) * (s ** 2).sum()) / len(g)
        return pd.Series({"n": len(g), "days": G, "mean": m, "t_day": m / se})
    def tab(g, key):
        return g.groupby(key).apply(ct).round(4)
    g1 = grid(1).dropna(subset=["z1"])
    g1["dec"] = pd.qcut(g1["z1"], 10, labels=False)
    out["z1 decile -> next day excess (day-clustered t)"] = tab(g1, "dec")
    g1["q"] = pd.qcut(g1["z1"], 5, labels=False)
    out["z1 bottom quintile -> next day, by trend"] = tab(g1[g1.q == 0], "trend")
    out["z1 top quintile -> next day, by trend"] = tab(g1[g1.q == 4], "trend")
    out["z1 bottom quintile -> next day, by window"] = tab(g1[g1.q == 0], "win")
    out["z1 bottom quintile -> next day, by close position tercile"] = tab(g1[g1.q == 0].assign(cq=lambda x: pd.qcut(x.clp, 3, labels=False)), "cq")
    # graded within bottom quintile: correlation of z1 with next day
    b0 = g1[g1.q == 0]
    out["corr z1 vs next day within bottom quintile"] = float(b0["z1"].corr(b0["ex"]))
    for h in (2, 3):
        g = grid(h).dropna(subset=["z1"]); g["q"] = pd.qcut(g["z1"], 5, labels=False)
        out["z1 quintile -> next %dd excess" % h] = tab(g, "q")
    g7 = grid(7).dropna(subset=["z1"]); g7["q"] = pd.qcut(g7["z1"], 5, labels=False)
    out["z1 top quintile -> next 7d, by trend"] = tab(g7[g7.q == 4], "trend")
    g3 = grid(1).dropna(subset=["z3"]); g3["q"] = pd.qcut(g3["z3"], 5, labels=False)
    out["z3 (3-day scaled) quintile -> next day"] = tab(g3, "q")
    return out
