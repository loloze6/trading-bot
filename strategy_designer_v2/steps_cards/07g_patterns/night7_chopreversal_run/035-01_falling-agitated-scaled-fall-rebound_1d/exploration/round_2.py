def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = [b["close"].astype(float).pct_change().dropna() for b in wins.values()]
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30).std()
            d = pd.DataFrame({
                "ts": pd.to_datetime(b["timestamp"]).values, "coin": coin, "win": w,
                "z": (r / sd).values,
                "z2": ((c / c.shift(2) - 1) / (sd * np.sqrt(2))).values,
                "z3": ((c / c.shift(3) - 1) / (sd * np.sqrt(3))).values,
                "zprev": (r.shift(1) / sd).values,
                "f1": (c.shift(-1) / c - 1 - mu).values,
                "f2": (c.shift(-2) / c - 1 - 2 * mu).values,
                "tr60": (c / c.shift(60) - 1).values,
                "fa": (b["regime"] == "unknown").values,
                "pos": b["postRebalance_current_allocation"].astype(float).values,
            })
            d["vr"] = (sd / r.rolling(90).std()).values
            rows.append(d)
    D = pd.concat(rows).dropna(subset=["z", "f1"])

    def slope(g, x, y):
        g = g.dropna(subset=[x, y])
        if len(g) < 20: return pd.Series({"slope": np.nan, "t": np.nan, "n": len(g), "days": g.ts.nunique()})
        X = np.c_[np.ones(len(g)), g[x].values]; Y = g[y].values
        XtXi = np.linalg.inv(X.T @ X); b = XtXi @ X.T @ Y; e = Y - X @ b
        meat = np.zeros((2, 2))
        for _, idx in g.reset_index(drop=True).groupby("ts").indices.items():
            s = X[idx].T @ e[idx]; meat += np.outer(s, s)
        G = g.ts.nunique(); V = XtXi @ meat @ XtXi * G / (G - 1)
        return pd.Series({"slope": b[1], "t": b[1] / np.sqrt(V[1, 1]), "n": len(g), "days": G})

    def tday(g, col):
        s = g.groupby("ts")[col].mean().dropna()
        return pd.Series({"mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan, "days": len(s), "n": len(g)})

    FA = D[D.fa]; out = {}
    res = {}
    for x in ["z", "z2", "z3"]:
        for y in ["f1", "f2"]:
            sub = FA[FA[x] < 0].copy(); sub["neg"] = -sub[x]
            res[f"{x} falls -> {y}"] = slope(sub, "neg", y)
        sub = FA[FA[x] > 0]
        res[f"{x} rises -> f1"] = slope(sub, x, "f1")
    out["FA slopes (neg = size of fall)"] = pd.DataFrame(res).T
    # prev day within today's fall
    F = FA[FA.z < 0].copy(); F["neg"] = -F.z; F["negprev"] = -F.zprev
    F["prev"] = np.where(F.zprev < 0, "prev down", "prev up")
    out["FA falls slope on today's z, by prev sign"] = F.groupby("prev").apply(lambda g: slope(g, "neg", "f1"))
    F["zb"] = pd.cut(F.z, [-99, -1.5, -0.75, 0])
    out["FA falls f1 by z bucket x prev sign"] = F.groupby(["zb", "prev"], observed=True).apply(lambda g: tday(g, "f1"))
    # profiles outside FA: falls slope
    O = D[~D.fa & D.tr60.notna()].copy()
    O["trend"] = np.where(O.tr60 > 0.10, "rising", np.where(O.tr60 < -0.10, "falling", "choppy"))
    O["ag"] = np.where(O.vr > 1, "vol up", "vol down")
    Of = O[O.z < 0].copy(); Of["neg"] = -Of.z
    out["outside FA falls slope by trend x short/long vol"] = Of.groupby(["trend", "ag"]).apply(lambda g: slope(g, "neg", "f1"))
    Or = O[O.z > 0]
    out["outside FA rises slope by trend"] = Or.groupby("trend").apply(lambda g: slope(g, "z", "f1"))
    # within FA, by vol ratio
    F["vrb"] = pd.qcut(F.vr, 2, labels=["low ratio", "high ratio"])
    out["FA falls slope by 30d/90d vol ratio"] = F.groupby("vrb", observed=True).apply(lambda g: slope(g, "neg", "f1"))
    # book best/worst days
    days = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["win"] = w; days.append(x)
    DD = pd.concat(days)
    bk = DD.groupby(["win", "day"]).agg(b=("book_return", "mean"), c=("coin_return", "mean")).dropna()
    q = bk.b.quantile([0.02, 0.98])
    out["book worst 2% vs best 2% days: coin return same day"] = pd.DataFrame({
        "worst": bk[bk.b <= q.iloc[0]].mean(), "best": bk[bk.b >= q.iloc[1]].mean()})
    out["share of book sum from top 5% days"] = float(bk.b[bk.b >= bk.b.quantile(0.95)].sum() / bk.b.sum())
    return out
