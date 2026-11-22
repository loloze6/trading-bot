def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = {"1d":6, "3d":18, "7d":42, "13d":78}
    rows = []
    drift = {}
    for coin, ws in bars.items():
        for hn, h in H.items():
            rs = []
            for w, df in ws.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, hn)] = (np.mean(rs), np.std(rs))
        for w, df in ws.items():
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            runmin = 0.0
            taken_cell = set()
            for i in range(n):
                if f[i] <= 0:
                    runmin = 0.0
                    continue
                runmin = min(runmin, f[i])
                cell = i // 78
                if f[i] - runmin >= 2 and cell not in taken_cell:
                    taken_cell.add(cell)
                    runmin = f[i]
                    r = {"coin": coin, "win": w, "year": ts.iloc[i].year, "f": f[i]}
                    for hn, h in H.items():
                        if i + h < n:
                            d, s = drift[(coin, hn)]
                            r["u_" + hn] = c[i + h] / c[i] - 1 - d
                    r["prior30"] = c[i] / c[i - 180] - 1 if i >= 180 else np.nan
                    r["prior7"] = c[i] / c[i - 42] - 1 if i >= 42 else np.nan
                    hi = c[max(0, i - 540):i + 1].max()
                    r["dd90"] = c[i] / hi - 1
                    rows.append(r)
    d = pd.DataFrame(rows).dropna(subset=["u_13d"])
    def summ(g):
        x = g["u_13d"]
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "u7d": g["u_7d"].mean(), "u3d": g["u_3d"].mean(), "u1d": g["u_1d"].mean()})
    out = {}
    out["all"] = summ(d).to_frame().T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["fq"] = pd.qcut(d["f"].rank(method="first"), 5, labels=False)
    out["by_forecast_quintile"] = d.groupby("fq").apply(summ)
    d["p30"] = pd.qcut(d["prior30"], 3, labels=["low", "mid", "high"])
    out["by_prior30"] = d.groupby("p30").apply(summ)
    d["dd"] = pd.qcut(d["dd90"], 3, labels=["deep", "mid", "shallow"])
    out["by_dd90"] = d.groupby("dd").apply(summ)
    hs = {}
    for hn in H:
        x = d["u_" + hn].dropna()
        hs[hn] = {"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))}
    out["horizons_overlapping_note"] = pd.DataFrame(hs).T
    out["mean_forecast_quintiles"] = d.groupby("fq")["f"].mean()
    return out
