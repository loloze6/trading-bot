def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            d = pd.DataFrame({"ts": pd.to_datetime(b["timestamp"]), "coin": coin, "win": w})
            d["r1"] = c / c.shift(1) - 1
            d["r5"] = c / c.shift(5) - 1
            d["r60"] = c / c.shift(60) - 1
            d["f1"] = c.shift(-1) / c - 1
            d["vol20"] = d["r1"].rolling(20).std()
            d["z1"] = d["r1"] / d["vol20"].shift(1)
            d["z5"] = d["r5"] / (d["vol20"].shift(5) * np.sqrt(5))
            d["clpos"] = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            d["prof"] = (b["regime"] == "unknown").values
            d["pos"] = b["postRebalance_current_allocation"].astype(float).values
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu1 = D.groupby("coin")["f1"].mean()
    D["x1"] = D["f1"] - D["coin"].map(mu1)
    D["day"] = D["ts"].dt.floor("D")
    # vol relative to coin's median of vol20 within available bars
    D["volrel"] = D["vol20"] / D.groupby("coin")["vol20"].transform("median")

    def ct(s, days):
        s = s.dropna(); dd = days.loc[s.index]
        m = s.mean(); g = (s - m).groupby(dd).sum()
        se = np.sqrt((g**2).sum()) / len(s)
        return m, m / se if se > 0 else np.nan, len(s), dd.nunique()

    def tab(sub, by, col="x1"):
        out = []
        for k, g in sub.groupby(by, observed=True):
            m, t, n, nd = ct(g[col], g["day"])
            out.append({"grp": str(k), "mean%": m*100, "t": t, "n": n, "days": nd})
        return pd.DataFrame(out)

    def reg(sub, xs, y="x1"):
        s = sub.dropna(subset=xs+[y])
        X = np.column_stack([np.ones(len(s))] + [((s[x]-s[x].mean())/s[x].std()).values for x in xs])
        Y = s[y].values
        bt = np.linalg.lstsq(X, Y, rcond=None)[0]; e = Y - X @ bt
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((X.shape[1],)*2)
        for _, idx in s.groupby("day").indices.items():
            u = X[idx].T @ e[idx]; meat += np.outer(u, u)
        se = np.sqrt(np.diag(XtXi @ meat @ XtXi))
        return pd.DataFrame({"coef%_per_sd": bt*100, "t": bt/se, "n": len(s)}, index=["const"]+xs)

    res = {}
    P = D[D.prof]
    res["prof r1 tercile x r5 tercile"] = tab(P, [pd.qcut(P.r1, 3, labels=False), pd.qcut(P.r5, 3, labels=False)])
    res["prof reg z1 z5 clpos"] = reg(P, ["z1", "z5", "clpos"])
    A = D[D.volrel > 1]
    res["agit-proxy reg z1 z5 clpos"] = reg(A, ["z1", "z5", "clpos"])
    # trend proxy within window
    D["tr"] = pd.cut(D.r60, [-np.inf, -0.1, 0.1, np.inf], labels=["fall", "chop", "rise"])
    for tr in ["fall", "chop", "rise"]:
        for ag in [True, False]:
            S = D[(D.tr == tr) & ((D.volrel > 1) == ag)]
            if len(S) > 200:
                res[f"reg z1 {tr} {'agit' if ag else 'calm'}"] = reg(S, ["z1", "clpos"])
    U = D[(D.tr == "chop") & (D.volrel > 1)]
    res["chop agit z1 quintiles"] = tab(U, pd.qcut(U.z1, 5, labels=False))
    res["chop agit clpos quintiles"] = tab(U, pd.qcut(U.clpos, 5, labels=False))
    res["share in tr x agit"] = D.groupby([D.tr, D.volrel > 1], observed=True).size().rename("n").reset_index().astype(str)
    return res
