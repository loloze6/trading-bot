def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    drift1 = {}
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b.sort_values("timestamp")["close"].reset_index(drop=True)
            allr.append((c.shift(-1)/c - 1).dropna())
        drift1[coin] = pd.concat(allr).mean()
    # 3-day drift on non-overlapping grid
    drift3 = {}
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b.sort_values("timestamp")["close"].reset_index(drop=True)
            r = (c.shift(-3)/c - 1)
            allr.append(r[np.arange(len(c)) % 3 == 0].dropna())
        drift3[coin] = pd.concat(allr).mean()
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "fc": b["regime"].astype(str) == "unknown",
                "r3f": c.shift(-3)/c - 1,
                "r2f": c.shift(-2)/c - 1,
                "r5f": c.shift(-5)/c - 1,
                "r1": c/c.shift(1) - 1,
                "r2": c/c.shift(2) - 1,
                "r3": c/c.shift(3) - 1,
                "r5": c/c.shift(5) - 1,
                "r7": c/c.shift(7) - 1,
                "r30": c/c.shift(30) - 1,
                "vol30": (c/c.shift(1)-1).rolling(30).std(),
                "pos": np.arange(len(b)),
            })
            rows.append(d)
    df = pd.concat(rows, ignore_index=True)
    df["ex3"] = df["r3f"] - df["coin"].map(drift3)
    df["z3"] = df["r3"] / (df["vol30"]*np.sqrt(3))
    out = {}
    def tab(s, col, y, k=3):
        s = s.dropna(subset=[col, y]).copy()
        s["q"] = pd.qcut(s[col], k, labels=False, duplicates="drop")
        g = s.groupby("q")[y].agg(["count", "mean", "std"])
        g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
        rho, p = stats.spearmanr(s[col], s[y])
        g.loc["rho", "mean"] = rho; g.loc["rho", "t"] = p
        return g
    fc = df[df["fc"]]
    # robustness to grid offset
    for off in [0, 1, 2]:
        s = fc[fc["pos"] % 3 == off]
        out[f"fc ex3 by r3 off{off}"] = tab(s, "r3", "ex3")
    s0 = fc[fc["pos"] % 3 == 0]
    out["fc ex3 by z3"] = tab(s0, "z3", "ex3")
    out["fc ex3 by r2"] = tab(s0, "r2", "ex3")
    out["fc ex3 by r5"] = tab(s0, "r5", "ex3")
    # other profiles comparison
    nf = df[(~df["fc"]) & (df["pos"] % 3 == 0)]
    out["notfc ex3 by r3"] = tab(nf, "r3", "ex3")
    # per coin: slope of ex3 on r3 in fc
    res = {}
    for coin, g in s0.dropna(subset=["r3", "ex3"]).groupby("coin"):
        lr = stats.linregress(g["r3"], g["ex3"])
        res[coin] = pd.Series({"n": len(g), "slope": lr.slope, "t": lr.slope/lr.stderr})
    out["fc slope ex3~r3 by coin"] = pd.DataFrame(res).T
    # day-clustered slope, pooled
    s = s0.dropna(subset=["r3", "ex3"]).copy()
    lr = stats.linregress(s["r3"], s["ex3"])
    s["res"] = s["ex3"] - (lr.intercept + lr.slope*s["r3"])
    xd = s["r3"] - s["r3"].mean()
    num = (xd*s["res"]).groupby(s["day"]).sum()
    se = np.sqrt((num**2).sum())/(xd**2).sum()
    out["pooled fc slope"] = pd.Series({"slope": lr.slope, "t ols": lr.slope/lr.stderr,
                                        "t day-clustered": lr.slope/se, "n": len(s),
                                        "days": s["day"].nunique()})
    # short side only: the falling third, signed short gain (−ex3)
    s["q"] = pd.qcut(s["r3"], 3, labels=False)
    lo = s[s["q"] == 0]
    gd = (-lo["ex3"]).groupby(lo["day"]).sum()
    out["short after 3d fall, day t"] = pd.Series({"mean per case": -lo["ex3"].mean(),
        "t days": gd.mean()/(gd.std()/np.sqrt(len(gd))), "days": len(gd)})
    # by window halves (early windows vs late)
    s["late"] = s["win"].str[1:].astype(int) >= 12
    out["fc ex3 by r3 tercile x late"] = s.groupby(["late", "q"])["ex3"].agg(["count", "mean"])
    return out
