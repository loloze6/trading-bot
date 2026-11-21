def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 26
    bars = data["bars"]
    rows = []
    drift = {}; usual = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                rets.append(c[i + H] / c[i] - 1)
        drift[coin] = np.mean(rets) if rets else np.nan
        usual[coin] = np.std(rets) if len(rets) > 1 else np.nan
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = df["forecast"].fillna(0).values
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
            raw = df.get("debug_info.components.thin_cloud.last_history_value")
            ts = pd.to_datetime(df["timestamp"])
            seen = set()
            for i in range(1, len(df)):
                if f[i - 1] == 0 and f[i] - f[i - 1] >= 2:
                    cell = i // H
                    if cell in seen:
                        continue
                    seen.add(cell)
                    r = {"coin": coin, "year": ts.iloc[i].year,
                         "raw": raw.iloc[i] if raw is not None else np.nan,
                         "r26": c[i + 26] / c[i] - 1 if i + 26 < len(c) else np.nan,
                         "r52": c[i + 52] / c[i] - 1 if i + 52 < len(c) else np.nan,
                         "past26": c[i] / c[i - 26] - 1 if i >= 26 else np.nan,
                         "past10": c[i] / c[i - 10] - 1 if i >= 10 else np.nan,
                         "usual": usual[coin], "drift": drift[coin]}
                    rows.append(r)
    d = pd.DataFrame(rows)
    d["u26"] = d["r26"] - d["drift"]
    d["u52"] = d["r52"] - 2 * d["drift"]
    d = d.dropna(subset=["u26", "raw"])
    d["width"] = 1 / d["raw"] - 1
    med = d["raw"].median()
    d["thin"] = d["raw"] > med
    d["s26"] = d["u26"] / d["usual"]
    out = {}
    def wt(g, col="u26"):
        a = g[g.thin][col].dropna(); b = g[~g.thin][col].dropna()
        return pd.Series({"n_thin": len(a), "n_thick": len(b), "thin": a.mean(), "thick": b.mean(),
                          "diff": a.mean() - b.mean(),
                          "welch": stats.ttest_ind(a, b, equal_var=False).statistic if len(a) > 2 and len(b) > 2 else np.nan,
                          "all": g[col].mean(),
                          "t_all": g[col].mean() / (g[col].std() / np.sqrt(g[col].count())),
                          "spear_raw": stats.spearmanr(g["raw"], g[col], nan_policy="omit").correlation})
    out["all_vs_ex2024"] = pd.DataFrame({"all": wt(d), "ex2024": wt(d[d.year != 2024]), "only2024": wt(d[d.year == 2024])}).T
    # winsorised
    dw = d.copy(); lo_, hi_ = dw.u26.quantile([0.025, 0.975]); dw["u26"] = dw.u26.clip(lo_, hi_)
    out["winsor"] = wt(dw)
    out["strength_scaled"] = wt(d, "s26")
    dp = d.dropna(subset=["past26"]).copy()
    dp["pq"] = pd.qcut(dp["past26"], 3, labels=False)
    out["past26_terc"] = dp.groupby("pq").apply(wt)
    out["past26_terc_range"] = dp.groupby("pq")["past26"].agg(["min", "max", "median"])
    # ratio past26 / usual: rise into cross relative to coin's usual move
    dp["ps"] = dp["past26"] / dp["usual"]
    out["spear_past26_u26"] = pd.Series({"all": stats.spearmanr(dp.past26, dp.u26).correlation,
                                          "thick": stats.spearmanr(dp[~dp.thin].past26, dp[~dp.thin].u26).correlation,
                                          "thin": stats.spearmanr(dp[dp.thin].past26, dp[dp.thin].u26).correlation,
                                          "spear_width_past26": stats.spearmanr(dp.width, dp.past26).correlation})
    # past26 minus width: rise relative to cloud width
    dp["rel"] = dp["past26"] / dp["width"]
    dp["rq"] = pd.qcut(dp["rel"], 4, labels=False)
    out["rel_quart"] = dp.groupby("rq").agg(n=("u26", "size"), mean=("u26", "mean"), median=("u26", "median"),
                                            rel=("rel", "median"))
    # OLS u26 on z(raw), z(past26)
    X = np.column_stack([np.ones(len(dp)), (dp.raw - dp.raw.mean()) / dp.raw.std(),
                         (dp.past26 - dp.past26.mean()) / dp.past26.std()])
    y = dp.u26.values
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ b; s2 = res @ res / (len(y) - 3)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["ols"] = pd.DataFrame({"coef": b, "t": b / se}, index=["const", "z_raw", "z_past26"])
    out["u52_thin_thick"] = wt(d.dropna(subset=["u52"]), "u52")
    return out
