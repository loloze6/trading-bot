def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        drift = {}
        for H in (8, 24):
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - H, H)
                rr.append(c[idx + H] / c[idx] - 1)
            rr = np.concatenate(rr)
            drift[H] = (np.nanmean(rr), np.nanstd(rr))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            c = df["close"].values
            n = len(c)
            r2 = pd.Series(c).pct_change(2)
            ma = r2.abs().rolling(720, min_periods=100).mean()
            s = (r2 / ma).values
            out = {"coin": coin, "year": ts.dt.year.values, "win": w,
                   "hour": ts.dt.hour.values, "pos": np.arange(n),
                   "fc": df["forecast"].values, "s": s,
                   "r30": pd.Series(c).pct_change(720).values}
            for H in (8, 24):
                f = np.full(n, np.nan)
                f[:n - H] = c[H:] / c[:n - H] - 1
                out[f"u{H}"] = f - drift[H][0]
                out[f"tot{H}"] = f
                out[f"z{H}"] = (f - drift[H][0]) / drift[H][1]
            rows.append(pd.DataFrame(out))
    A = pd.concat(rows, ignore_index=True)
    A["cell"] = A["pos"] // 24
    A["trend"] = np.where(A["r30"] > 0, "up30d", np.where(A["r30"] <= 0, "down30d", "na"))
    A = A[A["trend"] != "na"]

    def summ(g, col="u24"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    sett = A[A["hour"].isin([23, 15])]
    cases = sett[sett["fc"] >= 2].groupby(["coin", "win", "cell"], as_index=False).first()
    res = {}
    res["cases_trend_u8"] = cases.groupby("trend").apply(lambda g: summ(g, "u8"))
    res["cases_trend_tot24"] = cases.groupby("trend").apply(lambda g: summ(g, "tot24"))
    res["cases_trend_strength24"] = cases.groupby("trend").apply(lambda g: summ(g, "z24"))
    up = cases[cases["trend"] == "up30d"].copy()
    res["up_by_year"] = up.groupby("year").apply(summ)
    up["fb"] = pd.cut(up["fc"], [2, 4, 8, 15, 19.99, 20.01])
    res["up_by_forecast"] = up.groupby("fb").apply(summ)
    up["cb"] = pd.qcut(up["r30"], 4)
    res["up_by_r30_quartile"] = up.groupby("cb").apply(summ)
    res["up_by_hour"] = up.groupby("hour").apply(summ)
    # all hours: fall >= 1 usual move, by trend, first per cell
    P = A[A["s"] <= -1.0].groupby(["coin", "win", "cell"], as_index=False).first()
    res["anyhour_fall_by_trend"] = P.groupby("trend").apply(summ)
    Pu = P[P["trend"] == "up30d"].copy()
    Pu["sb"] = pd.cut(Pu["s"], [-100, -3, -2, -1.5, -1.0])
    res["anyhour_up_by_fall"] = Pu.groupby("sb").apply(summ)
    res["anyhour_up_by_year"] = Pu.groupby("year").apply(summ)
    return res
