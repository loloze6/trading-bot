def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]
            d = pd.DataFrame({
                "coin": coin, "w": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "r1": c.shift(-1) / c - 1,
                "r2": c.shift(-2) / c - 1,
                "p1": c / c.shift(1) - 1,
                "p30": c / c.shift(30) - 1,
                "clpos": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "inprof": (b["regime"] == "unknown").astype(int),
                "pi": np.arange(len(b)),
            })
            d["vol30"] = d["p1"].rolling(30).std()
            d["z1"] = d["p1"] / d["vol30"].shift(1)
            rows.append(d)
    X = pd.concat(rows, ignore_index=True)
    drift = X.groupby("coin")["r1"].mean()
    X["ex1"] = X["r1"] - X["coin"].map(drift)
    d2 = X[X.pi % 2 == 0].groupby("coin")["r2"].mean()
    X["ex2"] = X["r2"] - X["coin"].map(d2)
    X["day"] = X["ts"].dt.floor("D")

    def tab(df, key, col="ex1"):
        g = df.dropna(subset=[key, col])
        out = []
        for k, s in g.groupby(key, observed=True):
            daily = s.groupby("day")[col].mean()
            out.append({"grp": str(k), "n": len(s), "days": len(daily), "mean%": 100 * daily.mean(),
                        "t": daily.mean() / (daily.std(ddof=1) / np.sqrt(len(daily))) if len(daily) > 2 else np.nan})
        return pd.DataFrame(out)

    def graded(df, xcol, col="ex1"):
        g = df.dropna(subset=[xcol, col]).copy()
        g["prod"] = g[xcol] * g[col]
        daily = g.groupby("day")["prod"].sum()
        return {"n": len(g), "days": len(daily), "mean": daily.mean(),
                "t": daily.mean() / (daily.std(ddof=1) / np.sqrt(len(daily)))}

    res = {}
    F = X[X.p30 < 0].copy()
    P = X[X.inprof == 1].copy()
    O = X[(X.p30 < 0) & (X.inprof == 0)].copy()
    out = []
    for nm, df in [("down30 all", F), ("profile", P), ("down30 outside profile", O), ("up30", X[X.p30 > 0])]:
        r = graded(df, "z1"); r["set"] = nm; out.append(r)
        r = graded(df, "clpos"); r["set"] = nm + " clpos"; out.append(r)
    res["graded: sum(z1 * ex1) per day"] = pd.DataFrame(out)
    for nm, df in [("down30", F), ("profile", P), ("down30 out", O)]:
        df = df.copy()
        df["zb"] = pd.cut(df["z1"], [-99, -1.5, -0.5, 0.5, 1.5, 99])
        res[nm + ": by z1 bin, next day"] = tab(df, "zb")
    F["zb"] = pd.cut(F["z1"], [-99, -1.5, -0.5, 0.5, 1.5, 99])
    res["down30: by z1 bin, 2-day (grid)"] = tab(F[F.pi % 2 == 0], "zb", "ex2")
    # per window and per year consistency of up-day-in-down30 effect
    U = F[F.z1 > 0.5]
    res["down30 up-days by window"] = tab(U, "w")
    U = U.copy(); U["yr"] = U["ts"].dt.year
    res["down30 up-days by year"] = tab(U, "yr")
    res["down30 up-days by coin"] = tab(U, "coin")
    # depth interaction: does a deeper 30d fall grade the up-day reversal?
    U2 = F[F.z1 > 0].copy()
    U2["d"] = pd.qcut(U2["p30"], 3, labels=False)
    res["down30 up-days by 30d depth tercile"] = tab(U2, "d")
    return res
