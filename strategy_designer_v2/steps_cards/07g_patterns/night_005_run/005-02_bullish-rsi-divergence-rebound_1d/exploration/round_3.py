def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c); r1 = c.pct_change()
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(n)})
            df["r1p"] = r1
            df["vol20"] = r1.rolling(20).std()
            df["f1"] = c.shift(-1) / c - 1
            df["f2"] = c.shift(-2) / c - 1
            df["f3"] = c.shift(-3) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df["year"] = ts.dt.year
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["vt"] = D.groupby("coin")["vol20"].transform(
        lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))

    def spread(d, col, y, q=5):
        d = d.dropna(subset=[col, y]).copy()
        if len(d) < 30:
            return pd.Series({"low_minus_high": np.nan})
        d["b"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        lo = d[d.b == 0][y]; hi = d[d.b == q-1][y]
        t = stats.ttest_ind(lo, hi, equal_var=False)
        rho = stats.spearmanr(d[col], d[y])
        return pd.Series({"low_minus_high": lo.mean()-hi.mean(), "welch_t": t.statistic,
                          "n_each": len(lo), "spearman": rho[0], "spear_p": rho[1]})
    g1 = D.dropna(subset=["f1"]).copy()
    g1["ex1"] = g1["f1"] - g1["coin"].map(g1.groupby("coin")["f1"].mean())
    H = g1[g1.vt == 2]
    out["hv_by_coin"] = pd.DataFrame({c: spread(H[H.coin == c], "r1p", "ex1") for c in H.coin.unique()}).T
    out["hv_by_year"] = pd.DataFrame({y: spread(H[H.year == y], "r1p", "ex1") for y in sorted(H.year.unique())}).T
    # quintile profile inside high vol
    d = H.dropna(subset=["r1p"]).copy()
    d["b"] = d.groupby("coin")["r1p"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    prof = d.groupby("b")["ex1"].agg(["mean", "count", "std"])
    prof["t"] = prof["mean"] / (prof["std"] / np.sqrt(prof["count"]))
    prof["r1p_mean"] = d.groupby("b")["r1p"].mean()
    out["hv_quintile_profile"] = prof.drop(columns="std")
    # interaction regression: ex1 on z(r1p) * vol z
    g = g1.dropna(subset=["r1p", "vol20"]).copy()
    g["x"] = g["r1p"]
    g["xv"] = g["r1p"] * (g["vol20"] / g.groupby("coin")["vol20"].transform("mean"))
    X = np.column_stack([np.ones(len(g)), g["x"], g["xv"]])
    beta, *_ = np.linalg.lstsq(X, g["ex1"].values, rcond=None)
    resid = g["ex1"].values - X @ beta
    s2 = resid @ resid / (len(g) - 3)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["interaction_reg"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["const", "r1p", "r1p_x_relvol"])
    # 2-day horizon, non-overlapping grid, high vol
    g2 = D[D.pos % 2 == 0].dropna(subset=["f2"]).copy()
    g2["ex2"] = g2["f2"] - g2["coin"].map(g2.groupby("coin")["f2"].mean())
    out["hv_2d"] = spread(g2[g2.vt == 2], "r1p", "ex2")
    g3 = D[D.pos % 3 == 0].dropna(subset=["f3"]).copy()
    g3["ex3"] = g3["f3"] - g3["coin"].map(g3.groupby("coin")["f3"].mean())
    out["hv_3d"] = spread(g3[g3.vt == 2], "r1p", "ex3")
    return out
