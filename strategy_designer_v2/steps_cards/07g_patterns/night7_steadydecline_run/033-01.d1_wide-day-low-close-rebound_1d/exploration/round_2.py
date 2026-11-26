def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float)
            allr.append((c.shift(-1) / c - 1).dropna())
        drift = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            rng = h - l
            r1 = c / c.shift(1) - 1
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "clv": (c - l) / rng.replace(0, np.nan),
                "rmult": rng / rng.shift(1).rolling(20).mean(),
                "r1": r1,
                "vol20": r1.rolling(20).std(),
                "vol30": r1.rolling(30).std(),
                "tr60": c / c.shift(60) - 1,
                "n1": c.shift(-1) / c - 1 - drift,
                "n2": c.shift(-2) / c - 1 - 2 * drift,
                "g2": c.shift(-2) / c.shift(-1) - 1 - drift,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "pos": np.arange(len(b)),
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["r1z"] = D["r1"] / D["vol20"]
    D["lowwide"] = (1 - D["clv"]) * D["rmult"]
    D["agit"] = D["vol30"] > D.groupby("coin")["vol30"].transform("median")
    D["trend"] = pd.cut(D["tr60"], [-np.inf, -0.1, 0.1, np.inf], labels=["falling", "choppy", "rising"])

    def tday(s, days):
        g = pd.DataFrame({"v": s.values, "d": days.values}).dropna().groupby("d")["v"].sum()
        se = np.sqrt((g ** 2).sum())
        return g.sum() / se if se > 0 else np.nan

    res = {}
    D["lwq"] = D.groupby("coin")["lowwide"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out = []
    for k, g in D.dropna(subset=["lwq", "n1"]).groupby("lwq"):
        out.append({"lwq": k, "n": len(g), "n1%": g.n1.mean()*100, "t1": tday(g.n1, g.day),
                    "day2%": g.g2.mean()*100, "t_day2": tday(g.g2.dropna(), g.dropna(subset=["g2"]).day)})
    res["lowwide quintile -> next day, day after"] = pd.DataFrame(out)
    # disentangle: r1z quintile x clv half
    D["r1q"] = D.groupby("coin")["r1z"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    D["clvh"] = (D["clv"] < 0.5).astype(int)
    out = []
    for (a, bb), g in D.dropna(subset=["r1q", "n1", "clv"]).groupby(["r1q", "clvh"]):
        out.append({"r1tercile": a, "lowhalf": bb, "n": len(g), "n1%": g.n1.mean()*100, "t": tday(g.n1, g.day)})
    res["day return tercile x close half"] = pd.DataFrame(out)
    # regression on both
    X = D.dropna(subset=["clv", "r1z", "n1", "rmult"])
    A = np.column_stack([np.ones(len(X)), 1 - X.clv, X.r1z, X.rmult])
    beta, *_ = np.linalg.lstsq(A, X.n1.values, rcond=None)
    e = X.n1.values - A @ beta
    sc = pd.DataFrame(A * e[:, None]).groupby(X.day.values).sum().values
    Ainv = np.linalg.inv(A.T @ A)
    V = Ainv @ (sc.T @ sc) @ Ainv
    res["joint OLS: const, 1-clv, r1z, rmult"] = pd.DataFrame({"beta%": beta*100, "t": beta/np.sqrt(np.diag(V))},
                                                             index=["const", "1-clv", "r1z", "rmult"])
    # profile split of top lowwide quintile vs rest
    out = []
    for (tr, ag), g in D.dropna(subset=["trend", "n1", "lwq"]).groupby(["trend", "agit"], observed=True):
        top = g[g.lwq == 4]; bot = g[g.lwq <= 1]
        out.append({"trend": tr, "agit": ag, "n_all": len(g), "n_top": len(top),
                    "top%": top.n1.mean()*100, "t_top": tday(top.n1, top.day),
                    "bottom2%": bot.n1.mean()*100})
    res["profile x lowwide top"] = pd.DataFrame(out)
    out = []
    for ag, g in D.dropna(subset=["n1", "lwq"]).groupby("agit"):
        top = g[g.lwq == 4]
        out.append({"agit": ag, "n_top": len(top), "top%": top.n1.mean()*100, "t_top": tday(top.n1, top.day),
                    "all%": g.n1.mean()*100})
    res["agitation x lowwide top"] = pd.DataFrame(out)
    # mirror: high close on wide day
    D["highwide"] = D["clv"] * D["rmult"]
    D["hwq"] = D.groupby("coin")["highwide"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    res["highwide quintile -> next1"] = D.dropna(subset=["hwq", "n1"]).groupby("hwq").apply(
        lambda g: pd.Series({"n": len(g), "n1%": g.n1.mean()*100, "t": tday(g.n1, g.day)}))
    # book: largest loss days -> preceding conditions
    B = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            B.append(d.assign(coin=coin, win=w))
    B = pd.concat(B)
    bk = B.groupby(["win", "day"])["book_return"].mean().dropna()
    q = bk.quantile([0.02, 0.98])
    res["book tails"] = pd.DataFrame({"n_worst": [(bk <= q.iloc[0]).sum()], "mean_worst%": [bk[bk <= q.iloc[0]].mean()*100],
                                     "n_best": [(bk >= q.iloc[1]).sum()], "mean_best%": [bk[bk >= q.iloc[1]].mean()*100],
                                     "sum_all%": [bk.sum()*100], "sum_wo_best%": [bk[bk < q.iloc[1]].sum()*100]})
    res["mean alloc by lowwide q"] = D.groupby("lwq")["alloc"].mean()
    return res
