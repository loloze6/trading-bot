def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            r1 = c.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            vol30 = r1.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n),
                "r1": r1, "ret28": c / c.shift(28) - 1, "near": c / c.rolling(90, min_periods=30).max(),
                "vol30": vol30, "fwd1": c.shift(-1) / c - 1, "fwd5": c.shift(-5) / c - 1,
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "wd": ts.dt.weekday, "yr": ts.dt.year,
            })
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    out = {}
    d1 = D.dropna(subset=["fwd1"]).copy()
    d1["ex1"] = d1["fwd1"] - d1["coin"].map(d1.groupby("coin")["fwd1"].mean())
    def tt(s): return s.mean() / (s.std() / np.sqrt(len(s)))
    # weekday excess next-day return by coin (t)
    out["wd excess next-day t by coin"] = d1.groupby(["coin", "wd"])["ex1"].apply(tt).unstack()
    out["wd excess next-day mean by coin"] = d1.groupby(["coin", "wd"])["ex1"].mean().unstack()
    out["wd excess next-day t by year"] = d1.groupby(["yr", "wd"])["ex1"].apply(tt).unstack()
    # is the weekday effect graded by volatility? vol tercile within coin
    d1 = d1.dropna(subset=["vol30"])
    d1["vq"] = d1.groupby("coin")["vol30"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["wd excess next-day mean by vol tercile"] = d1.groupby(["vq", "wd"])["ex1"].mean().unstack()
    out["wd excess next-day t by vol tercile"] = d1.groupby(["vq", "wd"])["ex1"].apply(tt).unstack()
    # persistence of signals' predictive power: per coin, per year spearman vs 5d grid excess, then corr year t vs t+1
    G = D[(D["pos"] % 5 == 0) & D["fwd5"].notna()].copy()
    G["ex5"] = G["fwd5"] - G["coin"].map(G.groupby("coin")["fwd5"].mean())
    pers = {}
    for col in ["ret28", "r1", "near", "vol30"]:
        g = G.dropna(subset=[col])
        cy = g.groupby(["coin", "yr"]).apply(lambda x: stats.spearmanr(x[col], x["ex5"])[0] if len(x) > 20 else np.nan).unstack()
        a = cy.iloc[:, :-1].values.ravel(); bnext = cy.iloc[:, 1:].values.ravel()
        m = ~np.isnan(a) & ~np.isnan(bnext)
        pers[col] = {"corr year to next year": stats.pearsonr(a[m], bnext[m])[0], "pairs": m.sum(),
                     "mean abs yearly spearman": np.nanmean(np.abs(cy.values))}
    out["persistence of predictive power"] = pd.DataFrame(pers).T
    # book: alloc x next-day return, decomposed by weekday
    D["gain"] = D["alloc"] * D["fwd1"]
    out["position gain by weekday"] = D.groupby("wd")[["gain", "alloc"]].mean()
    # largest book days: what preceded (coin's prior 1d) and position sign
    allD = []
    for coin, wins in days.items():
        for w, dd in wins.items():
            allD.append(dd.assign(coin=coin, win=w))
    DD = pd.concat(allD, ignore_index=True)
    DD["wd"] = pd.to_datetime(DD["day"]).dt.weekday
    out["book daily mean by weekday"] = DD.groupby("wd")[["book_return", "coin_return"]].mean()
    return out
