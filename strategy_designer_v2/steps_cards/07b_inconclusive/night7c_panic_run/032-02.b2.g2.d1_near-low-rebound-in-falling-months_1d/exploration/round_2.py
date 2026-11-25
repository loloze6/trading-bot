def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "regime": b["regime"], "fc": b["forecast"],
                "alloc": b["postRebalance_current_allocation"],
                "cl": (h - c) / (h - l).replace(0, np.nan),
                "ret30": c / c.shift(30) - 1,
                "rng": (h - l) / c,
                "r1": c.shift(-1) / c - 1,
            })
            rec = b.get("debug_info.components.fall30.last_history_value")
            if rec is not None:
                df["ret30"] = rec.where(rec.notna(), df["ret30"])
            df["rng_z"] = df["rng"] / df["rng"].rolling(30).mean()
            df["year"] = df["day"].dt.year
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["x1"] = d["r1"] - d.groupby("coin")["r1"].transform("mean")

    def ct(s, days):
        s = s.dropna(); days = days.loc[s.index]; n = len(s)
        if n < 5: return (np.nan, np.nan, n)
        m = s.mean(); S = (s - m).groupby(days).sum()
        return (m, m / (np.sqrt((S ** 2).sum()) / n), n)

    def tab(sub, key):
        out = {}
        for g, gg in sub.groupby(key, observed=True):
            m, t, n = ct(gg["x1"], gg["day"]); out[g] = {"mean": m, "t": t, "n": n}
        return pd.DataFrame(out).T

    R = d[d["regime"] == "mean_reversion"].copy()
    R["cl_t"] = pd.qcut(R["cl"], 3, labels=False, duplicates="drop")
    R["f_t"] = pd.qcut(-R["ret30"], 3, labels=False, duplicates="drop")
    R["rz_t"] = pd.qcut(R["rng_z"], 3, labels=False, duplicates="drop")
    R["cell"] = R["cl_t"].astype(str) + "_" + R["f_t"].astype(str)
    res = {}
    res["regime cl tercile x fall tercile (cl_fall)"] = tab(R, "cell")
    res["regime top cl tercile by today's range vs 30d (2=widest)"] = tab(R[R["cl_t"] == 2], "rz_t")
    res["regime top cl tercile by year"] = tab(R[R["cl_t"] == 2], "year")
    res["regime top cl tercile by coin"] = tab(R[R["cl_t"] == 2], "coin")
    # same slope by regime vs not: top minus bottom close-location tercile
    NR = d[d["regime"] != "mean_reversion"].copy()
    NR["cl_t"] = pd.qcut(NR["cl"], 3, labels=False, duplicates="drop")
    out = {}
    for name, S in (("regime", R), ("non-regime", NR)):
        a = S.loc[S["cl_t"] == 2, "x1"].dropna(); b_ = S.loc[S["cl_t"] == 0, "x1"].dropna()
        from scipy import stats
        t = stats.ttest_ind(a, b_, equal_var=False).statistic
        out[name] = {"top_minus_bottom": a.mean() - b_.mean(), "welch_t": t, "n_top": len(a), "n_bot": len(b_)}
    res["near-low minus near-high, regime vs not"] = pd.DataFrame(out).T
    res["sd of x1 regime"] = float(R["x1"].std())
    res["sd of x1 non-regime"] = float(NR["x1"].std())
    return res
