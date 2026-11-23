def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    drift = {}
    for coin, wins in bars.items():
        g = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 24, 24)
            g.extend(list(c[idx + 24] / c[idx] - 1))
        drift[coin] = np.mean(g)
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            ts = pd.to_datetime(df["timestamp"], utc=True)
            closeh = ((ts + pd.Timedelta(hours=1)).dt.hour).values
            r2 = c / c.shift(2) - 1
            sc = r2 / r2.abs().rolling(720, min_periods=200).mean()
            n = len(df)
            rows.append(pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(n), "cell": np.arange(n) // 24,
                "closeh": closeh, "sc": sc.values, "fc": df["forecast"].values,
                "r8f": (c.shift(-8) / c - 1).values, "r24f": (c.shift(-24) / c - 1).values,
                "year": ts.dt.year.values}))
    A = pd.concat(rows, ignore_index=True)
    A["ex24"] = A["r24f"] - A["coin"].map(drift)
    A = A.dropna(subset=["sc", "r24f"])
    def summ(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean%": 100 * s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})
    bk = [-99, -4, -3, -2.5, -2, -1.5, -1]
    # first bar in each cell (chronological, no lookahead) with scaled fall <= -1
    F = A[A["sc"] <= -1].sort_values(["coin", "win", "pos"])
    F = F.groupby(["coin", "win", "cell"]).head(1).copy()
    F["bucket"] = pd.cut(F["sc"], bk)
    F["settle"] = np.where(F["closeh"].isin([0, 16]), "settle", "other")
    first_by_depth = F.groupby(["settle", "bucket"], observed=True)["ex24"].apply(summ).unstack()
    D = F[F["sc"] <= -2]
    first_deep_year = D.groupby("year")["ex24"].apply(summ).unstack()
    first_deep_coin = D.groupby("coin")["ex24"].apply(summ).unstack()
    # settlement cases: correlation of depth with excess, and forecast vs depth
    S = A[A["closeh"].isin([0, 16]) & (A["fc"] >= 2)]
    sp_s = stats.spearmanr(-S["sc"], S["ex24"], nan_policy="omit")
    sp_f = stats.spearmanr(-F["sc"], F["ex24"], nan_policy="omit")
    sp_fc = stats.spearmanr(S["fc"], -S["sc"], nan_policy="omit")
    corr = pd.Series({"spearman_depth_ex24_settlecases": sp_s.correlation, "p1": sp_s.pvalue,
                      "spearman_depth_ex24_firstfalls": sp_f.correlation, "p2": sp_f.pvalue,
                      "spearman_fc_depth_settlecases": sp_fc.correlation})
    hz = pd.DataFrame({"r8f": summ(D["r8f"]), "ex24": summ(D["ex24"])}).T
    return {"first_fall_by_depth": first_by_depth, "first_deep_le-2_year": first_deep_year,
            "first_deep_le-2_coin": first_deep_coin, "corr": corr, "first_deep_horizons": hz}
