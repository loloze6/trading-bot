def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]
    out = {}
    allgrid = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True).copy()
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"].values; n = len(b)
            s = pd.Series(cl)
            r3 = np.full(n, np.nan); r3[:n-3] = cl[3:] / cl[:-3] - 1
            r1 = s.pct_change()
            sma50 = s.rolling(50, min_periods=50).mean()
            f = pd.DataFrame({"coin": c, "w": w, "wn": int(w[1:]), "wd": ts.dt.weekday, "year": ts.dt.year, "r3": r3, "r1": r1,
                              "r2": s / s.shift(2) - 1,
                              "dist50": cl / sma50 - 1, "slope50": sma50 / sma50.shift(10) - 1,
                              "p30": s / s.shift(30) - 1, "p14": s / s.shift(14) - 1,
                              "vol30": r1.rolling(30).std(),
                              "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                              "zf": b.get("debug_info.components.weekend_fall.post_pipeline_value"),
                              "zd": b.get("debug_info.components.below_sma50.post_pipeline_value")})
            f["pos"] = np.arange(n)
            allgrid.append(f)
    A = pd.concat(allgrid, ignore_index=True)
    g = A[A["pos"] % 3 == 0]
    drift = g.groupby("coin")["r3"].mean()
    A["ex3"] = A["r3"] - A["coin"].map(drift)
    A["pnl"] = A["alloc"] * A["r3"]
    def summ(x):
        return pd.Series({"n": len(x), "r3": x["r3"].mean(), "ex3": x["ex3"].mean(),
                          "t_ex": stats.ttest_1samp(x["ex3"].dropna(), 0).statistic if len(x) > 2 else np.nan,
                          "win": (x["r3"] > 0).mean(), "alloc": x["alloc"].mean(), "pnl_sum": x["pnl"].sum()})
    C = A[(A["wd"] == 6) & (A["fc"] > 0)].dropna(subset=["r3"]).copy()
    C["slq"] = pd.qcut(C["slope50"], 4, labels=False)
    out["by_slope50_q"] = C.groupby("slq").apply(summ)
    C["zfq"] = pd.qcut(C["zf"].rank(method="first"), 4, labels=False)
    out["by_weekendfall_part_q"] = C.groupby("zfq").apply(summ)
    C["zdq"] = pd.qcut(C["zd"].rank(method="first"), 4, labels=False)
    out["by_depth_part_q"] = C.groupby("zdq").apply(summ)
    C["d50q"] = pd.qcut(C["dist50"], 4, labels=False)
    out["by_dist50_q"] = C.groupby("d50q").apply(summ)
    C["vq"] = pd.qcut(C["vol30"], 4, labels=False)
    C["p30q"] = pd.qcut(C["p30"], 4, labels=False)
    out["slope_x_p30_ex3"] = C.pivot_table(index="slq", columns="p30q", values="ex3", aggfunc="mean")
    out["slope_x_p30_n"] = C.pivot_table(index="slq", columns="p30q", values="ex3", aggfunc="size")
    # drawdown windows w1-w2 vs rest
    C["dd"] = np.where(C["wn"].isin([1, 2]), "w1-2", "rest")
    out["dd_vs_rest"] = C.groupby("dd").apply(summ)
    out["dd_features"] = C.groupby("dd")[["fc", "dist50", "slope50", "p30", "vol30", "r1", "alloc"]].mean()
    out["dd_by_slope_q"] = C[C["dd"] == "w1-2"].groupby("slq").apply(summ)
    # pnl share by forecast quartile
    C["fcq"] = pd.qcut(C["fc"], 4, labels=False)
    out["pnl_by_fcq"] = C.groupby("fcq").apply(summ)
    # condition-alone checks on non-Sunday grid bars below sma50 with fall
    O = A[(A["wd"] != 6) & (A["pos"] % 3 == 0) & (A["r1"] < 0) & (A["dist50"] < 0)].dropna(subset=["r3", "slope50", "vol30", "p30"]).copy()
    edges_sl = C["slope50"].quantile([0.25, 0.5, 0.75]).values
    O["slq"] = np.digitize(O["slope50"], edges_sl)
    out["other_days_by_slope_q"] = O.groupby("slq").apply(summ)
    edges_v = C["vol30"].quantile([0.25, 0.5, 0.75]).values
    O["vq"] = np.digitize(O["vol30"], edges_v)
    out["other_days_by_vol_q"] = O.groupby("vq").apply(summ)
    edges_p = C["p30"].quantile([0.25, 0.5, 0.75]).values
    O["p30q"] = np.digitize(O["p30"], edges_p)
    out["other_days_by_p30_q"] = O.groupby("p30q").apply(summ)
    # two-day weekend return (Sat+Sun) as situation
    C["r2q"] = pd.qcut(C["r2"], 4, labels=False)
    out["by_sat_sun_2day_q"] = C.groupby("r2q").apply(summ)
    return out
