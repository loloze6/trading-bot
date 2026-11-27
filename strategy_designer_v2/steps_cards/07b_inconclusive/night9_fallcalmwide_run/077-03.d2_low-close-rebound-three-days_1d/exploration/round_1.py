def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        allr = {1: [], 3: []}
        for w, b in ws.items():
            c = b["close"].values
            for h in (1, 3):
                idx = np.arange(0, len(c) - h, h)
                allr[h] += list(c[idx + h] / c[idx] - 1)
        drift[coin] = {h: np.mean(allr[h]) for h in (1, 3)}
        sd3 = np.std(allr[3], ddof=1)
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]; hi = b["high"]; lo = b["low"]
            r1 = c.pct_change()
            s30 = r1.rolling(30, min_periods=10).std()
            mid = (hi + lo) / 2
            clv = 2 * (c - mid) / (hi - lo).replace(0, np.nan)
            width = (hi - lo) / c / s30
            f1 = c.shift(-1) / c - 1
            f2 = c.shift(-2) / c - 1
            f3 = c.shift(-3) / c - 1
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                               "year": pd.to_datetime(b["timestamp"]).dt.year,
                               "prof": b["regime"] == "unknown", "fc": b["forecast"],
                               "clv": clv, "width": width, "prod": clv * width,
                               "x1": f1 - drift[coin][1], "x3": f3 - drift[coin][3],
                               "x2": f2 - 2 * drift[coin][1], "sd3": sd3,
                               "d": pd.to_datetime(b["timestamp"]).dt.floor("D")})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    P = A[A.prof].dropna(subset=["clv", "width"])
    # replicate cases: first bet bar per 3-bar cell
    C = P[P.fc >= 2].copy()
    C["cell"] = C.pos // 3
    C = C.sort_values("pos").groupby(["coin", "win", "cell"]).head(1).dropna(subset=["x3"])
    def cl_t(df, col):
        s = df.groupby("d")[col].apply(lambda v: (v - df[col].mean()).sum())
        D = len(s); se = np.sqrt((s ** 2).sum() * D / (D - 1)) / len(df)
        return pd.Series({"n": len(df), "days": D, "mean": df[col].mean(), "t": df[col].mean() / se})
    out = {}
    out["cases_h"] = pd.DataFrame({h: cl_t(C, h) for h in ["x1", "x2", "x3"]}).T
    C["q"] = pd.qcut(C.fc.rank(method="first"), 4, labels=False)
    out["cases_by_fc_quart"] = C.groupby("q").apply(lambda g: pd.concat([cl_t(g, "x3"), cl_t(g, "x1").rename(lambda k: k + "_1")]))
    out["cases_by_coin"] = C.groupby("coin").apply(lambda g: cl_t(g, "x3"))
    out["cases_by_year"] = C.groupby("year").apply(lambda g: cl_t(g, "x3"))
    out["cases_by_win"] = C.groupby("win").apply(lambda g: cl_t(g, "x3"))
    # all profile bars, 1-day grid (non-overlap h=1 is every bar)
    P1 = P.dropna(subset=["x1"]).copy()
    P1["cq"] = pd.qcut(P1.clv, 5, labels=False)
    out["prof_all_by_clv_quint_next1"] = P1.groupby("cq").apply(lambda g: pd.Series({"clv": g.clv.mean(), **cl_t(g, "x1").to_dict()}))
    P1["wide"] = P1.width > P1.width.median()
    out["prof_wide_by_clv_next1"] = P1[P1.wide].groupby("cq").apply(lambda g: cl_t(g, "x1"))
    P3 = P[P.pos % 3 == 0].dropna(subset=["x3"]).copy()
    P3["cq"] = pd.qcut(P3.clv, 5, labels=False)
    out["prof_grid3_by_clv_next3"] = P3.groupby("cq").apply(lambda g: cl_t(g, "x3"))
    out["corr_prod_next1"] = float(stats.spearmanr(P1["prod"], P1.x1).correlation)
    out["corr_prod_next3_grid"] = float(stats.spearmanr(P3["prod"], P3.x3).correlation)
    return out
