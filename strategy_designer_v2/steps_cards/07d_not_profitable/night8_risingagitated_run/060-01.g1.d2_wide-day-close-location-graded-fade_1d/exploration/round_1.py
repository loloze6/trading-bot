def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    bookrows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            rng = b["high"] - b["low"]
            b["cpos"] = np.where(rng > 0, 2 * (b["close"] - b["low"]) / rng - 1, 0)
            b["rr"] = rng / rng.rolling(20, min_periods=20).mean()
            b["r1"] = b["close"].shift(-1) / b["close"] - 1
            b["r2"] = b["close"].shift(-2) / b["close"] - 1
            b["r3"] = b["close"].shift(-3) / b["close"] - 1
            b["dret"] = b["close"] / b["close"].shift(1) - 1
            b["ret5"] = b["close"] / b["close"].shift(5) - 1
            b["ret60"] = b["close"] / b["close"].shift(60) - 1
            b["iday"] = b["close"] / b["open"] - 1
            b["alloc"] = b["postRebalance_current_allocation"]
            b["coin"] = coin; b["win"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b[["coin","win","year","forecast","regime","cpos","rr","r1","r2","r3","dret","ret5","ret60","iday","alloc"]])
        for w, d in data["days"][coin].items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            bookrows.append(d[["day","win","coin","book_return","coin_return"]])
    A = pd.concat(rows, ignore_index=True)
    drift = A.groupby("coin")["r1"].mean()
    A["ex1"] = -(A["r1"] - A["coin"].map(drift))
    A["s1"] = -A["r1"]; A["s2"] = -A["r2"]; A["s3"] = -A["r3"]
    cases = A[A["forecast"] < 0].dropna(subset=["r1"])
    out["n_cases"] = len(cases)
    out["regime_counts"] = A["regime"].value_counts()
    def summ(g):
        return pd.Series({"n": len(g), "s1": g["s1"].mean(), "t1": stats.ttest_1samp(g["s1"], 0).statistic if len(g) > 2 else np.nan,
                          "s2": g["s2"].mean(), "s3": g["s3"].mean(), "worst": g["s1"].min(), "share_neg": (g["s1"] < 0).mean()})
    cases = cases.copy()
    cases["cpos_bin"] = pd.cut(cases["cpos"], [0, 0.33, 0.66, 1.01])
    out["by_cpos"] = cases.groupby("cpos_bin", observed=True).apply(summ)
    cases["rr_bin"] = pd.qcut(cases["rr"], 3)
    out["by_rr"] = cases.groupby("rr_bin", observed=True).apply(summ)
    cases["dret_bin"] = pd.qcut(cases["dret"], 3)
    out["by_dayret"] = cases.groupby("dret_bin", observed=True).apply(summ)
    cases["ret5_bin"] = pd.qcut(cases["ret5"], 3)
    out["by_ret5"] = cases.groupby("ret5_bin", observed=True).apply(summ)
    cases["ret60_bin"] = pd.qcut(cases["ret60"], 3)
    out["by_ret60"] = cases.groupby("ret60_bin", observed=True).apply(summ)
    out["by_year"] = cases.groupby("year").apply(summ)
    out["by_coin"] = cases.groupby("coin").apply(summ)
    # condition alone in profile
    inprof = A[A["regime"].isin(["mean_reversion", "unknown"])].dropna(subset=["r1"])
    inprof = inprof.copy()
    inprof["grp"] = np.select([(inprof["rr"] >= 1) & (inprof["cpos"] > 0), (inprof["rr"] >= 1) & (inprof["cpos"] <= 0), (inprof["rr"] < 1) & (inprof["cpos"] > 0)], ["wide_high", "wide_low", "narrow_high"], "narrow_low")
    out["inprofile_groups"] = inprof.groupby("grp").apply(summ)
    # book
    B = pd.concat(bookrows, ignore_index=True)
    wins_order = sorted(B["win"].unique(), key=lambda s: int(s[1:]))
    bk = B.groupby(["win", "day"])["book_return"].mean().dropna()
    chain = []
    for w in wins_order:
        if w in bk.index.get_level_values(0):
            s = bk.loc[w]; chain.append(pd.DataFrame({"win": w, "r": s.values}))
    C = pd.concat(chain, ignore_index=True)
    v = (1 + C["r"]).cumprod(); dd = v / v.cummax() - 1
    C["dd"] = dd
    out["max_dd"] = dd.min()
    out["yearly"] = v.iloc[-1] ** (365 / len(C)) - 1
    out["dd_by_window"] = C.groupby("win").agg(minDD=("dd", "min"), sumret=("r", "sum"), worstday=("r", "min"))
    out["worst_book_days"] = C["r"].nsmallest(10).reset_index(drop=True)
    out["best_book_days"] = C["r"].nlargest(10).reset_index(drop=True)
    # alloc of cases
    out["case_abs_alloc"] = cases["alloc"].abs().describe()
    cases["wloss"] = cases["s1"] * cases["alloc"].abs()
    out["worst_cases"] = cases.nsmallest(12, "wloss")[["coin", "year", "cpos", "rr", "dret", "ret5", "s1", "s2", "alloc"]].reset_index(drop=True)
    return out
