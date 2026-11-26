def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            hi = b["high"].astype(float).rolling(20, min_periods=20).max()
            lo = b["low"].astype(float).rolling(20, min_periods=20).min()
            rp = 2 * (c - lo) / (hi - lo) - 1
            r1 = c.pct_change()
            tr60 = c / c.shift(60) - 1
            vol30 = r1.rolling(30, min_periods=20).std()
            vol_rel = vol30 / vol30.expanding(min_periods=30).median()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "rp": rp,
                               "f5": c.shift(-5) / c - 1, "f10": c.shift(-10) / c - 1,
                               "ret10": c / c.shift(10) - 1, "tr60": tr60, "vol_rel": vol_rel,
                               "vol30": vol30, "regime": b["regime"].values,
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "wd": ts.dt.weekday, "year": ts.dt.year, "day": ts.dt.floor("D")})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    for H in (5, 10):
        g = A[A["pos"] % H == 0].dropna(subset=[f"f{H}"])
        A[f"ex{H}"] = A[f"f{H}"] - A["coin"].map(g.groupby("coin")[f"f{H}"].mean())
    def trl(x):
        if pd.isna(x): return "na"
        return "rising" if x > 0.1 else ("falling" if x < -0.1 else "choppy")
    A["trend"] = A["tr60"].map(trl)
    A["agit"] = np.where(A["vol_rel"].isna(), "na", np.where(A["vol_rel"] > 1, "agit", "calm"))
    def clslope(g, x, y):
        g = g.dropna(subset=[x, y])
        if len(g) < 15: return pd.Series({"n": len(g), "days": g["day"].nunique(), "slope": np.nan, "t_cl": np.nan})
        X = np.column_stack([np.ones(len(g)), g[x].values]); Y = g[y].values
        beta, *_ = np.linalg.lstsq(X, Y, rcond=None)
        e = Y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((2, 2)); days = g["day"].values
        for d in np.unique(days):
            m = days == d; s = (X[m] * e[m][:, None]).sum(0); meat += np.outer(s, s)
        G_ = len(np.unique(days)); V = XtXi @ meat @ XtXi * G_ / max(G_ - 1, 1)
        return pd.Series({"n": len(g), "days": G_, "slope": beta[1], "t_cl": beta[1] / np.sqrt(V[1, 1])})
    out = {}
    res = {}
    for H in (5, 10):
        G = A[A["pos"] % H == 0]
        for (t, a), g in G.groupby(["trend", "agit"]):
            res[(H, t, a, "rp")] = clslope(g, "rp", f"ex{H}")
            res[(H, t, a, "ret10")] = clslope(g, "ret10", f"ex{H}")
    out["clustered_slopes_by_profile"] = pd.DataFrame(res).T
    # choppy continuation by year, H=5
    G5 = A[(A["pos"] % 5 == 0) & (A["trend"] == "choppy")]
    out["choppy_rp_slope_by_year_h5"] = G5.groupby("year").apply(lambda g: clslope(g, "rp", "ex5"))
    out["choppy_rp_slope_by_coin_h5"] = G5.groupby("coin").apply(lambda g: clslope(g, "rp", "ex5"))
    # choppy short side: lower half
    G5["half"] = np.where(G5["rp"] < 0, "lower", "upper")
    out["choppy_half_h5"] = G5.groupby(["agit", "half"])["ex5"].agg(["count", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    # weekday: day-clustered (mean over coins per day)
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d.copy(); dd["coin"] = coin; dd["w"] = w; dl.append(dd)
    D = pd.concat(dl)
    dm = D.groupby(["w", "day"])["coin_return"].mean().dropna().reset_index()
    dm["wd"] = pd.to_datetime(dm["day"]).dt.weekday; dm["year"] = pd.to_datetime(dm["day"]).dt.year
    out["weekday_daymean"] = dm.groupby("wd")["coin_return"].agg(["count", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    dm["fs"] = dm["wd"].isin([4, 5])
    out["friSat_minus_rest_by_year"] = dm.groupby("year").apply(lambda g: pd.Series({"n": len(g),
        "diff": g[g.fs]["coin_return"].mean() - g[~g.fs]["coin_return"].mean(),
        "t": stats.ttest_ind(g[g.fs]["coin_return"], g[~g.fs]["coin_return"], equal_var=False).statistic}))
    # book largest days: what preceded
    book = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    q = book["book_return"].quantile([0.02, 0.98])
    out["book_extreme_days"] = pd.DataFrame({
        "worst_n": [(book["book_return"] <= q.iloc[0]).sum()],
        "worst_mean_book": [book.loc[book["book_return"] <= q.iloc[0], "book_return"].mean()],
        "worst_mean_coin": [book.loc[book["book_return"] <= q.iloc[0], "coin_return"].mean()],
        "best_mean_book": [book.loc[book["book_return"] >= q.iloc[1], "book_return"].mean()],
        "best_mean_coin": [book.loc[book["book_return"] >= q.iloc[1], "coin_return"].mean()],
        "share_gain_top2pct": [book.loc[book["book_return"] >= q.iloc[1], "book_return"].sum() / book["book_return"].sum()]})
    # book gain split long vs short days
    A["side"] = np.sign(A["alloc"]).map({1.0: "long", -1.0: "short", 0.0: "flat"})
    A["g1"] = A["alloc"] * (A.groupby(["coin", "w"])["f5"].transform(lambda s: s) * 0 + 0)
    return out
