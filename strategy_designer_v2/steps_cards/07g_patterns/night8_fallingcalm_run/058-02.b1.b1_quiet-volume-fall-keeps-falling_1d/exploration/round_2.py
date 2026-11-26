def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            b["fwd5"] = c.shift(-5) / c - 1
            b["ret30"] = c / c.shift(30) - 1
            b["ret60"] = c / c.shift(60) - 1
            b["std30"] = r1.rolling(30).std()
            b["coin"] = coin; b["win"] = w
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b.iloc[::5].copy())
    G = pd.concat(rows, ignore_index=True)
    G = G[G["fwd5"].notna()]
    drift = G.groupby("coin")["fwd5"].mean()
    G["adj"] = G["fwd5"] - G["coin"].map(drift)
    G["z30"] = G["ret30"] / (G["std30"] * np.sqrt(30))
    med = G.groupby("coin")["std30"].median()
    G["agit"] = np.where(G["std30"] > G["coin"].map(med), "agitated", "calm")
    G["trend"] = np.where(G["ret60"] > 0.10, "rising", np.where(G["ret60"] < -0.10, "falling", np.where(G["ret60"].notna(), "choppy", "na")))

    def reg(q, x):
        q = q.dropna(subset=[x, "adj"])
        n = len(q)
        if n < 15: return pd.Series({"n": n, "slope": np.nan, "t": np.nan, "days": 0})
        X = np.column_stack([np.ones(n), q[x].values]); y = q["adj"].values
        XtX = np.linalg.inv(X.T @ X); bta = XtX @ X.T @ y; e = y - X @ bta
        S = pd.DataFrame(X * e[:, None]).groupby(q["day"].values).sum().values
        V = XtX @ (S.T @ S) @ XtX * len(S) / (len(S) - 1)
        return pd.Series({"n": n, "slope": bta[1], "t": bta[1] / np.sqrt(V[1, 1]), "days": len(S)})

    def st(x, days):
        x = pd.Series(x).astype(float); n = len(x)
        if n < 5: return pd.Series({"n": n, "mean%": np.nan, "t": np.nan})
        m = x.mean(); s = (x - m).groupby(pd.Series(days).values).sum()
        return pd.Series({"n": n, "mean%": 100 * m, "t": m / (np.sqrt((s ** 2).sum()) / n)})

    out = {}
    A = G[G["trend"] != "na"]
    out["slope adj~z30 by trend x agitation"] = A.groupby(["trend", "agit"]).apply(lambda q: reg(q, "z30"))
    C = A[A["trend"] == "choppy"]
    out["choppy: slope adj~z30 by window"] = C.groupby("win").apply(lambda q: reg(q, "z30"))
    out["choppy: slope adj~z30 by year"] = C.groupby("year").apply(lambda q: reg(q, "z30"))
    out["choppy: slope adj~z30 by agitation"] = C.groupby("agit").apply(lambda q: reg(q, "z30"))
    C2 = C.copy(); C2["s"] = np.sign(C2["z30"]) * C2["adj"]
    out["choppy: signed adj (direction of 30d move), by agitation"] = C2.dropna(subset=["s"]).groupby("agit").apply(lambda q: st(q["s"], q["day"]))
    F = A[(A["trend"] == "falling") & (A["agit"] == "calm")]
    out["falling calm: slope adj~ret30"] = reg(F, "ret30").to_frame().T
    T = G[G["regime"] == "trending"].copy()
    T["dq"] = pd.qcut(T["ret30"], 5, labels=False)
    out["fall regime: depth quintile by agitation"] = T.groupby(["agit", "dq"]).apply(lambda q: st(q["adj"], q["day"]))
    T["mid"] = T["dq"].isin([1, 2, 3])
    out["fall regime mid-depth (q1-3) by window: mean%"] = T[T["mid"]].groupby("win").apply(lambda q: st(q["adj"], q["day"]))
    return out
