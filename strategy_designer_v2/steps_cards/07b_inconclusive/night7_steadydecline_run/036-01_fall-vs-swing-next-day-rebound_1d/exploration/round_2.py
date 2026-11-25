def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            zs = (z - z.rolling(60, min_periods=20).mean()) / z.rolling(60, min_periods=20).std()
            df = pd.DataFrame({"coin": coin, "win": w, "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                               "z": z, "zs": zs, "fc": b["forecast"].astype(float),
                               "f1": c.shift(-1) / c - 1,
                               "raw": pd.to_numeric(b.get("debug_info.components.rel_fall.last_history_value"), errors="coerce")})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["x1"] = d["f1"] - d.groupby("coin")["f1"].transform("mean")
    cases = d[(d["fc"] > 0)].dropna(subset=["x1", "z"]).copy()
    out = {}
    def thirds(col, asc_top_is_large=True):
        s = cases.sort_values(col)
        n = len(s) // 3
        lo, hi = s.iloc[:n]["x1"], s.iloc[-n:]["x1"]
        # 'top' = deepest fall when col is z (most negative) -> first third
        t = stats.ttest_ind(lo, hi, equal_var=False)
        return {"first_third_mean": lo.mean(), "last_third_mean": hi.mean(), "diff_first_minus_last": lo.mean() - hi.mean(), "welch_t": t.statistic, "n_each": n}
    out["thirds_by_raw_z (first=deepest)"] = pd.Series(thirds("z"))
    out["thirds_by_forecast (first=smallest)"] = pd.Series(thirds("fc"))
    out["spearman_z_x1"] = stats.spearmanr(cases["z"], cases["x1"]).correlation
    out["spearman_fc_x1"] = stats.spearmanr(cases["fc"], cases["x1"]).correlation
    out["spearman_fc_z"] = stats.spearmanr(cases["fc"], cases["z"]).correlation
    out["corr_raw_debug_vs_z"] = cases[["raw", "z"]].corr().iloc[0, 1]
    # z grading within windows: per-window spearman z vs x1
    pw = cases.groupby("win").apply(lambda g: stats.spearmanr(g["z"], g["x1"]).correlation)
    out["per_window_spearman_z_x1"] = pw
    out["share_windows_negative_spearman"] = (pw < 0).mean()
    # z quartiles mean x1
    cases["zq"] = pd.qcut(cases["z"], 4, labels=["q1_deepest", "q2", "q3", "q4_shallowest"])
    out["by_z_quartile"] = cases.groupby("zq", observed=True)["x1"].agg(["count", "mean"])
    # forecast quartile within z bins: is fc scrambled
    cases["zbin"] = pd.cut(cases["z"], [-99, -2, -1.5, 0])
    out["fc_mean_by_zbin"] = cases.groupby("zbin", observed=True)["fc"].agg(["count", "mean"])
    return out
