def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            r1 = c.pct_change()
            s = pd.DataFrame({
                "mom28": c / c.shift(28) - 1,
                "ret1": r1,
                "absr1": r1.abs(),
                "near90": c / c.rolling(90, min_periods=30).max() - 1,
                "vol30": np.log(c).diff().rolling(30).std(),
                "fc": b["forecast"].astype(float),
            })
            s["fwd5"] = c.shift(-5) / c - 1
            s["year"] = pd.to_datetime(b["timestamp"]).dt.year
            s["coin"] = coin; s["win"] = w
            s["grid"] = (np.arange(n) % 5 == 0)
            rows.append(s)
    d = pd.concat(rows, ignore_index=True)
    mu = d[d.grid].groupby("coin")["fwd5"].mean()
    sd = d[d.grid].groupby("coin")["fwd5"].std()
    d["ex5"] = d["fwd5"] - d["coin"].map(mu)
    g = d[d.grid & d.fwd5.notna()].copy()
    # per coin-year spearman, and persistence of sign from year y-1 to y
    cy = []
    for (coin, y), gg in g.groupby(["coin", "year"]):
        if len(gg) < 30: continue
        rec = {"coin": coin, "year": y}
        for k in ["mom28", "ret1", "near90", "vol30"]:
            rec[k] = stats.spearmanr(gg[k], gg["ex5"], nan_policy="omit")[0]
        cy.append(rec)
    cy = pd.DataFrame(cy).sort_values(["coin", "year"])
    pers = {}
    for k in ["mom28", "ret1", "near90", "vol30"]:
        prev = cy.groupby("coin")[k].shift(1)
        m = prev.notna() & cy[k].notna()
        pers[k] = {"corr_prev_year_vs_this": np.corrcoef(prev[m], cy[k][m])[0, 1],
                   "same_sign_share": (np.sign(prev[m]) == np.sign(cy[k][m])).mean(),
                   "n_pairs": m.sum()}
    out["weight_persistence"] = pd.DataFrame(pers).T.round(3)
    # size of mom28 top/bottom and abs ret1 graded, as strength
    for k in ["mom28", "absr1", "near90"]:
        gg = g.dropna(subset=[k]).copy()
        gg["q"] = gg.groupby("coin")[k].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
        gg["str"] = gg.ex5 / gg["coin"].map(sd)
        out[f"q_{k}"] = gg.groupby("q").agg(ex5=("ex5", "mean"), fwd5=("fwd5", "mean"), strength=("str", "mean"),
            n=("ex5", "size"), t=("ex5", lambda x: x.mean() / x.std() * np.sqrt(len(x)))).round(4)
    # mom28 by year: top minus bottom quintile
    gg = g.dropna(subset=["mom28"]).copy()
    gg["q"] = gg.groupby("coin")["mom28"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["mom28_top_minus_bottom_by_year"] = gg.groupby("year").apply(
        lambda x: x[x.q == 4].ex5.mean() - x[x.q == 0].ex5.mean()).round(4)
    # volatility regime: mom28 spearman within vol30 terciles
    gg["vt"] = gg.groupby("coin")["vol30"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    out["mom28_corr_by_vol_tercile"] = gg.groupby("vt").apply(
        lambda x: pd.Series({"rho": stats.spearmanr(x.mom28, x.ex5)[0], "n": len(x)})).round(3)
    # book falls
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            dd.append(t.assign(coin=coin, win=w))
    D = pd.concat(dd)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    out["book_by_year"] = D.groupby("year").agg(book=("book_return", "mean"), coin=("coin_return", "mean")).round(5)
    return out
