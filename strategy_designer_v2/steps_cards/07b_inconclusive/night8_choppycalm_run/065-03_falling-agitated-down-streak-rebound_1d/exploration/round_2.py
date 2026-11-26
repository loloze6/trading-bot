def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            allr.append(c[1:] / c[:-1] - 1)
        cm = np.nanmean(np.concatenate(allr))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            nxt = c.shift(-1) / c - 1
            r1 = c / c.shift(1) - 1
            down = (r1 < 0).astype(int)
            grp = (down == 0).cumsum()
            streak = down.groupby(grp).cumsum()
            lr = np.log(c / c.shift(1)).where(down == 1, 0.0)
            depth = lr.groupby(grp).cumsum()  # log fall over the streak (<=0)
            vol = r1.rolling(30).std()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "prof": (b["regime"] == "unknown"),
                "ex": nxt - cm, "r1z": r1 / vol, "streak": streak,
                "depthz": depth / vol, "r5z": (c / c.shift(5) - 1) / vol,
            })
            rows.append(d)
    D = pd.concat(rows).dropna(subset=["ex", "r1z", "depthz"])
    P = D[D.prof & (D.streak > 0)]

    def ols(x, cols):
        X = np.column_stack([np.ones(len(x))] + [x[c].values for c in cols])
        y = x["ex"].values
        XtX = np.linalg.inv(X.T @ X)
        b = XtX @ X.T @ y
        e = y - X @ b
        S = pd.DataFrame(X * e[:, None]).groupby(x["day"].values).sum().values
        V = XtX @ (S.T @ S) @ XtX
        t = b / np.sqrt(np.diag(V))
        return pd.DataFrame({"coef": b[1:], "t": t[1:]}, index=cols)

    out = {}
    out["down days in profile: ex on streak"] = ols(P, ["streak"])
    out["down days in profile: ex on depthz"] = ols(P, ["depthz"])
    out["down days in profile: ex on r1z"] = ols(P, ["r1z"])
    out["down days in profile: ex on r1z + streak"] = ols(P, ["r1z", "streak"])
    out["down days in profile: ex on r1z + depthz"] = ols(P, ["r1z", "depthz"])
    x = P.copy()
    x["q"] = pd.qcut(x["depthz"], 5, labels=False)
    def tc(g):
        dev = g["ex"] - g["ex"].mean()
        s = dev.groupby(g["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / len(g)
        return pd.Series({"n": len(g), "mean_ex%": 100 * g["ex"].mean(), "t": g["ex"].mean() / se})
    out["down days in profile by depthz quintile (0 deepest)"] = x.groupby("q").apply(tc)
    # same slope outside profile
    Q = D[(~D.prof) & (D.streak > 0)]
    out["down days outside profile: ex on depthz"] = ols(Q, ["depthz"])
    out["down days outside profile: ex on r1z"] = ols(Q, ["r1z"])
    # by window sign of depthz slope
    res = {}
    for w, g in P.groupby("win"):
        if len(g) >= 30:
            r = ols(g, ["depthz"]); res[w] = pd.Series({"n": len(g), "coef": r.coef.iloc[0], "t": r.t.iloc[0]})
    out["depthz slope by window (profile down days)"] = pd.DataFrame(res).T
    return out
