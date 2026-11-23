def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        g = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 24, 24)
            g.extend(list(c[idx + 24] / c[idx] - 1))
        drift[coin] = np.mean(g)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            ts = pd.to_datetime(df["timestamp"], utc=True)
            closeh = ((ts + pd.Timedelta(hours=1)).dt.hour).values
            r2 = c / c.shift(2) - 1
            sc = r2 / r2.abs().rolling(720, min_periods=200).mean()
            out = {}
            for h in [2, 8, 24]:
                out[h] = (c.shift(-h) / c - 1).values
            n = len(df)
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(n), "cell": np.arange(n) // 24,
                              "closeh": closeh, "sc": sc.values, "fc": df["forecast"].values,
                              "r2f": out[2], "r8f": out[8], "r24f": out[24],
                              "year": ts.dt.year.values,
                              "prevtrend": (c / c.shift(72) - 1).values,
                              "vol": df["volume"].values})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A["ex24"] = A["r24f"] - A["coin"].map(drift)
    A = A.dropna(subset=["sc", "r24f"])
    def summ(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean%": 100 * s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})
    # falls at each close hour (scaled fall <= -1), one per cell automatically
    F = A[A["sc"] <= -1]
    by_hour = F.groupby("closeh")["ex24"].apply(summ).unstack()
    # all bars per close hour (unconditional) excess 24
    allh = A.groupby("closeh")["ex24"].apply(summ).unstack()
    # settlement cases
    S = A[A["closeh"].isin([0, 16])].copy()
    S["bucket"] = pd.cut(S["sc"], [-99, -3, -2, -1.5, -1, -0.5, 0, 0.5, 1, 2, 99])
    by_bucket = S.groupby("bucket", observed=True)["ex24"].apply(summ).unstack()
    Sc = S[S["fc"] >= 2]
    by_coin = Sc.groupby("coin")["ex24"].apply(summ).unstack()
    by_year = Sc.groupby("year")["ex24"].apply(summ).unstack()
    by_sh = Sc.groupby("closeh")["ex24"].apply(summ).unstack()
    Sc = Sc.copy()
    Sc["trend"] = np.where(Sc["prevtrend"] > 0, "up3d", "down3d")
    by_trend = Sc.groupby("trend")["ex24"].apply(summ).unstack()
    hz = pd.DataFrame({"r2f": summ(Sc["r2f"]), "r8f": summ(Sc["r8f"]), "r24f_raw": summ(Sc["r24f"]), "ex24": summ(Sc["ex24"])}).T
    # bucket for all hours falls (non settlement)
    NS = A[~A["closeh"].isin([0, 8, 16])].copy()
    NS["bucket"] = pd.cut(NS["sc"], [-99, -3, -2, -1.5, -1, -0.5, 0, 0.5, 1, 2, 99])
    ns_bucket = NS.groupby("bucket", observed=True)["ex24"].apply(summ).unstack()
    return {"falls_by_closehour": by_hour, "all_by_closehour": allh, "settle_by_scaledbucket": by_bucket,
            "nonsettle_by_scaledbucket": ns_bucket, "cases_by_coin": by_coin, "cases_by_year": by_year,
            "cases_by_settlehour": by_sh, "cases_by_3dtrend": by_trend, "cases_horizons": hz}
