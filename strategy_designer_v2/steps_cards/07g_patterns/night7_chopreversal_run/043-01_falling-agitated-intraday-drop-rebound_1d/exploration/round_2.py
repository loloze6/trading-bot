def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            o, h, l, c = b["open"], b["high"], b["low"], b["close"]
            r = c.pct_change()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "oc": c / o - 1,
                "rng": (h - l) / o,
                "clv": (c - l) / (h - l).replace(0, np.nan),
                "r1": c.shift(-1) / c - 1,
                "r3": c.shift(-3) / c - 1,
                "ret5": c / c.shift(5) - 1,
                "ret20": c / c.shift(20) - 1,
                "ret60": c / c.shift(60) - 1,
                "vol20": r.rolling(20).std(),
                "inprof": (b["regime"] == "unknown").astype(int),
            })
            rows.append(d)
    df = pd.concat(rows, ignore_index=True)
    drift = df.groupby("coin")["r1"].mean()
    drift3 = df.groupby("coin")["r3"].mean()
    df["x1"] = df["r1"] - df["coin"].map(drift)
    df["x3"] = df["r3"] - df["coin"].map(drift3)
    df["drop"] = (-df["oc"]).clip(lower=0)
    df["rise"] = df["oc"].clip(lower=0)
    df["ocv"] = df["oc"] / df["vol20"]
    out = {}

    def ols_cl(s, ycol, xcols):
        s = s.dropna(subset=[ycol] + xcols)
        X = np.column_stack([np.ones(len(s))] + [s[c].values for c in xcols])
        y = s[ycol].values
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        e = y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        g = s["day"].values
        meat = np.zeros((X.shape[1], X.shape[1]))
        for k in np.unique(g):
            m = g == k
            u = X[m].T @ e[m]
            meat += np.outer(u, u)
        G = len(np.unique(g)); N, K = X.shape
        V = XtXi @ meat @ XtXi * G / (G - 1) * (N - 1) / (N - K)
        se = np.sqrt(np.diag(V))
        return pd.DataFrame({"coef": beta, "t": beta / se}, index=["const"] + xcols).round(5).assign(n=N, days=G)

    dn = df[(df.inprof == 1) & (df.oc < 0)]
    up = df[(df.inprof == 1) & (df.oc > 0)]
    out["in-prof down: x1 on drop"] = ols_cl(dn, "x1", ["drop"])
    out["in-prof down: x1 on drop+clv+ret5+rng"] = ols_cl(dn, "x1", ["drop", "clv", "ret5", "rng"])
    out["in-prof down: x1 on drop+ret20"] = ols_cl(dn, "x1", ["drop", "ret20"])
    out["in-prof down: x1 on ocv (drop vs own swing)"] = ols_cl(dn, "x1", ["ocv"])
    out["in-prof down: x3 on drop"] = ols_cl(dn, "x3", ["drop"])
    out["in-prof up: x1 on rise"] = ols_cl(up, "x1", ["rise"])
    out["in-prof up: x1 on rise+ret5+clv"] = ols_cl(up, "x1", ["rise", "ret5", "clv"])
    out["in-prof all: x1 on ret5"] = ols_cl(df[df.inprof == 1], "x1", ["ret5"])
    out["out-prof down: x1 on drop"] = ols_cl(df[(df.inprof == 0) & (df.oc < 0)], "x1", ["drop"])
    # out-of-profile down days split by in-window 60d trend
    o = df[(df.inprof == 0) & (df.oc < 0)].dropna(subset=["ret60"]).copy()
    o["trend"] = np.where(o.ret60 < -0.10, "falling", np.where(o.ret60 > 0.10, "rising", "choppy"))
    res = {}
    for t, s in o.groupby("trend"):
        r = ols_cl(s, "x1", ["drop"])
        res[t] = [r.loc["drop", "coef"], r.loc["drop", "t"], r["n"].iloc[0]]
    out["out-prof down: slope on drop by 60d trend"] = pd.DataFrame(res, index=["slope", "t", "n"]).T
    # out-of-profile down days split by vol20 high/low within coin
    o2 = df[(df.inprof == 0) & (df.oc < 0)].dropna(subset=["vol20"]).copy()
    o2["vhi"] = o2.groupby("coin")["vol20"].transform(lambda v: v > v.median()).astype(int)
    res = {}
    for t, s in o2.groupby("vhi"):
        r = ols_cl(s, "x1", ["drop"])
        res[t] = [r.loc["drop", "coef"], r.loc["drop", "t"], r["n"].iloc[0]]
    out["out-prof down: slope on drop by vol20 high(1)/low(0)"] = pd.DataFrame(res, index=["slope", "t", "n"]).T
    # in-profile up days tercile by rise
    u = up.dropna(subset=["x1"]).copy()
    u["q"] = pd.qcut(u["rise"], 3, labels=False)
    g = u.groupby("q")["x1"].agg(["count", "mean", "std"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["in-prof up days by rise tercile"] = g.round(5)
    return out
