def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        # drift per horizon
        drift = {}
        for H in (8, 24, 48, 72):
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - H, H)
                rr.append(c[idx + H] / c[idx] - 1)
            rr = np.concatenate(rr) if rr else np.array([])
            drift[H] = (np.nanmean(rr), np.nanstd(rr))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            c = df["close"].values
            n = len(c)
            r2 = pd.Series(c).pct_change(2)
            ma = r2.abs().rolling(720, min_periods=100).mean()
            s = (r2 / ma).values
            r30 = pd.Series(c).pct_change(720).values
            out = {"coin": coin, "win": w, "year": ts.dt.year.values,
                   "hour": ts.dt.hour.values, "pos": np.arange(n),
                   "fc": df["forecast"].values, "s": s, "r30": r30}
            for H in (8, 24, 48, 72):
                f = np.full(n, np.nan)
                f[:n - H] = c[H:] / c[:n - H] - 1
                out[f"u{H}"] = f - drift[H][0]
                out[f"z{H}"] = (f - drift[H][0]) / drift[H][1]
            rows.append(pd.DataFrame(out))
    A = pd.concat(rows, ignore_index=True)
    A["cell"] = A["pos"] // 24
    sett = A[A["hour"].isin([23, 15])]

    def summ(g, col="u24"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    cases = sett[sett["fc"] >= 2].groupby(["coin", "win", "cell"], as_index=False).first()
    small = sett[(sett["fc"] > 0) & (sett["fc"] < 2)].groupby(["coin", "win", "cell"], as_index=False).first()
    res = {}
    res["check_cases"] = summ(cases)
    res["by_horizon"] = pd.DataFrame({H: summ(cases, f"u{H}") for H in (8, 24, 48, 72)}).T
    res["by_hour"] = cases.groupby("hour").apply(summ)
    res["by_year"] = cases.groupby("year").apply(summ)
    res["by_coin"] = cases.groupby("coin").apply(summ)
    cases["fb"] = pd.cut(cases["fc"], [2, 4, 8, 15, 19.99, 20.01])
    res["by_forecast"] = cases.groupby("fb").apply(summ)
    cases["trend"] = np.where(cases["r30"] > 0, "up30d", "down30d")
    res["by_trend"] = cases.groupby("trend").apply(summ)
    # placebo: fall of >=1.5 usual moves at every hour, first per cell
    P = A[A["s"] <= -1.5].groupby(["coin", "win", "cell", "hour"], as_index=False).first()
    res["placebo_by_hour_u24"] = P.groupby("hour").apply(summ)
    res["all_falls_any_hour"] = summ(P.groupby(["coin", "win", "cell"], as_index=False).first())
    return res
