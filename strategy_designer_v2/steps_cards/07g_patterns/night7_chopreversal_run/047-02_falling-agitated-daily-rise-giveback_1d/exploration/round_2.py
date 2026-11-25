def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "r0": r, "r1": c.shift(-1) / c - 1, "r2": c.shift(-2) / c.shift(-1) - 1,
                "rng": (b["high"] - b["low"]) / c.shift(1),
                "clv": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "inprof": (b["regime"] == "unknown").astype(int),
            })
            df["absmean60"] = r.abs().rolling(60, min_periods=20).mean().shift(1)
            df["z"] = df["r0"] / df["absmean60"]
            df["rngz"] = df["rng"] / ((b["high"] - b["low"]) / c.shift(1)).rolling(60, min_periods=20).mean().shift(1)
            df["r60"] = c / c.shift(60) - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["r1"].mean()
    D["x1"] = D["r1"] - D["coin"].map(mu)
    D["x2"] = D["r2"] - D["coin"].map(mu)
    D["day"] = D["ts"].dt.floor("D")
    D["cl"] = D["clv"] - 0.5   # close location centred: + near high
    out = {}

    def reg(d, xs, y="x1"):
        d = d[xs + [y, "day"]].dropna()
        X = np.c_[np.ones(len(d)), d[xs].values]; Y = d[y].values
        beta = np.linalg.lstsq(X, Y, rcond=None)[0]; e = Y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        g = pd.DataFrame(X * e[:, None]).groupby(d["day"].values).sum().values
        V = XtXi @ (g.T @ g) @ XtXi
        se = np.sqrt(np.diag(V))
        return {"n": len(d), "days": d["day"].nunique(),
                **{f"b_{k}%": beta[i + 1] * 100 for i, k in enumerate(xs)},
                **{f"t_{k}": beta[i + 1] / se[i + 1] for i, k in enumerate(xs)}}

    D["tr"] = np.where(D["r60"] > 0.1, "rising", np.where(D["r60"] < -0.1, "falling", "choppy"))
    res = []
    for name, g in [("all", D), ("inprof", D[D.inprof == 1]), ("outprof", D[D.inprof == 0]),
                    ("inprof up", D[(D.inprof == 1) & (D.r0 > 0)]), ("inprof down", D[(D.inprof == 1) & (D.r0 < 0)]),
                    ("rising", D[D.tr == "rising"]), ("choppy", D[D.tr == "choppy"]), ("falling", D[D.tr == "falling"])]:
        a = reg(g, ["cl"]); a["set"] = name; res.append(a)
        a2 = reg(g, ["cl"], y="x2"); res.append({"set": name + " day2", **a2})
    out["next-day excess on close location (cl=-0.5 low .. +0.5 high)"] = pd.DataFrame(res).set_index("set")
    res = []
    for name, g in [("all", D), ("inprof", D[D.inprof == 1]), ("outprof", D[D.inprof == 0])]:
        a = reg(g, ["cl", "z"]); a["set"] = name; res.append(a)
    out["joint cl and z"] = pd.DataFrame(res).set_index("set")
    # graded by range: cl x relative range
    D["clr"] = D["cl"] * D["rngz"]
    res = []
    for name, g in [("all", D), ("inprof", D[D.inprof == 1]), ("outprof", D[D.inprof == 0])]:
        a = reg(g, ["cl", "clr"]); a["set"] = name; res.append(a)
    out["cl and cl x relative range"] = pd.DataFrame(res).set_index("set")
    # cl effect by window (stability), all bars
    res = []
    for w, g in D.groupby("win"):
        a = reg(g, ["cl"]); a["win"] = w; res.append(a)
    out["cl slope by window"] = pd.DataFrame(res).set_index("win")
    res = []
    for cn, g in D.groupby("coin"):
        a = reg(g, ["cl"]); a["coin"] = cn; res.append(a)
    out["cl slope by coin"] = pd.DataFrame(res).set_index("coin")
    # inprof down days: graded z, day2
    g = D[(D.inprof == 1) & (D.r0 < 0)]
    out["inprof down: z on x1 and x2"] = pd.DataFrame([reg(g, ["z"]), reg(g, ["z"], y="x2")], index=["x1", "x2"])
    # weekday stability: by year
    D["wd"] = D["ts"].dt.weekday; D["yr"] = D["ts"].dt.year
    out["weekday x1 bp by year"] = (D.pivot_table(index="yr", columns="wd", values="x1", aggfunc="mean") * 1e4).round(0)
    return out
