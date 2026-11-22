def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        rs = []
        for w, b in wins.items():
            c = b["close"].values
            rs.extend(c[1:] / c[:-1] - 1)
        drift = np.mean(rs)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r = c.pct_change()
            vsr = r / r.rolling(20).std()
            z60 = (vsr - vsr.rolling(60, min_periods=20).mean()) / vsr.rolling(60, min_periods=20).std()
            d = pd.DataFrame({"coin": coin, "window": w,
                              "year": pd.to_datetime(b["timestamp"]).dt.year,
                              "regime": b["regime"], "forecast": b["forecast"],
                              "vsr": vsr, "z60": z60,
                              "u1": -(c.shift(-1) / c - 1 - drift)})
            rows.append(d)
    df = pd.concat(rows, ignore_index=True).dropna(subset=["vsr", "u1"])
    fall = df[(df.regime == "mean_reversion") & (df.vsr > 0)]
    rise = df[(df.regime != "mean_reversion") & (df.vsr > 0)]
    out = {}

    def welch(a, b):
        t = stats.ttest_ind(a, b, equal_var=False)
        return pd.Series({"n_a": len(a), "n_b": len(b), "a_minus_b": a.mean() - b.mean(), "t": t.statistic})

    out["falling_rises_spearman"] = pd.Series({
        "vsr_vs_u1": stats.spearmanr(fall.vsr, fall.u1)[0],
        "z60_vs_u1": stats.spearmanr(fall.z60, fall.u1, nan_policy="omit")[0],
        "abs_fc_vs_u1": stats.spearmanr(fall.forecast.abs(), fall.u1)[0],
        "n": len(fall)})
    med = fall.vsr.median()
    out["falling_rises_vsr_halves"] = welch(fall[fall.vsr > med].u1, fall[fall.vsr <= med].u1)
    out["falling_rises_vsr_gt2_vs_le1"] = welch(fall[fall.vsr > 2].u1, fall[fall.vsr <= 1].u1)
    out["falling_vs_notfalling_vsr_gt1.5"] = welch(fall[fall.vsr > 1.5].u1, rise[rise.vsr > 1.5].u1)
    fall = fall.assign(q=pd.qcut(fall.vsr, 4, labels=False))
    out["falling_vsr_quartile_by_year_top_minus_bottom"] = fall.groupby("year").apply(
        lambda g: pd.Series({"top": g[g.q == 3].u1.mean(), "bottom": g[g.q == 0].u1.mean(),
                             "diff": g[g.q == 3].u1.mean() - g[g.q == 0].u1.mean(), "n": len(g)}))
    cases = df[df.forecast <= -2]
    out["cases_corr_vsr_z60"] = pd.Series({
        "spearman_vsr_z60": stats.spearmanr(cases.vsr, cases.z60, nan_policy="omit")[0],
        "spearman_vsr_absfc": stats.spearmanr(cases.vsr, cases.forecast.abs())[0],
        "share_cases_vsr_below_1": (cases.vsr < 1).mean()})
    return out
