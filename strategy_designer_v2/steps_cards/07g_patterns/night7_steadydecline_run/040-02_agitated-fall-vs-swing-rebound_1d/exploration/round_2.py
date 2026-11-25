def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; r = c.pct_change()
            d = pd.DataFrame({"coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "ret": r, "vol30": r.rolling(30, min_periods=20).std(),
                "n1": c.shift(-1)/c-1, "n3": c.shift(-3)/c-1,
                "r5p": c.shift(1)/c.shift(5)-1,
                "volrel": b["volume"]/b["volume"].rolling(20, min_periods=10).mean(),
                "agit": (b["regime"] != "chop").astype(int), "i": np.arange(len(b))})
            d["z"] = d["ret"]/d["vol30"]
            d["r5z"] = d["r5p"]/(d["vol30"]*2)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for h in (1, 3):
        g = D[D["i"] % h == 0].groupby("coin")["n%d" % h].mean()
        D["x%d" % h] = D["n%d" % h] - D["coin"].map(g)
    D["yr"] = D["day"].dt.year
    D["lv"] = np.log(D["volrel"])

    def ols(sub, y, xs):
        sub = sub.dropna(subset=[y]+xs)
        X = np.column_stack([np.ones(len(sub))]+[sub[x].values for x in xs]); Y = sub[y].values
        XtXi = np.linalg.inv(X.T@X); bta = XtXi@X.T@Y; e = Y-X@bta
        G = pd.DataFrame(X*e[:, None]).groupby(sub["day"].values).sum().values
        V = XtXi@(G.T@G)@XtXi
        n, k, m = len(Y), X.shape[1], G.shape[0]
        V *= m/(m-1)*(n-1)/(n-k)
        return pd.Series(dict(zip(["const"]+xs, bta/np.sqrt(np.diag(V)))), name="t").to_frame().assign(coef=bta, n=n, days=m)

    def ct(sub, col):
        sub = sub.dropna(subset=[col]); x = sub[col]; n = len(x)
        if n < 5: return pd.Series({"n": n})
        m = x.mean(); S = (x-m).groupby(sub["day"]).sum()
        return pd.Series({"n": n, "days": sub["day"].nunique(), "mean%": 100*m, "t": m/(np.sqrt((S**2).sum())/n)})
    out = {}
    for a in (1, 0):
        F = D[(D["z"] < 0) & (D["agit"] == a)].copy()
        F["fall"] = -F["z"]; F["fall_x_lv"] = F["fall"]*F["lv"]; F["fall_x_r5"] = F["fall"]*(-F["r5z"])
        out["agit=%d falls: x1 ~ fall + lv + -r5z" % a] = ols(F.assign(mr5=-F["r5z"]), "x1", ["fall", "lv", "mr5"]).round(4)
        out["agit=%d falls: x1 ~ fall + fall*lv + fall*-r5" % a] = ols(F, "x1", ["fall", "fall_x_lv", "fall_x_r5"]).round(4)
    A = D[(D["z"] < -0.75) & (D["agit"] == 1)].copy()
    A["volq"] = pd.qcut(A["volrel"], 3, labels=["low", "mid", "high"])
    A["r5q"] = pd.qcut(A["r5p"], 3, labels=["r5low", "mid", "r5high"])
    out["agit falls: volq x year"] = A.groupby(["yr", "volq"], observed=True).apply(lambda s: ct(s, "x1")).round(2).unstack()["mean%"]
    out["agit falls: r5q x year"] = A.groupby(["yr", "r5q"], observed=True).apply(lambda s: ct(s, "x1")).round(2).unstack()["mean%"]
    G3 = A[A["i"] % 3 == 0]
    out["agit falls h3 grid: volq"] = G3.groupby("volq", observed=True).apply(lambda s: ct(s, "x3")).round(3)
    out["agit falls h3 grid: r5q"] = G3.groupby("r5q", observed=True).apply(lambda s: ct(s, "x3")).round(3)
    out["agit falls: r5q x volq"] = A.groupby(["r5q", "volq"], observed=True).apply(lambda s: ct(s, "x1")).round(3)
    return out
