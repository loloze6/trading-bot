def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            allr.append(pd.Series(c).pct_change().dropna())
        mu1 = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            rng = (h - l)
            cl = ((c - l) / rng.replace(0, np.nan))
            rm = rng / rng.rolling(20).mean()
            r20 = c / c.shift(20) - 1
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                              "f": b["forecast"], "cl": cl, "rm": rm, "r20": r20,
                              "yr": pd.to_datetime(b["timestamp"]).dt.year})
            for H in (1, 3, 5, 10):
                d[f"x{H}"] = -(c.shift(-H) / c - 1 - mu1 * H)
            rows.append(d)
    D = pd.concat(rows)
    C = D[(D.f < 0)].copy()
    C["af"] = C.f.abs()
    out = {}
    def summ(g, col="x1"):
        g = g.dropna(subset=[col])
        n = len(g); m = g[col].mean()
        t = m / (g[col].std() / np.sqrt(n)) if n > 2 else np.nan
        wm = (g[col] * g.af).sum() / g.af.sum()
        return pd.Series({"n": n, "mean": m, "t": t, "wmean": wm})
    out["overall_by_horizon"] = pd.DataFrame({f"x{H}": summ(C[C.pos % H == 0], f"x{H}") for H in (1, 3, 5, 10)}).T
    C["clq"] = pd.qcut(C.cl, 5, labels=False, duplicates="drop")
    C["rmq"] = pd.qcut(C.rm, 5, labels=False, duplicates="drop")
    C["afq"] = pd.qcut(C.af, 5, labels=False, duplicates="drop")
    C["r20q"] = pd.qcut(C.r20, 4, labels=False, duplicates="drop")
    out["by_closeloc_q"] = C.groupby("clq").apply(summ)
    out["by_rangemult_q"] = C.groupby("rmq").apply(summ)
    out["by_absforecast_q"] = C.groupby("afq").apply(summ)
    out["by_ret20_q"] = C.groupby("r20q").apply(summ)
    out["by_coin"] = C.groupby("coin").apply(summ)
    out["by_window"] = C.groupby("w").apply(summ)
    out["by_year"] = C.groupby("yr").apply(summ)
    out["clq_x_rmq_mean"] = C.groupby(["clq", "rmq"]).x1.mean().unstack()
    # outside regime: same close-loc gradient?
    N = D[(D.r20 >= 0)].copy(); N["af"] = 1.0
    N["clq"] = pd.qcut(N.cl, 5, labels=False, duplicates="drop")
    out["nonregime_by_closeloc_q"] = N.groupby("clq").apply(summ)
    # by closeloc q, 3-day horizon
    C3 = C[C.pos % 3 == 0]
    out["by_closeloc_q_x3"] = C3.groupby("clq").apply(lambda g: summ(g, "x3"))
    out["by_rangemult_q_x3"] = C3.groupby("rmq").apply(lambda g: summ(g, "x3"))
    out["corr_cl_rm_x1"] = pd.Series({"cl": C[["cl","x1"]].corr().iloc[0,1], "rm": C[["rm","x1"]].corr().iloc[0,1], "af": C[["af","x1"]].corr().iloc[0,1]})
    return out
