def explore(data):
    import numpy as np, pandas as pd
    H = 3
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            df = pd.DataFrame({
                "coin": coin, "w": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "pos": np.arange(len(b)),
                "r30": c / c.shift(30) - 1,
                "r7": c / c.shift(7) - 1,
                "r1": r1,
                "z1": r1 / r1.rolling(30).std(),
                "vol30": r1.rolling(30).std(),
                "fwd": fwd, "fwd1": fwd1,
                "choppy": (b["regime"] == "unknown"),
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            df["wd"] = df["day"].dt.weekday
            df["yr"] = df["day"].dt.year
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    grid = A[A["pos"] % H == 0].dropna(subset=["fwd"]).copy()
    drift = grid.groupby("coin")["fwd"].mean()
    grid["ex"] = grid["fwd"] - grid["coin"].map(drift)
    sd = grid.groupby("coin")["fwd"].std()
    grid["exs"] = grid["ex"] / grid["coin"].map(sd)

    def ct(s, days):
        s = pd.Series(s.values, index=days.values).dropna()
        if len(s) < 10: return (np.nan, np.nan, len(s))
        m = s.mean(); g = (s - m).groupby(level=0).sum()
        G = len(g)
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(s)
        return (m, m / se, len(s))

    def tab(df, by, col="exs"):
        out = []
        for k, g in df.groupby(by, observed=True):
            m, t, n = ct(g[col], g["day"])
            out.append({"grp": str(k), "mean": m, "t": t, "n": n, "days": g["day"].nunique()})
        return pd.DataFrame(out)

    res = {}
    for name, sub in [("choppy", grid[grid.choppy]), ("trend", grid[~grid.choppy])]:
        s = sub.dropna(subset=["r30"]).copy()
        s["q"] = pd.qcut(s["r30"], 5, labels=False)
        res[f"{name}: r30 quintile -> 3d excess (std units)"] = tab(s, "q")
        s["q7"] = pd.qcut(s["r7"], 5, labels=False)
        res[f"{name}: r7 quintile -> 3d excess"] = tab(s, "q7")
        s["qz"] = pd.qcut(s["z1"], 5, labels=False)
        res[f"{name}: z1 (day move / 30d vol) quintile -> 3d excess"] = tab(s, "qz")
    g2 = grid.dropna(subset=["vol30"]).copy()
    g2["vq"] = g2.groupby("coin")["vol30"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    g2["q"] = pd.qcut(g2["r30"], 3, labels=False)
    g2["k"] = g2["vq"].astype(str) + "_" + g2["q"].astype(str) + "_" + g2["choppy"].astype(str)
    res["volTercile_r30Tercile_choppy -> 3d excess"] = tab(g2, "k")
    # weekday next-day
    A2 = A.dropna(subset=["fwd1"]).copy()
    A2["ex1"] = A2["fwd1"] - A2["coin"].map(A2.groupby("coin")["fwd1"].mean())
    res["weekday -> next day excess (raw)"] = tab(A2, "wd", "ex1")
    # book days
    dd = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; dd.append(d)
    D = pd.concat(dd, ignore_index=True)
    bk = D.groupby(["w", "day"])["book_return"].mean().dropna()
    res["book daily by window: mean, n"] = bk.groupby(level=0).agg(["mean", "std", "count"])
    # positions: gain by alloc sign and r30 depth
    A3 = A.dropna(subset=["fwd1"]).copy()
    A3["gain"] = A3["alloc"] * A3["fwd1"]
    act = A3[A3["alloc"] != 0]
    res["active bars: gain by year"] = act.groupby("yr")["gain"].agg(["mean", "count"])
    res["active bars: gain by coin"] = act.groupby("coin")["gain"].agg(["mean", "count"])
    return res
