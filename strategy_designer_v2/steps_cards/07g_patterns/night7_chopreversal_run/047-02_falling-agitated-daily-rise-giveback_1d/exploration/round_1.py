def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "r0": r, "r1": c.shift(-1) / c - 1, "r2": c.shift(-2) / c.shift(-1) - 1,
                "r1_3": c.shift(-3) / c.shift(-1) - 1,
                "rng": (b["high"] - b["low"]) / c,
                "clv": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "inprof": (b["regime"] == "unknown").astype(int),
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            df["absmean60"] = r.abs().rolling(60, min_periods=20).mean().shift(1)
            df["z"] = df["r0"] / df["absmean60"]
            df["r60"] = c / c.shift(60) - 1
            df["vol30"] = r.rolling(30).std()
            df["volrank"] = df["vol30"].rolling(200, min_periods=60).rank(pct=True)
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["r1"].mean()
    D["x1"] = D["r1"] - D["coin"].map(mu)
    D["x2"] = D["r2"] - D["coin"].map(mu)
    D["day"] = D["ts"].dt.floor("D")
    out = {}

    def slope(d, y="x1", x="z"):
        d = d[[x, y, "day"]].dropna()
        if len(d) < 30: return (np.nan, np.nan, len(d))
        X = np.c_[np.ones(len(d)), d[x].values]; Y = d[y].values
        beta = np.linalg.lstsq(X, Y, rcond=None)[0]; e = Y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        g = pd.DataFrame(X * e[:, None]).groupby(d["day"].values).sum().values
        V = XtXi @ (g.T @ g) @ XtXi
        return (beta[1], beta[1] / np.sqrt(V[1, 1]), len(d))

    D["tr"] = np.where(D["r60"] > 0.1, "rising", np.where(D["r60"] < -0.1, "falling", "choppy"))
    D["ag"] = np.where(D["volrank"] > 0.5, "agit", "calm")
    D["prof"] = D["tr"] + "_" + D["ag"]
    res = []
    for (p, side), g in D.assign(side=np.sign(D["r0"])).groupby(["prof", "side"]):
        if side == 0: continue
        s, t, n = slope(g); s2, t2, _ = slope(g, y="x2")
        res.append([p, "up" if side > 0 else "down", n, g["x1"].mean() * 100, s * 100, t, s2 * 100, t2])
    out["slope next-day excess on z, by profile and side (pct per z)"] = pd.DataFrame(
        res, columns=["prof", "side", "n", "mean_x1%", "slope1", "t1", "slope_day2", "t_day2"])
    res = []
    for ip, g in D.assign(side=np.sign(D["r0"])).groupby(["inprof", "side"]):
        if ip == 0 and False: pass
        s, t, n = slope(g); res.append([ip, side, n, g["x1"].mean() * 100, s * 100, t])
    out["recorded profile x side"] = pd.DataFrame(res, columns=["inprof", "side", "n", "mean_x1%", "slope", "t"])
    # quintiles of z overall
    D["zq"] = pd.qcut(D["z"], 10, labels=False, duplicates="drop")
    q = D.groupby("zq").agg(n=("x1", "size"), z=("z", "mean"), x1=("x1", "mean"), x2=("x2", "mean"))
    q["t1"] = D.groupby("zq")["x1"].apply(lambda s: s.mean() / s.std() * np.sqrt(s.count()))
    out["deciles of z, all bars"] = q
    # clv and range
    D["clvq"] = pd.qcut(D["clv"], 5, labels=False, duplicates="drop")
    out["close location quintile, all"] = D.groupby("clvq").agg(n=("x1", "size"), x1=("x1", lambda s: s.mean() * 100),
        t=("x1", lambda s: s.mean() / s.std() * np.sqrt(s.count())))
    out["close location quintile, falling agit"] = D[D.prof == "falling_agit"].groupby("clvq").agg(n=("x1", "size"),
        x1=("x1", lambda s: s.mean() * 100), t=("x1", lambda s: s.mean() / s.std() * np.sqrt(s.count())))
    D["wd"] = D["ts"].dt.weekday
    out["weekday next-day excess"] = D.groupby("wd").agg(n=("x1", "size"), x1=("x1", lambda s: s.mean() * 100),
        t=("x1", lambda s: s.mean() / s.std() * np.sqrt(s.count())))
    # book by coin/window
    gains = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            gains.append([coin, w, d["book_return"].mean() * 1e4, d["coin_return"].mean() * 1e4])
    G = pd.DataFrame(gains, columns=["coin", "win", "book_bp", "coin_bp"])
    out["book mean daily bp by window"] = G.groupby("win")[["book_bp", "coin_bp"]].mean()
    out["book mean daily bp by coin"] = G.groupby("coin")[["book_bp", "coin_bp"]].mean()
    return out
