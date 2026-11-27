def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c / c.shift(1) - 1
            sd = r1.rolling(20, min_periods=15).std()
            hi = c.rolling(20, min_periods=15).max()
            up = (r1 > 0).astype(int)
            run = up.groupby((up != up.shift()).cumsum()).cumsum() * up
            r5p = c.shift(1) / c.shift(6) - 1  # 5-day return before the up day
            d = pd.DataFrame({
                "coin": coin, "w": w, "ts": pd.to_datetime(b["timestamp"]),
                "r1": r1, "sd": sd, "depth": (c / hi - 1) / sd,
                "r5p_sw": r5p / (sd * np.sqrt(5)),
                "r5": c / c.shift(5) - 1,
                "run": run,
                "tr60": c / c.shift(60) - 1,
                "f1": c.shift(-1) / c - 1,
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["x1"] = D["f1"] - D["coin"].map(D.groupby("coin")["f1"].mean())
    D["day"] = D["ts"].dt.floor("D")
    D["up"] = D["r1"] > 0

    def summ(g, col="x1"):
        g = g.dropna(subset=[col])
        if len(g) < 5:
            return pd.Series({"n": len(g), "mean": np.nan, "t": np.nan})
        s = g.groupby("day")[col].sum()
        t = s.mean() / (s.std(ddof=1) / np.sqrt(len(s))) if len(s) > 2 else np.nan
        return pd.Series({"n": len(g), "days": len(s), "mean": g[col].mean(), "t": t})

    out = {}
    u = D[D.up].dropna(subset=["x1", "depth", "r5p_sw"]).copy()
    u["pq"] = pd.qcut(u["r5p_sw"].rank(method="first"), 5, labels=["fellmost", "p2", "p3", "p4", "rosemost"])
    out["up_by_prior5_all"] = u.groupby("pq").apply(summ)
    u["dq"] = pd.qcut(u["depth"].rank(method="first"), 3, labels=["deep", "mid", "shallow"])
    out["up_prior5_x_depth_mean"] = u.groupby(["pq", "dq"])["x1"].mean().unstack()
    out["up_prior5_x_depth_n"] = u.groupby(["pq", "dq"])["x1"].count().unstack()
    fm = u[u.pq == "fellmost"]
    out["fellmost_by_year"] = fm.groupby(fm.ts.dt.year).apply(summ)
    fm = fm.copy()
    fm["trend"] = np.where(fm["tr60"] > 0.1, "rising", np.where(fm["tr60"] < -0.1, "falling", np.where(fm["tr60"].notna(), "choppy", "na")))
    out["fellmost_by_trend"] = fm.groupby("trend").apply(summ)
    out["fellmost_by_run"] = fm.groupby(fm["run"].clip(upper=2)).apply(summ)
    # down days after a 5-day fall, for contrast
    dn = D[~D.up].dropna(subset=["x1", "r5p_sw"]).copy()
    dn["pq"] = pd.qcut(dn["r5p_sw"].rank(method="first"), 5, labels=["fellmost", "p2", "p3", "p4", "rosemost"])
    out["down_by_prior5"] = dn.groupby("pq").apply(summ)
    # spearman grading within up days
    from scipy.stats import spearmanr
    rho, p = spearmanr(u["r5p_sw"], u["x1"])
    out["up_spearman_prior5_x1"] = pd.Series({"rho": rho, "p": p, "n": len(u)})
    return out
