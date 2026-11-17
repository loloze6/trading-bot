def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 7
    rows = []; rows1 = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); v = b["volume"].astype(float)
            hi = b["high"].astype(float); lo = b["low"].astype(float); op = b["open"].astype(float)
            n = len(b)
            ts = pd.to_datetime(b["timestamp"])
            r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=20).std()
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(n),
                              "fwd": c.shift(-H) / c - 1, "fwd1": c.shift(-1) / c - 1,
                              "r1": r1, "z1": r1 / sd, "r3": c / c.shift(3) - 1,
                              "dist": c / c.rolling(20, min_periods=20).max() - 1,
                              "vr": v / v.rolling(30, min_periods=30).mean(),
                              "clv": (c - lo) / (hi - lo).replace(0, np.nan),
                              "yr": ts.dt.year, "fc": b["forecast"].astype(float)})
            rows.append(d[d["pos"] % H == 0]); rows1.append(d)
    S = pd.concat(rows).dropna(subset=["fwd"])
    S["ex"] = S["fwd"] - S.groupby("coin")["fwd"].transform("mean")
    A = pd.concat(rows1).dropna(subset=["fwd1"])
    A["ex1"] = A["fwd1"] - A.groupby("coin")["fwd1"].transform("mean")
    out = {}
    def st(x, y):
        m = pd.concat([x, y], axis=1).dropna()
        if len(m) < 10: return np.nan, len(m)
        r = stats.linregress(m.iloc[:, 0], m.iloc[:, 1]); return round(r.slope / r.stderr, 2), len(m)
    res = {}
    for col in ["r1", "z1", "r3", "clv"]:
        res[col] = dict(zip(["t", "n"], st(S[col], S["ex"])))
    S["svr"] = S["vr"] * np.sign(S["r1"])
    S["z1vr"] = S["z1"] * S["vr"]
    for col in ["svr", "z1vr"]:
        res[col] = dict(zip(["t", "n"], st(S[col], S["ex"])))
    out["7d slope t extra vars"] = pd.DataFrame(res).T
    # multiple regression
    m = S[["ex", "dist", "vr", "z1", "r1"]].dropna()
    X = m[["dist", "vr", "z1"]]; X = (X - X.mean()) / X.std(); X = np.column_stack([np.ones(len(X)), X.values])
    y = m["ex"].values; beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta; s2 = resid @ resid / (len(y) - X.shape[1])
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["multi reg t (const,dist,vr,z1)"] = pd.Series(np.round(beta / se, 2), index=["c", "dist", "vr", "z1"])
    out["multi reg n"] = len(y)
    q = pd.qcut(S["z1"], 5, labels=False)
    g = S.groupby(q)["ex"].agg(["mean", "count", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["7d ex by z1 quintile"] = g.round(4)
    pc = {}
    for coin, gg in S.groupby("coin"):
        pc[coin] = {"z1_t": st(gg["z1"], gg["ex"])[0], "z1vr_t": st(gg["z1vr"], gg["ex"])[0]}
    for y_, gg in S.groupby("yr"):
        pc[str(y_)] = {"z1_t": st(gg["z1"], gg["ex"])[0], "z1vr_t": st(gg["z1vr"], gg["ex"])[0]}
    out["z1 t per coin / year"] = pd.DataFrame(pc).T
    # z1 split by volume tercile
    S["vrq"] = pd.qcut(S["vr"], 3, labels=["thin", "mid", "heavy"])
    S["zq"] = pd.qcut(S["z1"], 3, labels=["down", "flat", "up"])
    out["7d ex z1 x vol"] = S.pivot_table(index="zq", columns="vrq", values="ex", aggfunc="mean").round(4)
    out["7d count z1 x vol"] = S.pivot_table(index="zq", columns="vrq", values="ex", aggfunc="count")
    # next-day after large moves (1-bar, non-overlap automatically)
    q1 = pd.qcut(A["z1"], 10, labels=False)
    g1 = A.groupby(q1)["ex1"].agg(["mean", "count", "std"]); g1["t"] = g1["mean"] / (g1["std"] / np.sqrt(g1["count"]))
    out["next-day ex by z1 decile"] = g1.round(5)
    # book around its largest days
    D = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            dd = d.copy(); dd["w"] = w; D.append(dd)
    D = pd.concat(D)
    bk = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index().sort_values(["w", "day"])
    bk["prev_coin"] = bk.groupby("w")["coin_return"].shift(1)
    bk["next_book"] = bk.groupby("w")["book_return"].shift(-1)
    bk["q"] = pd.qcut(bk["book_return"], [0, .02, .1, .5, .9, .98, 1], labels=False)
    out["book by own-return bucket"] = bk.groupby("q")[["book_return", "prev_coin", "coin_return", "next_book"]].mean().round(5)
    return out
