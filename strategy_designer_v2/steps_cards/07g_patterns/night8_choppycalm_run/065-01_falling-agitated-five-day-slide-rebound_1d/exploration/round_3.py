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
            d["r4p"] = c.shift(1) / c.shift(5) - 1
            d["r60"] = c / c.shift(60) - 1
            d["f1"] = c.shift(-1) / c - 1
            d["f2"] = c.shift(-2) / c - 1
            d["vol20"] = d["r1"].rolling(20).std()
            d["prof"] = (b["regime"] == "unknown").values
            d["pos"] = b["postRebalance_current_allocation"].astype(float).values
            d["g2"] = (np.arange(len(b)) % 2 == 0)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["x1"] = D["f1"] - D["coin"].map(D.groupby("coin")["f1"].mean())
    D["x2"] = D["f2"] - D["coin"].map(D[D.g2].groupby("coin")["f2"].mean())
    D["day"] = D["ts"].dt.floor("D")
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
        XtXi = np.linalg.inv(X.T @ X); meat = np.zeros((X.shape[1],)*2)
        for _, idx in s.groupby("day").indices.items():
            u = X[idx].T @ e[idx]; meat += np.outer(u, u)
        se = np.sqrt(np.diag(XtXi @ meat @ XtXi))
        return pd.DataFrame({"coef%_per_sd": bt*100, "t": bt/se, "n": len(s)}, index=["const"]+xs)
    res = {}
    P = D[D.prof].copy()
    P["r1neg"] = P.r1.clip(upper=0); P["r1pos"] = P.r1.clip(lower=0)
    P["r4neg"] = P.r4p.clip(upper=0)
    res["prof reg r1neg r1pos r4neg"] = reg(P, ["r1neg", "r1pos", "r4neg"])
    deep = P[P.r4p < P.r4p.median()]
    res["prof deep prior4 r1 quintiles"] = tab(deep, pd.qcut(deep.r1, 5, labels=False))
    res["prof deep prior4 r1 quintiles x2 grid"] = tab(deep[deep.g2], pd.qcut(deep[deep.g2].r1, 5, labels=False), "x2")
    sh = deep[deep.r1 > 0]
    res["prof deep prior4 up-day reg r1"] = reg(sh, ["r1"])
    res["prof deep up-day by year"] = tab(sh, sh.ts.dt.year)
    Fa = D[(D.r60 < -0.1) & (D.volrel > 1) & (~D.prof)]
    Fa = Fa[Fa.r4p < Fa.r4p.median()]
    res["proxy-falling-agit outside prof deep r1 quintiles"] = tab(Fa, pd.qcut(Fa.r1, 5, labels=False))
    O = D[(~D.prof) & (D.r60 >= -0.1)]
    O = O[O.r4p < O.r4p.median()]
    res["other profiles deep prior4 r1 quintiles"] = tab(O, pd.qcut(O.r1, 5, labels=False))
    # book: daily returns
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            dd.append(t.assign(coin=coin))
    B = pd.concat(dd)
    br = B.dropna(subset=["book_return"])
    res["book day ret by year mean%"] = br.groupby(pd.to_datetime(br.day).dt.year)["book_return"].agg(lambda s: s.mean()*100)
    return res
