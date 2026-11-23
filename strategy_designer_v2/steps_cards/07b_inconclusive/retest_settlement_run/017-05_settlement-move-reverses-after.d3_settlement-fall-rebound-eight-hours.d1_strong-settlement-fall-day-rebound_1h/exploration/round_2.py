def explore(data):
    import numpy as np, pandas as pd
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
            rows.append(pd.DataFrame({"coin": coin, "win": w, "cell": np.arange(n) // 24,
                "closeh": closeh, "sc": sc.values, "fc": df["forecast"].values,
                "r8f": (c.shift(-8) / c - 1).values, "r24f": (c.shift(-24) / c - 1).values,
                "year": ts.dt.year.values}))
    A = pd.concat(rows, ignore_index=True)
    A["ex24"] = A["r24f"] - A["coin"].map(drift)
    A = A.dropna(subset=["sc", "r24f"])
    def summ(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean%": 100 * s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})
    bk = [-99, -4, -3, -2.5, -2, -1.5, -1, 0]
    S = A[A["closeh"].isin([0, 16]) & (A["fc"] >= 2)].copy()
    S["fcgrp"] = np.where(S["fc"] >= 10, "fc>=10", "fc2-10")
    S["bucket"] = pd.cut(S["sc"], bk)
    fc_vs_depth = S.groupby(["fcgrp", "bucket"], observed=True)["ex24"].apply(summ).unstack()
    # one case per cell: the deepest scaled fall of the cell, any hour
    F = A[A["sc"] < 0].copy()
    F = F.loc[F.groupby(["coin", "win", "cell"])["sc"].idxmin()]
    F["bucket"] = pd.cut(F["sc"], bk)
    F["settle"] = np.where(F["closeh"].isin([0, 16]), "settle", "other")
    deep_any = F.groupby(["settle", "bucket"], observed=True)["ex24"].apply(summ).unstack()
    D = F[F["sc"] <= -3]
    deep_year = D.groupby("year")["ex24"].apply(summ).unstack()
    deep_coin = D.groupby("coin")["ex24"].apply(summ).unstack()
    deep_h = pd.DataFrame({"r8f": summ(D["r8f"]), "ex24": summ(D["ex24"])}).T
    corr = pd.Series({"spearman_sc_ex24_cellmin": F[["sc", "ex24"]].corr(method="spearman").iloc[0, 1],
                      "n": len(F)})
    return {"settle_cases_fcgroup_by_depth": fc_vs_depth, "cellmin_fall_by_depth": deep_any,
            "deep_le-3_by_year": deep_year, "deep_le-3_by_coin": deep_coin,
            "deep_horizons": deep_h, "corr": corr}
